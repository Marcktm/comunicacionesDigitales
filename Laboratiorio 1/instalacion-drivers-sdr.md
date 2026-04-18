# Instalación de drivers SDR en Linux Mint (local)

Guía para ejecutar la Jupyter Notebook localmente y conectarse a las SDR remotas por VPN, cuando el servidor JupyterHub (`192.168.1.60`) está caído.

## Contexto

El laboratorio tiene una JupyterHub conectada por switch a las SDRs (ADALM-Pluto, AD9363). Cuando el servidor de Jupyter está caído, se puede correr la notebook localmente y conectarse a las SDRs directamente por VPN, ya que las IPs de las SDRs (`192.168.1.31` a `192.168.1.35`) siguen accesibles.

La cadena de software es:

```
Jupyter Notebook → pyadi-iio → libiio → [VPN] → iiod (en la PlutoSDR)
```

Lo que corre en la SDR es su propio firmware (U-Boot, Linux kernel, etc.). Lo que hay que instalar en la PC host es `libiio` y `pyadi-iio`.

---

## Paso 1: Instalar `libiio`

```bash
sudo apt install libiio-dev libiio-utils python3-libiio
```

---

## Paso 2: Crear entorno virtual de Python

> **Problema encontrado:** `pip install pyadi-iio` directo falla con `externally-managed-environment` (PEP 668 — Mint protege el Python del sistema).

Solución: usar un entorno virtual.

```bash
python3 -m venv ~/venv-sdr
source ~/venv-sdr/bin/activate
```

Opcional — agregar alias en `~/.bashrc` o `~/.zshrc` para no activarlo manualmente:

```bash
alias sdr='source ~/venv-sdr/bin/activate && jupyter notebook'
```

---

## Paso 3: Instalar paquetes Python (SIN VPN activa)

> **Problema encontrado:** la VPN bloquea el acceso a internet (DNS/routing), por lo que `pip install` falla dentro de la notebook cuando la VPN está conectada. Instalar todo **antes** de conectar la VPN.

```bash
source ~/venv-sdr/bin/activate
pip install pyadi-iio jupyter matplotlib scikit-dsp-comm scikit-commpy
```

---

## Paso 4: Conectar la VPN

Conectarse con Cisco AnyConnect a:

```
IP:   200.16.19.5
Port: 443
User: LabSDR2024
```

---

## Paso 5: Verificar conectividad con la SDR

```bash
ping 192.168.1.31
iio_info -u ip:192.168.1.31  # debe listar los canales del AD9363
```

---

## Paso 6: Abrir la Jupyter Notebook

```bash
source ~/venv-sdr/bin/activate
jupyter notebook "Laboratiorio 1/Como Configurar un SDR-20260417/How To Config SDR.ipynb"
```

---

## Paso 7: Configurar la notebook

En la notebook, saltear las celdas de `pip install` (ya están instalados) y asegurarse de que la URI apunte a la SDR deseada:

```python
sdr = adi.Pluto("ip:192.168.1.31")  # cambiar último dígito: 31 a 35
```

---

## Paso 8: Cerrar todo

1. En Jupyter: `File → Shut Down` (o `Ctrl+C` en la terminal donde corre)
2. Desconectar la VPN desde AnyConnect
3. Desactivar el venv:

```bash
deactivate
```

---

## Resumen de inconvenientes

| Problema | Causa | Solución |
|---|---|---|
| `externally-managed-environment` al hacer `pip install` | Mint protege el Python del sistema (PEP 668) | Usar `python3 -m venv` |
| `pip install` falla en la notebook con VPN activa | La VPN bloquea DNS/salida a internet | Instalar paquetes antes de activar la VPN |
