#!/usr/bin/env python3
# Author: David Cardozo <david@updata.ca>
from json.decoder import JSONDecodeError
from os import chdir
import subprocess as sp
import json
import asyncio
import argparse


async def run(cmd):
    proc = await asyncio.create_subprocess_shell(
        cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
    )

    stdout, stderr = await proc.communicate()

    print(f"[{cmd!r} exited with {proc.returncode}]")
    if stdout:
        print(f"[stdout]\n{stdout.decode()}")
    if stderr:
        print(f"[stderr]\n{stderr.decode()}")


if __name__ == "__main__":
    custom_parser = argparse.ArgumentParser(description="Move images beetwen registry")
    custom_parser.add_argument(
        '--registry-src',
        metavar="registry_src",
        type=str,
        help="Source registry",
        required=True
    )
    custom_parser.add_argument(
        '--destination-src',
        metavar="destination_src",
        type=str,
        help="Destination registry",
        required=True
    )
    args = custom_parser.parse_args()
    registry_src = args.registry_src
    registry_dst = args.destination_src
    completed_process = sp.run(
        [f"skopeo list-tags {registry_src}"],
        shell=True,
        check=True,
        stdout=sp.PIPE,
    )

    try:
        tags = json.loads(completed_process.stdout.decode("utf-8"))["Tags"]
    except (JSONDecodeError, KeyError) as e:
        print("Malformed output of skopeo, please check output.")

    run_cmds = []
    for tag in tags:
        print(f"skopeo copy {registry_src}:{tag} {registry_dst}:{tag}")
        run_cmds.append(
                run(

                    f"skopeo copy {registry_src}:{tag} {registry_dst}:{tag}"
                )
        )

    async def async_copy():
        return await asyncio.gather(*run_cmds)

    asyncio.run(async_copy())
    print("Finished copy")
