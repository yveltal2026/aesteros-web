# Aesteros · Entrega 5 · Integración sobre lo publicado

22 de noviembre de 2026 · Para Cristian

Esta entrega no es un sitio nuevo para sustituir el tuyo. Es la versión de hoy del sitio, ya montada sobre lo que tienes publicado en www.aesteros.com, con tus cambios conservados. La carpeta `integrado/` usa tu misma estructura: `index.html`, `css/aesteros.css` y `js/aesteros.js`.

Trabajé solo con lo que se ve desde fuera: bajé tu `index.html`, tu hoja de estilos, tu script, el mapa del sitio y `llms.txt` el 22 de noviembre. No vi tu repositorio ni el paso que genera una página por ruta, así que esa parte la tienes que correr tú.

## 1. Lo que encontré publicado

Partiste del paquete del 18 de noviembre (26 vistas) y le sumaste bastante. Esto es lo que detecté y lo que hice con cada cosa.

| Lo tuyo | Qué pasó aquí |
|---|---|
| Estilos y script en archivos aparte, con `?v=` | Se conserva. Los `?v=` de `integrado/` salen del contenido; pon los tuyos |
| Cabecera completa (canónica, Open Graph, datos estructurados, iconos, manifiesto) | Intacta, copiada tal cual |
| Rutas por dirección (`/producto`, `/blog/...`, `/ayuda/...`) con `__AE_META__` y `__AE_P2V__` | Se conserva. La tabla crece de 25 a 53 vistas |
| Una página por ruta, `sitemap.xml`, `robots.txt`, `llms.txt` | No los toco. Van propuestas en `propuestos/` |
| Iconos en el menú, en los chips de Producto, en «También incluye», en Planes y en Ayuda | Se conservan los 26. Sumé 9 del mismo juego a las entradas nuevas del menú |
| Marca fija arriba en teléfono (`.mbrand`) | Se conserva |
| «Entrar a» lleva a `app.aesteros.com/entrar` | Se conserva |
| «Pruébalo tú» con teclado, imagen de 700 px, pista como enlace | Se conserva |
| Sellos en las tarjetas de herramientas de la portada | Se conservan 8. «Video con lectura del rostro» lleva «En desarrollo» |
| GSAP con integridad, Speed Insights de Vercel | Se conservan |
| Leyenda del pie y «(requerido)» en los campos | Se conservan. «(requerido)» ahora está en los nueve campos obligatorios |
| Diálogo de demostración y página `/demo` | **Sustituidos.** Ver el punto 3 |
| Logotipos de edición en las tarjetas de Planes (`.edlogo`) | **Sustituidos** por los nuestros, que además cambian el color de la tarjeta |
| Tarjetas de audiencia de la portada | **Sustituidas** por tres tarjetas, una por edición |

## 2. Cómo se armó

- **Estilos:** fusión a tres bandas entre lo entregado el 18, lo tuyo y lo de hoy. Resultado: tu archivo completo, sin una sola línea quitada, más las líneas nuevas al final. Lo puedes comprobar en `cambios/aesteros.css.diff`.
- **Script:** misma fusión. De tu archivo cambian cinco líneas y se añade una (están en `cambios/aesteros.js.diff`), y se suma nuestro código nuevo.
- **Marcado:** cambió demasiado para fusionarlo así. Tomé el marcado de hoy y volví a aplicar tus cambios uno por uno. Cada paso está en `BITACORA.txt`.

Todo lo hace `herramienta/integrar.py`. Está escrito para mi entorno y sus rutas de carpeta son las mías; va como referencia de qué se hizo, no para correrlo tal cual.

### Lo que cambia en tu script

1. `__AE_META__` y `__AE_P2V__`: la tabla nueva de rutas.
2. `curView()`: una línea añadida para que `#demo` y `#hablemos` lleven a la vista `solicitar`.
3. `setMeta()`: la vista `error` también sale con `noindex`.
4. `show()`: si se le pide una vista que no existe, muestra `error` en lugar de la portada. Con tu `curView()` eso casi no ocurre, porque un `#` desconocido se resuelve por la dirección; sirve para el `404.html` del paso 7.
5. `route()` y el final del manejador de clics (dos líneas): **una corrección**. Al navegar con `data-go` hacia un punto dentro de otra página, `show()` bajaba al destino y enseguida el `hashchange` que disparas llamaba a `route()`, que volvía arriba. Pasa hoy en lo publicado: «Verla en Producto» o cualquier enlace con destino llega al inicio de la página. Ahora `route()` se salta esa segunda llamada.

## 3. Lo que tienes que decidir

**Hablemos en lugar del diálogo de demostración.** Tu diálogo y tu página `/demo` tienen un solo formulario con «Vengo por». Desde entonces el sitio cambió: hay tres ediciones y cada una tiene su propio formulario y su propio camino (demostración para Campus y Pro, lista de espera para Lite). Lo que hice:

