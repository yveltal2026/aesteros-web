# Sitio de Aesteros: entrega para Cristian

18 de noviembre de 2026. Este paquete contiene la maqueta completa del sitio público, su contenido en texto y lo que falta para llevarlo a los dominios. La maqueta define diseño, movimiento y textos. No es código de producción.

## Qué hay en el paquete

| Carpeta o archivo | Qué es |
|---|---|
| `sitio/index.html` | La maqueta completa en un solo archivo. Se abre con cualquier servidor local (por ejemplo `python3 -m http.server` dentro de `sitio/`). Abrirlo con doble clic también funciona, salvo el sonido |
| `sitio/img/` | Capturas de la interfaz y el anuncio de ejemplo de Brisa |
| `sitio/snd/` | Seis sonidos de marca en mp3 |
| `fuente/` | Lo que genera el index: `build.py` (contenido y estructura), `site.css` y `home.css` (estilos), `site.js` y `home.js` (rutas, animación, interacción), `curvas.json`, la biblioteca de ilustraciones y el logotipo |
| `contenido/` | Un archivo de texto por vista, extraído de la maqueta, para copiar a la versión en código sin leer HTML |
| `LEEME.md` | Este documento |

En el proyecto de Claude quedan además tres documentos de apoyo: el plan del sitio a la plataforma, la guía de voz para blog y ayuda, y la tabla de títulos y descripciones para buscadores (resumida abajo).

## Cómo está hecha la maqueta

