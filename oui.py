"""A small, hand-curated OUI (MAC address vendor prefix) lookup table.

This is NOT the full IEEE registry — just common consumer/network vendors, enough to be useful
for "what kind of device is this" at a glance. Returns "Unknown" for anything not in the table.
"""

OUI_VENDORS = {
    "00:1A:11": "Google",
    "3C:5A:B4": "Google",
    "F4:F5:D8": "Google",
    "AC:DE:48": "Apple",
    "F0:18:98": "Apple",
    "A4:83:E7": "Apple",
    "DC:A6:32": "Raspberry Pi Foundation",
    "B8:27:EB": "Raspberry Pi Foundation",
    "E4:5F:01": "Raspberry Pi Foundation",
    "00:0C:42": "MikroTik",
    "4C:5E:0C": "MikroTik",
    "64:D1:54": "MikroTik",
    "18:FD:74": "Ubiquiti Networks",
    "24:5A:4C": "Ubiquiti Networks",
    "FC:EC:DA": "Ubiquiti Networks",
    "00:50:56": "VMware",
    "00:0C:29": "VMware",
    "08:00:27": "Oracle VirtualBox",
    "52:54:00": "QEMU/KVM",
    "B4:2E:99": "Amazon (Echo/Kindle)",
    "68:37:E9": "Amazon (Echo/Kindle)",
    "3C:71:BF": "Samsung",
    "5C:0A:5B": "Samsung",
}


def lookup_vendor(mac: str) -> str:
    prefix = mac.upper().replace("-", ":")[:8]
    return OUI_VENDORS.get(prefix, "Unknown")
