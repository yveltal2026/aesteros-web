# Sitio de Aesteros

Sitio público comercial de **Aesteros** («Percepción, comparada»), con su arquitectura original sin frameworks intermedios:

- **WebGL nativo de 15,000 puntos** (`fuente/home.js`): 15,000 puntos en escritorio (5,000 en móvil) formando las seis figuras de la portada a partir de la posición real de los elementos y `fuente/curvas.json`.
- **GSAP 3.12.5 + ScrollTrigger con capítulos `position: sticky`** (`fuente/home.js`, `fuente/home.css`): cinco capítulos con `scrub: 1.1` y margen negativo de traslape (`-100svh`), más apertura pausada (`3.4 s`).
- **Síntesis y reproducción de audio interactivo** (`sitio/snd/*.mp3` y `snd/*.mp3`): logo sonoro recreado por síntesis (`logo.mp3`), colchón (`base.mp3`) con filtro pasa bajos (`BiquadFilterNode`) que se abre al enfocar, y sonidos de interacción (`foco.mp3`, `sello.mp3`, `ok.mp3`, `menu.mp3`).
- **Tipografía variable `Archivo`** (Google Fonts, ejes `wdth 62..125` y `wght 400..800`).
- **Buscador estático (`Pagefind`)** pre-indexado en `pagefind/` y `sitio/pagefind/` en español (`1,238` palabras indexadas).

## Estructura

| Carpeta o archivo | Qué es |
|---|---|
| `index.html` y `sitio/index.html` | El sitio compilado completo en un solo archivo listo para servir |
| `img/` y `sitio/img/` | Capturas de la interfaz y el anuncio de ejemplo de Brisa |
| `snd/` y `sitio/snd/` | Seis sonidos de marca en mp3 |
| `pagefind/` y `sitio/pagefind/` | Índice estático de búsqueda generado con Pagefind |
| `fuente/` | Generador (`build.py`), estilos (`site.css`, `home.css`), lógica (`site.js`, `home.js`), `curvas.json`, biblioteca de ilustraciones (`ilus_lib.py`) y logotipo (`aesteros-logo-claro.svg`) |
| `contenido/` | Archivos Markdown con el texto de las 24 vistas |
| `buscadores.csv` | Tabla de direcciones, títulos y descripciones para buscadores |
| `LEEME.md` | Documentación completa de la entrega |

## Cómo regenerar el sitio

```bash
cd fuente && python3 build.py
npx -y pagefind --site sitio && cp -r sitio/pagefind .
```
