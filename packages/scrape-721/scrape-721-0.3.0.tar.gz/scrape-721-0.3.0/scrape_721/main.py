"""scrape-721"""
import os
import csv
import json

from datetime import datetime
from pathlib import Path
from operator import itemgetter

import typer

from dotenv import load_dotenv
from web3 import Web3
from redis import Redis

from scrape_721.constants import ERC_165_ABI, ERC_721_ABI, ERC_721_INTERFACE_ID
from scrape_721.contract_utils import find_contract_deploy  # type: ignore

load_dotenv()
app = typer.Typer()


def fetch(job_hash, contract_address, from_block, to_block, config):
    w3, path = itemgetter("w3", "path")(config)

    address = w3.toChecksumAddress(contract_address)
    supports_721 = supports_erc_721(address, w3)

    if supports_721:
        contract_erc_721 = w3.eth.contract(address=address, abi=ERC_721_ABI)
        write_header(job_hash, path)
        fetch_records(job_hash, contract_erc_721, from_block, to_block, config)


def supports_erc_721(address, w3):
    contract_erc_165 = w3.eth.contract(address=address, abi=ERC_165_ABI)

    try:
        return contract_erc_165.functions.supportsInterface(ERC_721_INTERFACE_ID).call()
    except:
        return False


def write_header(job_hash, path):
    with open(f"{path}/{job_hash}.csv", "w+") as f:
        writer = csv.writer(f)
        writer.writerow(
            [
                "tx_hash",
                "block_number",
                "block_timestamp",
                "block_hash",
                "contract_address",
                "from",
                "to",
                "token_id",
                "token_name",
                "token_symbol",
                "transaction_index",
                "gas",
                "gas_used",
                "gas_price",
                "nonce",
                "from_balance",
                "to_balance",
            ]
        )


def fetch_records(job_hash, contract, from_block, to_block, config):
    show_progress = itemgetter("show_progress")(config)

    token_name = contract.functions.name().call()
    token_symbol = contract.functions.symbol().call()

    current_block = from_block
    end_block = to_block

    if show_progress:
        with typer.progressbar(
            length=to_block - from_block,
            label="Block progress",
        ) as block_range:
            while current_block < end_block:
                increment = (
                    2000
                    if current_block <= end_block - 2000
                    else end_block - current_block
                )

                fetch_block_range(
                    job_hash,
                    contract,
                    current_block,
                    current_block + increment,
                    token_name,
                    token_symbol,
                    config,
                )

                current_block += increment
                block_range.update(increment, current_item=current_block)
    else:
        while current_block < end_block:
            increment = (
                2000 if current_block <= end_block - 2000 else end_block - current_block
            )

            fetch_block_range(
                job_hash,
                contract,
                current_block,
                current_block + increment,
                token_name,
                token_symbol,
                config,
            )

            current_block += increment


def fetch_block_range(
    job_hash, contract, from_block, to_block, token_name, token_symbol, config
):
    path = itemgetter("path")(config)
    filter = contract.events.Transfer.createFilter(
        fromBlock=from_block, toBlock=to_block
    )

    entries = filter.get_all_entries()

    if len(entries) != 0:
        try:
            records = [
                get_record_from_log(entry, token_name, token_symbol, config)
                for entry in entries
            ]

            with open(f"{path}/{job_hash}.csv", "a+") as f:
                writer = csv.writer(f)
                for record in records:
                    write_row(writer, record)
        except Exception:
            print(f"Request timed out - missing block range {from_block} to {to_block}")


def get_record_from_log(log, token_name, token_symbol, config):
    w3 = itemgetter("w3")(config)

    record = {
        "tx_hash": w3.toHex(log["transactionHash"]),
        "block_number": log["blockNumber"],
        "block_hash": w3.toHex(log["blockHash"]),
        "transaction_index": log["transactionIndex"],
        "contract_address": log["address"],
        "from": log["args"]["from"],
        "to": log["args"]["to"],
        "token_id": log["args"]["tokenId"],
        "token_name": token_name,
        "token_symbol": token_symbol,
    }

    return get_balance_data(get_block_and_transaction_data(record, config), config)


def get_block_and_transaction_data(record, config):
    w3, r, cache = itemgetter("w3", "r", "cache")(config)

    block_number = record["block_number"]
    transaction_index = record["transaction_index"]

    if cache and r.exists(block_number):
        block = json.loads(r.get(block_number).decode("utf-8"))
        transaction = block["transactions"][transaction_index]
    else:
        base_block = w3.eth.get_block(block_number, full_transactions=True)

        block = {
            "block_timestamp": base_block.timestamp,
            "gas_used": base_block.gasUsed,
            "transactions": list(
                map(
                    lambda tx: {
                        "gas": tx.gas,
                        "gas_price": tx.gasPrice,
                        "nonce": tx.nonce,
                    },
                    base_block.transactions,
                )
            ),
        }
        transaction = block["transactions"][transaction_index]
        if cache:
            r.set(block_number, json.dumps(block))

    return record | {
        "block_timestamp": block["block_timestamp"],
        "gas_used": block["gas_used"],
        "gas": transaction["gas"],
        "gas_price": transaction["gas_price"],
        "nonce": transaction["nonce"],
    }


