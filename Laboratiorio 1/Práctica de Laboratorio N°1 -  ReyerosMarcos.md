# Instalación y configuración de Cisco AnyConnect e IIO Oscilloscope en macOS (Apple Silicon) y puesta en funcionamiento del Laboratorio de SDR Remoto

## Video

[PASO A PASO DEL AULA VIRTUAL](https://drive.google.com/file/d/1U6wCyRbvpqBAhrER_0ZbsdVBeik4sR2q/view?usp=drive_link)

## 1. Introducción

En el marco de la **Práctica de Laboratorio N°1: Puesta en funcionamiento y uso de los recursos brindados por el Laboratorio de SDR Remoto**, fue necesario preparar un entorno de trabajo en macOS con arquitectura Apple Silicon que permitiera acceder a la infraestructura remota de la cátedra y operar un sistema SDR basado en tecnología de Analog Devices.

La actividad se desarrolló en dos planos complementarios. En primer lugar, fue necesario resolver el acceso remoto al laboratorio mediante una conexión VPN institucional. En segundo lugar, se debió instalar y poner en funcionamiento el software requerido para interactuar con dispositivos compatibles con la infraestructura **IIO (Industrial I/O)**, en particular la herramienta **ADI IIO Oscilloscope** y el entorno de ejecución remoto basado en **Jupyter Hub**.

Los objetivos principales del trabajo fueron los siguientes:

* establecer una conexión segura mediante **Cisco AnyConnect VPN** con la red del laboratorio;
* instalar y ejecutar correctamente **IIO Oscilloscope** en macOS;
* resolver incompatibilidades de compilación y ejecución asociadas al uso de software originalmente orientado a Linux en un entorno macOS moderno;
* acceder al **Jupyter Hub** del laboratorio remoto;
* ejecutar la notebook **How To Config SDR.ipynb**;
* comprender la arquitectura básica del hardware SDR utilizado;
* interpretar los parámetros principales de configuración del transceptor;
* obtener y analizar una gráfica de **Densidad Espectral de Potencia (PSD)** a partir de muestras capturadas por el SDR.

El trabajo requirió la compilación manual de varias bibliotecas, la modificación de archivos de configuración del sistema de build y la validación final del funcionamiento del entorno de laboratorio remoto.

---

## 2. Instalación de Cisco AnyConnect VPN

## 2.1 Descarga del instalador

La conexión con la red interna del laboratorio requiere el uso de una **VPN institucional** basada en **Cisco AnyConnect**.

La versión utilizada fue:

```text
anyconnect-macos-4.10.06090-predeploy-k9.dmg
```

Este archivo corresponde a un paquete preconfigurado que contiene el cliente VPN para macOS.

El instalador puede obtenerse desde la infraestructura provista por la institución o, en su defecto, desde una fuente equivalente que provea exactamente la misma versión del cliente. El enlace utilizado fue el siguiente:

[https://www.msupply.org.nz/files/VPN_Software/Cisco_AnyConnect/anyconnect-macos-4.10.06090-predeploy-k9.dmg](https://www.msupply.org.nz/files/VPN_Software/Cisco_AnyConnect/anyconnect-macos-4.10.06090-predeploy-k9.dmg)

---

## 2.2 Instalación

El procedimiento de instalación fue el siguiente:

1. Descargar el archivo `.dmg`.
2. Abrir la imagen montada.
3. Ejecutar el instalador contenido en el paquete.
4. Seleccionar e instalar el componente **Cisco Secure Client VPN**.

Durante la instalación, macOS solicita permisos administrativos para instalar componentes de red y extensiones necesarias para el funcionamiento del cliente VPN.

Una vez completado el proceso, la aplicación quedó disponible en:

```text
/Applications/Cisco Secure Client.app
```

---

## 2.3 Uso

El cliente VPN se utilizó para establecer conexión con la red institucional del laboratorio, lo cual permitió acceder a:

* redes internas del entorno académico;
* recursos del laboratorio remoto;
* dispositivos SDR accesibles únicamente desde la red privada;
* servicios internos como **Jupyter Hub**.

La conexión VPN resultó indispensable, ya que los dispositivos SDR y los servicios asociados no se encuentran expuestos directamente a Internet pública, sino que sólo son accesibles desde la red privada del laboratorio.

---

## 3. Instalación de dependencias mediante Homebrew

Para compilar y ejecutar **IIO Oscilloscope** fue necesario instalar múltiples bibliotecas requeridas por el proyecto. Para ello se utilizó **Homebrew**, gestor de paquetes ampliamente empleado en macOS.

Entre las dependencias instaladas se encontraron:

* `cmake`
* `pkg-config`
* `gtk+`
* `glib`
* `cairo`
* `fftw`
* `jansson`
* `libserialport`
* `libxml2`
* `curl`
* `pango`
* `gdk-pixbuf`
* `harfbuzz`
* `gtkdatabox`

Estas bibliotecas cumplen funciones específicas dentro del sistema:

* construcción y configuración del proyecto;
* soporte para interfaz gráfica GTK;
* procesamiento y visualización de señales;
* comunicación con dispositivos IIO;
* manejo de archivos, datos y dependencias auxiliares.

---

## 4. Instalación de libiio

## 4.1 Qué es libiio

La biblioteca **libiio** es el componente central de la infraestructura **Industrial I/O** desarrollada por Analog Devices.

Su función es proporcionar una interfaz de software para:

* descubrir dispositivos IIO;
* conectarse a hardware local o remoto;
* configurar canales y atributos;
* transferir muestras entre el dispositivo y la aplicación de usuario.

En la práctica, `libiio` constituye la base sobre la cual se apoyan tanto **IIO Oscilloscope** como bibliotecas de más alto nivel, por ejemplo `pyadi-iio`.

---

## 4.2 Instalación

La biblioteca se instaló mediante Homebrew con el siguiente comando:

```bash
brew install libiio
```

Esta instalación generó el framework:

```text
iio.framework
```

ubicado en:

```text
/opt/homebrew/opt/libiio/Frameworks
```

Esta ruta resultó importante posteriormente durante la etapa de compilación manual de otras bibliotecas y del programa principal.

---

## 5. Instalación de libad9361-iio

## 5.1 Función

La biblioteca **libad9361-iio** provee soporte específico para el transceptor **AD9361/AD9363**, muy utilizado en plataformas SDR de Analog Devices.

Esta biblioteca expone funciones relacionadas con:

* configuración de filtros;
* control de ganancia;
* sincronización;
* calibración;
* configuración de PLL;
* control general de la cadena de radiofrecuencia.

Su presencia es necesaria para que determinadas funciones de **IIO Oscilloscope** puedan interactuar correctamente con dispositivos basados en esta familia de transceptores.

---

## 5.2 Compilación manual

La biblioteca no pudo instalarse de manera directa mediante Homebrew en el entorno utilizado, por lo que fue necesario compilarla manualmente a partir de su código fuente.

El procedimiento básico fue:

```bash
git clone https://github.com/analogdevicesinc/libad9361-iio.git
cd libad9361-iio
mkdir build
cd build
cmake ..
make
sudo make install
```

Durante este proceso aparecieron incompatibilidades con el compilador moderno de macOS. En particular, varios archivos fuente necesitaban incluir explícitamente el encabezado:

```c
#include <stdio.h>
```

El motivo fue que funciones como `snprintf` no estaban siendo reconocidas si no se declaraban de forma explícita en el código. Esta situación puede producirse en proyectos antiguos cuando se compilan en toolchains más recientes y estrictos.

Además, fue necesario corregir parámetros de CMake debido a que algunas versiones antiguas del proyecto no resultaban plenamente compatibles con las políticas actuales de `cmake`.

Finalmente, la biblioteca se instaló correctamente en:

```text
/usr/local/lib/ad9361.framework
```

y sus archivos auxiliares quedaron disponibles para el proceso de compilación del programa principal.

---

## 6. Compilación de IIO Oscilloscope

## 6.1 Descarga del código fuente

Se trabajó con la versión:

```text
iio-oscilloscope v0.11
```

El archivo descargado fue:

```text
iio-oscilloscope-0.11-master.tar.gz
```

Una vez extraído, se trabajó directamente sobre el código fuente para compilarlo en forma manual.

---

## 6.2 Preparación del entorno de compilación

Dentro del directorio fuente se creó un subdirectorio de build:

```bash
mkdir build
cd build
```

A continuación, se exportaron variables de entorno necesarias para que el compilador y el linker pudieran encontrar correctamente las bibliotecas `libiio` y `libad9361-iio`:

```bash
export PKG_CONFIG_PATH=/opt/homebrew/opt/libiio/lib/pkgconfig:/usr/local/lib/pkgconfig:$PKG_CONFIG_PATH
export CPPFLAGS="-I/opt/homebrew/opt/libiio/Frameworks/iio.framework/Headers -I/usr/local/lib/ad9361.framework/Headers"
export LDFLAGS="-F/opt/homebrew/opt/libiio/Frameworks -framework iio -F/usr/local/lib -framework ad9361"
```

Posteriormente se ejecutó `cmake` con la indicación explícita de las rutas relevantes:

```bash
cmake .. \
  -DCMAKE_POLICY_VERSION_MINIMUM=3.5 \
  -DCMAKE_PREFIX_PATH=/opt/homebrew \
  -DLIBIIO_INCLUDE_DIRS=/opt/homebrew/opt/libiio/Frameworks/iio.framework/Headers \
  -DLIBIIO_LIBRARIES=/opt/homebrew/opt/libiio/Frameworks/iio.framework/iio \
  -DLIBAD9361_INCLUDE_DIRS=/usr/local/lib/ad9361.framework/Headers \
  -DLIBAD9361_LIBRARIES=/usr/local/lib/ad9361.framework/ad9361
```

Una vez configurado el proyecto, se realizó la compilación mediante:

```bash
make -j6
```

y finalmente la instalación:

```bash
sudo make install
```

---

## 7. Problemas encontrados durante la compilación

La compilación de **IIO Oscilloscope** y sus dependencias presentó varias dificultades técnicas que debieron resolverse manualmente.

### 7.1 Variables de CMake no encontradas

El proyecto esperaba encontrar automáticamente las variables:

```text
LIBIIO_INCLUDE_DIRS
LIBAD9361_INCLUDE_DIRS
```

Sin embargo, en macOS estas rutas no fueron detectadas correctamente, debido a que:

* `libiio` quedó instalada como framework en `/opt/homebrew`;
* `libad9361-iio` fue instalada manualmente en `/usr/local/lib`.

Por este motivo fue necesario indicar manualmente las rutas de include y las bibliotecas.

---

### 7.2 Error causado por `-Werror`

El archivo `CMakeLists.txt` contenía la opción:

```text
-Werror
```

Esto implica que cualquier advertencia del compilador se trate como error fatal. En proyectos antiguos esta práctica suele generar problemas cuando se compilan con toolchains nuevas, debido a que aparecen warnings por extensiones o cambios de comportamiento del compilador.

En este caso, la opción se eliminó para permitir que el proyecto continuara compilando aun cuando surgieran advertencias no críticas.

---

### 7.3 Variable `FRU_FILES` incompatible con macOS

El código contenía una definición similar a la siguiente:

```cmake
if(UNIX)
add_definitions(-DFRU_FILES="${CMAKE_PREFIX_PATH}/lib/fmc-tools/")
endif()
```

Si bien macOS es un sistema tipo Unix, esta definición estaba pensada para Linux. En el entorno macOS generó conflictos de quoting y rutas durante el proceso de compilación.

Se reemplazó por una condición más precisa:

```cmake
if(${CMAKE_SYSTEM_NAME} MATCHES "Linux")
```

De este modo, la macro `FRU_FILES` quedó activa sólo en sistemas Linux y no en macOS.

---

### 7.4 Problema con `LC_RPATH`

Una vez compilado e instalado el ejecutable, el programa no iniciaba correctamente debido a errores del cargador dinámico de macOS, por ejemplo:

```text
Library not loaded: @rpath/ad9361.framework
```

Este problema se originó porque el ejecutable no incluía correctamente las rutas necesarias para localizar bibliotecas y frameworks externos en tiempo de ejecución.

La situación se resolvió agregando rutas con `install_name_tool`, en particular:

```text
/usr/local/lib
/opt/homebrew/opt/libiio/Frameworks
```

A partir de esa corrección, el binario pudo localizar correctamente tanto `ad9361.framework` como `iio.framework`.

---

## 8. Instalación final

Luego de corregir los problemas anteriores, la instalación quedó finalizada mediante:

```bash
sudo make install
```

Los componentes principales quedaron ubicados en:

| Componente        | Ubicación              |
| ----------------- | ---------------------- |
| ejecutable `osc`  | `/usr/local/bin`       |
| librerías `osc`   | `/usr/local/lib`       |
| plugins           | `/usr/local/lib/osc`   |
| recursos gráficos | `/usr/local/share/osc` |

---

## 9. Ejecución del programa

El programa puede ejecutarse mediante:

```text
osc
```

o bien con la ruta completa:

```text
/usr/local/bin/osc
```

La interfaz gráfica **ADI IIO Oscilloscope** permite:

* descubrir dispositivos IIO;
* conectarse a hardware local, remoto, USB o serial;
* visualizar señales;
* configurar distintos parámetros del SDR.

Su correcta ejecución constituyó una validación importante de que todas las bibliotecas necesarias habían sido compiladas, enlazadas e instaladas de forma adecuada.

---

## 10. Creación de una aplicación macOS (Launcher)

Con el objetivo de facilitar el uso del programa y evitar su ejecución manual desde la terminal, se creó un launcher con formato `.app`, compatible con el entorno gráfico de macOS.

Esto permitió abrir la aplicación desde Finder, Launchpad o Spotlight.

### 10.1 Creación de la estructura de la aplicación

Se generó la estructura estándar de una aplicación macOS:

```bash
mkdir -p ~/Applications/ADI-IIO-Oscilloscope.app/Contents/MacOS
```

---

### 10.2 Creación del script ejecutable

Se creó el archivo:

```text
~/Applications/ADI-IIO-Oscilloscope.app/Contents/MacOS/osc
```

con el siguiente contenido:

```bash
#!/bin/bash

export DYLD_LIBRARY_PATH=/usr/local/lib
export DYLD_FRAMEWORK_PATH=/usr/local/lib:/opt/homebrew/opt/libiio/Frameworks

/usr/local/bin/osc
```

Este script define las variables necesarias para que macOS encuentre las bibliotecas dinámicas requeridas al iniciar el programa.

---

### 10.3 Permisos de ejecución

Se asignaron permisos de ejecución al script:

```bash
chmod +x ~/Applications/ADI-IIO-Oscilloscope.app/Contents/MacOS/osc
```

---

### 10.4 Creación del archivo `Info.plist`

Para que macOS reconociera el launcher como aplicación, se creó el archivo:

```text
~/Applications/ADI-IIO-Oscilloscope.app/Contents/Info.plist
```

con el siguiente contenido:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN"
"http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>CFBundleName</key>
    <string>ADI IIO Oscilloscope</string>
    <key>CFBundleExecutable</key>
    <string>osc</string>
    <key>CFBundleIdentifier</key>
    <string>com.analogdevices.iio-osc</string>
    <key>CFBundleVersion</key>
    <string>0.11</string>
</dict>
</plist>
```

---

### 10.5 Resultado

Una vez creado el launcher, la aplicación pudo abrirse directamente como una aplicación nativa de macOS, sin necesidad de recurrir a la terminal.

---

## 11. Resultado final de la instalación local

El proceso permitió ejecutar correctamente **ADI IIO Oscilloscope** en macOS Apple Silicon.

La herramienta quedó plenamente funcional para:

* detección de dispositivos IIO;
* acceso a recursos locales o remotos;
* uso en prácticas de laboratorio con hardware de Analog Devices;
* integración con el entorno de trabajo del laboratorio remoto.

---

## 12. Conclusiones sobre la instalación local

La instalación de herramientas científicas y de laboratorio en macOS puede requerir ajustes manuales debido a:

* diferencias entre Linux y macOS;
* cambios en compiladores modernos;
* proyectos no actualizados para toolchains recientes;
* rutas de bibliotecas distintas a las esperadas por el código original.

No obstante, mediante la compilación manual, la modificación controlada del sistema de build y la configuración correcta de rutas de frameworks y bibliotecas, fue posible ejecutar exitosamente software originalmente orientado a Linux en un entorno macOS moderno.

Este procedimiento permitió disponer de un entorno local apto para interactuar con la infraestructura del laboratorio remoto.

---

## 13. Puesta en funcionamiento del Laboratorio de SDR Remoto

## 13.1 Objetivo específico de la práctica

Además de la instalación local del software, la práctica tuvo como objetivo verificar el acceso y uso de los recursos brindados por el **Laboratorio de SDR Remoto**.

La consigna solicitó específicamente:

* una captura de pantalla de la página web del SDR al acceder a alguna de sus IP internas;
* una captura de pantalla del **Jupyter Hub** disponible en la IP `192.168.1.60`;
* una captura de pantalla de la **gráfica de Densidad Espectral de Potencia (PSD)** obtenida a partir de las muestras capturadas por el SDR mediante la notebook **How To Config SDR.ipynb**;
* reconocer la arquitectura del hardware utilizado;
* comprender las configuraciones básicas del SDR;
* interpretar el flujo de diseño presentado en la notebook.

Por lo tanto, la actividad no se limitó a una instalación de software, sino que incluyó la validación completa del acceso remoto y el uso efectivo del SDR.

---

## 13.2 Acceso al laboratorio remoto

Una vez instalado el cliente VPN, se estableció la conexión a la red institucional del laboratorio usando las credenciales provistas por la cátedra.

Los datos indicados para el acceso fueron:

* servidor VPN: `200.16.19.5:443`
* usuario: `LabSDR2024`
* contraseña: `ComDigitales2024`

Luego de conectarse a la VPN, se obtuvo acceso a la red interna del laboratorio, donde estaban disponibles los siguientes recursos:

* servidor **Jupyter Hub**: `192.168.1.60`
* SDRs remotos:

  * `192.168.1.31`
  * `192.168.1.32`
  * `192.168.1.33`
  * `192.168.1.34`
  * `192.168.1.35`

El flujo de acceso quedó, por lo tanto, definido de la siguiente manera:

**Equipo personal → VPN AnyConnect → Red interna del laboratorio → Jupyter Hub / SDRs remotos**

Este esquema evidencia que el acceso al laboratorio se realiza sobre una red privada y controlada, y no sobre servicios abiertos a Internet pública.

---

## 13.3 Relación entre VPN, Jupyter Hub y SDR remoto

Desde el punto de vista operativo, el procedimiento seguido fue el siguiente:

1. Se estableció la conexión a la red del laboratorio mediante VPN.
2. Se accedió a **Jupyter Hub** en la IP interna `192.168.1.60`.
3. Dentro de ese entorno se ejecutó la notebook **How To Config SDR.ipynb**.
4. Desde la notebook se creó una instancia de control del SDR remoto mediante la biblioteca `pyadi-iio`.
5. A través de dicha instancia se configuraron parámetros del transmisor y del receptor, se transmitieron o capturaron muestras y se obtuvo la gráfica PSD.

Es importante destacar que **Jupyter Hub no reemplaza al SDR**, sino que funciona como entorno remoto de ejecución dentro de la red del laboratorio. El dispositivo físico realmente configurado y utilizado fue el SDR accesible por su dirección IP interna.

En términos técnicos, puede afirmarse que el flujo real fue:

**VPN → acceso a la red privada → Jupyter Hub → código Python con pyadi-iio → SDR remoto**

---

## 14. Arquitectura del hardware utilizado por el SDR

## 14.1 Visión general

El sistema SDR utilizado en la práctica puede entenderse a partir de dos bloques principales:

* un **transceptor RF AD9363**, compatible con la familia AD9361;
* un **SoC Zynq-7000**, encargado del procesamiento digital y del control del sistema.

Ambos componentes conforman una arquitectura SDR típica, donde la parte analógica/radiofrecuencia y la parte digital trabajan de manera integrada.

---

## 14.2 Rol del transceptor AD9363

El **AD9363** es el bloque responsable del procesamiento de radiofrecuencia. Integra funciones de transmisión y recepción, entre ellas:

* mezcladores en cuadratura;
* filtros analógicos de RF y banda base;
* conversores ADC y DAC;
* bloques de interpolación y decimación;
* control automático o manual de ganancia;
* filtros FIR digitales;
* sintetizadores locales para conversión de frecuencia;
* mecanismos de calibración y loopback.

Esto convierte al AD9363 en el núcleo reconfigurable del SDR, ya que muchos parámetros físicos del sistema pueden modificarse por software.

Los parámetros que se controlan desde la notebook, como frecuencia de muestreo, ancho de banda, frecuencia local o ganancia, se corresponden directamente con bloques funcionales concretos dentro del transceptor.

---

## 14.3 Rol del Zynq-7000

El **Zynq-7000 SoC** cumple la función de plataforma de procesamiento digital y de interfaz con el software de usuario. Combina:

* procesadores ARM Cortex-A9;
* lógica programable tipo FPGA;
* controladores DMA;
* memoria y periféricos;
* interfaces de comunicación.

Su función dentro del SDR es:

* recibir datos del transceptor;
* mover muestras mediante DMA;
* exponerlas al sistema Linux;
* permitir que software como `libiio`, `pyadi-iio`, Jupyter o IIO Oscilloscope controle el hardware.

Por lo tanto, el Zynq actúa como el puente entre la parte RF y la capa software.

---

## 14.4 Cadena software-hardware

La pila de trabajo utilizada durante la práctica puede resumirse de la siguiente forma:

**Notebook en Jupyter**
→ **pyadi-iio**
→ **libiio**
→ **Linux + drivers IIO**
→ **DMA / Zynq**
→ **AD9363**
→ **cadena de transmisión/recepción RF**

Esta descripción permite visualizar que la experiencia integró varias capas, desde la interfaz de programación en Python hasta el comportamiento físico del hardware SDR.

---

## 15. Interpretación de la notebook “How To Config SDR.ipynb”

## 15.1 Propósito general

La notebook **How To Config SDR.ipynb** tiene como finalidad introducir el uso básico del SDR y mostrar cómo se relacionan los parámetros configurados por software con el comportamiento de la señal observada.

No se trata solamente de ejecutar código para obtener una figura, sino de comprender:

* cómo se crea el objeto SDR;
* qué parámetros del hardware pueden modificarse;
* qué efecto produce cada uno;
* cómo verificar esos efectos en el dominio temporal y frecuencial.

---

## 15.2 Vinculación con el SDR remoto

La notebook crea una instancia del tipo:

```python
sdr = adi.Pluto(Uri)
```

donde `Uri` representa la dirección del dispositivo remoto.

Esto significa que el código Python interactúa con un equipo real accesible por red. A partir de ese objeto, es posible:

* configurar transmisión;
* configurar recepción;
* ajustar ganancias;
* establecer anchos de banda y frecuencias locales;
* transmitir muestras;
* capturar muestras;
* representar resultados gráficamente.

---

## 15.3 Señales de prueba utilizadas

La notebook trabaja con señales complejas, en particular con:

### a) Exponencial compleja

Se utiliza una señal del tipo:

$$
s(nT_s) = e^{j2\pi f_c n T_s}
$$

Esta señal permite estudiar el comportamiento de una portadora compleja en banda base y observar:

* componentes I y Q;
* relación entre frecuencia configurada y ubicación del pico espectral;
* respuesta básica del sistema de transmisión y recepción.

### b) Señal QPSK

También se utiliza una señal modulada QPSK, que representa un caso más realista de modulación digital.

Su uso permite observar:

* naturaleza compleja de la modulación;
* distribución de energía en banda;
* diferencias respecto de una portadora tonal simple.

---

## 15.4 Parámetros principales del SDR configurados en la notebook

La notebook introduce una serie de parámetros fundamentales:

### 1. Loopback

Permite realimentar internamente la señal para realizar pruebas controladas, evitando en algunos casos depender de un trayecto RF externo.

### 2. Frecuencia de muestreo (`sample_rate`)

Determina la tasa a la que se procesan las muestras digitales.

### 3. Ancho de banda RF (`tx_rf_bandwidth`, `rx_rf_bandwidth`)

Define el ancho de banda de los filtros asociados a la cadena analógica del transmisor y del receptor.

### 4. Ganancia o atenuación

Permite ajustar el nivel de transmisión y la sensibilidad de recepción.

### 5. Frecuencia local (`tx_lo`, `rx_lo`)

Define la frecuencia de conversión entre banda base y RF.

### 6. Buffers

Establece la cantidad de muestras transmitidas o recibidas en cada operación.

### 7. Transmisión y recepción de muestras

Finalmente, la notebook efectúa la transmisión de la señal y la captura de muestras en el receptor.

---

## 16. Interpretación de la gráfica de Densidad Espectral de Potencia (PSD)

## 16.1 Qué representa la PSD

La **Power Spectral Density (PSD)** representa cómo se distribuye la potencia de la señal en función de la frecuencia.

En el contexto de la práctica, la PSD es una herramienta de validación que permite verificar:

* que el SDR está capturando muestras correctamente;
* que la señal transmitida aparece en la región espectral esperada;
* que los parámetros configurados en el sistema tienen coherencia con el resultado obtenido.

---

## 16.2 Qué observar en la PSD

Para interpretar correctamente la gráfica es conveniente prestar atención a los siguientes aspectos:

### a) Presencia de energía claramente visible

La existencia de un pico o una banda claramente distinguible respecto del piso de ruido indica que la señal fue efectivamente transmitida y recibida.

### b) Ubicación espectral

La posición del contenido espectral debe ser consistente con la frecuencia configurada y con el esquema de representación utilizado.

### c) Ancho de banda observado

Permite diferenciar entre una señal de tipo tonal y una señal modulada, como por ejemplo QPSK.

### d) Piso de ruido

Permite evaluar el nivel de ruido de fondo o la presencia de interferencias.

### e) Forma general del espectro

Una forma razonable y estable del espectro indica coherencia en la generación y captura de la señal.

---

## 16.3 Interpretación del resultado obtenido

Si la gráfica PSD obtenida en la práctica mostró la señal esperada, puede afirmarse que:

* la conexión con el SDR remoto fue correcta;
* la configuración aplicada desde la notebook fue efectiva;
* la transmisión y recepción de muestras se realizó satisfactoriamente;
* el entorno del laboratorio remoto funcionó de forma integral.

Una formulación adecuada para el informe sería la siguiente:

> La gráfica de densidad espectral de potencia obtenida a partir de las muestras recibidas evidenció la presencia de la señal configurada en la notebook. Esto permitió verificar el funcionamiento correcto de toda la cadena de acceso remoto, configuración del SDR, transmisión, recepción y análisis espectral. La PSD actuó, por lo tanto, como evidencia experimental del correcto uso del sistema SDR remoto.

---

## 17. Flujo de diseño observado en la práctica

A partir del trabajo realizado, el flujo general de diseño puede resumirse del siguiente modo:

1. Definición de la señal a transmitir en Python.
2. Configuración de parámetros del SDR.
3. Envío de muestras complejas al transmisor.
4. Procesamiento interno del transceptor:

   * interpolación;
   * filtrado;
   * mezcla;
   * conversión D/A;
   * salida RF.
5. Recepción:

   * conversión descendente;
   * filtrado;
   * conversión A/D;
   * decimación;
   * entrega de muestras I/Q.
6. Transferencia de datos por DMA y exposición al software.
7. Captura en Python y representación de resultados.

Este flujo deja en evidencia la integración entre procesamiento digital, configuración de hardware por software y validación experimental mediante observación espectral.

---

## 18. Evidencias solicitadas por la consigna

De acuerdo con la consigna de la práctica, las evidencias a adjuntar en la entrega son las siguientes:

### 18.1 Acceso a una IP del SDR

Debe incluirse una captura de pantalla de la página accesible desde alguna IP interna del SDR, por ejemplo:

```text
192.168.1.31
```

Esta captura demuestra conectividad con el recurso remoto.

### 18.2 Acceso a Jupyter Hub

Debe incluirse una captura del servicio accesible en:

```text
192.168.1.60
```

Esta evidencia demuestra que el entorno remoto de ejecución estuvo disponible y operativo.

### 18.3 Gráfica PSD generada desde la notebook

Debe incluirse una captura de la PSD obtenida a partir de las muestras capturadas en la notebook **How To Config SDR.ipynb**.

Esta es la evidencia principal del uso efectivo del SDR.

---

## 19. Resultado operativo de la práctica

A partir del procedimiento realizado, puede afirmarse que:

* se logró establecer la conexión al laboratorio remoto mediante VPN;
* se accedió correctamente al servidor Jupyter Hub;
* se obtuvo acceso a los dispositivos SDR internos;
* se ejecutó la notebook de configuración del SDR;
* se configuraron parámetros del equipo remoto;
* se capturaron muestras del sistema;
* se generó la gráfica PSD solicitada.

Por lo tanto, la práctica permitió tanto la puesta en funcionamiento del entorno remoto como la validación del flujo completo de control y observación del SDR.

---

## 20. Conclusión final de la práctica

La práctica permitió integrar en una misma experiencia los siguientes aspectos:

* conectividad segura mediante VPN;
* acceso remoto a infraestructura académica;
* uso de notebooks como interfaz de control de hardware;
* comprensión básica de la arquitectura de un sistema SDR;
* configuración de parámetros fundamentales del transceptor;
* validación experimental mediante análisis espectral.

Desde el punto de vista formativo, la actividad resultó especialmente valiosa porque articuló contenidos de:

* comunicaciones digitales;
* procesamiento digital de señales;
* radiofrecuencia;
* sistemas embebidos;
* instrumentación y control por software.

Asimismo, mostró de manera concreta cómo herramientas de alto nivel como **Jupyter Hub**, **Python**, **pyadi-iio** e **IIO Oscilloscope** pueden emplearse para operar hardware complejo de forma remota, vinculando directamente teoría, configuración y observación experimental.
