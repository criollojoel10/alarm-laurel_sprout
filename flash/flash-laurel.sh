#!/bin/bash
# flash-laurel.sh — Flash Arch Linux ARM on Xiaomi Mi A3 (laurel_sprout)
set -euo pipefail

echo "=== Arch Linux ARM on pmOS — Xiaomi Mi A3 (laurel_sprout) ==="
echo ""

# Check files
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
BOOT_IMG="$SCRIPT_DIR/boot-begonia-arch.img"
ROOTFS="$SCRIPT_DIR/rootfs-archlinuxarm-laurel-console.img.xz"

[ ! -f "$BOOT_IMG" ] && { echo "❌ Missing: boot-begonia-arch.img"; exit 1; }
[ ! -f "$ROOTFS" ] && { echo "❌ Missing: rootfs-archlinuxarm-laurel-console.img.xz"; exit 1; }

# Decompress rootfs if needed
if [[ "$ROOTFS" == *.xz ]]; then
    RAW_ROOTFS="${ROOTFS%.xz}"
    if [ ! -f "$RAW_ROOTFS" ]; then
        echo "📦 Decompressing rootfs..."
        xz -d -v "$ROOTFS"
    fi
    ROOTFS="$RAW_ROOTFS"
fi

echo "📱 Checking fastboot..."
fastboot devices || { echo "❌ No device in fastboot mode"; exit 1; }

echo ""
echo "⚠️  WARNING: This will erase userdata on your device!"
echo "   Bootloader MUST be unlocked."
echo ""
read -p "Continue? (y/N): " confirm
[ "$confirm" != "y" ] && [ "$confirm" != "Y" ] && echo "Aborted." && exit 1

echo ""
echo "=== Step 1: Format userdata ==="
fastboot format:ext4 userdata

echo ""
echo "=== Step 2: Flash boot.img ==="
fastboot flash boot "$BOOT_IMG"

echo ""
echo "=== Step 3: Flash rootfs ==="
fastboot flash userdata "$ROOTFS"

echo ""
echo "=== Step 4: Reboot ==="
fastboot reboot

echo ""
echo "✅ Done! Device should boot into Arch Linux ARM."
echo "   Login via SSH: alarm@<device-ip> / password: alarm"
