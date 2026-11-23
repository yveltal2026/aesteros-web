"""Integra la versión actual del sitio de Aesteros sobre lo que Cristian tiene publicado en www.aesteros.com.

Tres entradas:
  BASE  = lo que se le entregó el 18 nov (paquete 3 de entonces)
  PUB   = lo publicado (index.html, css/aesteros.css, js/aesteros.js), bajado el 22 nov
  HOY   = el sitio actual en un solo archivo (sitio/index.html)

Estilos y script se fusionan a tres bandas con git merge-file: lo que Cristian cambió se conserva y lo nuestro
se suma. El marcado cambió demasiado para fusionarlo así, de modo que sus cambios se vuelven a aplicar uno por uno
sobre el marcado de hoy. Cada paso deja una línea en salida/BITACORA.txt.
"""
import re, subprocess, sys, json, os, hashlib, csv, shutil, tempfile
sys.path.insert(0, '/home/claude/scripts')
import io, contextlib
with contextlib.redirect_stdout(io.StringIO()):
    from assets_manual import icon_svg

R = '/home/claude/integra/'
PUB = R + 'publicado/'
OUT = R + 'salida/'
BASE = '/home/claude/pk/3/Aesteros-Entrega-3-Sitio/sitio/index.html'
HOY = '/home/claude/sitio/index.html'
CSV = '/home/claude/entrega_sitio/buscadores.csv'
LOG = []


def log(s):
    LOG.append(s)
    print(s)


def rd(p):
    return open(p, encoding='utf-8').read()


def parts(h):
    css = re.search(r'<style>(.*?)</style>', h, re.S).group(1)
    js = re.findall(r'<script>(.*?)</script>', h, re.S)[-1]
    body = h[h.index('<body'):]
    body = re.sub(r'<script>.*?</script>', '', body, flags=re.S)
    return css.strip('\n') + '\n', js.strip('\n') + '\n', body


def merge3(ours, base, theirs, name, order):
    d = tempfile.mkdtemp()
    for n, t in (('ours', ours), ('base', base), ('theirs', theirs)):
        open(f'{d}/{n}', 'w', encoding='utf-8').write(t)
    r = subprocess.run(['git', 'merge-file', '-p', f'{d}/ours', f'{d}/base', f'{d}/theirs'], capture_output=True, text=True)
    t = r.stdout
    n = len(re.findall(r'^<<<<<<< ', t, re.M))

    def fix(m):
        a, b = m.group(1), m.group(2)
        return (b + a) if order == 'pub-primero' else (a + b)
    t = re.sub(r'^<<<<<<< [^\n]*\n(.*?)^=======\n(.*?)^>>>>>>> [^\n]*\n', fix, t, flags=re.S | re.M)
    assert '<<<<<<<' not in t and '>>>>>>>' not in t
    log(f'{name}: fusión a tres bandas, {n} choque(s) resuelto(s) sumando los dos bloques ({order})')
    return t


bc, bj, bb = parts(rd(BASE))
oc, oj, ob = parts(rd(HOY))
pub = rd(PUB + 'index.html')
pc = rd(PUB + 'aesteros.css')
pj = rd(PUB + 'aesteros.js')

# ---------- estilos y script ----------
css = merge3(oc, bc, pc, 'css/aesteros.css', 'pub-primero')
js = merge3(oj, bj, pj, 'js/aesteros.js', 'hoy-primero')

css += "\n/* integración: la etiqueta de edición del menú convive con los iconos */\n.shg a small{flex:none}\n@media (min-width:640px){.ask .form.nx{display:flex;flex-direction:column;align-items:stretch}}\n.repx .reph em{color:rgba(20,17,12,.74)}\n@media (max-width:820px){.shg a{flex-wrap:wrap}.shg a small{flex-basis:100%;margin:0 0 0 30px}}\n"
log('css: cuatro reglas al final: la etiqueta de edición del menú convive con los iconos, y el selector de edición de la portada (.form.nx) no hereda la rejilla de dos columnas del formulario de demostración')

