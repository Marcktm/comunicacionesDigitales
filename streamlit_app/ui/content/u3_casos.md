## Casos de modulación: mismo codebook, distintas formas de onda

> **Referencias.** Bixio Rimoldi, Ejemplo 3.7 (señales ortogonales, **págs. 103–106**, con la
> **Fig. 3.5, pág. 103**) y Ejemplos 3.8–3.10 (PAM/PSK/QAM de un solo pulso, **pág. 106**).
> Dos lecciones: (1) formas de onda muy distintas pueden compartir el **mismo codebook** ⇒ misma
> $P_e$; (2) en binario, **sólo importa la distancia** entre señales.

---

### 1. Cuatro elecciones con el mismo codebook

Elegimos $\mathcal W=\{w_0(t),w_1(t)\}$ con dos señales **ortogonales de energía $E$**:

$$
\langle w_i,w_j\rangle=\begin{cases}E,& i=j\\ 0,& i\neq j\end{cases}
\;\Longrightarrow\;
c_0=(\sqrt E,\,0)^{\mathsf T},\quad c_1=(0,\,\sqrt E)^{\mathsf T}.
$$

**Elección 1 — PPM rectangular:** un pulso rectangular en $[0,T]$ para $H=0$ y en $[T,2T]$ para
$H=1$ (la información va en la **posición**). Fácil de generar (un interruptor), pero sus lóbulos
espectrales decaen lento.

**Elección 2 — FSK ortogonal:** dos senos de frecuencias distintas $\tfrac{k}{2T}$ y
$\tfrac{l}{2T}$ ($k\neq l$ enteros) en $[0,T]$ (la información va en la **frecuencia**). La
ortogonalidad sale de $\sin\alpha\sin\beta=\tfrac12[\cos(\alpha-\beta)-\cos(\alpha+\beta)]$: al
integrar sobre $[0,T]$ con $k\ne l$ enteros, ambas integrales se anulan.

**Elección 3 — PPM sinc:** $w_0\propto\operatorname{sinc}(t/T)$ y
$w_1\propto\operatorname{sinc}((t-T)/T)$. Tienen **soporte finito en frecuencia** y son
ortogonales (se ve por Fourier/Parseval, o por el criterio de Nyquist de la Unidad 5).

**Elección 4 — Espectro ensanchado:** secuencias de *chips* $\pm1$ **ortogonales** (p. ej. filas
de Hadamard) de duración $T/n$. Usa mucho ancho de banda pero es robusto a interferencias.

---

### 2. Misma probabilidad de error para las cuatro

Como el codebook es el mismo y el decoder es el de la Unidad 2, $P_e$ es **idéntica**. Con ML y
priori uniforme:

$$
P_e=Q\!\left(\frac{\lVert c_1-c_0\rVert}{2\sigma}\right),\qquad \sigma^2=\frac{N_0}{2}.
$$

La distancia se calcula de tres maneras equivalentes:

$$
\lVert c_1-c_0\rVert=\sqrt{E+E}=\sqrt{2E}
\;=\;\lVert w_1-w_0\rVert=\sqrt{\textstyle\int (w_1-w_0)^2\,dt}
\;=\;\sqrt{\lVert w_0\rVert^2+\lVert w_1\rVert^2}\ \text{(Pitágoras, por ortogonalidad)} .
$$

Sustituyendo:

$$
\boxed{\;P_e=Q\!\left(\frac{\sqrt{2E}}{2\sqrt{N_0/2}}\right)=Q\!\left(\sqrt{\frac{E}{N_0}}\right).\;}
$$

**Sólo depende de $E/N_0$** — no de la forma de onda elegida.

---

### 3. PAM, PSK y QAM de un solo pulso

Con un pulso $\psi(t)$ de energía unitaria y (para PSK/QAM) el par ortonormal
$\psi_1(t)=\sqrt{\tfrac2T}\cos(2\pi f_ct)\,\mathbb 1_{[0,T]}$,
$\psi_2(t)=\sqrt{\tfrac2T}\sin(2\pi f_ct)\,\mathbb 1_{[0,T]}$ (ortonormales si $2f_cT$ es entero):

- **PAM** ($n=1$): $w_i(t)=c_i\,\psi(t)$ con $c_i\in\{\pm a,\pm3a,\dots\}$ — la información va en
  la **amplitud**.
- **PSK** ($n=2$): $w_i(t)=\sqrt{\tfrac{2E}{T}}\cos\big(2\pi f_ct+\tfrac{2\pi i}{m}\big)$; con la
  identidad del coseno de la suma, $c_i=\sqrt E\,(\cos\tfrac{2\pi i}{m},\,\sin\tfrac{2\pi i}{m})^{\mathsf T}$
  — puntos sobre un **círculo** (la información va en la **fase**).
- **QAM** ($n=2$): $w_i=c_{i,1}\psi_1+c_{i,2}\psi_2$ con $c_{i,k}\in\{\pm a,\pm3a,\dots\}$ —
  **grilla** en el plano (amplitud + fase). Es la modulación dominante (WiFi, 4G/5G, TV digital).

Sus constelaciones y $P_e$ son las de la Unidad 2 (m-PAM, m-QAM, Voronoi): el canal continuo se
redujo al discreto.

---

### 4. Para el pizarrón

1. Señales ortogonales de energía $E$ ⇒ codebook $(\sqrt E,0)$, $(0,\sqrt E)$ para las 4 elecciones.
2. Verificar ortogonalidad: rectángulos disjuntos / identidad de senos / Fourier / chips Hadamard.
3. $d=\sqrt{2E}$ (por Pitágoras) y $\sigma^2=N_0/2$ ⇒ $P_e=Q(\sqrt{E/N_0})$, **igual para todas**.
4. PAM/PSK/QAM single-shot: base $\{\psi_1,\psi_2\}$ coseno/seno; constelaciones de la Unidad 2.
