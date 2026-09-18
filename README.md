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

First run establishes the baseline (nothing to compare against yet). From then on:

```
2 new device(s):
  DD:EE:FF:44:55:66  192.168.88.11  (Unknown)
  B8:27:EB:11:22:33  192.168.88.14  (Raspberry Pi Foundation)
1 device(s) no longer present:
  11:22:33:44:55:66
```

The baseline is stored in `state.json` next to the script by default (`--state path/to/file.json`
to override) and updated automatically at the end of every run.

### Vendor lookup

New devices are annotated with a best-guess vendor from their MAC's OUI prefix, using a small
hand-curated table in `oui.py` (common network/consumer vendors — not the full IEEE registry).
Unrecognized prefixes show as "Unknown".

### Notifications

Set `notify.webhook_url` in `config.json` to get an alert whenever a new device shows up:

```json
"notify": {
  "webhook_url": "https://hooks.slack.com/services/...",
  "webhook_type": "slack"
}
```

`webhook_type`: `"slack"`, `"discord"`, `"ntfy"`, or `"generic"` (posts `{"text": message}` as JSON).

### Running on a schedule

```
*/15 * * * * cd /path/to/arp-watch-lite && python3 arpwatch.py config.json >> arpwatch.log 2>&1
```

## Running the tests

```sh
python -m unittest discover -s tests
```

## License

MIT — see [LICENSE](LICENSE).