# ---------- tabla de rutas ----------
dec = json.JSONDecoder()
i = js.index('window.__AE_META__=') + len('window.__AE_META__=')
META, e1 = dec.raw_decode(js, i)
k = js.index('window.__AE_P2V__=') + len('window.__AE_P2V__=')
P2V, e2 = dec.raw_decode(js, k)
rows = {r['direccion']: r for r in csv.DictReader(open(CSV, encoding='utf-8-sig'))}
NUESTRA = {'inicio': '/', 'producto': '/producto', 'metodo': '/metodo', 'planes': '/planes', 'solicitar': '/hablemos', 'novedades': '/novedades',
           'preguntas': '/preguntas', 'seguridad': '/seguridad', 'calculadora': '/calculadora', 'informe-pro': '/informe-de-ejemplo',
           'informe-lite': '/lite/informe-de-ejemplo', 'plantillas': '/estudios', 'kit': '/universidades/kit', 'nosotros': '/nosotros',
           'universidades': '/universidades', 'agencias': '/agencias', 'empresas': '/empresas', 'lite': '/lite', 'blog': '/blog',
           'a-mapa': '/blog/como-leer-un-mapa-de-atencion', 'a-asociacion': '/blog/que-mide-una-prueba-de-asociacion-implicita',
           'a-practica': '/blog/practica-de-neuromarketing-cuatro-semanas', 'a-brisa': '/blog/caso-brisa-un-anuncio-tres-medidas',
           'a-sonrisa': '/blog/una-sonrisa-no-es-una-emocion', 'a-margen': '/blog/margen-de-error-explicado',
           'a-muestra': '/blog/cuanta-gente-necesitas-para-un-estudio', 'a-dos': '/blog/como-elegir-entre-dos-versiones',
           'a-rutas': '/blog/probar-dos-rutas-creativas', 'a-ia': '/blog/mapa-de-atencion-con-ia',
           'a-evaluar': '/blog/calificar-una-practica-de-investigacion', 'a-precio': '/blog/como-preguntar-un-precio', 'glosario': '/glosario',
           'ayuda': '/ayuda', 'participar': '/ayuda/participar', 'guia-inicio': '/ayuda/primer-estudio', 'guia-herramientas': '/ayuda/herramientas',
           'guia-graficas': '/ayuda/graficas', 'guia-bateria': '/ayuda/baterias', 'guia-invitar': '/ayuda/invitar', 'guia-exportar': '/ayuda/exportar',
           'guia-grupos': '/ayuda/grupos', 'guia-docente': '/ayuda/docente', 'guia-alumno': '/ayuda/alumno', 'guia-presentar': '/ayuda/presentar',
           'guia-informe-lite': '/ayuda/informe-lite', 'guia-usuarios': '/ayuda/usuarios', 'guia-cupos': '/ayuda/cupos', 'guia-marca': '/ayuda/marca',
           'guia-privacidad': '/ayuda/privacidad', 'privacidad': '/privacidad', 'terminos': '/terminos', 'camara': '/camara'}
VISTAS = re.findall(r'id="v-([\w-]+)"', ob)
ORIG = 'https://aesteros.com'
NEW = {}
tabla = []
for v in VISTAS:
    if v == 'error':
        continue
    if v == 'entrar':
        NEW[v] = META['entrar']
        tabla.append((v, META['entrar']['p'], 'igual', META['entrar']['t']))
        continue
    r = rows[NUESTRA[v]]
    if v == 'solicitar':
        p, est = '/demo', 'ruta de Cristian (/demo), vista nueva «Hablemos»'
    elif v in META:
        p, est = META[v]['p'], 'ruta de Cristian' + ('' if META[v]['t'] == r['titulo'] and META[v]['d'] == r['descripcion'] else ', título o descripción al día')
    else:
        p, est = NUESTRA[v], 'NUEVA'
    NEW[v] = {'p': p, 'u': ORIG + ('' if p == '/' else p), 't': r['titulo'], 'd': r['descripcion']}
    tabla.append((v, p, est, r['titulo']))
NP2V = {m['p']: v for v, m in NEW.items()}
js = js[:i] + json.dumps(NEW, ensure_ascii=False) + js[e1:]
k = js.index('window.__AE_P2V__=') + len('window.__AE_P2V__=')
_, e2 = dec.raw_decode(js, k)
js = js[:k] + json.dumps(NP2V, ensure_ascii=False) + js[e2:]
log(f'rutas: {len(NEW)} vistas en la tabla ({sum(1 for t in tabla if t[2]=="NUEVA")} nuevas); la vista «demo» de Cristian sale y «solicitar» ocupa /demo')

