# Arch Linux ARM on postmarketOS — Xiaomi Mi A3 (laurel_sprout)

**Arch Linux ARM userspace** sobre el **kernel mainline de postmarketOS** para Xiaomi Mi A3.

## Esquema

```
Bootloader → kernel pmOS 6.1 (qcom-sm6125 mainline)
→ pmOS initramfs (busca pmOS_root por label)
→ switch_root → systemd de Arch Linux ARM 🚀
```

## Build pipeline

| Workflow | Descripción |
|---|---|
| `01_build_pmos_base.yml` | Build de pmOS base via pmbootstrap (kernel, initramfs, dtb, módulos) |
| `02_build_alarm_laurel.yml` | Superpone Arch Linux ARM rootfs sobre el base pmOS |

## Estado

| Componente | Estado |
|---|---|
| pmOS boot.img (kernel + initramfs + DTB) | Pendiente (workflow 01) |
| Arch rootfs overlay | ✅ Configurado (workflow 02) |
| /etc/fstab (evita wait_boot_partition) | ✅ Configurado |
| UUIDs stale removal | ✅ Script incluido |
| SSH + NetworkManager | ✅ Configurado |

## Install

1. Desbloquear bootloader
2. Bootear a fastboot
3. ```bash
   xz -d rootfs-archlinuxarm-laurel-console.img.xz
   fastboot format:ext4 userdata
   fastboot flash boot boot-begonia-arch.img
   fastboot flash userdata rootfs-archlinuxarm-laurel-console.img
   fastboot reboot
   ```
4. SSH: `alarm@<IP>` / pass: `alarm`

## Device info

- **Nombre:** Xiaomi Mi A3
- **Codename:** laurel_sprout
- **SoC:** Qualcomm SM6125 (Snapdragon 665)
- **Kernel:** linux-postmarketos-qcom-sm6125 6.1 (mainline fork)
- **DTB:** qcom/sm6125-xiaomi-laurel_sprout.dtb
- **pmOS wiki:** [Xiaomi Mi A3](https://wiki.postmarketos.org/wiki/Xiaomi_Mi_A3_(xiaomi-laurel))

## Repos relacionados

- [alarm-begonia](https://github.com/criollojoel10/alarm-begonia) — Port para Redmi Note 8 Pro
- [termux-setup](https://github.com/criollojoel10/termux-setup) — Stack + workspace unificado
