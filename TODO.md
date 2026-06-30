# TODO — alarm-laurel_sprout

## Inmediato
- [ ] Ejecutar workflow 01 para generar primer pmOS base artifact
- [ ] Ejecutar workflow 02 para generar release con Arch
- [ ] Probar flasheo en dispositivo real

## Pendientes
- [ ] Verificar que el Qualcomm WiFi (ath10k) funcione out-of-the-box
- [ ] Probar getty en framebuffer (tty1)
- [ ] Agregar soporte para TTL UART si aplica
- [ ] Evaluar si el pmOS initramfs necesita fstab en Qualcomm (el bug de wait_boot_partition es Mediatek-specific)
- [ ] Port Kupfer para laurel_sprout (cuando begonia esté estable)

## Package names usados (pmOS binary mirror)
- kernel: `linux-postmarketos-qcom-sm6125` (6.1-r3)
- device: `device-xiaomi-laurel` (5-r0)
- base: `postmarketos-base-core`
- mkinitfs: `postmarketos-mkinitfs`
- mkbootimg: `mkbootimg-osm0sis`
- mirror: `https://mirror.postmarketos.org/postmarketos/main`
