## Arquitectura del transmisor y del receptor

> **Referencias.** Bixio Rimoldi §3.4 (*Transmitter and receiver architecture*,
> **págs. 102–107**; la descomposición es la **Fig. 3.2, pág. 96** y su detalle la **Fig. 3.4,
> pág. 103**). La suficiencia de $Y$ **dicta la arquitectura**.

---

### 1. Transmisor en dos etapas

- **Encoder:** mapea el mensaje $i\in\mathcal H$ a la n-tupla $c_i\in\mathbb R^n$ (la *palabra de
  código*; el conjunto $\mathcal C$ es el *codebook*). Es el mismo objeto de la Unidad 2.
- **Waveform former:** convierte la n-tupla en forma de onda multiplicando cada coeficiente por
  su función base y sumando:

$$
\boxed{\;w_i(t)=\sum_{j=1}^{n} c_{i,j}\,\psi_j(t).\;}
$$

Es el "interpolador" del mundo discreto al continuo.

---

### 2. Receptor en dos etapas

- **n-Tuple former:** proyecta la señal recibida sobre cada elemento de la base (un
  **correlador** por rama: multiplicar por $\psi_j^*(t)$ e integrar):

$$
Y_j=\int R(\alpha)\,\psi_j^*(\alpha)\,d\alpha .
$$

  Realiza una **reducción masiva de datos**: de la función $R(t)$ a $n$ números — sin perder
  información (estadística suficiente).
- **Decoder:** resuelve $H=i:\;Y=c_i+Z$, $Z\sim\mathcal N(0,\tfrac{N_0}{2}I_n)$ — el problema de
  la Unidad 2 (MAP/ML/mínima distancia).

---

### 3. Por qué recuperar los coeficientes funciona

Las $\psi_j$ son **ortonormales**. Al proyectar la suma $w_i=\sum_k c_{i,k}\psi_k$ sobre
$\psi_j$, sobreviven sólo los términos con $k=j$:

$$
\langle w_i,\psi_j\rangle=\sum_k c_{i,k}\underbrace{\langle\psi_k,\psi_j\rangle}_{\delta_{kj}}=c_{i,j}.
$$

Sin ruido, el n-tuple former devuelve exactamente la palabra $c_i$; con ruido, le suma
$Z\sim\mathcal N(0,\tfrac{N_0}{2}I_n)$. *(La demo interactiva de abajo hace exactamente esto.)*

---

### 4. Observaciones de diseño

- La descomposición refleja la **filosofía de capas** (OSI): encoder y decoder "conversan" como
  si mediara un canal AWGN discreto; el servicio lo prestan waveform former y n-tuple former.
- Siempre se podría mapear directamente $\mathcal H\to\mathcal W$ sin pasar por $\mathcal C$,
  pero la descomposición es el **estándar moderno** (la teoría de codificación estudia pares
  encoder/decoder).
- La base $\{\psi_j\}$ se obtiene con **Gram–Schmidt** sobre $\mathcal W$ (o se elige "a mano"
  una más cómoda).

---

### 5. Para el pizarrón

1. TX = encoder ($i\to c_i$) + waveform former ($w_i=\sum_j c_{i,j}\psi_j$).
2. RX = n-tuple former ($Y_j=\langle R,\psi_j\rangle$, correladores) + decoder (Unidad 2).
3. Ortonormalidad ⇒ $\langle w_i,\psi_j\rangle=c_{i,j}$ (se recuperan los coeficientes).
4. Canal equivalente: $Y=c_i+Z$, $\sigma^2=N_0/2$.
5. Es la materialización de la estadística suficiente + capas OSI.
