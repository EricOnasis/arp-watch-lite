#!/usr/bin/env python3
"""Watch a MikroTik router's ARP table for new devices.

Usage:
    python arpwatch.py config.json
"""
import argparse
import json
import os
import re
import socket

import paramiko

ARP_ENTRY_RE = re.compile(r"address=(\S+).*?mac-address=(\S+)")
DEFAULT_TIMEOUT = 10
DEFAULT_STATE_PATH = "state.json"


def fetch_arp_table(router: dict, timeout: int = DEFAULT_TIMEOUT) -> list:
    """SSH to the router and return a list of {ip, mac} currently in its ARP table."""
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        client.connect(
            router["host"],
            port=router.get("port", 22),
            username=router["username"],
            password=router["password"],
            timeout=timeout,
        )
        stdin, stdout, stderr = client.exec_command("/ip arp print terse without-paging",
                                                      timeout=timeout)
        output = stdout.read().decode(errors="replace")
    except (paramiko.ssh_exception.SSHException, socket.timeout, socket.error, OSError) as e:
        raise RuntimeError(f"Could not fetch ARP table from {router['host']}: {e}")
    finally:
        client.close()

    return parse_arp_output(output)


def parse_arp_output(output: str) -> list:
    entries = []
    for line in output.splitlines():
        match = ARP_ENTRY_RE.search(line)
        if match:
            entries.append({"ip": match.group(1), "mac": match.group(2).upper()})
    return entries


def load_state(path: str) -> dict:
    if not os.path.exists(path):
        return {"known_macs": []}
    with open(path) as f:
        return json.load(f)


def save_state(path: str, state: dict) -> None:
    with open(path, "w") as f:
        json.dump(state, f, indent=2)


def diff_against_baseline(entries: list, known_macs: list) -> tuple:
    current_macs = {e["mac"] for e in entries}
    known = set(known_macs)

    new_entries = [e for e in entries if e["mac"] not in known]
    removed_macs = sorted(known - current_macs)

    return new_entries, removed_macs


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("config_file", help="Path to a config.json with router details")
    parser.add_argument("--state", default=DEFAULT_STATE_PATH, help="Path to the baseline state file")
    args = parser.parse_args()

    with open(args.config_file) as f:
        router = json.load(f)["router"]

    entries = fetch_arp_table(router)
    state = load_state(args.state)
    new_entries, removed_macs = diff_against_baseline(entries, state["known_macs"])

    if new_entries:
        print(f"{len(new_entries)} new device(s):")
        for e in new_entries:
            print(f"  {e['mac']}  {e['ip']}")
    if removed_macs:
        print(f"{len(removed_macs)} device(s) no longer present:")
        for mac in removed_macs:
            print(f"  {mac}")
    if not new_entries and not removed_macs:
        print("No changes.")

    state["known_macs"] = sorted({e["mac"] for e in entries})
    save_state(args.state, state)


if __name__ == "__main__":
    main()
