# aesteros-web — Sitio comercial de Aesteros

Sitio web comercial de **Aesteros** («Percepción, comparada»), construido sobre la misma infraestructura tecnológica de la plataforma (`Next.js 16`, `React 19`, `TypeScript 5`, `Supabase`, `Vitest`, `Playwright`) a partir del paquete `Aesteros-Entrega-3-Sitio`.

## Qué incluye

- **24 páginas con dirección propia y SEO completo (`buscadores.csv`):**
  - Principales: `/` (Inicio), `/producto`, `/metodo`
  - Soluciones: `/universidades`, `/agencias`, `/empresas`, `/planes`, `/novedades`
  - Blog y glosario: `/blog`, `/blog/como-leer-un-mapa-de-atencion`, `/blog/que-mide-una-prueba-de-asociacion-implicita`, `/blog/practica-de-neuromarketing-cuatro-semanas`, `/blog/caso-brisa-un-anuncio-tres-medidas`, `/blog/una-sonrisa-no-es-una-emocion`, `/blog/margen-de-error-con-una-grafica`, `/glosario`
  - Centro de ayuda: `/ayuda`, `/ayuda/participar`, `/ayuda/como-leer-cada-grafica`, `/ayuda/tu-primer-estudio`
  - Legales y acceso: `/privacidad`, `/terminos`, `/camara`, `/entrar` (`noindex`)
- **Identidad visual y movimiento de marca:**
  - Paleta oficial: Ámbar `#FFB000`, Tinta `#14110C`, Crema `#FFF7E6`, Café `#7A3E12` (`#D9935A` en profundo) y Fondo profundo `#0B0907`.
  - Tipografía variable `Archivo` (ejes de peso y ancho).
  - Nube de puntos en **WebGL** (15 000 puntos en escritorio, 5 000 en móvil) que forma las seis figuras de la portada al avanzar por los capítulos fijos con **GSAP + ScrollTrigger**.
  - Menú flotante con pastilla ámbar viajera (`420 ms`, curva trasladar) y punto difuso para el panel «Explorar».
  - Diseño sonoro interactivo (`public/snd/*.mp3`) con filtro pasa bajos que se abre al enfocar.
- **Laboratorios interactivos:**
  - «Pruébalo tú» en portada: mapa de calor del cursor en vivo y prueba corta de tiempos de respuesta (`E` / `I`).
  - Estudio interactivo de Brisa en `/producto`: áreas de interés del anuncio, subgrupos de asociación implícita, curva de sensibilidad de precio y armador de estudio («Arma tu estudio»).
  - Demostraciones de confianza en portada y `/metodo`: calculadora de intervalo de confianza por muestra, tarjetas de referencia metodológica y línea de tiempo del recorrido de un dato.
- **Formulario conectado (`/api/leads`):**
  - Validación con `Zod` y limitador de peticiones (`src/lib/rate-limit.ts`).
  - Persistencia en `Supabase` (tabla `public.leads` con RLS en `supabase/migrations/20261119000000_leads.sql`) cuando las variables `NEXT_PUBLIC_SUPABASE_URL` y `SUPABASE_SERVICE_ROLE_KEY` están configuradas.
- **Mapa del sitio y buscadores:**
  - `/sitemap.xml` y `/robots.txt` generados automáticamente por Next.js (`src/app/sitemap.ts` y `src/app/robots.ts`).

## Comandos

| Comando | Qué hace |
|---|---|
| `npm run dev` | Levanta el servidor de desarrollo en `http://localhost:3000` |
| `npm run build` | Compila la versión de producción |
| `npm run lint` / `npm run typecheck` | Valida ESLint y tipos de TypeScript |
| `npm test` | Ejecuta pruebas unitarias con Vitest |
| `npm run test:e2e` | Ejecuta pruebas E2E con Playwright |
