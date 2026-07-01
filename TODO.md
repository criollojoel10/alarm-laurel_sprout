# TODO — alarm-laurel_sprout

## Inmediato
- [ ] Ejecutar workflow en `laurel-postmarketos-build` para generar primer pmOS base
- [ ] Ejecutar workflow 01 para extraer pmOS base artifact
- [ ] Ejecutar workflow 02 para generar release con Arch
- [ ] Probar flasheo en dispositivo real

## Pendientes
- [ ] Verificar que el Qualcomm WiFi (ath10k) funcione out-of-the-box
- [ ] Probar getty en framebuffer (tty1)
- [ ] Agregar soporte para TTL UART si aplica
- [ ] Probar si `fastboot erase dtbo` es necesario o no

## Referencia de builds
- pmOS base build: `criollojoel10/laurel-postmarketos-build` (workflow `build.yml`)
- pmOS base artifact: `01_build_pmos_base.yml` → descarga de `laurel-postmarketos-build`
- Arch overlay: `02_build_alarm_laurel.yml` → imagen final + release nightly