- La vista se llama `solicitar` y vive en tu ruta `/demo`, para no romper la dirección que ya está en tu mapa del sitio.
- Los botones «Pedir una demostración» van a esa página con la edición ya elegida. Ya no abren el diálogo.
- El marcado del diálogo y de `v-demo` no está en `integrado/`. Tu código (`AE.openDemo`, `AE.fillAsk`, `initAsk`) sigue en el script y no estorba: si no encuentra el diálogo, no hace nada. Los estilos de `dialog.demod` también siguen.

Si prefieres mantener el diálogo como atajo, se puede: habría que darle los tres caminos. Dime y lo armamos.

**Tres rutas con dos nombres posibles.** Para lo que ya tenías dejé tus direcciones. En nuestra tabla original tres eran distintas; quédate con las tuyas salvo que quieras cambiarlas:

| Vista | La tuya (se queda) | La que teníamos |
|---|---|---|
| `a-margen` | `/blog/margen-de-error-con-una-grafica` | `/blog/margen-de-error-explicado` |
| `guia-graficas` | `/ayuda/como-leer-cada-grafica` | `/ayuda/graficas` |
| `guia-inicio` | `/ayuda/tu-primer-estudio` | `/ayuda/primer-estudio` |

Las guías nuevas usan nombres cortos (`/ayuda/invitar`, `/ayuda/cupos`). Si quieres que todas sigan tu estilo largo, cámbialas en `rutas.json` antes de generar.

**Dos sellos que conviene revisar.** En la portada marcaste «Baterías e informe» como Estimado y «Auditoría SEO» como Medido. Los dejé como los pusiste. En el brief, las baterías son mixtas (cada cifra lleva su propio sello) y la auditoría es verificable. Jorge y tú deciden si se quedan.

## 4. Qué hay nuevo desde el 18 de noviembre

**Vistas nuevas (28):** `lite`, `solicitar`, `seguridad`, `nosotros`, `preguntas`, seis artículos (`a-muestra`, `a-dos`, `a-rutas`, `a-ia`, `a-evaluar`, `a-precio`), trece guías, `calculadora`, `informe-pro`, `informe-lite`, `plantillas`, `kit` y `error`. La lista completa con ruta, título y descripción está en `rutas.csv`.

**Cambios en lo que ya tenías:**

- **Marca independiente.** FRSKO ya no aparece en ningún lado. En lo publicado quedan tres menciones y una en `llms.txt`.
- **Ocho herramientas.** «Video con lectura del rostro» pasa a «En desarrollo» y deja de contarse. Cambian titulares, textos y la descripción de `/producto`.
- **Ediciones con color.** Campus en crema, Pro en negro, Lite en ámbar, con su logotipo.
- **Producto por edición.** Un selector cambia toda la página: recorrido de Campus, de Pro o de Lite. Dentro de Pro, «para agencias» y «para empresas» cuentan el mismo caso desde dos sillas.
- **Planes.** Tres tarjetas por edición y, abajo, «Y esto es lo que cambia»: siete diferencias, una nota para Pro y el resto plegado.
- **Portada.** El bloque «¿Qué quieres saber?» ya no pide datos: lleva a Hablemos con la pregunta escrita.
- **Método, Universidades, Agencias, Empresas, Novedades, Ayuda y Blog** crecieron. El texto de cada vista está en `referencia/contenido/`.
- **Aviso de cookies** en una píldora abajo, con el interruptor de sonido.

## 5. Pasos para integrar

1. **Abre una rama.** No lo montes sobre la rama que publica.
2. **Copia los tres archivos** de `integrado/` sobre los tuyos: `index.html`, `css/aesteros.css` y `js/aesteros.js`. Revisa el resultado con tu `diff`: en estilos solo debe haber líneas añadidas; en el script, las cinco de arriba y el código nuevo.
3. **Si tu tabla de rutas sale de un archivo propio**, toma `rutas.json`: es el contenido de `__AE_META__` en tu mismo formato (`p`, `u`, `t`, `d`). La vista `demo` ya no existe; `solicitar` ocupa `/demo`.
4. **Genera las páginas por ruta** con tu paso de siempre. Son 53 con `/entrar`.
5. **Sustituye `sitemap.xml` y `llms.txt`** por los de `propuestos/`, o regénéralos con tu herramienta. Los propuestos siguen tu formato: 52 direcciones, ocho herramientas, sin FRSKO.
6. **Imágenes y sonidos:** no hay que subir nada. Las imágenes que usa el sitio y los seis sonidos ya están en tu servidor. `integrado/img/` trae además tres imágenes para compartir por edición (`compartir-campus.jpg`, `compartir-pro.jpg`, `compartir-lite.jpg`), por si quieres que `/universidades`, `/agencias` y `/lite` tengan su propia imagen de Open Graph. Es opcional.
7. **Página no encontrada:** hoy una dirección que no existe devuelve un texto plano de Vercel. La vista `error` ya está en el marcado; basta con generar un `404.html` que la muestre.
8. **Opcional:** redirigir `/hablemos` a `/demo`, porque el menú dice «Hablemos».
9. **Prueba** con la lista del punto 6 y publica.

