#!/usr/bin/env python3
"""Build boot.img for laurel from kernel + initramfs + DTB."""
import os
import struct
import subprocess
import sys

def main():
    if len(sys.argv) < 5:
        print(f"Usage: {sys.argv[0]} <vmlinuz> <initramfs> <cmdline> <output> [dtb]")
        sys.exit(1)
    
    kernel = sys.argv[1]
    initramfs = sys.argv[2]
    cmdline = sys.argv[3]
    output = sys.argv[4]
    dtb = sys.argv[5] if len(sys.argv) > 5 else None

    for f in [kernel, initramfs]:
        if not os.path.exists(f):
            print(f"Missing: {f}")
            sys.exit(1)

    # Apppend DTB to kernel if needed (laurel: append_dtb=true)
    kernel_path = kernel
    if dtb and os.path.exists(dtb):
        tmp_kernel = '/tmp/kernel-dtb.img'
        with open(kernel, 'rb') as kf, open(dtb, 'rb') as df:
            with open(tmp_kernel, 'wb') as out:
                out.write(kf.read())
                out.write(df.read())
        kernel_path = tmp_kernel
        print(f"DTB appended: {os.path.getsize(kernel)} -> {os.path.getsize(tmp_kernel)}")

    # Build mkbootimg command
    cmd = [
        'python3', '-m', 'mkbootimg',
        '--kernel', kernel_path,
        '--ramdisk', initramfs,
        '--cmdline', cmdline,
        '--base', '0x00000000',
        '--kernel_offset', '0x00008000',
        '--ramdisk_offset', '0x01000000',
        '--second_offset', '0x00f00000',
        '--tags_offset', '0x00000100',
        '--pagesize', '4096',
        '--header_version', '2',
        '--os_version', '23.0.0',
        '--os_patch_level', '2026-06',
        '-o', output
    ]
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    print(result.stdout)
    if result.returncode != 0:
        print(f"mkbootimg failed: {result.stderr}")
        sys.exit(1)

    # Verify
    with open(output, 'rb') as f:
        data = f.read(1024)
    c = data[64:576].rstrip(b'\x00').decode('ascii', 'replace')
    has_label = 'pmOS_root' in c
    r_size = struct.unpack('<I', data[16:20])[0]
    k_size = struct.unpack('<I', data[8:12])[0]
    hdr_ver = struct.unpack('<I', data[36:40])[0]
    
    print(f"\n=== boot.img ===")
    print(f"Size: {os.path.getsize(output):,} B")
    print(f"Cmdline: {c}")
    print(f"pmOS_root: {has_label}")
    print(f"Ramdisk: {r_size:,} B | Kernel: {k_size:,} B | Header v{hdr_ver}")
    
    if not has_label:
        print("WARNING: pmOS_root not in cmdline!")
        sys.exit(1)

if __name__ == '__main__':
    main()
