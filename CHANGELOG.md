# CHANGELOG

## 2026-07-01
- **Simplificado:** `01_build_pmos_base.yml` ahora sigue el patrón exacto de begonia
  - Descarga artifact de `criollojoel10/laurel-postmarketos-build` (pmbootstrap build)
  - Extrae boot.img, vmlinuz, modules/firmware via `scan-extract-fs.py`
  - Ya no genera initramfs en chroot (usa el initramfs de pmOS directamente)
- **Simplificado:** `02_build_alarm_laurel.yml`
  - Eliminado kernel build externo (`sm6125-mainline` clone)
  - Eliminado RTL8192EU (laurel tiene ath10k built-in)
  - Solo inyecta modules + firmware del pmOS base artifact
- **Nuevo repo:** `criollojoel10/laurel-postmarketos-build` — build de pmOS via pmbootstrap para xiaomi-laurel

## 2026-06-29
- Repo creado
- Workflow 01: pmOS base build via pmbootstrap (xiaomi-laurel, linux-postmarketos-qcom-sm6125)
- Workflow 02: Arch Linux ARM overlay (mismo patrón que alarm-begonia)
- scripts/fix-cmdline