## 6. Lista de comprobación

- [ ] Las 53 rutas abren su vista al entrar directo por dirección y el título de la pestaña coincide con `rutas.csv`.
- [ ] `/demo` muestra «Hablemos» con los tres formularios; `#demo` también.
- [ ] En `/producto`, el selector de edición cambia fondo y contenido; «para agencias | empresas» cambia titular e informe.
- [ ] En `/producto`, «Comparar ediciones» lleva a `/planes` y baja hasta la tabla. El botón atrás regresa a Producto.
- [ ] En la portada, las tres tarjetas de «Sigue con tu edición» ocupan todo el ancho de su caja.
- [ ] El menú desplegable muestra iconos en todas las entradas y la etiqueta de edición no se corta en teléfono.
- [ ] En `/lite`, el duelo responde al tocar una versión.
- [ ] `/calculadora` muestra su resultado.
- [ ] Ninguna página menciona FRSKO ni «nueve herramientas».
- [ ] Sin errores en la consola. En local faltará `/_vercel/speed-insights/script.js`; es normal.

## 7. Lo que probé yo

Serví `integrado/` con un servidor local que devuelve `index.html` en cualquier ruta, para imitar tu enrutado.

- Las 54 vistas en 1440 y 390 px: cada una se muestra sola, sin desbordes y sin errores de consola.
- Las 53 rutas por dirección abren la vista correcta.
- Navegación con clic, destino dentro de la página y botón atrás.
- Ediciones, selector de Pro, envío del formulario de Campus, duelo de Lite y calculadora.
- Comparé las medidas de cada bloque contra nuestra versión de referencia. Las diferencias que quedan vienen de tus estilos: iconos, sellos y márgenes de cabecera en teléfono.
- Revisión de accesibilidad con axe en las 54 vistas, sin fallas después del último ajuste de contraste.

Lo que no pude probar: tu generador de páginas, el despliegue en Vercel y un teléfono real.

Dos ajustes que salieron de las pruebas y ya están en los estilos: tu regla `.ask .form` en dos columnas rompía el selector de edición de la portada (se corrige con una regla para `.form.nx`), y la etiqueta de edición del menú se cortaba junto a los iconos.

Una observación sobre lo tuyo: cambiaste la regla de movimiento reducido, que antes apagaba todas las animaciones y ahora apaga solo `.focus` y `.blob`. Quien pide menos movimiento sigue viendo el resto. No lo toqué; si fue a propósito, queda así.

## 8. Qué sigue abierto

- Los formularios siguen sin enviar. Hace falta el destino (correo o base) y hola@aesteros.com.
- Privacidad y Términos son borradores con datos entre corchetes. La entidad por ahora es Yveltal.
- Lite sigue en lista de espera; el sitio lo dice en todos lados.

## 9. Para que no vuelva a chocar

El choque de esta vez vino de trabajar los dos sobre copias distintas durante cuatro días. Propuesta:

1. **Tu repositorio es la fuente.** Si nos das acceso de lectura, las siguientes entregas salen ya sobre tu estructura y con tu generador.
2. **Mientras no haya acceso**, cada entrega se arma igual que esta: se baja lo publicado, se fusiona y se entrega `integrado/` con su bitácora y sus diferencias.
3. **Reparto:** cabecera, rutas, despliegue, rendimiento y formularios son tuyos. Texto, vistas nuevas y diseño llegan de este lado. Si cambias texto o diseño, avísanos para tomarlo como base.
4. **Avisa cuando publiques.** La fusión se hace contra lo que esté en línea ese día.

## Contenido del paquete

| Carpeta o archivo | Qué es |
|---|---|
| `integrado/` | El sitio de hoy sobre tu estructura. Es lo que hay que montar |
| `rutas.csv`, `rutas.json` | Las 53 vistas con ruta, título y descripción, y si la ruta es tuya o nueva |
| `propuestos/` | `sitemap.xml` y `llms.txt` actualizados, en tu formato |
| `cambios/` | Diferencias de estilos y script contra tus archivos publicados |
| `BITACORA.txt` | Cada paso de la integración |
| `referencia/publicado-22-nov/` | Lo que bajé de www.aesteros.com y usé como base |
| `referencia/sitio-en-un-archivo/` | Nuestra versión de hoy en un solo archivo, para comparar |
| `referencia/contenido/` | El texto de las 54 vistas en Markdown |
| `herramienta/` | El guion de integración y el servidor local de pruebas |
| `documentos/` | Brief 2.1 con las decisiones 1 a 24 |