def get_balance_data(record, config):
    w3, r, cache = itemgetter("w3", "r", "cache")(config)

    block_number = record["block_number"]
    from_address = record["from"]
    to_address = record["to"]

    from_balance_key = f"{from_address}{block_number}"
    to_balance_key = f"{to_address}{block_number}"

    if cache and r.exists(from_balance_key):
        from_balance = r.get(from_balance_key)
    else:
        from_balance = float(
            w3.fromWei(w3.eth.get_balance(from_address, block_number), "ether")
        )
        if cache:
            r.set(from_balance_key, from_balance)

    if cache and r.exists(to_balance_key):
        to_balance = r.get(to_balance_key)
    else:
        to_balance = float(
            w3.fromWei(w3.eth.get_balance(to_address, block_number), "ether")
        )
        if cache:
            r.set(to_balance_key, to_balance)

    return record | {
        "from_balance": from_balance,
        "to_balance": to_balance,
    }


def write_row(writer, record):
    writer.writerow(
        [
            record["tx_hash"],
            record["block_number"],
            record["block_timestamp"],
            record["block_hash"],
            record["contract_address"],
            record["from"],
            record["to"],
            record["token_id"],
            record["token_name"],
            record["token_symbol"],
            record["transaction_index"],
            record["gas"],
            record["gas_used"],
            record["gas_price"],
            record["nonce"],
            record["from_balance"],
            record["to_balance"],
        ]
    )


@app.command()
def scrape(
    address: str,
    from_block: int = typer.Option(
        None,
        "--from-block",
        "-f",
        help="Starting block of data fetch. If not passed the script will intelligently determine the creation block of the contract and use that as the starting block",
        show_default=False,
    ),
    to_block: int = typer.Option(
        None,
        "--to-block",
        "-t",
        help="Ending block of data fetch. Defaults to latest block at execution time",
        show_default=False,
    ),
    path: Path = typer.Option(
        os.getcwd(),
        "--path",
        "-p",
        help="Where to save the resulting output csv. Defaults to current working directory",
        show_default=False,
    ),
    rpc_url: str = typer.Option(
        None,
        "--rpc-url",
        "-r",
        help="The Ethereum RPC Node URL. If not provided the script will search the environment for $RPC_URL. The RPC must be provided by one of these two channels",
    ),
    cache: bool = typer.Option(
        True,
        "--cache/--no-cache",
        "-r/-R",
        help="Highly recommended: Use redis caching for improved job time. If true, a redis server is required to be available on localhost:6379. Defaults to --cache",
        show_default=False,
    ),
):
    """
    Retrieve ERC-721 token information. Expects a required contract address.
    The output file is appended continously. That way, in case the program crashes, the already fetched data is preserved.
    """
    if rpc_url is None:
        try:
            rpc_url = os.environ["RPC_URL"]
        except:
            typer.secho(
                "ERROR: Could not retrieve RPC_URL from environment. Please be sure to pass in the --rpc-url argument or set the $RPC_URL environment variable to the address of a valid Ethereum RPC Node.",
                fg=typer.colors.BRIGHT_RED,
                bold=True,
                err=True,
            )
            raise typer.Exit(code=1)

    try:
        w3 = Web3(Web3.HTTPProvider(os.environ["RPC_URL"]))
    except Exception:
        typer.secho(
            "ERROR: Could not establish connection to the RPC server. Please check the provided URL.",
            fg=typer.colors.BRIGHT_RED,
            bold=True,
            err=True,
        )
        raise typer.Exit(code=1)

    if cache:
        try:
            r: Redis = Redis(host="localhost", port=6379, db=0)
            r.ping()
        except Exception:
            typer.secho(
                "ERROR: Redis server could not be succesfully contacted. Are you running a local redis instance? If you wish to continue without caching functionality pass --no-cache or -R.",
                fg=typer.colors.BRIGHT_RED,
                bold=True,
                err=True,
            )
            raise typer.Exit(code=1)

    if from_block is None:
        typer.echo("Searching for contract start block....")
        from_block = find_contract_deploy(address, w3, 0, w3.eth.get_block_number()) + 1
        typer.echo(f"Contract start block found: {from_block}")

    if to_block is None:
        to_block = w3.eth.get_block_number()

    job_hash = f"{address[:10]}_{str(datetime.now().isoformat(timespec='minutes'))}"
    caching = "Yes" if cache else "No"

    typer.secho(
        f"---Starting Job---\nHash: {job_hash}\nContract address: {address}\nFrom block: {from_block}\nTo block: {to_block}\nPath: {path}\nCache: {caching}",
        fg=typer.colors.GREEN,
        bold=True,
    )

    config = {
        "w3": w3,
        "r": Redis(host="localhost", port=6379, db=0) if cache else None,
        "path": path,
        "cache": cache,
        "show_progress": True,
    }

    fetch(job_hash, address, from_block, to_block, config)


if __name__ == "__main__":
    config = {
        "w3": Web3(Web3.HTTPProvider(os.environ["RPC_URL"])),
        "r": Redis(host="localhost", port=6379, db=0),
        "path": os.getcwd(),
        "cache": True,
        "show_progress": True,
    }

    fetch(
        "my_job",
        "0xBC4CA0EdA7647A8aB7C2061c2E118A18a936f13D",
        15101305 - 8000,
        15101305,
        config,
    )