a = "var h=(location.hash||'').slice(1);\n  if(h&&V.indexOf(h)>=0)return h;"
assert js.count(a) == 1
js = js.replace(a, "var h=(location.hash||'').slice(1);\n  if(h==='demo'||h==='hablemos')h='solicitar';\n  if(h&&V.indexOf(h)>=0)return h;")
log('script: #demo y #hablemos llevan a la vista «solicitar»')
a = "show(name,a.dataset.go);window.dispatchEvent(new Event('hashchange'))});"
assert js.count(a) == 1
js = js.replace(a, "show(name,a.dataset.go);route.hecho=1;window.dispatchEvent(new Event('hashchange'));route.hecho=0});")
a = "function route(){show(curView())}"
assert js.count(a) == 1
js = js.replace(a, "function route(){if(route.hecho)return;show(curView())}")
log('script: CORRECCIÓN, los enlaces con destino dentro de otra página (data-go) ya no vuelven arriba al llegar')
a = "name==='entrar'?'noindex, nofollow'"
assert js.count(a) == 1
js = js.replace(a, "(name==='entrar'||name==='error')?'noindex, nofollow'")
log('script: la vista de error también sale con noindex')

# ---------- marcado: se vuelven a aplicar los cambios de Cristian ----------
h = ob
_n = [0]


def ic(name, uid, size=18):
    s = icon_svg(name, size)
    s = re.sub(r'<svg ', '<svg class="ic" ', s, 1)
    s = re.sub(r' style="color:#[0-9A-Fa-f]{6}"', ' aria-hidden="true" style="color:currentColor"', s, 1)
    g = re.search(r'<radialGradient id="([^"]+)"', s)
    if g:
        s = s.replace(g.group(1), 'ic_' + name.replace('-', '') + '_' + uid)
    return s


def one(a, b, what, count=1):
    global h
    n = h.count(a)
    assert n == count, (what, n)
    h = h.replace(a, b)
    log(f'marcado: {what} ({n})')


# 1 menú desplegable: iconos
SH = {('inicio', ''): 'inicio', ('producto', ''): 'bateria', ('metodo', ''): 'confianza', ('universidades', ''): 'alumno', ('agencias', ''): 'cliente',
      ('empresas', ''): 'equipo', ('lite', ''): 'comparar', ('calculadora', ''): 'muestra', ('informe-pro', ''): 'informe', ('plantillas', ''): 'biblioteca',
      ('lite', 'duelo'): 'vistazo', ('planes', ''): 'tabla', ('solicitar', ''): 'enviar', ('preguntas', ''): 'info', ('seguridad', ''): 'privacidad',
      ('nosotros', ''): 'participante', ('novedades', ''): 'notificacion', ('blog', ''): 'informe', ('ayuda', ''): 'ayuda'}
s0 = h.index('<div class="sheet" id="sheet"')
s1 = h.index('<div class="shg end">', s0)
sheet = h[s0:s1]
cnt = [0]


def shf(m):
    tag = m.group(0)
    hr = re.search(r'href="#([\w-]+)"', tag).group(1)
    go = re.search(r'data-go="([\w-]+)"', tag)
    key = (hr, go.group(1) if go else '')
    if key not in SH:
        return tag
    cnt[0] += 1
    return tag + ic(SH[key], 'sh' + str(cnt[0]))


sheet2 = re.sub(r'<a [^>]*href="#[\w-]+"[^>]*>', shf, sheet)
h = h[:s0] + sheet2 + h[s1:]
log(f'marcado: iconos del menú desplegable ({cnt[0]}; 10 eran de Cristian, el resto son de las entradas nuevas)')

# 2 chips de «¿Qué quieres saber?» en Producto
for q, n in (('mira', 'mirada'), ('emo', 'video'), ('asoc', 'iat'), ('ab', 'comparar'), ('precio', 'encuesta'), ('sitio', 'seo')):
    a = f'<button type="button" class="chip" data-q="{q}" aria-pressed="false">'
    one(a, a + ic(n, 'aq_' + q), f'icono en el chip «{q}»')

# 3 títulos con icono
for t, n, u in (('Laboratorio de calibración', 'calibracion', 'ex1'), ('Calculadora de muestra', 'muestra', 'ex2'), ('Proyectos y alumnos', 'alumno', 'ex3'),
                ('Sellos de evidencia', 'terminado', 'pl_s1'), ('Margen de error', 'confianza', 'pl_s2'), ('Privacidad por defecto', 'privacidad', 'pl_s3')):
    one(f'<div><b>{t}</b><span>', f'<div><b class="ex3Title">{ic(n, u, 20)}{t}</b><span>', f'icono en «{t}»')

# 4 Ayuda
a = '<label class="hsrch" for="h-q">'
one(a, a + ic('buscar', 'hq_s'), 'icono en el buscador de Ayuda')
for i_, n in (('hd-inv', 'maestro'), ('hd-adm', 'ajustes'), ('hd-par', 'participante')):
    m = re.search(r'<button type="button" role="tab" id="%s"[^>]*>' % i_, h)
    assert m, i_
    h = h[:m.end()] + ic(n, i_.replace('-', '_')) + h[m.end():]
    log(f'marcado: icono en la pestaña {i_} de Ayuda (1)')

