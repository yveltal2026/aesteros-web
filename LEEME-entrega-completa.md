# Aesteros: entrega completa para Cristian

18 de noviembre de 2026. Todo lo desarrollado hasta hoy para la marca, la interfaz de la plataforma y el sitio público, en tres paquetes. Este documento es el índice: qué hay, dónde está, en qué orden conviene usarlo y qué falta.

## Los tres paquetes

| Paquete | Para qué | Empieza por |
|---|---|---|
| `Aesteros-Entrega-1-Marca.zip` | Identidad: manual, logotipo, color, tipografía, iconos, ilustraciones, gráficas, movimiento, sonido, plantillas | `Aesteros-Manual-v2.html` |
| `Aesteros-Entrega-2-Interfaz.zip` | Las 88 pantallas de la plataforma en claro y profundo, con su fuente y el mapa pantalla a componente | `documentos/entrega.md` |
| `Aesteros-Entrega-3-Sitio.zip` | La maqueta del sitio público, su fuente, su contenido en texto y la tabla para buscadores | `LEEME.md` |

## 1. Marca

| Carpeta | Contenido |
|---|---|
| `Aesteros-Manual-v2.html` y `.pdf` | Manual de identidad, versión 3.0, 130 páginas. La versión HTML tiene las animaciones y los sonidos |
| `aesteros-colores.css` | Variables de color listas para usar |
| `logo/` | Logotipo en SVG y PNG, ediciones (claro, oscuro, una tinta, reducido) y versión animada |
| `elementos/iconos/` | 56 iconos en SVG (color, crema, tinta) y PNG (24, 48, 96) y los sellos Medido, Estimado y Modelado |
| `ilustracion/` | 99 ilustraciones del sistema de puntos en SVG |
| `graficas/` | 16 gráficas modelo en SVG y PNG, con ejemplos |
| `fondos/`, `fotografia/`, `3d/` | Fondos, referencias de fotografía y renders |
| `movimiento/` y `sonido/` | Sonidos de interfaz, de movimiento, logo sonoro y música |
| `presentacion/`, `redes/`, `firma/` | Plantilla de PowerPoint, portadas y perfiles para redes, firma de correo |
| `laboratorios/ilustraciones.html` | Visor de todas las ilustraciones |
| `laboratorios/movimiento/` | Laboratorio de movimiento: cada animación con su curva, su duración y su sonido |

Lo esencial para programar: Archivo como única tipografía (sin monoespaciada), ámbar #FFB000, tinta #14110C, crema #FFF7E6, café #7A3E12 y fondo profundo #0B0907. Todo movimiento entra borroso y termina nítido.

## 2. Interfaz de la plataforma

| Carpeta | Contenido |
|---|---|
| `pantallas/` | 88 pantallas en imagen: 50 en claro y 38 en profundo |
| `html/` | Las mismas pantallas en HTML, para inspeccionar medidas, colores y textos. Las fotos y capturas incrustadas pueden no cargar fuera del lienzo: la referencia visual son las imágenes de `pantallas/` |
| `fuente/` | El generador (`gen.py` y sus partes) y los archivos del lienzo de diseño |
| `documentos/entrega.md` | Mapa pantalla a componente, valores del sistema y 13 decisiones por validar |
| `documentos/conciliacion.md` | Cómo se concilió el diseño con los cuatro PDF de especificación de módulos |
| `documentos/investigacion-graficas.md` | Investigación de gráficas por herramienta que respalda las decisiones |

Los 12 módulos de la especificación tienen diseño. Faltan por validar las 13 decisiones de `entrega.md`; la más delicada es la escala de emoción con figuras redibujadas.

## 3. Sitio público

Detallado en el `LEEME.md` de ese paquete: 24 vistas, sistema visual, piezas que conviene portar, qué es maqueta, herramientas sugeridas, dominios y lista de pendientes. `buscadores.csv` trae dirección, título y descripción de cada página.

## Artefactos en línea

Viven en la cuenta de Claude de Jorge y son privados hasta que él los comparta.

| Artefacto | Qué es |
|---|---|
| Sitio de Aesteros | La maqueta navegable del sitio, siempre en su última versión |
| Aesteros · Interfaz | El lienzo con las 88 pantallas, editable |
| Kit de marca | El manual y el kit publicados |
| Ilustraciones | El visor del sistema de ilustración |
| Plantilla en Google Slides | Copia de la plantilla de presentación. No se verificó después de convertirla |

## Documentos que quedan en el proyecto de Claude

No vienen en los paquetes porque se mantienen ahí: el brief de plataforma, el plan del sitio a la plataforma y la guía de voz para blog y ayuda. Jorge puede compartir el proyecto o exportarlos.

## Orden de trabajo sugerido

1. Leer `entrega.md` de interfaz y resolver con Jorge las 13 decisiones.
2. Montar el sistema de diseño en código: variables de color, tipografía, curvas y duraciones, sellos, botones, tarjetas de vidrio y menú flotante. Sirve a la plataforma y al sitio.
3. Construir las pantallas de la plataforma por módulo, empezando por la carcasa y un módulo completo.
4. Pasar el sitio a código con una dirección por página y conectar el formulario.
5. Configurar dominios, correo y medición, y publicar.

## Herramientas sugeridas

Parten de lo que ya usan (Vercel y Supabase). Son propuesta, no requisito.

| Para | Sugerencia |
|---|---|
| Sistema de diseño compartido | Un paquete de componentes en el mismo repositorio o en uno aparte, con Storybook para revisarlos |
| Variables de diseño | Un solo archivo de variables CSS, a partir de `aesteros-colores.css` |
| Plataforma | El marco que ya tienen, con los componentes del punto anterior |
| Sitio | Astro o Next.js en Vercel, contenido en Markdown |
| Animación | CSS para revelados y GSAP con ScrollTrigger para la portada. Confirmar licencia vigente |
| Gráficas de la plataforma | SVG propio o D3, siguiendo las gráficas modelo. Las bibliotecas de gráficas genéricas no dibujan el margen difuso |
| Pruebas visuales | Capturas automáticas con Playwright contra `pantallas/`, para detectar diferencias |
| Formularios y correo | Supabase y un servicio de correo con dominio propio |
| Medición | Analítica sin cookies y Search Console |
| Errores | Sentry o similar |

## Todo lo que falta

### Decisiones

- Las 13 decisiones de interfaz.
- Nombres Campus, Pro y Lite.
- Si la lectura del rostro se muestra desde el inicio: el brief la deja como módulo opcional tras revisión legal.
- Quién opera la plataforma y firma contratos.

### Legal

- Revisión por abogado de privacidad, términos y uso de cámara, con sus datos pendientes.
- Revisión propia para Honduras.
- Contrato de encargo por cliente.

### Marca

- Verificar la plantilla en PowerPoint y en Google Slides reales.
- Plantilla para las presentaciones de Claude.
- Grabación profesional de la voz, que quedó en pausa.

### Interfaz

- Ver las pantallas dentro del visor del lienzo y las tres últimas en profundo.
- Pantallas que surjan al programar y no estén en la especificación.

### Sitio

- Pasarlo a código, conectar formularios y acceso.
- Probarlo en teléfonos reales.
- Ocho artículos de ayuda que dependen de la plataforma final.
- Validar las cifras del ejemplo de Brisa y las afirmaciones de método escritas para la maqueta.
- Imagen para compartir, icono del sitio y mapa del sitio.

### Antes de cobrar

- Infraestructura de paga y prueba de carga.
- Correo propio, medición de uso y cupos de IA por organización.
