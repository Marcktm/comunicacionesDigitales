# Arranque del entorno SDR para Laboratorio 3

## Donde estamos trabajando

Todo lo de esta practica queda dentro de:

```text
/Users/marcosreyeros/Repos-Facu/ComDigitales/comunicacionesDigitales/Parcial 2/Laboratorio 3
```

## Estado actual detectado

Anaconda esta instalado en:

```text
/opt/anaconda3
```

Desde la terminal no aparece `conda` directamente en el `PATH`, pero se puede usar asi:

```bash
/opt/anaconda3/bin/conda
```

El entorno `base` ya tiene:

- `numpy`
- `matplotlib`
- `scipy`
- `jupyter`

Pero todavia faltan los paquetes especificos para conectarse al SDR:

- `adi`
- `iio`

Actualizacion: el entorno `lab3-sdr` ya fue creado y los imports `adi` e `iio` fueron verificados correctamente.

## Crear el entorno

Desde esta carpeta:

```bash
cd "/Users/marcosreyeros/Repos-Facu/ComDigitales/comunicacionesDigitales/Parcial 2/Laboratorio 3"
```

crear el entorno con:

```bash
/opt/anaconda3/bin/conda env create -f environment.yml
```

Si ya aparece creado, no hace falta repetir este paso.

Si el entorno ya existe y solo queres actualizarlo:

```bash
/opt/anaconda3/bin/conda env update -f environment.yml --prune
```

## Activar el entorno

Primero cargar `conda` en la terminal:

```bash
source /opt/anaconda3/bin/activate
```

Despues activar el entorno:

```bash
conda activate lab3-sdr
```

## Registrar el kernel para Jupyter

Una vez activado `lab3-sdr`:

```bash
python -m ipykernel install --user --name lab3-sdr --display-name "Python (lab3-sdr)"
```

Esto hace que Jupyter muestre el kernel `Python (lab3-sdr)`.

Actualizacion: el kernel `Python (lab3-sdr)` ya fue registrado en Jupyter.

## Abrir Jupyter desde la carpeta correcta

Con el entorno activado:

```bash
cd "/Users/marcosreyeros/Repos-Facu/ComDigitales/comunicacionesDigitales/Parcial 2/Laboratorio 3"
jupyter lab
```

Si preferis el notebook clasico:

```bash
jupyter notebook
```

## Verificar conexion con el SDR

Con la VPN conectada, abrir la notebook `laboratorio3_sdr.ipynb` y ejecutar las primeras celdas.

La primera prueba importante es:

```python
import adi

uri = "ip:192.168.1.32"
sdr = adi.Pluto(uri)
print(sdr)
```

Si funciona, Python pudo conectarse al SDR.

Si falla:

- revisar que la VPN siga conectada;
- confirmar que la IP del SDR sea `192.168.1.32`;
- verificar que nadie mas este usando el SDR;
- revisar que el kernel activo sea `Python (lab3-sdr)`;
- confirmar que `pyadi-iio`, `pylibiio` y `libiio` esten instalados.

## Nota importante

Como la conexion SDR depende de la VPN y del equipo remoto, Codex no siempre va a poder ejecutar esas celdas desde aca. La idea es que la notebook quede preparada para que vos la ejecutes localmente, y me pases el error o la salida si algo no conecta.
