# arp-watch-lite

Polls a MikroTik router's ARP table over SSH, compares it against a saved baseline, and flags
new or disappeared devices — a lightweight rogue-device detector you can run from cron.

## Installation

```sh
pip install -r requirements.txt
```

## Usage

```sh
cp config.example.json config.json   # fill in your router
python arpwatch.py config.json
```

First run establishes the baseline. From then on:

```
2 new device(s):
  DD:EE:FF:44:55:66  192.168.88.11
1 device(s) no longer present:
  11:22:33:44:55:66
```

The baseline is stored in `state.json` next to the script by default (`--state path/to/file.json`
to override) and updated automatically at the end of every run.

Vendor lookup by MAC prefix and webhook notifications on new devices coming soon.

## License

MIT — see [LICENSE](LICENSE).