- **Una sola página con 24 vistas.** Cada vista es una `<section class="view" id="v-nombre">`. La ruta es el símbolo `#nombre`. En producción cada vista debe ser una página con dirección propia.
- **Tres vistas principales** (inicio, producto, metodo) y el resto en «modo explorar», que cambia el menú flotante. El atributo `data-nav` de una vista dice qué opción del menú se marca.
- **Tonos.** Las vistas con clase `dk` son profundas (fondo #0B0907) y las `lt` claras (fondo #FFF7E6). La portada abre profunda y aclara al avanzar.
- **Sin dependencias propias**, salvo GSAP 3.12.5 con ScrollTrigger (desde cdnjs) y la tipografía Archivo (Google Fonts, ejes de ancho y peso).

### Mapa de vistas

| Vista | Qué contiene | Interacción |
|---|---|---|
| inicio | Cinco capítulos fijos al scroll, prueba «Pruébalo tú», nueve herramientas, confianza, antes y después, llamado final | Puntos en WebGL, mapa del cursor, tiempos de respuesta, deslizador de muestra, pestañas, formulario |
| producto | Estudio de Brisa en cinco pasos, «Arma tu estudio», acordeón de las nueve | Selector de audiencia, tres gráficas que se tocan, armador |
| metodo | Sí y no por medida, recorrido de un dato, referencias, preguntas | Tarjetas que se enfocan, línea que avanza |
| universidades, agencias, empresas | Páginas de solución con un caso de ejemplo | Interruptor de marca en el informe (agencias) |
| planes | Campus, Pro y Lite sin cifras | Columnas que se desenfocan al comparar |
| blog, a-mapa, a-asociacion, a-practica, a-brisa, a-sonrisa, a-margen, glosario | Índice, seis artículos y glosario | Filtro por línea |
| novedades | Disponible y en desarrollo | |
| ayuda, participar, guia-graficas, guia-inicio | Centro de ayuda y tres guías | Buscador, tres puertas |
| privacidad, terminos, camara | Borradores legales | |
| entrar | Acceso | Maqueta |

### Sistema visual

- **Color.** Ámbar #FFB000, tinta #14110C, crema #FFF7E6, café #7A3E12 (en profundo #D9935A), fondo profundo #0B0907. Nada más.
- **Punto difuso.** `radial-gradient(circle closest-side, #FFA200 0, #FFA800 30%, rgba(255,176,0,.5) 62%, rgba(255,176,0,0) 100%)`.
- **Tipografía.** Archivo. Títulos en 800 con ancho 108 a 112 %. Sin monoespaciada.
- **Curvas.** Enfocar `cubic-bezier(.16,.84,.24,1)`, desenfocar `cubic-bezier(.6,0,.84,.2)`, trasladar `cubic-bezier(.65,0,.35,1)`.
- **Duraciones.** 160 ms (toque), 360 a 420 ms (cambio), 720 ms (entrada), 1,4 a 1,8 s (enfoque de titular).
- **Regla de movimiento.** Todo entra borroso y termina nítido. Una sola idea de movimiento por página fuera de la portada.

### Piezas que conviene portar tal cual

| Pieza | Dónde está | Nota |
|---|---|---|
| Puntos de la portada | `home.js`, bloque «puntos en WebGL» | WebGL sin biblioteca. 15 000 puntos en escritorio, 5 000 en teléfono. Seis figuras calculadas a partir de la posición de elementos de la página. El avance se suaviza con inercia |
| Capítulos fijos | `home.js`, función `chapter` | `position: sticky` más ScrollTrigger con `scrub`. Los capítulos se traslapan con margen negativo de una pantalla |
| Menú flotante | `home.js`, bloques de menú | Pastilla ámbar que viaja 420 ms con estiramiento y desenfoque a medio camino. Punto difuso que revela «Explorar» y abre el panel |
| Sonido | `home.js`, bloque de sonido | Activado por defecto, arranca con el primer toque (los navegadores no permiten antes). Filtro pasa bajos que se abre al enfocar. Recuerda si se apagó |
| Apertura pausada | `home.js`, variables `IT0`, `ITD` y función `endIntro` | Al cargar la portada, la nube de puntos se forma desde los bordes durante unos 3,4 segundos y después se enfoca el texto. Un toque, una tecla o deslizar la saltan. Solo corre si se entra por la portada |
| Logo sonoro suave | `sitio/snd/logo.mp3` | Recreado por síntesis (colchón que se abre y las notas mi y si), a 160 kbps. Suena con el primer toque y la música entra después con una subida lenta |
| Revelados | Atributo `data-rv` y un IntersectionObserver | Sirve en todas las vistas |
| Mini gráficas | `build.py`, diccionario `MINI` | SVG de 200 por 120. Se dibujan con clases `dr`, `po`, `gx`, `gy` |
| Modo sin movimiento | Clase `anim` en `html` | Sin GSAP o con movimiento reducido, todo el contenido queda visible y estático |

## Qué es maqueta y hay que construir

- **Formularios.** El de demostración, el de entrada y el de código de grupo no envían nada.
- **Entrar.** No abre la plataforma.
- **Buscador de ayuda.** Filtra los títulos que están en la página; no busca en el contenido.
- **Direcciones.** Todo vive en una página con `#`. Los buscadores no ven las vistas por separado.
- **«Pruébalo tú».** El mapa sigue el cursor y los tiempos se miden en el navegador. Nada se guarda. Así debe quedarse en el sitio público.
- **Datos.** Todas las cifras son del ejemplo de Brisa.

## Herramientas sugeridas

Son sugerencias pensadas para un equipo chico que ya usa Vercel y Supabase. Cristian decide.

| Necesidad | Sugerencia | Por qué |
|---|---|---|
| Sitio público | Astro o Next.js en Vercel, en un repositorio aparte del de la plataforma | Páginas estáticas rápidas, una dirección por página y despliegue igual al que ya conocen. Astro pesa menos para un sitio de contenido; Next.js si prefieren un solo marco con la plataforma |
| Contenido de blog, glosario y ayuda | Archivos Markdown o MDX en el repositorio | Sin costo ni panel que mantener. Si después escriben personas no técnicas, se añade un gestor de contenido sin cabeza |
| Animación | GSAP con ScrollTrigger, como en la maqueta | Ya está resuelto con eso. Confirmar la licencia vigente antes de publicar |
| Formularios | Una tabla en Supabase más una función que avise por correo | Ya tienen Supabase. Añadir protección contra envíos automáticos |
| Correo de salida | Un servicio de correo transaccional con dominio propio (por ejemplo Resend, Postmark o Amazon SES) | El brief ya lo pide para las altas. Configurar SPF, DKIM y DMARC |
| DNS | El del registrador o Cloudflare | Hace falta manejar el subdominio de la aplicación y el comodín de organizaciones |
| Medición de visitas | Una herramienta sin cookies (por ejemplo Plausible o la analítica de Vercel) | Evita el aviso de cookies y es coherente con el discurso de privacidad |
| Buscadores | Google Search Console y un mapa del sitio generado en el despliegue | Para ver qué se indexa y con qué búsquedas llegan |
| Buscador de la ayuda | Pagefind u otro índice estático | Busca en el contenido sin servidor |
| Estado del servicio | Una página de estado alojada aparte | Para cuando haya clientes; no es urgente |
| Errores en producción | Sentry o similar, en sitio y plataforma | Para enterarse antes que el cliente |

## Dominios

1. `aesteros.com` para el sitio público. Los otros dominios comprados redirigen a este con redirección permanente.
2. `app.aesteros.com` para la plataforma, fuera del índice de buscadores.
3. `*.aesteros.com` para la entrada de cada organización (por ejemplo `unitec.aesteros.com`), resuelto por la plataforma.
4. Certificados para el dominio, el subdominio y el comodín.
5. Correo del dominio con SPF, DKIM y DMARC antes de enviar la primera invitación.

## Direcciones, títulos y descripciones

| Vista | Dirección | Título |
|---|---|---|
| inicio | / | Aesteros: neuromarketing en línea, con personas reales |
| producto | /producto | Cómo funciona un estudio de neuromarketing en Aesteros |
| metodo | /metodo | Método: lo que Aesteros puede decir y lo que no |
| universidades | /universidades | Laboratorio de neuromarketing para universidades |
| agencias | /agencias | Pruebas de creatividad para agencias, con evidencia |
| empresas | /empresas | Prueba tu empaque, anuncio o precio antes de producir |
| planes | /planes | Planes de Aesteros: Campus, Pro y Lite |
| novedades | /novedades | Novedades de Aesteros |
| blog | /blog | Blog de Aesteros: leer la percepción, con calma |
| a-mapa | /blog/como-leer-un-mapa-de-atencion | Cómo leer un mapa de atención sin engañarte |
| a-asociacion | /blog/que-mide-una-prueba-de-asociacion-implicita | Qué mide una prueba de asociación implícita |
| a-practica | /blog/practica-de-neuromarketing-cuatro-semanas | Una práctica de neuromarketing para cuatro semanas |
| a-brisa | /blog/caso-brisa-un-anuncio-tres-medidas | Un anuncio, tres medidas: el caso de Brisa |
| a-sonrisa | /blog/una-sonrisa-no-es-una-emocion | Una sonrisa no es una emoción |
| a-margen | /blog/margen-de-error-con-una-grafica | Margen de error, explicado con una sola gráfica |
| glosario | /glosario | Glosario de neuromarketing en español llano |
| ayuda | /ayuda | Centro de ayuda de Aesteros |
| participar | /ayuda/participar | Voy a participar en un estudio: lo que conviene saber |
| guia-graficas | /ayuda/como-leer-cada-grafica | Cómo leer cada gráfica |
| guia-inicio | /ayuda/tu-primer-estudio | Tu primer estudio, en cinco pasos |
| privacidad | /privacidad | Aviso de privacidad de Aesteros |
| terminos | /terminos | Términos del servicio de Aesteros |
| camara | /camara | Cómo usa Aesteros la cámara |
| entrar | app.aesteros.com | Entrar a Aesteros (sin indexar) |

Las descripciones y la palabra principal de cada página están en el documento del proyecto «Sitio: títulos y descripciones para buscadores».

## Lo que falta

### Para poder publicar

- [ ] Revisión legal de los tres borradores y sus datos entre corchetes: razón social, domicilio, correo de privacidad, encargados, plazos de conservación y jurisdicción. Honduras necesita su propia revisión.
- [ ] Definir quién opera la plataforma y firma contratos.
- [ ] Conectar el formulario de demostración y decidir quién recibe y responde.
- [ ] Pasar la maqueta a código con una dirección por página.
- [ ] Probar la portada en teléfonos reales, sobre todo en iPhone: fluidez de los puntos, sonido y capítulos fijos.
- [ ] Imagen para compartir en redes, icono del sitio y mapa del sitio.
- [ ] Medición de visitas y Search Console.

### Por validar con Cristian (contenido escrito para la maqueta)

- [ ] Nombres Campus, Pro y Lite, que el brief marca como provisionales.
- [ ] Lectura del rostro: el brief la deja como módulo opcional tras revisión legal y el sitio la presenta como una de las nueve herramientas. Hay además un artículo sobre ella.
- [ ] Cifras de Brisa: indicadores por área, subgrupos de la asociación, 52 válidas, 5 excluidas y 3 sin terminar, rango de precio.
- [ ] «Control de calidad»: que cada sesión se revise y se excluyan las que no alcanzan.
- [ ] «No instala nada», «contesta en unos minutos», «resultados en días».
- [ ] Lo que recomienda «Arma tu estudio» para cada pregunta.
- [ ] Consejos de calibración y de cámara de la guía del participante.
- [ ] «El video no sale del dispositivo» y «no da nombre ni correo», que vienen del brief: confirmar que siguen siendo ciertos en todos los módulos.
- [ ] «Portal para tu cliente» marcado como en desarrollo.
- [ ] «Las sumamos conforme pasan nuestra propia validación», que es un compromiso público.

### Contenido pendiente

- [ ] Ocho artículos de ayuda que dependen de la plataforma final: armar un estudio con varias herramientas, invitar, exportar, grupos y códigos, usuarios y permisos, cupos, logotipo y portada, privacidad y borrado.
- [ ] Novedades con fechas reales cuando haya lanzamientos.
- [ ] Casos reales y página de quiénes somos, cuando existan clientes y operador.
- [ ] Versión en inglés, si se decide.

### Antes de cobrar (del brief)

- [ ] Infraestructura de paga y prueba de carga.
- [ ] Correo propio para altas.
- [ ] Contrato de encargo y consentimiento de cámara por país.
- [ ] Medición de uso y cupos de IA por organización.

## Cómo regenerar la maqueta

`fuente/build.py` arma `index.html` a partir de los demás archivos de `fuente/`. Tiene dos rutas fijas del entorno donde se creó (la biblioteca de ilustraciones y el logotipo): hay que cambiarlas a las copias incluidas en `fuente/` antes de ejecutarlo. Para leer o portar el sitio no hace falta regenerarlo: `sitio/index.html` ya es el resultado.
