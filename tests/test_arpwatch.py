import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from arpwatch import diff_against_baseline, parse_arp_output
from oui import lookup_vendor

SAMPLE_OUTPUT = """
 0   address=192.168.88.10 mac-address=AA:BB:CC:11:22:33 interface=ether1 status=reachable
 1   address=192.168.88.11 mac-address=DD:EE:FF:44:55:66 interface=ether1 status=reachable
 2 D address=192.168.88.12 mac-address=11:22:33:44:55:66 interface=ether1 status=stale
"""


class ParseTests(unittest.TestCase):
    def test_parses_all_entries(self):
        entries = parse_arp_output(SAMPLE_OUTPUT)
        self.assertEqual(len(entries), 3)
        self.assertEqual(entries[0], {"ip": "192.168.88.10", "mac": "AA:BB:CC:11:22:33"})

    def test_empty_output_returns_no_entries(self):
        self.assertEqual(parse_arp_output(""), [])


class DiffTests(unittest.TestCase):
    def test_new_device_is_detected(self):
        entries = parse_arp_output(SAMPLE_OUTPUT)
        new, removed = diff_against_baseline(entries, ["AA:BB:CC:11:22:33"])
        new_macs = {e["mac"] for e in new}
        self.assertEqual(new_macs, {"DD:EE:FF:44:55:66", "11:22:33:44:55:66"})
        self.assertEqual(removed, [])

    def test_removed_device_is_detected(self):
        entries = parse_arp_output(SAMPLE_OUTPUT)
        new, removed = diff_against_baseline(entries, ["AA:BB:CC:11:22:33", "99:99:99:99:99:99"])
        self.assertEqual(removed, ["99:99:99:99:99:99"])

    def test_no_changes_when_baseline_matches(self):
        entries = parse_arp_output(SAMPLE_OUTPUT)
        known = [e["mac"] for e in entries]
        new, removed = diff_against_baseline(entries, known)
        self.assertEqual(new, [])
        self.assertEqual(removed, [])


class OuiTests(unittest.TestCase):
    def test_known_prefix_is_identified(self):
        self.assertEqual(lookup_vendor("B8:27:EB:11:22:33"), "Raspberry Pi Foundation")

    def test_unknown_prefix_returns_unknown(self):
        self.assertEqual(lookup_vendor("AA:BB:CC:11:22:33"), "Unknown")

    def test_lookup_is_case_insensitive(self):
        self.assertEqual(lookup_vendor("b8:27:eb:11:22:33"), "Raspberry Pi Foundation")


if __name__ == "__main__":
    unittest.main()