# 5 Entrar lleva a la aplicación
one('<a class="entb" href="#entrar" aria-label="Entrar a Aesteros">', '<a class="entb" href="https://app.aesteros.com/entrar" aria-label="Entrar a Aesteros">', 'el botón «Entrar a» lleva a app.aesteros.com/entrar')

# 6 marca fija en teléfono
mb = re.search(r'\s*<a class="mbrand".*?</a>', pub, re.S).group(0)
one('<main id="contenido">', '<main id="contenido">' + mb, 'marca fija arriba en teléfono (.mbrand)')

# 7 Portada
one('<div class="hintw" aria-hidden="true"><span class="hint"><i></i>Desliza para enfocar</span></div>',
    '<div class="hintw"><a class="hint" href="#inicio" data-go="prueba"><i aria-hidden="true"></i>Desliza para enfocar o salta a probar</a></div>', 'la pista de la portada es un enlace a «Pruébalo tú»')
one('<img src="img/anuncio.jpg" alt="Anuncio de ejemplo de agua mineral Brisa con un toque de limón" width="1400" height="875">',
    '<img src="img/anuncio.jpg" srcset="img/anuncio-700.jpg 700w, img/anuncio.jpg 1400w" sizes="(max-width: 820px) 100vw, 55vw" alt="Anuncio de ejemplo de agua mineral Brisa con un toque de limón" loading="lazy" width="1400" height="875">', 'imagen del anuncio con versión de 700 px')
one('<div class="canvas-wrap"><img src="img/anuncio.jpg" alt="Anuncio de ejemplo de agua mineral Brisa" width="1400" height="875">',
    '<div class="canvas-wrap" tabindex="0" role="application" aria-label="Área interactiva del anuncio para simular mirada con cursor o flechas"><img src="img/anuncio.jpg" srcset="img/anuncio-700.jpg 700w, img/anuncio.jpg 1400w" sizes="(max-width: 820px) 100vw, 45vw" alt="Anuncio de ejemplo de agua mineral Brisa" loading="lazy" width="1400" height="875">', '«Pruébalo tú» se puede usar con el teclado')
one('Mueve el cursor o el dedo sobre él durante cinco segundos, como si fuera tu mirada.', 'Mueve el cursor, el dedo o las flechas sobre él durante cinco segundos, como si fuera tu mirada.', 'instrucción de «Pruébalo tú» con flechas')

# 8 sellos en las tarjetas de herramientas de la portada
SE = {'Seguimiento ocular': ('s', 'Medido'), 'Análisis visual con IA': ('f', 'Estimado'), 'Asociación implícita': ('s', 'Medido'), 'Variantes implícitas': ('s', 'Medido'),
      'Encuestas y precio': ('s', 'Medido'), 'Recorrido web': ('h', 'Modelado'), 'Auditoría SEO': ('s', 'Medido'), 'Baterías e informe': ('f', 'Estimado')}
c8 = 0
for t, (k_, lab) in SE.items():
    m = re.search(r'(<a class="tc"[^>]*>(?:(?!</a>).)*?<b>%s</b><span>[^<]*</span>)(</a>)' % re.escape(t), h, re.S)
    if not m:
        log(f'marcado: OJO, no encontré la tarjeta «{t}» para ponerle sello')
        continue
    h = h[:m.end(1)] + f'<span class="seal"><i class="d {k_}"></i>{lab}</span>' + h[m.end(1):]
    c8 += 1
log(f'marcado: sello en las tarjetas de herramientas de la portada ({c8}; «Video con lectura del rostro» conserva su etiqueta «En desarrollo»)')

# 9 pie
one('<span class="fine">Maqueta del sitio. Pantallas con datos de ejemplo.</span>', '<span class="fine">Aesteros® 2026, Derechos reservados</span>', 'pie de página con la leyenda de Cristian')

# 10 campos obligatorios
h, n10 = re.subn(r'(<label[^>]*>)([^<]+?)(<input[^>]*\brequired\b)', lambda m: m.group(1) + m.group(2) + ' (requerido)' + m.group(3), h)
log(f'marcado: «(requerido)» en las etiquetas de campos obligatorios ({n10})')

# 11 scripts externos
h, n11 = re.subn(r'<script src="https://cdnjs[^>]*></script>', '', h)
tail = re.search(r'<script src="https://cdnjs.*?</script>\s*<script src="https://cdnjs.*?</script>', pub, re.S).group(0)
vc = hashlib.md5(css.encode()).hexdigest()[:8]
vj = hashlib.md5(js.encode()).hexdigest()[:8]
h = h.replace('</body>', tail + f'<script src="js/aesteros.js?v={vj}"></script>\n</body>')
log(f'marcado: GSAP con integridad como lo tiene Cristian, y script externo (quité {n11} etiquetas nuestras)')

