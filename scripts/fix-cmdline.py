#!/usr/bin/env python3
"""
Fix cmdline in pmOS boot.img by removing hardcoded UUIDs.

The pmOS initramfs has a `find_partition()` function that first tries UUID,
then falls back to path, then to label. If stale UUIDs are present in the
cmdline, find_partition() returns empty (UUID exists but doesn't match the
new partition). Removing them allows falling back to label detection.

Usage: python3 fix-cmdline.py <boot.img> [output.img]
"""

import struct, sys, re, os

PAGE_SIZE = 2048


def main():
    if len(sys.argv) < 2:
        in_path = "boot.img"
    else:
        in_path = sys.argv[1]

    if len(sys.argv) >= 3:
        out_path = sys.argv[2]
    else:
        out_path = in_path  # in-place

    with open(in_path, 'rb') as f:
        data = f.read()

    # Read header
    magic = data[0:8]
    if magic != b'ANDROID!':
        print(f"❌ Not an Android boot image: {magic!r}")
        sys.exit(1)

    cmdline_area = data[64:576]
    cmdline = cmdline_area.rstrip(b'\x00').decode('ascii', errors='replace')
    print(f"Old cmdline: {cmdline}")

    # Remove PMOS UUID entries
    new_cmdline = re.sub(r'\s*pmos_root_uuid=[-a-fA-F0-9]+\s*', ' ', cmdline)
    new_cmdline = re.sub(r'\s*pmos_boot_uuid=[-a-fA-F0-9]+\s*', ' ', new_cmdline)
    new_cmdline = re.sub(r'\s+', ' ', new_cmdline).strip()

    if new_cmdline == cmdline:
        print("✓ No stale UUIDs found, cmdline unchanged")
    else:
        print(f"New cmdline: {new_cmdline}")

    cmd_bytes = new_cmdline.encode('ascii', errors='replace')[:511]

    buf = bytearray(data)
    for i in range(64, 576):
        buf[i] = 0
    buf[64:64+len(cmd_bytes)] = cmd_bytes

    with open(out_path, 'wb') as f:
        f.write(buf)

    # Verify
    with open(out_path, 'rb') as f:
        verify = f.read(1648)
    v_cmdline = verify[64:576].rstrip(b'\x00').decode('ascii', 'replace')
    has_stale = 'pmos_root_uuid=' in v_cmdline or 'pmos_boot_uuid=' in v_cmdline
    print(f"\n{'✅' if not has_stale else '❌'} boot.img cmdline fixed → {out_path}")
    print(f"   Cmdline: {v_cmdline[:120]}...")
    print(f"   Stale UUIDs: {'NO ✅' if not has_stale else 'YES ❌'}")


if __name__ == '__main__':
    main()
