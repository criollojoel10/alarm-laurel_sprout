# Arch Linux ARM on postmarketOS — Xiaomi Mi A3 (laurel_sprout)

**Arch Linux ARM userspace** sobre el **kernel mainline de postmarketOS** para Xiaomi Mi A3.

## Esquema

```
Bootloader → kernel pmOS 6.1 (qcom-sm6125 mainline)
→ pmOS initramfs (busca pmOS_root por label)
→ /etc/fstab presente → salta wait_boot_partition()
→ switch_root → systemd de Arch Linux ARM 🚀
```

## Build pipeline

| Workflow | Descripción | Repo |
|---|---|---|
| `build.yml` | pmbootstrap build de pmOS base (kernel, initramfs, DTB, módulos) | [`laurel-postmarketos-build`](https://github.com/criollojoel10/laurel-postmarketos-build) |
| `01_build_pmos_base.yml` | Descarga artifact pmOS base, extrae boot.img + modules + firmware | este repo |
| `02_build_alarm_laurel.yml` | Superpone Arch Linux ARM rootfs sobre el base pmOS | este repo |

## Estado

| Componente | Estado |
|---|---|
| Repo pmOS build (`laurel-postmarketos-build`) | ✅ Creado, listo para primer build |
| pmOS boot.img (kernel + initramfs + DTB) | ⏳ Primer build pendiente |
| Arch rootfs overlay | ✅ Workflow listo |
| /etc/fstab (evita wait_boot_partition) | ✅ Configurado |
| UUIDs stale removal | ✅ Script incluido |
| SSH + NetworkManager | ✅ Configurado |
| WiFi (Qualcomm WCN3990 / ath10k) | ✅ Built-in en kernel |
| flash script | ✅ Incluido |

## Flasheo (cuando los builds estén listos)

```bash
# 1. Extraer imágenes
xz -d rootfs-archlinuxarm-laurel-console.img.xz

# 2. Flashear (IMPORTANTE: erase dtbo primero)
fastboot erase dtbo
fastboot flash boot boot-laurel-arch.img
fastboot flash userdata rootfs-archlinuxarm-laurel-console.img
fastboot reboot
```

> **Nota:** `fastboot erase dtbo` es necesario según la wiki de pmOS para laurel.

## Device info

- **Nombre:** Xiaomi Mi A3
- **Codename:** laurel_sprout
- **SoC:** Qualcomm SM6125 (Snapdragon 665)
- **Kernel:** linux-postmarketos-qcom-sm6125 6.1 (mainline fork)
- **DTB:** qcom/sm6125-xiaomi-laurel_sprout.dtb
- **pmOS wiki:** [Xiaomi Mi A3](https://wiki.postmarketos.org/wiki/Xiaomi_Mi_A3_(xiaomi-laurel))
- **WiFi:** Qualcomm WCN3990 (ath10k) — built-in, no dongle needed

## Repos relacionados

- [laurel-postmarketos-build](https://github.com/criollojoel10/laurel-postmarketos-build) — pmbootstrap CI para xiaomi-laurel
- [alarm-begonia](https://github.com/criollojoel10/alarm-begonia) — Port begonia (ya funcional)
- [termux-setup](https://github.com/criollojoel10/termux-setup) — Stack + workspace unificado