# cabecera de Cristian, tal cual
head = pub[:pub.index('<body')]
head = re.sub(r'css/aesteros\.css\?v=\w+', 'css/aesteros.css?v=' + vc, head)
m0 = NEW['inicio']
doc = head + h
assert 'demo-dlg' not in doc and 'id="v-demo"' not in doc

# ---------- salida ----------
if os.path.exists(OUT):
    shutil.rmtree(OUT)
os.makedirs(OUT + 'css')
os.makedirs(OUT + 'js')
open(OUT + 'index.html', 'w', encoding='utf-8').write(doc)
open(OUT + 'css/aesteros.css', 'w', encoding='utf-8').write(css)
open(OUT + 'js/aesteros.js', 'w', encoding='utf-8').write(js)
shutil.copytree('/home/claude/sitio/img', OUT + 'img')
shutil.copytree('/home/claude/sitio/snd', OUT + 'snd')
shutil.copy(PUB + 'anuncio-700.jpg', OUT + 'img/anuncio-700.jpg')  # imagen de Cristian, se incluye para que la carpeta quede completa
json.dump(NEW, open(OUT + 'rutas.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
with open(OUT + 'rutas.csv', 'w', encoding='utf-8-sig', newline='') as f:
    w = csv.writer(f)
    w.writerow(['vista', 'ruta', 'estado', 'titulo', 'descripcion'])
    for v, p, est, t in tabla:
        w.writerow([v, p, est, t, NEW[v]['d']])
# mapa del sitio y archivo para asistentes, en el formato de Cristian
os.makedirs(OUT + 'propuestos')
PR = {'inicio': '1.0', 'producto': '0.9', 'metodo': '0.9', 'universidades': '0.9', 'agencias': '0.9', 'empresas': '0.9', 'lite': '0.9', 'planes': '0.9'}
sm = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
for v, m in NEW.items():
    if v == 'entrar':
        continue
    pr = PR.get(v, '0.6' if v.startswith('a-') or v.startswith('guia-') else '0.7')
    sm += f'  <url>\n    <loc>{m["u"]}</loc>\n    <lastmod>2026-11-22</lastmod>\n    <changefreq>weekly</changefreq>\n    <priority>{pr}</priority>\n  </url>\n'
sm += '</urlset>\n'
open(OUT + 'propuestos/sitemap.xml', 'w', encoding='utf-8').write(sm)
ll = rd(PUB + 'llms.txt')
cab = ll[:ll.index('## Mapa de páginas públicas')]
for x, y in (('## Nueve herramientas en un mismo núcleo', '## Ocho herramientas en un mismo núcleo'),
             ('2. **Video con lectura del rostro (Medido):** Atención segundo a segundo y movimientos faciales observables (sonrisa, ceño, sorpresa).\n', ''),
             ('capacitación de FRSKO', 'capacitación con especialistas de Aesteros'),
             ('Baterías integradas, informes con tu propia marca y co-marca.', 'Una sola edición para agencias y para empresas, con las mismas herramientas. Baterías integradas e informes con tu propia marca.'),
             ('Autoservicio con plantillas (en lista de espera).', 'Autoservicio para comparar dos versiones, con cuatro plantillas y un informe de una página (en lista de espera).')):
    assert x in cab, x
    cab = cab.replace(x, y)
nums = iter(range(1, 20))
cab = re.sub(r'^\d+\. \*\*', lambda m: f'{next(nums)}. **', cab, flags=re.M)
cab = cab.replace('## Ediciones', '## En desarrollo\n- **Video con lectura del rostro:** módulo opcional. Se abre cuando termine su revisión legal.\n\n## Ediciones')
ll2 = cab + '## Mapa de páginas públicas\n' + ''.join(f'- [{m["t"]}]({m["u"]}): {m["d"]}\n' for v, m in NEW.items() if v != 'entrar')
open(OUT + 'propuestos/llms.txt', 'w', encoding='utf-8').write(ll2)
log('propuestos: sitemap.xml y llms.txt regenerados con las ' + str(len(NEW) - 1) + ' rutas, en el mismo formato que los publicados')
open(OUT + 'BITACORA.txt', 'w', encoding='utf-8').write('\n'.join(LOG) + '\n')
print('listo', len(doc) // 1024, 'KB html,', len(css) // 1024, 'KB css,', len(js) // 1024, 'KB js; vistas', len(VISTAS))
