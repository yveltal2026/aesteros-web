import os,re,sys,csv,json
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
import ilus_lib as L
import iconos_lib as I
def ic(k,uid,sz=20): return I.ic(k,uid,sz)
def logo(uid,h=24):
    s=open(os.path.join(os.path.dirname(os.path.abspath(__file__)),'aesteros-logo-claro.svg')).read()
    s=re.sub(r'<svg [^>]*>',f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="80 100 1200 170" role="img" aria-label="aesteros" style="height:{h}px;width:auto;display:block">',s,1)
    return s.replace('#000000','currentColor').replace('id="g"',f'id="lg{uid}"').replace('url(#g)',f'url(#lg{uid})')
def ed_logo(ed,uid,h=24):
    p=os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','logo','ediciones',f'aesteros-{ed}-claro.svg')
    s=open(p).read()
    vb=re.search(r'viewBox="([^"]+)"',s).group(1)
    s=re.sub(r'<svg [^>]*>',f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{vb}" role="img" aria-label="Aesteros {ed.capitalize()}" style="height:{h}px;width:auto;display:block">',s,1)
    return s.replace('#000000','currentColor').replace('id="e"',f'id="ed_{ed}_{uid}"').replace('url(#e)',f'url(#ed_{ed}_{uid})')
def il(fn,uid,w=120): return re.sub(r'<svg class="ilsvg"',f'<svg class="il" style="width:{w}px"',fn().svg(uid))
def shot(k,alt,cls=''): return f'<figure class="shot {cls}"><div class="bar" aria-hidden="true"><i></i><i></i><i></i></div><img src="img/{k}.jpg" alt="{alt}" loading="lazy" width="1200" height="700"></figure>'
def seal(k): return {'m':'<span class="seal"><i class="d s"></i>Medido</span>','e':'<span class="seal"><i class="d f"></i>Estimado</span>','o':'<span class="seal"><i class="d h"></i>Modelado</span>'}[k]
TOOLS=[
 ('ocular','Seguimiento ocular','¿Qué miran?','Dónde cae la mirada en una imagen, en qué orden y cuánto se queda. Con la cámara de la computadora o del teléfono.','Mapa de atención, recorrido de la mirada e indicadores por área de interés.','Participantes reales','m','Mapa de atención sobre un anuncio con sus áreas de interés',L.ocular),
 ('video','Video con lectura del rostro','¿Qué miran?','Lo mismo sobre un comercial, segundo a segundo, junto con lo que hizo la cara: sonrisa, ceño, sorpresa.','Línea de tiempo por escena, áreas que siguen al producto y movimientos faciales.','Participantes reales','m','Visor de video con línea de tiempo de expresión',L.video_facial),
 ('visual','Análisis visual con IA','¿Qué miran?','Una estimación de la atención en segundos, antes de invitar a nadie. Sirve para descartar versiones y llegar al estudio con las mejores.','Cinco capas sobre la pieza, diagnóstico en seis criterios y zonas ciegas.','Sin participantes','e','Visor de capas de atención estimada',L.atencion),
 ('iat','Asociación implícita','¿Qué asocian?','Qué tan rápido se une una marca con una idea. Lo que tarda la respuesta dice más que la respuesta.','Puntuación por dimensión con su margen de error y cada sesión revisada por calidad.','Participantes reales','m','Resultados de asociación implícita por dimensión',L.asociacion),
 ('variantes','Variantes implícitas','¿Qué asocian?','Tres pruebas cortas para cuando hay una sola marca y ningún competidor claro.','Cada medida frente al cero y avisos de validez.','Participantes reales','m','Resultados de tres variantes implícitas',L.variantes),
 ('encuesta','Encuestas y precio','¿Qué opinan?','Escalas validadas de usabilidad, recomendación y emoción, preguntas propias y dos modelos de precio.','Resultados con su intervalo, rango de precio aceptable y precio de mayor ingreso.','Participantes reales','m','Curvas de rango de precio',L.encuesta),
 ('web','Recorrido web','¿Cómo funciona tu sitio?','Dónde se atora la gente al hacer una tarea en tu sitio, comparado con los de tu competencia.','Índice de Fricción Digital por sitio y por tarea, y qué pesa más en el abandono.','Sin participantes','o','Índice de Fricción Digital de tres sitios',L.recorrido_web),
 ('seo','Auditoría SEO','¿Cómo funciona tu sitio?','Qué impide que Google lea bien tu sitio y qué arreglar primero.','Puntuación, hallazgos por severidad, rendimiento y un plan de acción.','Sin participantes','m','Resumen de auditoría SEO',L.seo),
 ('informe','Baterías e informe','Todo junto','Varias pruebas en una sola liga para quien participa, y un informe que cruza lo que dicen con lo que asocian.','Una conclusión por estudio, con la evidencia a la vista.','Participantes reales','e','Informe integrado de una batería',L.informe)]
QS=['¿Qué miran?','¿Qué asocian?','¿Qué opinan?','¿Cómo funciona tu sitio?']
quad=''.join(f'<a class="q" href="#producto"><span class="qt">{q}</span><ul>'+''.join(f'<li>{t[1]}</li>' for t in TOOLS if t[2]==q)+'</ul></a>' for q in QS)
tools=''.join(f'''<article class="tool" id="t-{k}"><div class="tx"><div class="th">{il(fn,"t"+k,84)}<div><span class="eyebrow">{q}</span><h3>{n}</h3></div></div><p class="lead">{d}</p><dl><div><dt>Qué entrega</dt><dd>{g}</dd></div><div><dt>Quién responde</dt><dd>{w}</dd></div><div><dt>Tipo de dato</dt><dd>{seal(s)}</dd></div></dl></div>{shot(k,alt)}</article>''' for k,n,q,d,g,w,s,alt,fn in TOOLS)
tnav=''.join(f'<a href="#producto" data-go="t-{t[0]}">{t[1]}</a>' for t in TOOLS)
REF=[('Asociación implícita','Greenwald, Nosek y Banaji (2003). Algoritmo de puntuación mejorado.'),('Una sola marca','Karpinski y Steinman (2006). Prueba de categoría única.'),('Responder o esperar','Nosek y Banaji (2001). Tarea de ir o no ir.'),('Primado evaluativo','Fazio y colegas (1995).'),('Usabilidad','Brooke (1996). Escala de usabilidad de 10 frases.'),('Recomendación','Reichheld (2003).'),('Emoción','Bradley y Lang (1994). Escala de figuras en tres dimensiones.'),('Rango de precio','Van Westendorp (1976).'),('Escalera de precios','Gabor y Granger (1966).')]
refs=''.join(f'<tr><th scope="row">{a}</th><td>{b}</td></tr>' for a,b in REF)
FAQ=[('¿Sustituye a un equipo de laboratorio?','No. Una cámara web mide con menos exactitud que un equipo dedicado. Sirve para áreas medianas y grandes, como un titular, un producto o un botón. La plataforma mide el error de cada sesión y lo muestra; lo que no alcanza a medir, lo dice.'),('¿Se graba a quien participa?','No por defecto. De la cámara se guardan las coordenadas de la mirada y los movimientos del rostro, no el video. Quien investiga puede pedir el video, y entonces el aviso de consentimiento lo dice.'),('¿Qué tan confiable es lo que estima la IA?','Es una predicción sobre la forma de la pieza: contraste, tamaño, posición. No sabe qué significa el mensaje. Por eso va siempre con el sello de estimado y nunca se mezcla en un mismo número con lo que se midió con personas.'),('¿Cuánta gente necesito?','Depende de qué tan chico es el efecto que buscas. La calculadora de muestra lo responde antes de empezar, y también al revés: con la gente que ya tienes, hasta dónde alcanza.'),('¿Qué pasa con una sesión mal hecha?','Se excluye sola y queda a la vista por qué: respuestas demasiado rápidas, demasiados errores o una calibración que no alcanzó. Nada se borra en silencio.')]
faq=''.join(f'<details><summary>{q}</summary><p>{a}</p></details>' for q,a in FAQ)
steps=''.join(f'<li>{il(fn,"s%d"%i,104)}<b>{t}</b><span>{d}</span></li>' for i,(fn,t,d) in enumerate(((L.paso1,'Plantea la pregunta','¿Cuál empaque se ve primero? ¿Con qué se asocia la marca?'),(L.paso2,'Elige la prueba','La plataforma sugiere cuál responde tu pregunta.'),(L.paso3,'Comparte una liga','Quien participa responde desde su casa, en computadora o teléfono.'),(L.paso4,'Lee el informe','La conclusión arriba y la evidencia debajo.'))))
gal=''.join(f'<a class="gcard" href="#producto" data-go="t-{t[0]}"><img src="img/{t[0]}.jpg" alt="{t[7]}" loading="lazy" width="1200" height="700"><span class="gq">{t[2]}</span><b>{t[1]}</b></a>' for t in TOOLS)

def _g(i): return f'<defs><radialGradient id="tg{i}"><stop offset="0" stop-color="#FFA200"/><stop offset=".3" stop-color="#FFA800"/><stop offset=".62" stop-color="#FFB000" stop-opacity=".5"/><stop offset="1" stop-color="#FFB000" stop-opacity="0"/></radialGradient></defs>'
def _d(x): return f'style="--d:{x}s"'
MINI={
'ocular':_g(1)+f'<circle class="po" {_d(0)} cx="62" cy="48" r="34" fill="url(#tg1)"/><circle class="po" {_d(.15)} cx="150" cy="70" r="24" fill="url(#tg1)"/><polyline class="dr" {_d(.3)} pathLength="1" points="62,48 150,70 84,96" /><g class="po" {_d(.35)}><circle class="nd" cx="62" cy="48" r="9"/><text x="62" y="52">1</text></g><g class="po" {_d(.6)}><circle class="nd" cx="150" cy="70" r="9"/><text x="150" y="74">2</text></g><g class="po" {_d(.85)}><circle class="nd" cx="84" cy="96" r="9"/><text x="84" y="100">3</text></g>',
'video':f'<line class="ax" x1="14" y1="100" x2="186" y2="100"/><path class="dr am" {_d(.1)} pathLength="1" d="M14,86 C40,84 52,40 78,44 S112,90 132,62 S168,30 186,36"/><path class="dr ds" {_d(.3)} pathLength="1" d="M14,92 C44,90 60,78 84,80 S128,60 150,74 S176,82 186,78"/><g class="po" {_d(.9)}><line class="ph" x1="132" y1="18" x2="132" y2="100"/><circle cx="132" cy="62" r="5" fill="#14110C"/></g>',
'visual':_g(3)+f'<rect class="fr" x="26" y="14" width="148" height="92" rx="10"/><circle class="po" {_d(.1)} cx="74" cy="52" r="36" fill="url(#tg3)"/><circle class="po" {_d(.3)} cx="136" cy="64" r="26" fill="url(#tg3)"/><circle class="po" {_d(.5)} cx="66" cy="88" r="14" fill="url(#tg3)"/><rect class="dr ds" {_d(.6)} pathLength="1" x="40" y="26" width="68" height="52" rx="6"/>',
'iat':f'<defs><linearGradient id="tg4"><stop offset="0" stop-color="#FFB000" stop-opacity="0"/><stop offset=".5" stop-color="#FFB000" stop-opacity=".45"/><stop offset="1" stop-color="#FFB000" stop-opacity="0"/></linearGradient></defs><line class="ax" x1="14" y1="60" x2="186" y2="60"/><line class="zr" x1="80" y1="22" x2="80" y2="98"/><rect class="gx" {_d(.15)} x="80" y="50" width="70" height="20" rx="4" fill="#FFB000"/><rect class="po" {_d(.6)} x="126" y="44" width="48" height="32" fill="url(#tg4)"/><circle class="po" {_d(.75)} cx="150" cy="60" r="6" fill="#14110C"/><text class="lb" x="80" y="114">0</text>',
'variantes':f'<line class="ax" x1="14" y1="100" x2="186" y2="100"/><rect class="gy" {_d(.1)} x="46" y="30" width="42" height="70" rx="5" fill="#FFB000"/><rect class="gy bd" {_d(.3)} x="112" y="58" width="42" height="42" rx="5"/><text class="lb" x="67" y="116">A</text><text class="lb" x="133" y="116">B</text>',
'encuesta':f'<rect class="po" {_d(.7)} x="78" y="14" width="44" height="86" fill="rgba(255,176,0,.3)"/><line class="ax" x1="14" y1="100" x2="186" y2="100"/><path class="dr" {_d(.1)} pathLength="1" d="M14,20 C70,22 90,96 186,98"/><path class="dr am" {_d(.3)} pathLength="1" d="M14,98 C110,96 130,22 186,20"/><circle class="po" {_d(.9)} cx="100" cy="59" r="6" fill="#14110C"/>',
'web':f'<rect class="gx" {_d(.05)} x="16" y="18" width="168" height="16" rx="4" fill="#14110C"/><rect class="gx" {_d(.2)} x="16" y="42" width="128" height="16" rx="4" fill="#14110C"/><rect class="gx" {_d(.35)} x="16" y="66" width="74" height="16" rx="4" fill="#FFB000"/><rect class="gx" {_d(.5)} x="16" y="90" width="52" height="16" rx="4" fill="#14110C"/><path class="dr ds" {_d(.7)} pathLength="1" d="M150,50 C150,74 110,74 96,74"/>',
'seo':f'<text class="bg po" {_d(.1)} x="16" y="74">68</text><text class="lb st" x="112" y="74">de 100</text><rect x="16" y="92" width="168" height="10" rx="5" fill="rgba(20,17,12,.12)"/><rect class="gx" {_d(.3)} x="16" y="92" width="114" height="10" rx="5" fill="#FFB000"/>',
'informe':f'<line class="ax" x1="20" y1="104" x2="186" y2="104"/><line class="ax" x1="20" y1="14" x2="20" y2="104"/>'+''.join(f'<circle class="po" {_d(round(.05*k,2))} cx="{x}" cy="{y}" r="4.5" fill="#14110C"/>' for k,(x,y) in enumerate([(38,90),(52,76),(60,88),(74,70),(88,74),(98,56),(112,62),(124,44),(140,50),(152,32),(168,36)]))+f'<path class="dr am" {_d(.6)} pathLength="1" d="M30,94 L178,26"/>',
}
TG=[('¿Qué miran?',[('ocular','Seguimiento ocular','Dónde cae la mirada y en qué orden.','m'),('video','Video con lectura del rostro','Qué hizo la cara en cada segundo.','m'),('visual','Análisis visual con IA','Qué partes atraen, antes de salir a campo.','e')]),
    ('¿Qué asocian y qué opinan?',[('iat','Asociación implícita','Hacia dónde se inclina la gente y con qué fuerza.','m'),('variantes','Variantes implícitas','Dos conceptos frente a frente.','m'),('encuesta','Encuestas y precio','Lo que dicen y cuánto pagarían.','m')]),
    ('¿Cómo funciona tu sitio?',[('web','Recorrido web','En qué paso se van.','o'),('seo','Auditoría SEO','Qué arreglar primero.','m'),('informe','Baterías e informe','Todas las pruebas en una sola lectura.','e')])]
TOOLSEC='<section class="tools2" id="c-tools"><div class="hd"><h2>Nueve herramientas, una misma lectura</h2><p>Tres preguntas. Cada herramienta responde una parte y entrega el resultado con su margen de error. Y vienen más.</p></div>'+''.join(f'<div class="tgr"><h3>{q}</h3><div class="tcs">'+''.join(f'<a class="tc" href="#producto" data-go="t-{k}"><svg viewBox="0 0 200 120" aria-hidden="true">{MINI[k]}</svg><b>{n}</b><span>{d}</span>{seal(s)}</a>' for k,n,d,s in ts)+'</div></div>' for q,ts in TG)+'<div class="tgr soon"><h3>Y lo que viene</h3><div><div class="tcs"><div class="tc sn" aria-hidden="true"><svg viewBox="0 0 200 120"><circle cx="70" cy="60" r="34" fill="#FFB000"/><rect x="120" y="30" width="56" height="60" rx="8" fill="#14110C"/></svg><i></i><i class="w"></i><em>En desarrollo</em></div><div class="tc sn" aria-hidden="true"><svg viewBox="0 0 200 120"><rect x="20" y="70" width="30" height="34" rx="5" fill="#14110C"/><rect x="62" y="44" width="30" height="60" rx="5" fill="#FFB000"/><rect x="104" y="58" width="30" height="46" rx="5" fill="#14110C"/><rect x="146" y="26" width="30" height="78" rx="5" fill="#FFB000"/></svg><i></i><i class="w"></i><em>En desarrollo</em></div><div class="tc sn" aria-hidden="true"><svg viewBox="0 0 200 120"><path d="M16,90 C60,20 120,110 184,36" fill="none" stroke="#14110C" stroke-width="8"/><circle cx="150" cy="60" r="22" fill="#FFB000"/></svg><i></i><i class="w"></i><em>En desarrollo</em></div></div><p class="snp">Empezamos con nueve. Estamos construyendo más y las sumamos conforme pasan nuestra propia validación. <a href="#inicio" data-go="espera">Avísenme de cada herramienta nueva</a></p></div></div>'+'<div class="proof"><div class="ptx"><span class="eyebrow">Así se ve por dentro</span><h3>La misma lectura, en la plataforma</h3><p>Una pantalla real con datos de ejemplo. Las demás están en Producto.</p><a class="lnk" href="#producto">Ver cada herramienta</a></div>'+shot('ocular','Pantalla de seguimiento ocular con mapa de atención y áreas de interés')+'</div></section>'

CURV=open('curvas.json').read()
PLOT='<svg viewBox="0 0 1000 400" preserveAspectRatio="none" aria-hidden="true"><path class="c-tb" pathLength="1" d="M0.0,73.0 L19.2,89.1 L38.5,107.6 L57.7,128.3 L76.9,151.0 L96.2,175.1 L115.4,200.0 L134.6,224.9 L153.8,249.0 L173.1,271.7 L192.3,292.4 L211.5,310.9 L230.8,327.0 L250.0,340.8 L269.2,352.3 L288.5,361.9 L307.7,369.7 L326.9,376.0 L346.2,381.0 L365.4,385.1 L384.6,388.3 L403.8,390.8 L423.1,392.8 L442.3,394.4 L461.5,395.6 L480.8,396.6 L500.0,397.3 L519.2,397.9 L538.5,398.4 L557.7,398.7 L576.9,399.0 L596.2,399.2 L615.4,399.4 L634.6,399.5 L653.8,399.6 L673.1,399.7 L692.3,399.8 L711.5,399.8 L730.8,399.9 L750.0,399.9 L769.2,399.9 L788.5,399.9 L807.7,400.0 L826.9,400.0 L846.2,400.0 L865.4,400.0 L884.6,400.0 L903.8,400.0 L923.1,400.0 L942.3,400.0 L961.5,400.0 L980.8,400.0 L1000.0,400.0"/><path class="c-bc" pathLength="1" d="M0.0,10.6 L19.2,12.9 L38.5,15.7 L57.7,19.0 L76.9,22.9 L96.2,27.7 L115.4,33.3 L134.6,39.9 L153.8,47.7 L173.1,56.7 L192.3,67.2 L211.5,79.1 L230.8,92.6 L250.0,107.6 L269.2,124.0 L288.5,141.7 L307.7,160.5 L326.9,180.1 L346.2,200.0 L365.4,219.9 L384.6,239.5 L403.8,258.3 L423.1,276.0 L442.3,292.4 L461.5,307.4 L480.8,320.9 L500.0,332.8 L519.2,343.3 L538.5,352.3 L557.7,360.1 L576.9,366.7 L596.2,372.3 L615.4,377.1 L634.6,381.0 L653.8,384.3 L673.1,387.1 L692.3,389.4 L711.5,391.2 L730.8,392.8 L750.0,394.1 L769.2,395.1 L788.5,396.0 L807.7,396.7 L826.9,397.3 L846.2,397.8 L865.4,398.2 L884.6,398.5 L903.8,398.8 L923.1,399.0 L942.3,399.2 L961.5,399.3 L980.8,399.5 L1000.0,399.6"/><path class="c-ca" pathLength="1" d="M0.0,397.8 L19.2,397.3 L38.5,396.7 L57.7,396.0 L76.9,395.1 L96.2,394.1 L115.4,392.8 L134.6,391.2 L153.8,389.4 L173.1,387.1 L192.3,384.3 L211.5,381.0 L230.8,377.1 L250.0,372.3 L269.2,366.7 L288.5,360.1 L307.7,352.3 L326.9,343.3 L346.2,332.8 L365.4,320.9 L384.6,307.4 L403.8,292.4 L423.1,276.0 L442.3,258.3 L461.5,239.5 L480.8,219.9 L500.0,200.0 L519.2,180.1 L538.5,160.5 L557.7,141.7 L576.9,124.0 L596.2,107.6 L615.4,92.6 L634.6,79.1 L653.8,67.2 L673.1,56.7 L692.3,47.7 L711.5,39.9 L730.8,33.3 L750.0,27.7 L769.2,22.9 L788.5,19.0 L807.7,15.7 L826.9,12.9 L846.2,10.6 L865.4,8.8 L884.6,7.2 L903.8,5.9 L923.1,4.9 L942.3,4.0 L961.5,3.3 L980.8,2.7 L1000.0,2.2"/><path class="c-dc" pathLength="1" d="M0.0,399.8 L19.2,399.8 L38.5,399.7 L57.7,399.6 L76.9,399.6 L96.2,399.5 L115.4,399.3 L134.6,399.2 L153.8,399.0 L173.1,398.8 L192.3,398.5 L211.5,398.2 L230.8,397.8 L250.0,397.3 L269.2,396.7 L288.5,396.0 L307.7,395.1 L326.9,394.1 L346.2,392.8 L365.4,391.2 L384.6,389.4 L403.8,387.1 L423.1,384.3 L442.3,381.0 L461.5,377.1 L480.8,372.3 L500.0,366.7 L519.2,360.1 L538.5,352.3 L557.7,343.3 L576.9,332.8 L596.2,320.9 L615.4,307.4 L634.6,292.4 L653.8,276.0 L673.1,258.3 L692.3,239.5 L711.5,219.9 L730.8,200.0 L750.0,180.1 L769.2,160.5 L788.5,141.7 L807.7,124.0 L826.9,107.6 L846.2,92.6 L865.4,79.1 L884.6,67.2 L903.8,56.7 L923.1,47.7 L942.3,39.9 L961.5,33.3 L980.8,27.7 L1000.0,22.9"/></svg>'
HIST='<svg viewBox="0 0 1000 300" preserveAspectRatio="none" aria-hidden="true"><path class="ha" d="M0,300 L0,300.0 L10,300.0 L20,300.0 L30,300.0 L40,299.9 L50,299.9 L60,299.9 L70,299.8 L80,299.7 L90,299.5 L100,299.2 L110,298.8 L120,298.3 L130,297.5 L140,296.4 L150,295.0 L160,293.1 L170,290.5 L180,287.2 L190,283.1 L200,277.8 L210,271.3 L220,263.5 L230,254.1 L240,243.1 L250,230.5 L260,216.2 L270,200.3 L280,183.1 L290,164.9 L300,145.9 L310,126.6 L320,107.6 L330,89.5 L340,72.9 L350,58.3 L360,46.3 L370,37.4 L380,31.9 L390,30.0 L400,31.9 L410,37.4 L420,46.3 L430,58.3 L440,72.9 L450,89.5 L460,107.6 L470,126.6 L480,145.9 L490,164.9 L500,183.1 L510,200.3 L520,216.2 L530,230.5 L540,243.1 L550,254.1 L560,263.5 L570,271.3 L580,277.8 L590,283.1 L600,287.2 L610,290.5 L620,293.1 L630,295.0 L640,296.4 L650,297.5 L660,298.3 L670,298.8 L680,299.2 L690,299.5 L700,299.7 L710,299.8 L720,299.9 L730,299.9 L740,299.9 L750,300.0 L760,300.0 L770,300.0 L780,300.0 L790,300.0 L800,300.0 L810,300.0 L820,300.0 L830,300.0 L840,300.0 L850,300.0 L860,300.0 L870,300.0 L880,300.0 L890,300.0 L900,300.0 L910,300.0 L920,300.0 L930,300.0 L940,300.0 L950,300.0 L960,300.0 L970,300.0 L980,300.0 L990,300.0 L1000,300.0 L1000,300Z"/><path class="hb" d="M0,300 L0,300.0 L10,300.0 L20,300.0 L30,300.0 L40,300.0 L50,300.0 L60,300.0 L70,300.0 L80,300.0 L90,300.0 L100,300.0 L110,300.0 L120,300.0 L130,300.0 L140,300.0 L150,300.0 L160,300.0 L170,300.0 L180,300.0 L190,300.0 L200,300.0 L210,299.9 L220,299.9 L230,299.9 L240,299.8 L250,299.7 L260,299.6 L270,299.4 L280,299.2 L290,298.9 L300,298.4 L310,297.9 L320,297.2 L330,296.2 L340,295.0 L350,293.5 L360,291.5 L370,289.2 L380,286.3 L390,282.8 L400,278.6 L410,273.6 L420,267.9 L430,261.2 L440,253.7 L450,245.3 L460,235.9 L470,225.7 L480,214.8 L490,203.2 L500,191.1 L510,178.8 L520,166.4 L530,154.1 L540,142.4 L550,131.4 L560,121.4 L570,112.7 L580,105.5 L590,100.1 L600,96.6 L610,95.1 L620,95.6 L630,98.1 L640,102.6 L650,108.9 L660,116.9 L670,126.2 L680,136.8 L690,148.2 L700,160.2 L710,172.6 L720,185.0 L730,197.2 L740,209.1 L750,220.3 L760,230.9 L770,240.7 L780,249.6 L790,257.6 L800,264.7 L810,270.8 L820,276.2 L830,280.7 L840,284.6 L850,287.8 L860,290.4 L870,292.6 L880,294.3 L890,295.6 L900,296.7 L910,297.5 L920,298.2 L930,298.7 L940,299.0 L950,299.3 L960,299.5 L970,299.7 L980,299.8 L990,299.8 L1000,299.9 L1000,300Z"/></svg>'

def mini(k,sfx): return '<svg viewBox="0 0 200 120" aria-hidden="true">'+MINI[k].replace('tg','tg'+sfx)+'</svg>'
def au(u,e,a): return f'<span data-au="u">{u}</span><span data-au="e">{e}</span><span data-au="a">{a}</span>'
SEALT={'m':'Medido','e':'Estimado','o':'Modelado'}
_dots=''.join('<i class="%s" style="--d:%.2fs"></i>'%('ok' if n<52 else ('ex' if n<57 else 'no'),n*.025) for n in range(60))
_acc=''.join(f'<details class="acc" id="t-{k}"><summary><span class="am">{mini(k,"p"+k)}</span><span class="an"><em>{q}</em><b>{n}</b></span>{seal(sl)}</summary><div class="ab"><div class="abt"><p class="lead">{d}</p><dl><div><dt>Qué entrega</dt><dd>{g}</dd></div><div><dt>Quién responde</dt><dd>{w}</dd></div></dl></div>{shot(k,alt)}</div></details>' for k,n,q,d,g,w,sl,alt,fn in TOOLS)
_qs=[('mira','Qué se mira en mi pieza','mirada'),('emo','Qué provoca mi video','video'),('asoc','Con qué se asocia mi marca','iat'),('ab','Cuál de dos versiones gana','comparar'),('precio','Cuánto pagarían','encuesta'),('sitio','Dónde se atoran en mi sitio','seo')]
PROD='<section class="view prod" id="v-producto" data-au="u" hidden>'+f"""
<div class="phd2"><span class="eyebrow">Producto</span><h1 class="focus">Un estudio,<br>de principio a fin</h1><p class="sub">Sigue a Brisa, una marca de agua mineral de ejemplo, desde la pregunta hasta la decisión. En el camino aparecen las nueve herramientas.</p>
<div class="ausel" role="group" aria-label="Ver los ejemplos como"><span>Ver como</span><button type="button" data-set="u" aria-pressed="true">Universidad</button><button type="button" data-set="e" aria-pressed="false">Empresa</button><button type="button" data-set="a" aria-pressed="false">Agencia</button></div></div>
<div class="story5"><nav class="rail" aria-label="Pasos del estudio"><ol><li><button type="button" data-to="p-1" aria-current="step">Armar</button></li><li><button type="button" data-to="p-2">Invitar</button></li><li><button type="button" data-to="p-3">Medir</button></li><li><button type="button" data-to="p-4">Leer</button></li><li><button type="button" data-to="p-5">Decidir</button></li></ol></nav>
<div class="sps">
<section class="sp" id="p-1"><div class="spt" data-rv><span class="num">01 · Armar</span><h2>Subes la pieza y eliges qué preguntar</h2><p class="lead">Un anuncio, un empaque, un video o la dirección de un sitio. Cada pregunta enciende una herramienta, y todas quedan en un mismo estudio.</p><p class="aul">{au('En clase, cada equipo arma el suyo en una sesión.','Lo arma quien lleva la marca, sin pedir nada a sistemas.','Se arma antes de presentar, con las dos rutas creativas.')}</p></div>
<div class="mock" data-rv><img src="img/anuncio.jpg" alt="Anuncio de ejemplo de agua mineral Brisa" loading="lazy" width="1400" height="875"><ul class="pick"><li style="--d:.2s">{mini('ocular','a1')}<b>¿Qué miran?</b><span>Seguimiento ocular</span></li><li style="--d:.45s">{mini('iat','a2')}<b>¿Qué asocian?</b><span>Asociación implícita</span></li><li style="--d:.7s">{mini('encuesta','a3')}<b>¿Cuánto pagarían?</b><span>Encuestas y precio</span></li></ul></div></section>
<section class="sp" id="p-2"><div class="spt" data-rv><span class="num">02 · Invitar</span><h2>Mandas una liga. Responden desde su casa</h2><p class="lead">Quien participa acepta el consentimiento, calibra su cámara y contesta en unos minutos, en computadora o teléfono. No instala nada.</p><p class="aul">{au('Tus alumnos consiguen a sus participantes y ven llegar las sesiones.','Invitas a tu panel o a tus propios clientes.','Invitas al público del cliente, sin rentar una sala.')}</p></div>
<div class="crowd" data-rv><div class="dots" aria-hidden="true">{_dots}</div><p class="cnt"><b>52</b> sesiones válidas</p><ul class="cl"><li><i class="ok"></i>52 válidas</li><li><i class="ex"></i>5 excluidas por calidad</li><li><i class="no"></i>3 sin terminar</li></ul><p class="fine2">Datos de ejemplo. El informe siempre dice cuántas sesiones entraron y cuántas se excluyeron.</p></div></section>
<section class="sp wide" id="p-3"><div class="spt" data-rv><span class="num">03 · Medir</span><h2>Tres preguntas, tres medidas</h2><p class="lead">Estas gráficas son del estudio de Brisa y se pueden tocar.</p></div>
<div class="lab3">
<div class="lb" data-rv><div class="lbh"><b>Toca un área del anuncio</b>{seal('m')}</div><div class="aoiw"><img src="img/anuncio.jpg" alt="" loading="lazy" width="1400" height="875"><button type="button" class="aoi" data-k="0" style="left:4%;top:21%;width:41%;height:36%" aria-pressed="true"><span>Titular</span></button><button type="button" class="aoi" data-k="1" style="left:74%;top:7%;width:17%;height:86%" aria-pressed="false"><span>Producto</span></button><button type="button" class="aoi" data-k="2" style="left:4%;top:64%;width:28%;height:15%" aria-pressed="false"><span>Botón</span></button><button type="button" class="aoi" data-k="3" style="left:52%;top:63%;width:14%;height:22%" aria-pressed="false"><span>Precio</span></button></div>
<dl class="kv" id="aoi-out" aria-live="polite"><div><dt>Lo vio primero</dt><dd>52 %</dd></div><div><dt>Lo vio en algún momento</dt><dd>94 %</dd></div><div><dt>Primera mirada</dt><dd>0,6 s</dd></div><div><dt>Tiempo de permanencia</dt><dd>1,8 s</dd></div></dl></div>
<div class="lb" data-rv><div class="lbh"><b>Cambia el grupo</b>{seal('m')}</div><div class="grp" role="group" aria-label="Grupo"><button type="button" data-g="0" aria-pressed="true">Todos</button><button type="button" data-g="1" aria-pressed="false">Ya compran Brisa</button><button type="button" data-g="2" aria-pressed="false">No la compran</button></div>
<div class="dbar" aria-hidden="true"><span class="zero"></span><span class="dband" id="d-band"></span><span class="dfill" id="d-fill"></span><span class="ddot" id="d-dot"></span><em class="l">Más con Cumbre</em><em class="r">Más con Brisa</em></div>
<p class="dread" id="d-out" aria-live="polite"><b>+0,58</b> Brisa se asocia con «natural». Intervalo de 0,41 a 0,75, con 52 personas.</p></div>
<div class="lb" data-rv><div class="lbh"><b>Mueve el precio</b>{seal('m')}</div><div class="plot pl2" id="plot2"><span class="rng"></span>{PLOT}<span class="mk" id="pr-mk"></span></div><label class="sld" for="pr-in"><span>Precio</span><input type="range" id="pr-in" min="10" max="36" step="0.5" value="20"><output id="pr-val">$20,00</output></label>
<p class="dread" id="pr-out" aria-live="polite"></p></div>
</div></section>
<section class="sp" id="p-4"><div class="spt" data-rv><span class="num">04 · Leer</span><h2>Cada resultado dice de dónde viene</h2><p class="lead">El informe cruza las tres medidas y marca cada dato con su sello y su margen de error.</p>
<ul class="finds"><li style="--d:.1s">{seal('m')}<span>El titular se lleva la primera mirada de 52 de cada 100 personas.</span></li><li style="--d:.3s">{seal('m')}<span>Brisa se asocia con «natural»: +0,58, de 0,41 a 0,75.</span></li><li style="--d:.5s">{seal('m')}<span>El precio no estorba entre $17,40 y $24,00.</span></li><li style="--d:.7s">{seal('e')}<span>La IA estima poca atención al precio. Coincide con lo medido.</span></li></ul></div>
<div data-rv>{shot('informe','Informe integrado con el cruce entre lo que dicen y lo que asocian')}</div></section>
<section class="sp" id="p-5"><div class="spt full" data-rv><span class="num">05 · Decidir</span><h2 class="dec">Brisa sale con el titular arriba, «natural» al frente y el precio en $20.</h2><p class="lead">{au('Tus alumnos entregan esta conclusión con sus propios datos, y saben defender hasta dónde llega.','Llegas a la junta con una recomendación y la evidencia a la vista.','Presentas la ruta ganadora con datos del público del cliente.')}</p></div></section>
</div></div>
<section class="arma" id="arma"><div class="hd" data-rv><span class="eyebrow">Arma tu estudio</span><h2>¿Qué quieres saber?</h2><p>Marca una o varias. Te decimos con qué herramientas se responde.</p></div>
<div class="armab" data-rv><div class="aq" role="group" aria-label="Lo que quieres saber">"""+''.join(f'<button type="button" class="chip" data-q="{k}" aria-pressed="false">{ic(ik,"aq_"+k,18)}{t}</button>' for k,t,ik in _qs)+"""</div>
<div class="ares" id="arma-out" aria-live="polite"><p class="aempty">Tu estudio aparece aquí.</p></div></div></section>
<section class="nueve"><div class="hd" data-rv><h2>Las nueve, una por una</h2><p>Abre la que te interese. Todas entregan el resultado con su margen de error y su sello.</p></div><div class="accs" data-rv>"""+_acc+"""</div></section>
"""+f"""<section class="extra" data-rv><div><span class="eyebrow">También incluye</span><h2>Lo que hace falta alrededor de una prueba</h2></div><div class="ex3"><div><b class="ex3Title">{ic('calibracion','ex1',20)}Laboratorio de calibración</b><span>Mide qué tan exacto es cada equipo y qué tamaño de área puede medir.</span></div><div><b class="ex3Title">{ic('muestra','ex2',20)}Calculadora de muestra</b><span>Cuánta gente hace falta, o hasta dónde alcanza la que hay.</span></div><div><b class="ex3Title">{ic('alumno','ex3',20)}Proyectos y alumnos</b><span>Estudios ordenados por proyecto, con permisos por persona.</span></div></div></section>
<section class="pcta" data-rv><h2>Míralo con tu propio caso</h2><div class="cta"><a class="btn" href="#inicio" data-go="demo">Pedir una demostración</a><a class="btn ghost" href="#metodo">Ver cómo medimos</a></div></section>
</section>"""
_LIM=[('Mirada con cámara web', 'Qué áreas medianas y grandes se ven, en qué orden y por cuánto tiempo.', 'Si se leyó una letra chica, ni lo que la persona pensó al mirar.'), ('Lectura del rostro', 'Qué hizo la cara en cada segundo: sonrisa, ceño, sorpresa.', 'Lo que la persona sintió. Una sonrisa puede ser de cortesía.'), ('Asociación implícita', 'Hacia dónde se inclina un grupo y con qué fuerza.', 'Nada sobre una persona en particular. Su puntuación cambia de un día a otro.'), ('Atención estimada con IA', 'Qué partes de una pieza atraen por su forma.', 'Si el mensaje se entiende o convence.'), ('Intención de compra', 'Cuál de dos conceptos gusta más.', 'Cuánto se va a vender. Lo declarado suele ser más de lo que se compra.'), ('Índice de fricción', 'Dónde un sitio estorba más que otro.', 'Qué harían usuarios reales: es una simulación a partir de una rúbrica.')]
_lk=['ocular','video','iat','visual','variantes','web']
_sn=''.join(f'<article class="sn" data-rv tabindex="0"><div class="snm">{mini(k,"m"+k)}</div><h3>{a}</h3><p class="si"><i class="d s"></i><span><em>Sí puede decir</em>{b}</span></p><p class="no"><i class="d f"></i><span><em>No puede decir</em>{c}</span></p></article>' for k,(a,b,c) in zip(_lk,_LIM))
_tl=[('Consentimiento','Antes de cualquier medición, quien participa lee qué se va a medir y acepta. Puede salir en cualquier momento.','La aceptación','Nada más, si no acepta'),
('Calibración','La persona sigue unos puntos en pantalla y la plataforma mide qué tan exacta es esa cámara en esa sesión.','El error de la sesión','La imagen de la cámara'),
('Medición','Se registran coordenadas de mirada, movimientos del rostro, tiempos de respuesta y respuestas. La pantalla no lleva marca, animación ni sonido.','Coordenadas, tiempos y respuestas','Video, salvo decisión explícita y avisada'),
('Control de calidad','Cada sesión se revisa. Las que no alcanzan la calidad necesaria se excluyen, y el informe dice cuántas fueron.','El motivo de cada exclusión','Sesiones excluidas dentro del resultado'),
('Análisis','Cada resultado sale con su margen de error. Si la muestra es chica hay un aviso, y si un intervalo cruza el cero la gráfica lo marca.','El intervalo junto a cada cifra','Promedios de lo medido con lo estimado'),
('Informe','Cada dato lleva su sello: medido, estimado o modelado. La referencia del método aparece junto a la prueba.','El sello en cada gráfica y cada archivo','Conclusiones sin su evidencia')]
_tls=''.join(f'<li data-rv><span class="tn">{n+1}</span><div><h3>{t}</h3><p>{d}</p><p class="keep"><span><i class="d s"></i>Queda: {g}</span><span><i class="d h"></i>No queda: {x}</span></p></div></li>' for n,(t,d,g,x) in enumerate(_tl))
MET='<section class="view met" id="v-metodo" hidden>'+f"""
<div class="phd2"><span class="eyebrow">Método y confianza</span><h1 class="focus">Lo que sí podemos decir.<br><span class="soft">Y lo que no.</span></h1><p class="sub">Una herramienta de investigación vale por lo que puede sostener. Aquí está qué mide Aesteros, con qué método y hasta dónde llega.</p></div>
<section class="mb"><div class="hd" data-rv><h2>Tres clases de dato</h2><p>Van marcadas en cada gráfica, en cada cifra y en cada archivo que se descarga.</p></div><div class="seals" data-rv><div><i class="d s big"></i><b>Medido</b><span>Viene de lo que hicieron personas reales. Lleva cuántas fueron y cuántas se excluyeron.</span></div><div><i class="d f big"></i><b>Estimado</b><span>Viene de un modelo de IA. Se dibuja con otra forma y nunca se promedia con lo medido.</span></div><div><i class="d h big"></i><b>Modelado</b><span>Viene de una simulación. Lleva su nota de método y el tamaño de su ruido.</span></div></div></section>
<section class="mb"><div class="hd" data-rv><h2>Lo que cada medida puede decir</h2><p>Lo que se sostiene está nítido. Lo que no, está difuso: pasa el cursor o toca la tarjeta para leerlo.</p></div><div class="sns">{_sn}</div></section>
<section class="mb"><div class="hd" data-rv><h2>El recorrido de un dato</h2><p>De la cámara de quien participa al informe, y qué queda en cada paso.</p></div><ol class="tl" id="tl"><span class="tlf" aria-hidden="true"><i id="tl-fill"></i></span>{_tls}</ol></section>
<section class="mb split2"><div data-rv><h2>Métodos con referencia</h2><p class="lead">Cada prueba sigue un procedimiento publicado. En la plataforma, la referencia aparece junto a la prueba.</p></div><div class="scr" data-rv><table class="ref"><tbody>{refs}</tbody></table></div></section>
<section class="mb faq"><div class="hd" data-rv><h2>Preguntas que nos hacen</h2></div><div data-rv>{faq}</div></section>
<section class="pcta" data-rv><h2>¿Tienes una duda de método?</h2><p class="lead">La resolvemos en la demostración, con tus propios casos.</p><div class="cta"><a class="btn" href="#inicio" data-go="demo">Pedir una demostración</a><a class="btn ghost" href="#producto">Ver el producto</a></div></section>
</section>"""


def hero2(eb,h,sub,extra=''): return f'<div class="phd2"><span class="eyebrow">{eb}</span><h1 class="focus">{h}</h1><p class="sub">{sub}</p>{extra}</div>'
def cta2(h,p,b2='<a class="btn ghost" href="#planes">Ver planes</a>'): return f'<section class="pcta" data-rv><h2>{h}</h2><p class="lead">{p}</p><div class="cta"><a class="btn" href="#inicio" data-go="demo">Pedir una demostración</a>{b2}</div></section>'
def li(xs): return '<ul class="ck">'+''.join(f'<li>{x}</li>' for x in xs)+'</ul>'
SOON='<em class="pill">En desarrollo</em>'
_sem=[('Arranque','El docente se capacita con FRSKO y deja lista la práctica.'),('Diseño','Cada equipo arma su estudio: pieza, preguntas y herramientas.'),('Campo','Los equipos invitan a sus participantes y ven llegar las sesiones.'),('Lectura','Leen los resultados, los cruzan y presentan su conclusión.')]
UNI='<section class="view dk" id="v-universidades" hidden>'+hero2('Para universidades','Un laboratorio<br>que cabe en un salón','Tus alumnos diseñan un estudio, lo aplican con personas reales y leen sus resultados en el mismo semestre. Con la cámara de su computadora o de su teléfono.')+f"""
<section class="mb"><div class="hd" data-rv><h2>Un semestre con Aesteros</h2><p>Un ejemplo de cómo se reparte. Cada programa lo ajusta a su calendario.</p></div><ol class="sem">{''.join(f'<li data-rv style="--i:{i}"><span>{i+1}</span><b>{t}</b><p>{d}</p></li>' for i,(t,d) in enumerate(_sem))}</ol></section>
<section class="mb"><div class="hd" data-rv><h2>Tres personas deciden. Hay una respuesta para cada una</h2></div><div class="tri3"><div class="pc" data-rv><em>Quien da la clase</em><h3>Práctica real, sin armar un laboratorio</h3>{li(['Plantillas de estudio para empezar el primer día.','Roles de docente y alumno, con grupos por código.','Cada equipo ve sus datos; el docente ve los de todos.','Capacitación del equipo de FRSKO.'])}</div><div class="pc" data-rv><em>Quien aprueba</em><h3>Método publicado y datos protegidos</h3>{li(['Cada prueba sigue un procedimiento con referencia.','El video de la cámara no sale del dispositivo.','Quien participa no da nombre ni correo.','Cada cifra dice si es medida, estimada o modelada.'])}<a class="lnk" href="#metodo">Leer el método</a></div><div class="pc" data-rv><em>Quien compra</em><h3>Una licencia por programa y periodo</h3>{li(['Semestral o anual.','Cupo de alumnos, participantes y uso de IA incluido.','Capacitación y soporte dentro de la licencia.','Lo que rebase el cupo se cotiza aparte.'])}<a class="lnk" href="#planes">Ver planes</a></div></div></section>
<section class="mb duo"><div data-rv><span class="eyebrow">Piloto</span><h2>Un semestre de prueba, sin costo</h2><p class="lead">Con un grupo y un docente. A cambio pedimos tres cosas.</p>{li(['Una carta de intención del programa.','Una fecha para decidir al terminar el periodo.','Permiso para contar el caso.'])}</div><div class="comark" data-rv><div class="cmh"><span class="cml">{logo("cm1",22)}</span><i></i><span class="cmo">Tu universidad</span></div><p>Aesteros para tu universidad</p><span>Con su logotipo, su portada de entrada, su dirección propia y sus plantillas.</span></div></section>
"""+cta2('Llévalo a tu programa','Te mostramos la plataforma con una práctica de tu materia.')+'</section>'
AGE='<section class="view dk" id="v-agencias" hidden>'+hero2('Para agencias','Llega a la presentación<br>con evidencia','Prueba las rutas creativas con el público del cliente antes de presentarlas, y respalda tu recomendación con datos de personas.')+f"""
<section class="mb duo"><div data-rv><h2>El informe sale con tu marca</h2><p class="lead">Tu cliente ve tu logotipo. El método y los sellos siguen a la vista, porque son lo que sostiene el dato.</p><div class="sw" role="group" aria-label="Marca del informe"><button type="button" data-b="0" aria-pressed="true">Con Aesteros</button><button type="button" data-b="1" aria-pressed="false">Con tu marca</button></div></div>
<div class="rep" id="rep" data-rv><div class="reph"><span class="rl a">{logo("rp",20)}</span><span class="rl b">Tu agencia</span><em>Informe de estudio</em></div><h3>El titular se lleva la mirada; el precio casi no se ve</h3><div class="repg">{mini('ocular','r1')}{mini('iat','r2')}{mini('encuesta','r3')}</div><p class="repf"><i class="d s"></i>Medido con Aesteros · 52 personas · datos de ejemplo</p></div></section>
<section class="mb"><div class="hd" data-rv><h2>Tres momentos donde cambia la conversación</h2></div><div class="tri3"><div class="pc" data-rv><em>Antes de presentar</em><h3>Dos rutas, una ganadora</h3><p>Llevas la que eligió el público, con la evidencia de por qué.</p></div><div class="pc" data-rv><em>Antes de producir</em><h3>Ajustar cuando todavía es barato</h3><p>Sabes qué se mira, qué se entiende y qué no, sobre el boceto.</p></div><div class="pc" data-rv><em>Después de lanzar</em><h3>Explicar qué pasó</h3><p>Mides la pieza al aire y el sitio donde aterriza la campaña.</p></div></div></section>
<section class="mb"><div class="hd" data-rv><h2>Lo que trae la edición Pro</h2></div><div class="tri3"><div class="pc" data-rv><h3>Baterías e informe</h3><p>Varias pruebas en una sola liga y un informe que las cruza.</p></div><div class="pc" data-rv><h3>Tu marca en lo que entregas</h3><p>Informes y archivos con tu logotipo. Incluido.</p></div><div class="pc" data-rv>{SOON}<h3>Portal para tu cliente</h3><p>Acceso de solo lectura para que consulte sus resultados.</p></div></div></section>
"""+cta2('Pruébalo con una cuenta real','Trae una pieza de un cliente y la corremos juntos.')+'</section>'
EMP='<section class="view dk" id="v-empresas" hidden>'+hero2('Para empresas','Sabe cuál versión funciona<br>antes de producirla','Prueba un empaque, un anuncio, un precio o una página con personas reales, y llega a la junta con evidencia.')+f"""
<section class="mb"><div class="hd" data-rv><h2>Cuatro decisiones que ya no dependen de quién insiste más</h2></div><div class="quad4">{''.join(f'<a class="tc" href="#producto" data-go="t-{k}" data-rv>{mini(k,"e"+k)}<b>{t}</b><span>{d}</span></a>' for k,t,d in [('ocular','¿Se entiende el empaque?','Qué se ve primero y qué nunca se ve.'),('variantes','¿Cuál de los dos anuncios?','Dos versiones frente a frente.'),('encuesta','¿A qué precio?','El rango en que el precio no estorba.'),('web','¿Dónde se van del sitio?','El paso que más pesa en el abandono.')])}</div></section>
<section class="mb duo"><div data-rv><h2>Para un equipo de marca o de investigación</h2><p class="lead">La edición Pro da capacidad propia de investigación, con cada resultado trazable hasta su método.</p><a class="lnk" href="#planes">Ver la edición Pro</a></div><div class="pc soft" data-rv>{SOON}<h3>Para negocios pequeños: Lite</h3><p>Autoservicio en pocos pasos, con plantillas y un informe. Todavía no está abierta.</p><a class="lnk" href="#inicio" data-go="espera">Avísenme cuando abra</a></div></section>
"""+cta2('Míralo con tu propio caso','En media hora, con una pieza tuya.')+'</section>'
_pl=[('campus','Campus','Universidades','Práctica real para tus alumnos, con capacitación.',['Roles de docente y alumno','Plantillas de estudio','Cupo por programa','Co-marca: Aesteros para tu universidad','Capacitación de FRSKO','Soporte con una persona'],'Por programa académico y periodo, semestral o anual.','<a class="btn" href="#inicio" data-go="demo">Pedir una demostración</a>',''),
('pro','Pro','Agencias y equipos de investigación','Evidencia para recomendar, con tu marca.',['Baterías e informe integrado','Tu marca en informes y archivos','Co-marca en la plataforma','Portal de cliente de solo lectura '+SOON,'Soporte con una persona'],'Por cotización, según equipo y uso.','<a class="btn" href="#inicio" data-go="demo">Pedir una demostración</a>',' hot'),
('lite','Lite','Negocios pequeños','Entiende cómo ven tu marca, en pocos pasos.',['Autoservicio','Plantillas','Un informe por estudio','Centro de ayuda como soporte'],'Aún sin abrir.','<a class="btn ghost" href="#inicio" data-go="espera">Unirme a la lista de espera</a>',' wait')]
PLA='<section class="view lt" id="v-planes" hidden>'+hero2('Planes','Tres ediciones,<br>un mismo núcleo','Las tres miden igual y dicen igual de dónde viene cada dato. Cambia para quién están pensadas y qué las acompaña.')+f"""
<div class="plans">{''.join(f'<article class="plan{c}" data-rv><em>{w}</em><div class="edlogo">{ed_logo(ek,"pl_"+ek,24)}</div><h2>{n}</h2><p class="lead">{d}</p>{li(inc)}<p class="how"><b>Cómo se cobra</b>{how}</p>{b}</article>' for ek,n,w,d,inc,how,b,c in _pl)}</div>
<section class="mb all" data-rv><h2>En las tres, sin excepción</h2><div class="ex3"><div><b class="ex3Title">{ic('terminado','pl_s1',20)}Sellos de evidencia</b><span>Medido, estimado o modelado en cada cifra.</span></div><div><b class="ex3Title">{ic('confianza','pl_s2',20)}Margen de error</b><span>Junto a cada resultado, con aviso si la muestra es chica.</span></div><div><b class="ex3Title">{ic('privacidad','pl_s3',20)}Privacidad por defecto</b><span>El video de la cámara no sale del dispositivo de quien participa.</span></div></div></section>
<section class="mb faq"><div class="hd" data-rv><h2>Preguntas sobre planes</h2></div><div data-rv><details><summary>¿Por qué no hay precios aquí?</summary><p>Porque dependen del programa, del periodo y del cupo. Te mandamos una cotización después de la demostración.</p></details><details><summary>¿Hay piloto para universidades?</summary><p>Sí. Un semestre con un grupo, sin costo, a cambio de una carta de intención, una fecha de decisión y permiso para contar el caso.</p></details><details><summary>¿Qué pasa si rebaso el cupo?</summary><p>El exceso se cotiza aparte. La plataforma avisa antes de llegar al límite.</p></details><details><summary>¿Puedo tener la plataforma solo con mi marca?</summary><p>Sí, por contrato y en una instancia dedicada. Los sellos y la nota de método se conservan.</p></details></div></section>
"""+cta2('¿Cuál te toca?','Cuéntanos tu caso y te decimos con cuál empezar.','<a class="btn ghost" href="#producto">Ver el producto</a>')+'</section>'
_bl=[('Aprender el método','Cómo leer un mapa de atención sin engañarte','ocular',1),('Aprender el método','Qué mide en realidad una prueba de asociación implícita','iat',0),('Para dar la clase','Una práctica de neuromarketing para cuatro semanas','informe',0),('Decidir con evidencia','Dos empaques, una decisión: el caso de Brisa','variantes',0),('Lo que no se puede afirmar','Una sonrisa no es una emoción','video',0),('Aprender el método','Margen de error, explicado con una sola gráfica','encuesta',0)]
BLO='<section class="view lt" id="v-blog" hidden>'+hero2('Blog','Leer la percepción,<br>con calma','Método, práctica de clase y casos. Escrito para entenderse sin formación técnica.')+f"""
<div class="bfil" role="group" aria-label="Línea"><button type="button" data-f="" aria-pressed="true">Todo</button>{''.join(f'<button type="button" data-f="{x}" aria-pressed="false">{x}</button>' for x in ['Aprender el método','Para dar la clase','Decidir con evidencia','Lo que no se puede afirmar'])}</div>
<div class="posts">{''.join((f'<a class="post" href="#articulo" data-l="{l}" data-rv><span class="pm">{mini(k,"b%d"%i)}</span><em>{l}</em><b>{t}</b><span class="rd">Artículo de muestra · 3 min</span></a>' if ok else f'<div class="post wip" data-l="{l}" data-rv><span class="pm">{mini(k,"b%d"%i)}</span><em>{l}</em><b>{t}</b><span class="rd">En preparación</span></div>') for i,(l,t,k,ok) in enumerate(_bl))}</div>
<section class="mb duo"><div data-rv><h2>Glosario</h2><p class="lead">Una página por término, en español llano.</p></div><div class="gls" data-rv>{''.join(f'<span>{x}</span>' for x in ['Área de interés','Asociación implícita','Intervalo de confianza','Mapa de atención','Primera mirada','Rango de precio aceptable','Recorrido de la mirada','Tiempo de permanencia'])}</div></section>
</section>"""
ART='<section class="view lt" id="v-articulo" hidden><article class="art"><a class="lnk" href="#blog">Volver al blog</a><span class="eyebrow">Aprender el método · Artículo de muestra</span><h1>Cómo leer un mapa de atención sin engañarte</h1><p class="sub">Un mapa de atención se ve tan claro que invita a concluir de más. Tres preguntas antes de creerle.</p>'+f"""
<figure class="artf">{mini('ocular','ar')}<figcaption>Las manchas dicen dónde cayó la mirada. No dicen por qué.</figcaption></figure>
<h2>1. ¿Cuánta gente hay detrás?</h2><p>Un mapa con ocho personas y uno con ochenta se ven igual de convincentes. Antes de mirar los colores, busca el número de sesiones válidas. Con pocas, una sola persona distraída mueve la mancha.</p>
<h2>2. ¿Qué tan grande es el área?</h2><p>Una cámara web mide bien áreas medianas y grandes: un titular, un producto, un botón. No distingue si alguien leyó la letra chica. Si tu pregunta depende de un detalle pequeño, el mapa no la puede responder.</p>
<h2>3. ¿Mirar es entender?</h2><p>Que un área reciba muchas miradas puede significar que atrae o que confunde. El mapa no lo separa. Por eso conviene cruzarlo con otra medida: qué recordó la gente, qué asoció o qué eligió.</p>
<h2>En corto</h2><p>Un mapa de atención responde «dónde» y «en qué orden». Para el «por qué» hace falta otra prueba al lado.</p>
<div class="artc"><b>¿Quieres verlo con una pieza tuya?</b><a class="btn" href="#inicio" data-go="demo">Pedir una demostración</a></div></article></section>"""
NOV='<section class="view lt" id="v-novedades" hidden>'+hero2('Novedades','Lo que hay,<br>y lo que viene','Cada herramienta nueva se anuncia aquí cuando pasa nuestra validación.')+f"""
<ol class="nov"><li data-rv><em>Disponible</em><h2>Nueve herramientas</h2><div class="novg">{''.join(f'<a href="#producto" data-go="t-{t[0]}">{t[1]}</a>' for t in TOOLS)}</div></li><li data-rv><em>Disponible</em><h2>Alrededor de la prueba</h2><div class="novg"><span>Laboratorio de calibración</span><span>Calculadora de muestra</span><span>Proyectos y alumnos</span></div></li><li class="nx" data-rv><em>En desarrollo</em><h2>Más herramientas</h2><p>Todavía sin nombre público. Las anunciamos cuando estén listas.</p><a class="lnk" href="#inicio" data-go="espera">Avísenme de cada una</a></li></ol></section>"""
_hp=[('inv','Investigo o doy clase',['Primeros pasos: tu primer estudio','Armar un estudio con varias herramientas','Invitar participantes','Cómo leer cada gráfica','Exportar resultados','Crear grupos y repartir códigos']),('adm','Administro la cuenta',['Usuarios y permisos','Cupos de alumnos, participantes e IA','Logotipo y portada de tu organización','Privacidad y borrado de datos']),('par','Voy a participar',['Qué se va a medir','Qué se guarda de mi cámara','Cómo calibrar la cámara','No me funciona la cámara','Puedo salir a la mitad'])]
AYU='<section class="view lt" id="v-ayuda" hidden>'+hero2('Centro de ayuda','¿En qué te ayudamos?','','<label class="hsrch" for="h-q"><span class="vh">Buscar en la ayuda</span><input id="h-q" type="search" placeholder="Busca: calibrar, exportar, código de grupo" autocomplete="off"></label>')+f"""
<div class="doors" role="tablist" aria-label="Quién eres">{''.join(f'<button type="button" role="tab" id="hd-{k}" aria-controls="hp-{k}" aria-selected="{"true" if i==0 else "false"}">{n}</button>' for i,(k,n,_) in enumerate(_hp))}</div>
{''.join(f'<div class="hlist" role="tabpanel" id="hp-{k}" aria-labelledby="hd-{k}"'+('' if i==0 else ' hidden')+'>'+''.join(f'<a class="hi" href="#ayuda"><b>{x}</b><span>En preparación</span></a>' for x in xs)+'</div>' for i,(k,n,xs) in enumerate(_hp))}
<p class="hnone" id="h-none" hidden>Nada con esas palabras. Prueba con otra o escríbenos.</p>
<section class="mb duo"><div data-rv><h2>Si vas a participar, lo esencial</h2><p class="lead">De tu cámara se guardan coordenadas y tiempos, no el video. No das nombre ni correo. Puedes salir cuando quieras.</p></div><div class="pc soft" data-rv><h3>¿No encontraste tu respuesta?</h3><p>Campus y Pro tienen soporte con una persona. El contacto se publica al abrir la plataforma.</p></div></section></section>"""
ENT='<section class="view dk" id="v-entrar" hidden><div class="ent"><span class="edot" aria-hidden="true"></span><div class="entc"><span class="entl">'+logo("en",30)+'</span><h1>Entrar</h1><form class="form" id="f-ent" novalidate><label for="e-mail">Correo institucional o de trabajo<input id="e-mail" type="email" autocomplete="email"></label><button class="btn" type="submit">Continuar</button><p class="msg" id="e-msg" role="status" aria-live="polite"></p></form><div class="ento"><form class="form row" id="f-cod" novalidate><label for="e-cod">Soy alumno y tengo un código de grupo<input id="e-cod" autocomplete="off" placeholder="Código"></label><button class="btn ghost" type="submit">Unirme</button></form><p class="note">¿Vas a participar en un estudio? No necesitas cuenta: abre la liga que te enviaron.</p></div></div></div></section>'
VIEWS2=UNI+AGE+EMP+PLA+BLO+ART+NOV+AYU+ENT


# ===== contenido: artículos, glosario, ayuda del participante, legales, casos =====
def artv(slug,linea,titulo,sub,k,cuerpo,nota='Artículo'): return f'<section class="view lt" id="v-{slug}" data-nav="blog" hidden><article class="art"><a class="lnk" href="#blog">Volver al blog</a><span class="eyebrow">{linea} · {nota}</span><h1>{titulo}</h1><p class="sub">{sub}</p><figure class="artf">{mini(k,"x"+slug.replace("-",""))}</figure>{cuerpo}<div class="artc"><b>¿Quieres verlo con una pieza tuya?</b><a class="btn" href="#inicio" data-go="demo">Pedir una demostración</a></div></article></section>'
_A=[
('a-mapa','Aprender el método','Cómo leer un mapa de atención sin engañarte','Un mapa de atención se ve tan claro que invita a concluir de más. Tres preguntas antes de creerle.','ocular',"""<h2>1. ¿Cuánta gente hay detrás?</h2><p>Un mapa con ocho personas y uno con ochenta se ven igual de convincentes. Antes de mirar los colores, busca el número de sesiones válidas. Con pocas, una sola persona distraída mueve la mancha.</p><h2>2. ¿Qué tan grande es el área?</h2><p>Una cámara web mide bien áreas medianas y grandes: un titular, un producto, un botón. No distingue si alguien leyó la letra chica. Si tu pregunta depende de un detalle pequeño, el mapa no la puede responder.</p><h2>3. ¿Mirar es entender?</h2><p>Que un área reciba muchas miradas puede significar que atrae o que confunde. El mapa no lo separa. Por eso conviene cruzarlo con otra medida: qué recordó la gente, qué asoció o qué eligió.</p><h2>En corto</h2><p>Un mapa de atención responde «dónde» y «en qué orden». Para el «por qué» hace falta otra prueba al lado.</p>"""),
('a-asociacion','Aprender el método','Qué mide en realidad una prueba de asociación implícita','No mide lo que la gente piensa de tu marca. Mide qué tan rápido la une con una idea, y eso es otra cosa.','iat',"""<h2>La mecánica</h2><p>En pantalla aparece una palabra o una imagen y hay que mandarla a la izquierda o a la derecha lo más rápido posible. En una ronda, tu marca comparte lado con «natural». En otra, lo comparte con «artificial». Si la gente responde más rápido en la primera, la marca y «natural» van más juntas en su cabeza.</p><h2>Qué sale</h2><p>Una puntuación que resume esa diferencia de tiempos. Cerca de cero no hay inclinación. Mientras más se aleja, más fuerte es la asociación. Siempre viene con su margen de error: si el margen toca el cero, no hay nada que afirmar.</p><h2>Lo que sí dice</h2><p>Hacia dónde se inclina un grupo y con qué fuerza. Sirve para comparar dos marcas, dos conceptos o el antes y el después de una campaña.</p><h2>Lo que no dice</h2><p>Nada sobre una persona en particular: la puntuación de alguien cambia de un día a otro. Tampoco dice que la gente vaya a comprar. Una asociación fuerte con «caro» puede ser buena o mala según lo que vendas.</p><h2>Cómo usarla bien</h2><p>Elige ideas que importen para la decisión, no las que te gustaría oír. Y léela junto a lo que la gente declara: cuando lo que dicen y lo que asocian no coinciden, ahí suele estar el hallazgo.</p>"""),
('a-practica','Para dar la clase','Una práctica de neuromarketing para cuatro semanas','Un guion para que cada equipo pase de una pregunta a una conclusión con datos propios, sin laboratorio.','informe',"""<h2>Semana 1. La pregunta</h2><p>Cada equipo elige una pieza real (un empaque, un anuncio, una página) y escribe una sola pregunta que se pueda contestar con una medida. «¿Se ve el precio?» sirve. «¿Le gusta a la gente?» no, porque no dice qué medir.</p><h2>Semana 2. El estudio</h2><p>Arman el estudio y lo prueban entre ellos. Aquí aparecen los errores baratos: instrucciones confusas, una imagen que tarda en cargar, un área de interés demasiado pequeña para la cámara.</p><h2>Semana 3. El campo</h2><p>Invitan a sus participantes. Conviene pedir una meta mínima por equipo y revisar a media semana cuántas sesiones válidas llevan, no cuántas ligas mandaron.</p><h2>Semana 4. La lectura</h2><p>Cada equipo presenta tres cosas: qué encontró, qué tan firme es y qué no puede afirmar con sus datos. La tercera es la que más enseña.</p><h2>Qué evaluar</h2><p>La calidad de la pregunta, el cuidado en el campo y la honestidad de la conclusión. Un equipo que dice «con nuestra muestra no alcanza» y lo demuestra entendió más que uno que presenta un hallazgo espectacular con ocho personas.</p>"""),
('a-brisa','Decidir con evidencia','Un anuncio, tres medidas: el caso de Brisa','Brisa es una marca de ejemplo. El caso muestra cómo tres pruebas pequeñas cambian una decisión de publicidad.','encuesta',"""<h2>La duda</h2><p>Brisa, agua mineral con un toque de limón, tenía listo su anuncio. El equipo discutía tres cosas: si el precio se veía, si la marca se entendía como natural y si $18 era el precio correcto.</p><h2>Qué miran</h2><p>Con seguimiento ocular, 52 personas vieron el anuncio cinco segundos. El titular se llevó la primera mirada de la mitad. El precio, de casi nadie. La discusión sobre el tamaño del precio dejó de ser de gustos.</p><h2>Qué asocian</h2><p>La prueba de asociación dio +0,58 entre Brisa y «natural», con un margen de 0,41 a 0,75. El margen no toca el cero, así que se puede afirmar. Entre quienes ya compran la marca la asociación fue más fuerte.</p><h2>Qué opinan</h2><p>Las preguntas de precio marcaron un rango aceptable de $17,40 a $24,00. Los $18 quedaban dentro, pero pegados al borde donde un precio empieza a generar duda por barato.</p><h2>La decisión</h2><p>Titular arriba, la palabra «natural» al frente y precio en $20. Ninguna de las tres pruebas decidió sola. Juntas quitaron de la mesa las opiniones.</p>""",'Caso de ejemplo'),
('a-sonrisa','Lo que no se puede afirmar','Una sonrisa no es una emoción','La cámara puede decir qué hizo una cara en cada segundo. No puede decir qué sintió la persona.','video',"""<h2>Lo que la cámara registra</h2><p>Movimientos: las comisuras suben, el ceño se junta, las cejas se levantan. Son hechos observables, segundo a segundo, y se pueden contar.</p><h2>El salto que no se debe dar</h2><p>De «sonrió» a «le gustó» hay un salto. La gente sonríe por cortesía, por nervios o porque recordó otra cosa. Frunce el ceño cuando se concentra, no solo cuando algo le molesta.</p><h2>Entonces, ¿para qué sirve?</h2><p>Para comparar momentos. Si en el segundo doce de un comercial la mayoría levanta las cejas y en otra versión no, algo distinto pasa ahí. Eso orienta dónde mirar. No explica por qué.</p><h2>Cómo leerlo</h2><p>Como una pista que se confirma con otra medida. Si la escena donde más gente sonríe es también la que más se recuerda y la que mejor se asocia con la marca, el argumento se sostiene. Si solo tienes la sonrisa, tienes una sonrisa.</p><h2>Por qué lo decimos así</h2><p>Porque prometer que una cámara lee emociones vende bien y no se puede cumplir. Preferimos decir qué se midió y dejar la interpretación a quien conoce el contexto.</p>"""),
]
ARTS=''.join(artv(*a) for a in _A)
_bl2=[('Aprender el método','Cómo leer un mapa de atención sin engañarte','ocular','a-mapa','3 min'),('Aprender el método','Qué mide en realidad una prueba de asociación implícita','iat','a-asociacion','4 min'),('Para dar la clase','Una práctica de neuromarketing para cuatro semanas','informe','a-practica','4 min'),('Decidir con evidencia','Un anuncio, tres medidas: el caso de Brisa','encuesta','a-brisa','4 min'),('Lo que no se puede afirmar','Una sonrisa no es una emoción','video','a-sonrisa','3 min'),('Aprender el método','Margen de error, explicado con una sola gráfica','variantes','','')]
_GL=[('Área de interés','La parte de una pieza sobre la que quieres saber algo: un titular, un logotipo, un botón. Todos los indicadores de mirada se calculan por área.'),('Asociación implícita','Qué tan unidas van dos ideas en la cabeza de un grupo, medido por la rapidez con que las relacionan y no por lo que declaran.'),('Intervalo de confianza','El rango donde probablemente está el valor real. Si es ancho, el dato es poco preciso. Si incluye el cero, no se puede afirmar que haya diferencia.'),('Mapa de atención','Una imagen que muestra dónde se concentraron las miradas de un grupo. Dice dónde, no por qué.'),('Primera mirada','El área que una persona ve antes que las demás, y cuánto tarda en llegar a ella.'),('Rango de precio aceptable','El tramo de precios en que la mayoría no considera el producto ni demasiado barato ni demasiado caro.'),('Recorrido de la mirada','El orden en que la mirada pasa de un área a otra.'),('Tiempo de permanencia','Cuánto tiempo, en total, se quedó la mirada dentro de un área.')]
GLO='<section class="view lt" id="v-glosario" data-nav="blog" hidden>'+hero2('Glosario','Las palabras,<br>en llano','Los términos que aparecen en los resultados, explicados en una o dos frases.')+'<dl class="glo">'+''.join(f'<div data-rv><dt>{t}</dt><dd>{d}</dd></div>' for t,d in _GL)+'</dl><a class="lnk" href="#blog">Volver al blog</a></section>'
BLO='<section class="view lt" id="v-blog" hidden>'+hero2('Blog','Leer la percepción,<br>con calma','Método, práctica de clase y casos. Escrito para entenderse sin formación técnica.')+f"""
<div class="bfil" role="group" aria-label="Línea"><button type="button" data-f="" aria-pressed="true">Todo</button>{''.join(f'<button type="button" data-f="{x}" aria-pressed="false">{x}</button>' for x in ['Aprender el método','Para dar la clase','Decidir con evidencia','Lo que no se puede afirmar'])}</div>
<div class="posts">{''.join((f'<a class="post" href="#{sl}" data-l="{l}" data-rv><span class="pm">{mini(k,"b%d"%i)}</span><em>{l}</em><b>{t}</b><span class="rd">{m} de lectura</span></a>' if sl else f'<div class="post wip" data-l="{l}" data-rv><span class="pm">{mini(k,"b%d"%i)}</span><em>{l}</em><b>{t}</b><span class="rd">En preparación</span></div>') for i,(l,t,k,sl,m) in enumerate(_bl2))}</div>
<section class="mb duo"><div data-rv><h2>Glosario</h2><p class="lead">Los términos de los resultados, en español llano.</p><a class="lnk" href="#glosario">Abrir el glosario</a></div><div class="gls" data-rv>{''.join(f'<span>{t}</span>' for t,_ in _GL)}</div></section>
</section>"""
_HPAR=[('hq-mide','Qué se va a medir','Depende del estudio, y siempre se te dice antes de empezar. Puede ser hacia dónde miras en una imagen, cuánto tardas en responder o lo que contestas en unas preguntas. No hay respuestas correctas: no se te evalúa a ti, se evalúa la pieza.'),('hq-guarda','Qué se guarda de mi cámara','Coordenadas y tiempos: en qué parte de la pantalla estuvo tu mirada y cuándo. El video no sale de tu equipo. No se te pide nombre ni correo.'),('hq-calibra','Cómo calibrar la cámara','Siéntate con la cara bien iluminada de frente, sin una ventana detrás. Coloca la pantalla a la altura de los ojos. Cuando aparezcan los puntos, síguelos con la mirada sin mover la cabeza. Si la calibración no sale bien, la plataforma te pide repetirla.'),('hq-falla','No me funciona la cámara','Revisa que el navegador tenga permiso para usarla: suele aparecer un aviso junto a la dirección de la página. Cierra otras aplicaciones que la estén usando, como una videollamada. Si sigue sin funcionar, prueba con otro navegador o desde una computadora.'),('hq-salir','Puedo salir a la mitad','Sí, en cualquier momento, cerrando la página. Una sesión sin terminar no entra en los resultados.')]
PARV='<section class="view lt" id="v-participar" data-nav="ayuda" hidden>'+hero2('Centro de ayuda · Voy a participar','Antes de<br>empezar','Lo que conviene saber si te invitaron a un estudio. Se lee en dos minutos.')+'<div class="hq">'+''.join(f'<section id="{i}" data-rv><h2>{t}</h2><p>{d}</p></section>' for i,t,d in _HPAR)+'</div><a class="lnk" href="#ayuda">Volver a la ayuda</a></section>'
_hp2=[('inv','Investigo o doy clase',[(x,'') for x in ['Primeros pasos: tu primer estudio','Armar un estudio con varias herramientas','Invitar participantes','Cómo leer cada gráfica','Exportar resultados','Crear grupos y repartir códigos']]),('adm','Administro la cuenta',[(x,'') for x in ['Usuarios y permisos','Cupos de alumnos, participantes e IA','Logotipo y portada de tu organización','Privacidad y borrado de datos']]),('par','Voy a participar',[(t,i) for i,t,_ in _HPAR])]
def _hi(x,go): return f'<a class="hi" href="#participar" data-go="{go}"><b>{x}</b><span>Leer</span></a>' if go else f'<a class="hi wip" href="#ayuda"><b>{x}</b><span>En preparación</span></a>'
_h_ic={'inv':'maestro','adm':'ajustes','par':'participante'}
def _htab(i,k,n): return f'<button type="button" role="tab" id="hd-{k}" aria-controls="hp-{k}" aria-selected="{"true" if i==0 else "false"}">{ic(_h_ic[k],"hd_"+k,18)}{n}</button>'
def _hpan(i,k,xs): return f'<div class="hlist" role="tabpanel" id="hp-{k}" aria-labelledby="hd-{k}"'+('' if i==0 else ' hidden')+'>'+''.join(_hi(x,go) for x,go in xs)+'</div>'
AYU='<section class="view lt" id="v-ayuda" hidden>'+hero2('Centro de ayuda','¿En qué te ayudamos?','','<label class="hsrch" for="h-q">'+ic('buscar','hq_s',20)+'<span class="vh">Buscar en la ayuda</span><input id="h-q" type="search" placeholder="Busca: calibrar, exportar, código de grupo" autocomplete="off"></label>')+'<div class="doors" role="tablist" aria-label="Quién eres">'+''.join(_htab(i,k,n) for i,(k,n,_) in enumerate(_hp2))+'</div>'+''.join(_hpan(i,k,xs) for i,(k,n,xs) in enumerate(_hp2))+"""<p class="hnone" id="h-none" hidden>Nada con esas palabras. Prueba con otra o escríbenos.</p>
<section class="mb duo"><div data-rv><h2>Si vas a participar, lo esencial</h2><p class="lead">De tu cámara se guardan coordenadas y tiempos, no el video. No das nombre ni correo. Puedes salir cuando quieras.</p><a class="lnk" href="#participar">Leer todo</a></div><div class="pc soft" data-rv><h3>¿No encontraste tu respuesta?</h3><p>Campus y Pro tienen soporte con una persona. El contacto se publica al abrir la plataforma.</p></div></section></section>"""
def legal(slug,eb,h,sub,secs): return f'<section class="view lt" id="v-{slug}" data-nav="legal" hidden><article class="art leg"><p class="draft">Borrador para revisión legal. Los datos entre corchetes están por definir. No es el texto vigente.</p><span class="eyebrow">{eb}</span><h1>{h}</h1><p class="sub">{sub}</p>'+''.join(f'<h2>{t}</h2>{b}' for t,b in secs)+'<p class="legn">Otros documentos: <a href="#privacidad">Privacidad</a> · <a href="#terminos">Términos</a> · <a href="#camara">Uso de cámara</a></p></article></section>'
LEG=legal('privacidad','Legal','Aviso de privacidad','Qué datos tratamos, para qué y cómo ejercer tus derechos.',[
('Quién es responsable','<p>[Razón social del responsable], con domicilio en [domicilio], es responsable del tratamiento de tus datos personales. Contacto: [correo de privacidad].</p>'),
('Si participas en un estudio','<p>No te pedimos nombre ni correo. Tratamos las respuestas que das, los tiempos de respuesta y, si el estudio usa la cámara, las coordenadas de tu mirada en la pantalla. El video de tu cámara se procesa en tu equipo y no se envía a nuestros servidores. Tu dirección de red se guarda solo de forma cifrada e irreversible, para evitar respuestas duplicadas dentro de un mismo estudio.</p>'),
('Si tienes una cuenta','<p>Tratamos tu nombre, tu correo y la organización a la que perteneces, para darte acceso, dar soporte y facturar el servicio a tu organización.</p>'),
('Para qué usamos los datos','<p>Para operar la plataforma, calcular los resultados de los estudios y dar soporte. No vendemos datos personales ni los usamos para publicidad de terceros.</p>'),
('Quién más los recibe','<p>Proveedores que alojan y operan la plataforma, bajo contrato y solo para ese fin: [lista de encargados]. La universidad, agencia o empresa que creó el estudio ve los resultados, que no incluyen tu identidad.</p>'),
('Inteligencia artificial','<p>Los textos que redacta la IA parten de resultados ya calculados y agregados. La IA no recibe respuestas individuales ni datos personales.</p>'),
('Cuánto tiempo se conservan','<p>[Plazo de conservación por tipo de dato]. Al terminar, se eliminan o se anonimizan.</p>'),
('Tus derechos','<p>Puedes pedir acceso, rectificación, cancelación u oposición, y revocar tu consentimiento, escribiendo a [correo de privacidad]. Respondemos en [plazo]. Si participaste sin dar datos que te identifiquen, es posible que no podamos localizar tu sesión.</p>'),
('Cambios','<p>Publicaremos aquí cualquier cambio a este aviso, con su fecha. Última actualización: [fecha].</p>')])+legal('terminos','Legal','Términos del servicio','Las reglas para usar Aesteros. Los contratos con cada organización pueden añadir condiciones.',[
('El servicio','<p>Aesteros es una plataforma para diseñar estudios de percepción, aplicarlos y leer sus resultados. La opera [razón social].</p>'),
('Cuentas','<p>Las cuentas se crean por invitación de una organización con contrato vigente. Cada persona es responsable del uso de su cuenta.</p>'),
('Tus estudios y tus datos','<p>Los estudios, las piezas que subes y los resultados pertenecen a tu organización. Los tratamos solo para darte el servicio.</p>'),
('Quien participa','<p>Quien crea un estudio es responsable de invitar a personas que puedan consentir y de no pedirles datos que no hagan falta. La plataforma muestra el consentimiento antes de cada medición.</p>'),
('Qué afirma un resultado','<p>Cada resultado indica si es medido, estimado o modelado, y su margen de error. Aesteros no garantiza ventas ni resultados comerciales. Las decisiones que tomes con los datos son tuyas.</p>'),
('Uso aceptable','<p>No se permite usar la plataforma para identificar a personas, para evaluarlas individualmente ni para fines distintos de la investigación descrita en el estudio.</p>'),
('Pago y vigencia','<p>El precio, el periodo y los cupos se fijan en el contrato o la cotización de cada organización.</p>'),
('Disponibilidad','<p>[Compromiso de disponibilidad y ventanas de mantenimiento].</p>'),
('Ley aplicable','<p>[Jurisdicción y ley aplicable].</p>')])+legal('camara','Legal','Uso de la cámara','Qué pasa cuando un estudio te pide encender la cámara, explicado sin letra chica.',[
('Para qué se usa','<p>Para estimar hacia qué parte de la pantalla miras mientras ves una imagen o un video. En algunos estudios, y solo si se indica en el consentimiento, también para registrar movimientos del rostro como una sonrisa o un ceño.</p>'),
('Qué sale de tu equipo','<p>Coordenadas y tiempos. Por ejemplo: «a los 1,2 segundos, la mirada estaba en la esquina superior izquierda».</p>'),
('Qué no sale de tu equipo','<p>El video. La imagen de la cámara se procesa en tu navegador y no se envía ni se guarda en nuestros servidores.</p>'),
('La calibración','<p>Antes de empezar se te pide seguir unos puntos con la mirada. Sirve para medir qué tan exacta es tu cámara en ese momento. Si no alcanza, la sesión no se usa.</p>'),
('Puedes decir que no','<p>Si no das permiso a la cámara, el estudio no puede medir la mirada. Puedes cerrar la página en cualquier momento.</p>'),
('Qué tan exacto es','<p>Una cámara web es menos exacta que un equipo de laboratorio. Sirve para áreas medianas y grandes. Los resultados lo indican.</p>')])
# casos a fondo
def caso(t,sub,pasos,cierre): return f'<section class="mb"><div class="hd" data-rv><h2>{t}</h2><p>{sub}</p></div><ol class="sem">'+''.join(f'<li data-rv style="--i:{i}"><span>{i+1}</span><b>{a}</b><p>{b}</p></li>' for i,(a,b) in enumerate(pasos))+f'</ol><p class="casoc" data-rv>{cierre}</p></section>'
_ca=caso('Un caso de ejemplo: dos rutas para Brisa','La agencia tiene dos rutas creativas y el cliente no se decide.',[('La duda','La ruta A es más vistosa. La B habla más del producto. En la sala hay opiniones para las dos.'),('La batería','La agencia arma un estudio con seguimiento ocular, variantes implícitas y dos preguntas de preferencia.'),('El público','Manda una sola liga a personas del público objetivo. Responden desde su casa.'),('La lectura','La A gana en atención al titular. La B gana en asociación con «natural». El informe lo muestra lado a lado.')],'La agencia recomienda la ruta B con el titular de la A, y lo presenta con su marca y con la evidencia a la vista.')
_ce=caso('Un caso de ejemplo: el relanzamiento de Brisa','El equipo de marca tiene que cerrar empaque, precio y página antes de producir.',[('El empaque','Seguimiento ocular sobre dos versiones. En una, el sabor se ve primero. En la otra, se pierde.'),('El precio','Cuatro preguntas marcan el rango en que el precio no estorba.'),('La página','El recorrido web muestra en qué paso la gente abandona la compra.'),('La junta','Un informe junta las tres medidas, cada una con su sello y su margen de error.')],'Tres decisiones que solían tomarse por separado y por intuición llegan juntas y con evidencia.')
AGE=AGE.replace('<section class="mb"><div class="hd" data-rv><h2>Tres momentos donde cambia la conversación</h2>',_ca+'<section class="mb"><div class="hd" data-rv><h2>Tres momentos donde cambia la conversación</h2>',1)
EMP=EMP.replace('<section class="mb duo"><div data-rv><h2>Para un equipo de marca o de investigación</h2>',_ce+'<section class="mb duo"><div data-rv><h2>Para un equipo de marca o de investigación</h2>',1)
VIEWS2=UNI+AGE+EMP+PLA+BLO+ARTS+GLO+NOV+AYU+PARV+ENT+LEG


# ===== guías visuales de ayuda y artículo de margen de error =====
def ilu(body): return '<svg class="ilu" viewBox="0 0 200 120" aria-hidden="true">'+body+'</svg>'
_PER='<circle cx="{x}" cy="46" r="13" fill="#14110C"/><path d="M{a},98 a22,22 0 0 1 44,0z" fill="#14110C"/>'
def per(x): return _PER.format(x=x,a=x-22)
_SCR='<rect x="{x}" y="26" width="64" height="46" rx="6" fill="#FFF7E6" stroke="#14110C" stroke-width="3"/><path d="M{m},72 v14 M{l},88 h36" stroke="#14110C" stroke-width="3" stroke-linecap="round"/>'
def scr(x): return _SCR.format(x=x,m=x+32,l=x+14)
I_LUZ=ilu(per(56)+scr(116)+'<circle cx="148" cy="14" r="8" fill="#FFB000"/><path d="M148,0 v-0 M132,14 h-6 M170,14 h-6 M137,3 l-4,-4 M159,3 l4,-4" stroke="#FFB000" stroke-width="3" stroke-linecap="round"/><path d="M82,40 L116,46" stroke="#FFB000" stroke-width="2.5" stroke-dasharray="4 4"/>')
I_ALT=ilu(per(56)+scr(116)+'<path d="M70,46 H114" stroke="#FFB000" stroke-width="3" stroke-dasharray="5 5"/><path d="M190,30 v38 M184,36 l6,-7 6,7 M184,62 l6,7 6,-7" stroke="#7A3E12" stroke-width="2.5" fill="none" stroke-linecap="round"/>')
I_PTS=ilu('<rect x="20" y="12" width="160" height="96" rx="10" fill="#FFF7E6" stroke="#14110C" stroke-width="3"/><circle cx="44" cy="32" r="5" fill="rgba(20,17,12,.25)"/><circle cx="156" cy="32" r="5" fill="rgba(20,17,12,.25)"/><circle cx="44" cy="88" r="5" fill="rgba(20,17,12,.25)"/><circle cx="156" cy="88" r="5" fill="rgba(20,17,12,.25)"/><circle cx="100" cy="60" r="16" fill="rgba(255,176,0,.3)"/><circle cx="100" cy="60" r="8" fill="#FFB000"/>')
I_PER=ilu('<rect x="14" y="20" width="172" height="80" rx="12" fill="#FFF7E6" stroke="#14110C" stroke-width="3"/><rect x="26" y="32" width="148" height="18" rx="9" fill="rgba(20,17,12,.1)"/><rect x="34" y="37" width="12" height="8" rx="2" fill="#14110C"/><path d="M46,39 l6,-3 v10 l-6,-3z" fill="#14110C"/><rect x="100" y="62" width="74" height="26" rx="13" fill="#FFB000"/><text x="137" y="80" text-anchor="middle" font-family="Archivo,sans-serif" font-weight="800" font-size="12" fill="#14110C">Permitir</text><rect x="26" y="62" width="64" height="26" rx="13" fill="none" stroke="rgba(20,17,12,.4)" stroke-width="2"/>')
I_MID=ilu(per(100)+'<circle cx="100" cy="46" r="26" fill="none" stroke="#FFB000" stroke-width="3" stroke-dasharray="5 5"/><text x="160" y="52" font-family="Archivo,sans-serif" font-weight="800" font-size="26" fill="#FFB000">?</text>')
I_GUA=ilu(scr(28)+'<circle cx="60" cy="49" r="9" fill="rgba(20,17,12,.3)"/><path d="M100,49 H128" stroke="#14110C" stroke-width="2.5" stroke-dasharray="4 4"/><circle cx="108" cy="49" r="4" fill="#FFB000"/><circle cx="121" cy="49" r="4" fill="#FFB000"/><rect x="134" y="26" width="52" height="46" rx="10" fill="rgba(255,176,0,.18)" stroke="#FFB000" stroke-width="3"/><circle cx="148" cy="40" r="4" fill="#FFB000"/><circle cx="166" cy="46" r="4" fill="#FFB000"/><circle cx="154" cy="58" r="4" fill="#FFB000"/><circle cx="174" cy="60" r="4" fill="#FFB000"/>')
I_SAL=ilu('<rect x="20" y="16" width="160" height="88" rx="10" fill="#FFF7E6" stroke="#14110C" stroke-width="3"/><path d="M20,36 H180" stroke="#14110C" stroke-width="3"/><circle cx="164" cy="26" r="7" fill="#FFB000"/><path d="M161,23 l6,6 M167,23 l-6,6" stroke="#14110C" stroke-width="2.2" stroke-linecap="round"/><rect x="40" y="52" width="84" height="8" rx="4" fill="rgba(20,17,12,.2)"/><rect x="40" y="68" width="56" height="8" rx="4" fill="rgba(20,17,12,.2)"/>')
def hqs(i,t,d,il,extra=''): return f'<section id="{i}" data-rv><div class="hqi">{il}</div><div><h2>{t}</h2><p>{d}</p>{extra}</div></section>'
_cal='<ol class="s3"><li>'+I_LUZ+'<b>Luz de frente</b><span>Sin una ventana detrás de ti.</span></li><li>'+I_ALT+'<b>Pantalla a la altura de los ojos</b><span>Y la cabeza quieta.</span></li><li>'+I_PTS+'<b>Sigue los puntos</b><span>Solo con la mirada.</span></li></ol>'
PARV='<section class="view lt" id="v-participar" data-nav="ayuda" hidden>'+hero2('Centro de ayuda · Voy a participar','Antes de<br>empezar','Lo que conviene saber si te invitaron a un estudio. Se lee en dos minutos.')+'<div class="hq">'+hqs('hq-mide','Qué se va a medir','Depende del estudio, y siempre se te dice antes de empezar. Puede ser hacia dónde miras en una imagen, cuánto tardas en responder o lo que contestas en unas preguntas. No hay respuestas correctas: no se te evalúa a ti, se evalúa la pieza.',I_MID)+hqs('hq-guarda','Qué se guarda de mi cámara','Coordenadas y tiempos: en qué parte de la pantalla estuvo tu mirada y cuándo. El video no sale de tu equipo. No se te pide nombre ni correo.',I_GUA)+f'<section id="hq-calibra" class="wide" data-rv><div><h2>Cómo calibrar la cámara</h2><p>Tres cosas hacen la diferencia. Si la calibración no sale bien, la plataforma te pide repetirla.</p>{_cal}</div></section>'+hqs('hq-falla','No me funciona la cámara','Revisa que el navegador tenga permiso para usarla: suele aparecer un aviso junto a la dirección de la página. Cierra otras aplicaciones que la estén usando, como una videollamada. Si sigue sin funcionar, prueba con otro navegador o desde una computadora.',I_PER)+hqs('hq-salir','Puedo salir a la mitad','Sí, en cualquier momento, cerrando la página. Una sesión sin terminar no entra en los resultados.',I_SAL)+'</div><a class="lnk" href="#ayuda">Volver a la ayuda</a></section>'
def cb(n,x,y): return f'<g class="cb"><circle cx="{x}" cy="{y}" r="10"/><text x="{x}" y="{y+4}">{n}</text></g>'
def gcard(t,k,sfx,marks,pts,ojo): return f'<article class="gc" data-rv><div class="gcv"><svg viewBox="0 0 200 120" aria-hidden="true">{MINI[k].replace("tg","tg"+sfx)}{"".join(cb(n+1,x,y) for n,(x,y) in enumerate(marks))}</svg></div><div class="gct"><h2>{t}</h2><ol>{"".join(f"<li>{p}</li>" for p in pts)}</ol><p class="ojo"><b>Ojo:</b> {ojo}</p></div></article>'
GGRA='<section class="view lt" id="v-guia-graficas" data-nav="ayuda" hidden>'+hero2('Centro de ayuda · Guía visual','Cómo leer<br>cada gráfica','Cinco gráficas que vas a ver seguido. En cada una, qué mirar primero y qué no concluir.')+'<div class="gcs">'+gcard('Recorrido de la mirada','ocular','g1',[(40,30),(172,52),(110,104)],['Los números son el orden en que la mayoría miró.','La mancha es cuánta atención recibió esa zona.','Lo que queda sin mancha casi nadie lo vio.'],'dice dónde y en qué orden, no por qué.')+gcard('Asociación implícita','iat','g2',[(80,14),(112,40),(176,40)],['La línea punteada es el cero: ninguna inclinación.','La barra es la fuerza de la asociación.','La franja difusa es el margen de error.'],'si la franja toca el cero, no hay nada que afirmar.')+gcard('Dos versiones frente a frente','variantes','g3',[(67,20),(133,48),(100,108)],['La barra llena es la versión que pruebas.','La punteada es la versión de comparación.','Las dos se leen sobre la misma línea base.'],'una barra más alta no gana si la diferencia cabe dentro del margen.')+gcard('Rango de precio','encuesta','g4',[(30,14),(170,14),(100,36)],['La curva que baja: quienes lo ven barato.','La curva que sube: quienes lo ven caro.','La franja es el rango donde el precio no estorba.'],'es el precio que la gente acepta, no el que más deja.')+gcard('Puntuación con barra','seo','g5',[(60,30),(130,82),(170,56)],['La cifra va de 0 a 100.','La barra repite la cifra para compararla de un vistazo.','El «de 100» recuerda la escala.'],'una puntuación sirve para ordenar prioridades, no predice resultados.')+'</div><a class="lnk" href="#ayuda">Volver a la ayuda</a></section>'
_g5=[('Sube tu pieza','Una imagen, un video o la dirección de un sitio. Ponle un nombre que tu equipo reconozca.','<img src="img/anuncio.jpg" alt="" loading="lazy" width="1400" height="875">'),('Elige qué preguntar','Cada pregunta enciende una herramienta. Empieza con una o dos.','<div class="g5p">'+mini('ocular','q1')+mini('iat','q2')+'</div>'),('Pruébalo tú primero','Contesta tu propio estudio antes de enviarlo. Aquí salen los errores baratos.',I_PTS),('Manda la liga','Una sola liga para todos. Revisa cuántas sesiones válidas llevas, no cuántas invitaciones mandaste.','<div class="dots sm">'+''.join('<i class="%s"></i>'%('ok' if n<17 else 'no') for n in range(24))+'</div>'),('Lee el informe','Cada resultado trae su sello y su margen de error. Empieza por lo que sí se sostiene.','<img src="img/informe.jpg" alt="" loading="lazy" width="1200" height="700">')]
GINI='<section class="view lt" id="v-guia-inicio" data-nav="ayuda" hidden>'+hero2('Centro de ayuda · Guía visual','Tu primer estudio,<br>en cinco pasos','Una vista general. Los nombres exactos de los botones pueden cambiar con la versión final de la plataforma.')+'<ol class="g5">'+''.join(f'<li data-rv><span class="g5n">{n+1}</span><div class="g5v">{v}</div><div><h2>{t}</h2><p>{d}</p></div></li>' for n,(t,d,v) in enumerate(_g5))+'</ol><a class="lnk" href="#ayuda">Volver a la ayuda</a></section>'
_hp3=[('inv','Investigo o doy clase',[('Primeros pasos: tu primer estudio','guia-inicio',''),('Cómo leer cada gráfica','guia-graficas',''),('Armar un estudio con varias herramientas','',''),('Invitar participantes','',''),('Exportar resultados','',''),('Crear grupos y repartir códigos','','')]),('adm','Administro la cuenta',[(x,'','') for x in ['Usuarios y permisos','Cupos de alumnos, participantes e IA','Logotipo y portada de tu organización','Privacidad y borrado de datos']]),('par','Voy a participar',[(t,'participar',i) for i,t,_ in _HPAR])]
def _hi3(x,v,go):
    if not v: return f'<a class="hi wip" href="#ayuda"><b>{x}</b><span>En preparación</span></a>'
    g=f' data-go="{go}"' if go else ''
    tag='Guía visual' if v.startswith('guia') else 'Leer'
    return f'<a class="hi" href="#{v}"{g}><b>{x}</b><span>{tag}</span></a>'
def _hpan3(i,k,xs): return f'<div class="hlist" role="tabpanel" id="hp-{k}" aria-labelledby="hd-{k}"'+('' if i==0 else ' hidden')+'>'+''.join(_hi3(*x) for x in xs)+'</div>'
AYU=AYU[:AYU.index('<div class="hlist"')]+''.join(_hpan3(i,k,xs) for i,(k,n,xs) in enumerate(_hp3))+AYU[AYU.index('<p class="hnone"'):]
_A2=artv('a-margen','Aprender el método','Margen de error, explicado con una sola gráfica','Todo resultado es una cifra y una franja. La franja importa tanto como la cifra.','iat',"""<h2>La cifra</h2><p>Supón que una prueba dice que tu marca se asocia con «natural» con una fuerza de +0,24. Esa cifra sale de las personas que respondieron. Si hubieran respondido otras, habría salido algo parecido, pero no idéntico.</p><h2>La franja</h2><p>El margen de error dice cuánto puede moverse esa cifra. Con 14 personas, el +0,24 podría estar en realidad entre −0,09 y +0,57. Con 60, entre +0,08 y +0,40. Mientras más gente, más angosta la franja.</p><h2>La regla del cero</h2><p>El cero significa «no hay diferencia». Si la franja lo incluye, no puedes descartar que el efecto no exista. Con 14 personas, el ejemplo toca el cero: todavía no se puede afirmar. Con 60 ya no lo toca: se sostiene.</p><h2>Qué hacer con esto</h2><p>Antes de presentar un resultado, mira tres cosas: la cifra, la franja y si la franja toca el cero. Si lo toca, hay dos caminos honestos. Uno es decir que con esa muestra no alcanza. El otro es conseguir más respuestas.</p><h2>Por qué Aesteros lo dibuja difuso</h2><p>Porque un dato incierto debe verse incierto. Una franja ancha se dibuja borrosa y una estrecha, nítida. Así se nota antes de leer un solo número.</p>""")
ARTS=ARTS+_A2
BLO=BLO.replace('<div class="post wip" data-l="Aprender el método" data-rv><span class="pm">'+mini('variantes','b5')+'</span><em>Aprender el método</em><b>Margen de error, explicado con una sola gráfica</b><span class="rd">En preparación</span></div>','<a class="post" href="#a-margen" data-l="Aprender el método" data-rv><span class="pm">'+mini('iat','b5')+'</span><em>Aprender el método</em><b>Margen de error, explicado con una sola gráfica</b><span class="rd">3 min de lectura</span></a>')
assert 'href="#a-margen"' in BLO
VIEWS2=UNI+AGE+EMP+PLA+BLO+ARTS+GLO+NOV+AYU+PARV+GGRA+GINI+ENT+LEG

ROOT_DIR=os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)),'..'))
SITE_URL='https://aesteros.com'
OG_IMG=f'{SITE_URL}/redes/aesteros-portada-facebook-oscuro.jpg'

ROWS=[]
with open(os.path.join(ROOT_DIR,'buscadores.csv'),encoding='utf-8-sig') as _f:
    for r in csv.DictReader(_f):
        v=r['vista'].strip()
        p=r['direccion'].strip()
        if not p.startswith('/'): p='/'+v
        u=SITE_URL+('' if p=='/' else p)
        ROWS.append({'v':v,'p':p,'u':u,'t':r['titulo'].strip(),'d':r['descripcion'].strip()})
META_MAP={r['v']:{'p':r['p'],'u':r['u'],'t':r['t'],'d':r['d']} for r in ROWS}
P2V_MAP={r['p']:r['v'] for r in ROWS}

import hashlib
CSS=open('site.css').read()+open('home.css').read()
JS='window.__AE_META__='+json.dumps(META_MAP,ensure_ascii=False)+';window.__AE_P2V__='+json.dumps(P2V_MAP,ensure_ascii=False)+';\n'+open('site.js').read()+open('home.js').read().replace('__CURV__',CURV)
CSS_H=hashlib.sha256(CSS.encode()).hexdigest()[:8]
JS_H=hashlib.sha256(JS.encode()).hexdigest()[:8]
for base_dir in (ROOT_DIR, os.path.join(ROOT_DIR,'sitio')):
    os.makedirs(os.path.join(base_dir,'css'), exist_ok=True)
    os.makedirs(os.path.join(base_dir,'js'), exist_ok=True)
    open(os.path.join(base_dir,'css','aesteros.css'),'w').write(CSS)
    open(os.path.join(base_dir,'js','aesteros.js'),'w').write(JS)

html=f'''<!DOCTYPE html>
<html lang="es" data-view="inicio" data-mode="main">
<head>
<meta charset="utf-8">
<base href="/">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<!--__SEO_HEAD__-->
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Archivo:wdth,wght@62..125,400..800&display=swap" rel="stylesheet">
<link rel="stylesheet" href="css/aesteros.css?v={CSS_H}">
</head>
<body>
<a class="skip" href="#contenido">Ir al contenido</a>
<header class="dock"><a class="brand" href="#inicio" aria-label="Aesteros, inicio">{logo("n",18)}</a><nav class="n1" aria-label="Principal"><i class="pil" aria-hidden="true"></i><a href="#inicio" data-v="inicio">Inicio</a><a href="#producto" data-v="producto">Producto</a><a href="#metodo" data-v="metodo">Método</a></nav><nav class="n2" aria-label="Explorar"><i class="pil" aria-hidden="true"></i><a class="bk" href="#inicio"><span aria-hidden="true">‹</span> Inicio</a><a href="#universidades" data-v="universidades">Universidades</a><a href="#agencias" data-v="agencias">Agencias</a><a href="#empresas" data-v="empresas">Empresas</a><a href="#planes" data-v="planes">Planes</a><a href="#blog" data-v="blog">Blog</a><a href="#ayuda" data-v="ayuda">Ayuda</a></nav><button type="button" class="more" id="more" aria-expanded="false" aria-controls="sheet" aria-label="Explorar más páginas"><i aria-hidden="true"></i><span aria-hidden="true">Explorar</span></button><button type="button" class="snd" id="snd" aria-pressed="false" aria-label="Sonido"><i aria-hidden="true"></i><span>Sonido</span></button><a class="btn sm" href="#inicio" data-go="demo"><span class="w">Demostración</span><span class="n">Demo</span></a></header><div class="sheet" id="sheet" hidden><div class="shg mob"><em>El sitio</em><a class="m1" href="#inicio">{ic("inicio","sh1",18)}Inicio</a><a class="m1" href="#producto">{ic("bateria","sh2",18)}Producto</a><a href="#metodo">{ic("confianza","sh3",18)}Método</a></div><div class="shg"><em>Para ti</em><a href="#universidades">{ic("alumno","sh4",18)}Universidades</a><a href="#agencias">{ic("cliente","sh5",18)}Agencias</a><a href="#empresas">{ic("equipo","sh6",18)}Empresas</a></div><div class="shg"><em>Comprar</em><a href="#planes">{ic("tabla","sh7",18)}Planes</a><a href="#novedades">{ic("notificacion","sh8",18)}Novedades</a></div><div class="shg"><em>Aprender</em><a href="#blog">{ic("informe","sh9",18)}Blog</a><a href="#ayuda">{ic("ayuda","sh10",18)}Centro de ayuda</a></div><div class="shg end"><a class="entb" href="#entrar" aria-label="Entrar a Aesteros"><span>Entrar a</span>{logo("sh",20)}</a></div></div><span class="cur" id="cur" aria-hidden="true"></span>
<main id="contenido">

<section class="view home" id="v-inicio">
<canvas id="gl" aria-hidden="true"></canvas>

<div id="sky" aria-hidden="true"></div>
<section class="ch intro" id="c-hero"><div class="pin"><div class="hero-in">
<span class="sello"><i class="d s"></i><i class="d f"></i>Deja de suponer. Mide.</span>
<h1 class="focus"><span class="hz">Percepción,</span><br>comparada.</h1>
<p class="q3"><span>Qué miran.</span> <span>Qué asocian.</span> <span>Qué opinan.</span></p>
<p class="sub sm">De tu empaque, tu anuncio o tu sitio, medido con personas reales.</p>
<div class="cta"><a class="btn" href="#inicio" data-go="demo">Pedir una demostración</a><a class="alt" href="#inicio" data-go="espera">o únete a la lista de espera</a></div></div>
<div class="hintw"><a class="hint" href="#inicio" data-go="prueba"><i aria-hidden="true"></i>Desliza para enfocar o salta a probar</a></div>
<div class="mark" aria-hidden="true"><span class="word">{logo("h",64)}</span><span class="tagl">De lo difuso a lo nítido</span></div></div></section>

<section class="ch" id="c-mirada" data-shape="heat"><div class="pin"><div class="cx">
<span class="num">01</span><h2>¿Qué miran?</h2>
<div class="steps-tx"><p class="st">Un anuncio. Cincuenta y dos personas lo ven cinco segundos desde su casa, con la cámara de su equipo.</p><p class="st">Cada punto es un instante de mirada. Donde se juntan, está la atención.</p><p class="st">Y este es el orden: primero el titular, luego la botella. El precio, casi nadie.</p></div>
<span class="seal on-d"><i class="d s"></i>Medido con personas</span></div>
<div class="vis"><div class="ad" id="ad"><img src="img/anuncio.jpg" srcset="img/anuncio-700.jpg 700w, img/anuncio.jpg 1400w" sizes="(max-width: 820px) 100vw, 55vw" alt="Anuncio de ejemplo de agua mineral Brisa con un toque de limón" loading="lazy" width="1400" height="875">
<span class="heatcss" aria-hidden="true"></span><svg class="path" viewBox="0 0 160 100" aria-hidden="true"><polyline pathLength="1" points="41.6,36 131.2,50 27.2,71"/><g class="nodes"><g><circle cx="41.6" cy="36" r="5"/><text x="41.6" y="38">1</text></g><g><circle cx="131.2" cy="50" r="5"/><text x="131.2" y="52">2</text></g><g><circle cx="27.2" cy="71" r="5"/><text x="27.2" y="73">3</text></g></g></svg>
<span class="tag" style="left:26%;top:17%">Titular: 52 % lo vio primero</span><span class="tag" style="left:80%;top:6%">Producto: 24 %</span><span class="tag low" style="left:58.5%;top:91%">Precio: 5 %</span></div></div></div></section>

<section class="ch" id="c-asocia" data-shape="piles"><div class="pin"><div class="cx">
<span class="num">02</span><h2>¿Qué asocian?</h2>
<div class="steps-tx"><p class="st">Aparece una palabra. Hay que mandarla a un lado o al otro, lo más rápido posible.</p><p class="st">Lo que cuenta es el tiempo. Cuando una marca y una idea van juntas en la cabeza, la respuesta sale más rápido.</p><p class="st">Brisa se une con «natural» 178 milisegundos antes que su competidor.</p></div>
<span class="seal on-d"><i class="d s"></i>Medido con personas</span></div>
<div class="vis"><div class="iat"><div class="sides"><span class="side l"><b>BRISA</b><i>o natural</i></span><span class="side r"><b>CUMBRE</b><i>o artificial</i></span></div>
<div class="words" aria-hidden="true"><span data-d="-1">Fresca<i>540 ms</i></span><span data-d="-1">Pura<i>598 ms</i></span><span data-d="1">Química<i>702 ms</i></span><span data-d="-1">Limpia<i>611 ms</i></span><span data-d="1">Sintética<i>688 ms</i></span><span data-d="-1">Viva<i>633 ms</i></span></div>
<div class="hist" id="hist">{HIST}<span class="hl a" style="left:39%">Brisa + natural<b>612 ms</b></span><span class="hl b" style="left:61.25%">Cumbre + natural<b>790 ms</b></span></div>
<div class="res"><span class="dn" id="dnum">+0,58</span><span>asociación con Brisa, de moderada a fuerte</span></div></div></div></div></div></section>

<section class="ch" id="c-precio" data-shape="curves"><div class="pin"><div class="cx">
<span class="num">03</span><h2>¿Qué opinan?</h2>
<div class="steps-tx"><p class="st">Cuatro preguntas sobre el precio. Cada respuesta es un punto.</p><p class="st">Juntas dibujan cuatro curvas: desde «tan barato que dudaría» hasta «demasiado caro».</p><p class="st">Donde se cruzan está el rango en el que el precio no estorba: de $17,40 a $24,00.</p></div>
<span class="seal on-d"><i class="d s"></i>Medido con personas</span></div>
<div class="vis"><div class="plotbox"><div class="plot" id="plot"><span class="rng"></span>{PLOT}<span class="opt"><i></i><b>Óptimo: $20,10</b></span><span class="rg">Rango aceptable</span></div><div class="axis"><span>$10</span><span>$17,40</span><span>$24,00</span><span>$36</span></div><div class="leg"><span><i class="k1"></i>Tan barato que dudaría</span><span><i class="k2"></i>Barato</span><span><i class="k3"></i>Caro</span><span><i class="k4"></i>Demasiado caro</span></div></div></div></div></section>

<section class="ch sellos" id="c-sellos" data-shape="seals"><div class="pin"><div class="top"><span class="num">04</span><h2>Cada dato dice de dónde viene</h2><p class="sub">Un resultado medido con personas y una predicción de un modelo no valen lo mismo. Aquí nunca se confunden.</p></div>
<div class="trio"><div class="sl" id="sl-1"><span class="hole s"></span><b>Medido</b><span>Lo que personas reales miraron, respondieron o tardaron.</span></div><div class="sl" id="sl-2"><span class="hole f"></span><b>Estimado</b><span>Lo que predice la IA. Sirve para decidir rápido, no para afirmar.</span></div><div class="sl" id="sl-3"><span class="hole h"></span><b>Modelado</b><span>Lo que sale de una simulación, siempre con su nota de método.</span></div></div></div></section>

<div class="lite">
<section class="band prueba" id="prueba"><div class="hd"><span class="eyebrow">Veinte segundos</span><h2>Pruébalo tú</h2><p>Dos tareas en miniatura para sentir cómo se mide. Nada se guarda ni sale de esta página.</p></div>
<div class="demos"><div class="demo" id="demo-heat"><div class="dh"><b>Mira este anuncio</b><span>Mueve el cursor, el dedo o las flechas sobre él durante cinco segundos, como si fuera tu mirada.</span></div>
<div class="canvas-wrap" tabindex="0" role="application" aria-label="Área interactiva del anuncio para simular mirada con cursor o flechas"><img src="img/anuncio.jpg" srcset="img/anuncio-700.jpg 700w, img/anuncio.jpg 1400w" sizes="(max-width: 820px) 100vw, 45vw" alt="Anuncio de ejemplo de agua mineral Brisa" loading="lazy" width="1400" height="875"><canvas id="heat" aria-label="Mapa de calor de tu cursor"></canvas><button class="btn sm start" type="button" id="heat-go">Empezar</button></div>
<div class="pbar" aria-hidden="true"><i id="heat-bar"></i></div><p class="out" id="heat-out" role="status" aria-live="polite">Aquí aparece tu mapa.</p></div>
<div class="demo" id="demo-rt"><div class="dh"><b>Clasifica seis palabras</b><span>¿Natural o artificial? Lo más rápido que puedas. En teclado: E y I.</span></div>
<div class="rt"><span class="rt-word" id="rt-word" aria-live="polite">Lista</span><div class="rt-btns"><button type="button" class="btn ghost" id="rt-l" disabled><kbd>E</kbd>Natural</button><button type="button" class="btn ghost" id="rt-r" disabled><kbd>I</kbd>Artificial</button></div><button class="btn sm" type="button" id="rt-go">Empezar</button></div>
<div class="pbar" aria-hidden="true"><i id="rt-bar"></i></div><p class="out" id="rt-out" role="status" aria-live="polite">Aquí aparece tu tiempo.</p></div></div></section>

{TOOLSEC}

<section class="band aud2"><a class="aud-c" href="#universidades"><span class="eyebrow">Para universidades · Aesteros Campus</span><h3>Un laboratorio de neuromarketing que cabe en un salón</h3><p>Tus alumnos diseñan un estudio, lo aplican y leen sus resultados en el mismo semestre. Incluye piloto semestral sin costo.</p><span class="goto">Ver Aesteros para universidades</span></a>
<a class="aud-c alt" href="#empresas"><span class="eyebrow">Para empresas y agencias · Aesteros Pro</span><h3>Sabe cuál versión funciona antes de producirla</h3><p>Prueba un empaque, un anuncio o una página con personas reales en días, y llega a la junta con evidencia.</p><span class="goto">Ver soluciones para empresas y agencias</span></a></section>

<section class="band trust2" id="confianza"><div class="hd"><h2>Te decimos hasta dónde llega cada dato</h2><p>Tres cosas que puedes comprobar aquí mismo.</p></div>
<div class="tr3">
<article class="trc" data-rv><h3>Si el dato es débil, te avisamos antes de que lo presentes</h3>
<div class="trd"><div class="nbar" aria-hidden="true"><span class="zero"></span><span class="nband" id="n-band"></span><span class="ndot" id="n-dot"></span><em>0</em></div>
<label class="sld" for="n-in"><span>Personas</span><input type="range" id="n-in" min="8" max="120" step="1" value="14"><output id="n-val">14</output></label>
<p class="nout" id="n-out" aria-live="polite"></p></div>
<p class="trp">Mueve el número de personas. Con pocas, el margen de error toca el cero y la gráfica lo marca.</p></article>
<article class="trc" data-rv><h3>Cuando pregunten «¿y eso de dónde sale?», ya está contestado</h3>
<div class="trd"><div class="rchips" role="group" aria-label="Prueba"><button type="button" data-r="0" aria-pressed="true">Asociación implícita</button><button type="button" data-r="1" aria-pressed="false">Usabilidad</button><button type="button" data-r="2" aria-pressed="false">Rango de precio</button></div>
<div class="rcard" id="r-card" aria-live="polite"><em>Método</em><b id="r-a">Greenwald, Nosek y Banaji (2003)</b><span id="r-b">Algoritmo de puntuación mejorado.</span></div></div>
<p class="trp">Cada prueba sigue un procedimiento publicado, y su referencia va junto al resultado.</p></article>
<article class="trc" data-rv><h3>Invitas a tus alumnos o a tus clientes sin pedirles su imagen</h3>
<div class="trd cam" aria-hidden="true"><div class="dev"><span class="face"><i></i><i></i></span><small>Su equipo</small><em>El video se queda aquí</em></div><div class="wire"><i></i><i></i><i></i><i></i></div><div class="srv"><span class="pts"><i></i><i></i><i></i><i></i><i></i><i></i></span><small>Aesteros</small><em>Solo coordenadas y tiempos</em></div></div>
<p class="trp">De la cámara salen puntos, no video. Quien participa no da nombre ni correo.</p></article>
</div><a class="lnk" href="#metodo">Leer el método completo</a></section>


<section class="ba" id="antes"><div class="hd"><h2>De la corazonada a la evidencia</h2><p>Elige tu caso.</p></div><div class="ba-tabs" role="tablist" aria-label="Tu caso"><button type="button" role="tab" id="bt-u" aria-controls="bp-u" aria-selected="true">Universidad</button><button type="button" role="tab" id="bt-e" aria-controls="bp-e" aria-selected="false" tabindex="-1">Empresa</button><button type="button" role="tab" id="bt-a" aria-controls="bp-a" aria-selected="false" tabindex="-1">Agencia</button></div><div class="ba-p" role="tabpanel" id="bp-u" aria-labelledby="bt-u"><div class="ba-c hoy"><h3>Hoy</h3><ul><li>El neuromarketing se enseña con diapositivas y casos ajenos.</li><li>El equipo de laboratorio es caro y lo usa un grupo a la vez.</li><li>El alumno lee estudios; rara vez hace uno.</li></ul></div><div class="ba-c con"><h3>Con Aesteros</h3><ul><li>Cada alumno diseña y corre su propio estudio.</li><li>Basta la cámara de su computadora o de su teléfono.</li><li>Entrega un informe con datos reales en el mismo semestre.</li></ul></div></div><div class="ba-p" role="tabpanel" id="bp-e" aria-labelledby="bt-e" hidden><div class="ba-c hoy"><h3>Hoy</h3><ul><li>La versión ganadora la elige quien más insiste en la junta.</li><li>Te enteras de si funcionó cuando ya está impresa o al aire.</li><li>Investigar toma semanas y se deja para lo grande.</li></ul></div><div class="ba-c con"><h3>Con Aesteros</h3><ul><li>La eligen personas reales, antes de producir.</li><li>Sabes qué miran, qué asocian y cuánto pagarían.</li><li>Resultados en días, cada uno con su margen de error.</li></ul></div></div><div class="ba-p" role="tabpanel" id="bp-a" aria-labelledby="bt-a" hidden><div class="ba-c hoy"><h3>Hoy</h3><ul><li>Defiendes la idea con tu experiencia contra el gusto del cliente.</li><li>Los cambios llegan sin saber qué es lo que falla.</li><li>La investigación se subcontrata y llega tarde.</li></ul></div><div class="ba-c con"><h3>Con Aesteros</h3><ul><li>Llegas a la presentación con evidencia.</li><li>Muestras dónde cae la mirada y qué se entiende.</li><li>La prueba cabe en el calendario del proyecto.</li></ul></div></div></section>
<section class="askw" id="demo"><div class="ask"><div class="ask-l"><span class="eyebrow">Míralo con tu propio caso</span><h2>¿Qué quieres saber?</h2>
<div class="chips" role="group" aria-label="Preguntas de ejemplo"><button type="button" class="chip">¿Mi empaque se entiende en cinco segundos?</button><button type="button" class="chip">¿Cuál de mis dos anuncios funciona mejor?</button><button type="button" class="chip">¿Mi marca se asocia con lo que quiero?</button><button type="button" class="chip">¿Cuánto pagarían por esto?</button><button type="button" class="chip">¿En qué paso se van de mi sitio?</button><button type="button" class="chip">¿Cómo enseño neuromarketing sin laboratorio?</button></div>
<div class="stage" aria-live="polite"><span class="sdot" aria-hidden="true"></span><p class="sq foc" id="sq">Elige una pregunta o escribe la tuya.</p></div>
<p class="note" id="espera">En media hora te la respondemos con la plataforma y un ejemplo de tu área. ¿Prefieres esperar al lanzamiento? Marca «Solo avísenme».</p></div>
<form class="form" id="f-demo" novalidate><label for="f-preg">Lo que quiero saber<input id="f-preg" name="pregunta" placeholder="Escribe tu pregunta" autocomplete="off"></label><label for="f-nombre">Nombre (requerido)<input id="f-nombre" name="nombre" autocomplete="name" required></label><label for="f-correo">Correo de trabajo o institucional (requerido)<input id="f-correo" name="correo" type="email" autocomplete="email" required></label><label for="f-org">Universidad o empresa<input id="f-org" name="org" autocomplete="organization"></label>
<fieldset><legend>Vengo por</legend><label class="rad"><input type="radio" name="tipo" id="f-t1" value="u" checked>Una universidad</label><label class="rad"><input type="radio" name="tipo" id="f-t2" value="e">Una empresa o agencia</label></fieldset>
<label class="rad"><input type="checkbox" id="f-espera" name="espera">Solo avísenme cuando abra el registro y de cada herramienta nueva</label>
<button class="btn" type="submit">Pedir una demostración</button><p class="msg" id="f-msg" role="status" aria-live="polite"></p></form></div></section>

</div>
</section>

{PROD}
{MET}
{VIEWS2}
</main>
<footer class="foot"><span class="brand">{logo("f",20)}</span><span>Percepción, comparada.</span><span class="flk"><a href="#privacidad">Privacidad</a><a href="#terminos">Términos</a><a href="#camara">Uso de cámara</a></span><span class="fine">Aesteros® 2026, Derechos reservados</span></footer>
<script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.5/gsap.min.js" integrity="sha512-7eHRwcbYkK4d9g/6tD/mhkf++eoTHwpNM9woBxtPUBWm67zeAfFC+HrdoE2GanKeocly/VxeLvIqwvCdk7qScg==" crossorigin="anonymous" referrerpolicy="no-referrer"></script><script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.5/ScrollTrigger.min.js" integrity="sha512-onMTRKJBKz8M1TnqqDuGBlowlH0ohFzMXYRNebz+yOcc5TQr/zAKsthzhuv0hiyUKEiQEQXEynnXCvNTOk50dg==" crossorigin="anonymous" referrerpolicy="no-referrer"></script><script src="js/aesteros.js?v={JS_H}"></script>
</body>
</html>'''

def seo_head(r):
    v,p,u,t,d = r['v'],r['p'],r['u'],r['t'],r['d']
    is_art = p.startswith('/blog/')
    og_type = 'article' if is_art else 'website'
    rob = 'noindex, nofollow' if v=='entrar' else 'index, follow, max-image-preview:large, max-snippet:-1'
    graph = [
        {
            "@type": "Organization",
            "@id": f"{SITE_URL}/#organization",
            "name": "Aesteros",
            "url": SITE_URL,
            "slogan": "Percepción, comparada.",
            "description": "Plataforma de investigación de percepción y neuromarketing en línea con personas reales.",
            "logo": f"{SITE_URL}/logo/png/aesteros-icono-claro-1024.png"
        },
        {
            "@type": "WebSite",
            "@id": f"{SITE_URL}/#website",
            "url": SITE_URL,
            "name": "Aesteros",
            "inLanguage": "es-MX",
            "publisher": {"@id": f"{SITE_URL}/#organization"}
        },
        {
            "@type": "Article" if is_art else "WebPage",
            "@id": f"{u}#webpage",
            "url": u,
            "name": t,
            "headline": t,
            "description": d,
            "inLanguage": "es-MX",
            "isPartOf": {"@id": f"{SITE_URL}/#website"},
            "publisher": {"@id": f"{SITE_URL}/#organization"},
            "image": OG_IMG
        }
    ]
    if v in ('inicio','producto','planes'):
        graph.append({
            "@type": "SoftwareApplication",
            "name": "Aesteros",
            "applicationCategory": "BusinessApplication",
            "operatingSystem": "Web",
            "inLanguage": "es-MX",
            "description": d,
            "url": SITE_URL,
            "publisher": {"@id": f"{SITE_URL}/#organization"}
        })
    ld = json.dumps({"@context": "https://schema.org", "@graph": graph}, ensure_ascii=False)
    return f'''<title>{t}</title>
<meta name="description" content="{d}">
<meta name="robots" content="{rob}">
<link rel="canonical" href="{u}">
<meta name="theme-color" content="#0B0907" media="(prefers-color-scheme: dark)">
<meta name="theme-color" content="#FFF7E6" media="(prefers-color-scheme: light)">
<link rel="icon" type="image/png" sizes="32x32" href="/logo/png/aesteros-favicon-claro-32.png">
<link rel="icon" type="image/png" sizes="16x16" href="/logo/png/aesteros-favicon-claro-16.png">
<link rel="icon" type="image/png" sizes="32x32" href="/logo/png/aesteros-favicon-oscuro-32.png" media="(prefers-color-scheme: dark)">
<link rel="apple-touch-icon" sizes="180x180" href="/logo/png/aesteros-icono-claro-1024.png">
<link rel="manifest" href="/site.webmanifest">
<meta property="og:type" content="{og_type}">
<meta property="og:site_name" content="Aesteros">
<meta property="og:locale" content="es_MX">
<meta property="og:title" content="{t}">
<meta property="og:description" content="{d}">
<meta property="og:url" content="{u}">
<meta property="og:image" content="{OG_IMG}">
<meta property="og:image:width" content="1702">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="Aesteros: Percepción, comparada. De lo difuso a lo nítido.">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{t}">
<meta name="twitter:description" content="{d}">
<meta name="twitter:image" content="{OG_IMG}">
<script type="application/ld+json">{ld}</script>'''

def render_for_view(base_html, r):
    v = r['v']
    mode = 'main' if v in ('inicio','producto','metodo') else 'mas'
    h = base_html.replace('<html lang="es" data-view="inicio" data-mode="main">', f'<html lang="es" data-view="{v}" data-mode="{mode}">', 1)
    h = h.replace('<!--__SEO_HEAD__-->', seo_head(r), 1)
    if v != 'inicio':
        h = h.replace('<section class="view home" id="v-inicio">', '<section class="view home" id="v-inicio" hidden>', 1)
        h = re.sub(rf'(<section class="view [^"]*" id="v-{re.escape(v)}"[^>]*?) hidden>', r'\1>', h, count=1)
    return h

for r in ROWS:
    page_html = render_for_view(html, r)
    rel = r['p'].lstrip('/')
    for base_dir in (ROOT_DIR, os.path.join(ROOT_DIR,'sitio')):
        out_p = os.path.join(base_dir, rel, 'index.html') if rel else os.path.join(base_dir, 'index.html')
        os.makedirs(os.path.dirname(out_p), exist_ok=True)
        open(out_p, 'w').write(page_html)

# Sitemap.xml
def _prio(p):
    if p=='/': return ('weekly','1.0')
    if p in ('/producto','/metodo','/planes','/universidades','/agencias','/empresas'): return ('weekly','0.9')
    if p in ('/blog','/ayuda','/novedades','/glosario'): return ('weekly','0.8')
    if p.startswith('/blog/') or p.startswith('/ayuda/'): return ('monthly','0.7')
    return ('yearly','0.4')

smap_items=[]
for r in ROWS:
    if r['v']=='entrar': continue
    cf,pr=_prio(r['p'])
    smap_items.append(f'  <url>\n    <loc>{r["u"]}</loc>\n    <lastmod>2026-11-19</lastmod>\n    <changefreq>{cf}</changefreq>\n    <priority>{pr}</priority>\n  </url>')
SMAP='<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'+'\n'.join(smap_items)+'\n</urlset>\n'

ROBOTS=f'''User-agent: *
Allow: /
Disallow: /entrar

Sitemap: {SITE_URL}/sitemap.xml
'''

LLMS_TXT=f'''# Aesteros

> Percepción, comparada. De lo difuso a lo nítido.
> Aesteros es una plataforma de investigación de percepción y neuromarketing en línea que mide qué miran, qué asocian y qué opinan personas reales sobre un empaque, un anuncio, un video o un sitio web, usando la cámara de su computadora o teléfono. Cada dato lleva su sello de evidencia (Medido, Estimado o Modelado) y su margen de error.

## Tres sellos de evidencia
- **Medido (punto sólido):** Viene de lo que personas reales miraron, respondieron o tardaron. Incluye cuántas sesiones válidas entraron y cuántas se excluyeron por calidad.
- **Estimado (punto difuso):** Viene de un modelo de inteligencia artificial. Sirve para descartar versiones rápido, nunca se mezcla con lo medido.
- **Modelado (punto hueco):** Viene de una simulación estructurada a partir de una rúbrica publicada, siempre con su nota de método.

## Nueve herramientas en un mismo núcleo
1. **Seguimiento ocular (Medido):** Mapa de atención, recorrido de la mirada e indicadores por área de interés con cámara web o teléfono.
2. **Video con lectura del rostro (Medido):** Atención segundo a segundo y movimientos faciales observables (sonrisa, ceño, sorpresa).
3. **Análisis visual con IA (Estimado):** Estimación de atención en cinco capas antes de salir a campo.
4. **Asociación implícita (Medido):** Tiempo de respuesta (Greenwald, Nosek y Banaji, 2003) con intervalo de confianza por dimensión.
5. **Variantes implícitas (Medido):** Categoría única (Karpinski y Steinman, 2006), responder o esperar (Nosek y Banaji, 2001) y primado evaluativo (Fazio, 1995).
6. **Encuestas y precio (Medido):** Escalas validadas de usabilidad (Brooke, 1996), recomendación (Reichheld, 2003), emoción (Bradley y Lang, 1994) y modelos de precio Van Westendorp (1976) y Gabor-Granger (1966).
7. **Recorrido web (Modelado):** Índice de Fricción Digital por sitio y por tarea frente a la competencia.
8. **Auditoría SEO (Medido):** Qué impide que los buscadores lean bien un sitio, hallazgos por severidad y plan de acción.
9. **Baterías e informe (Estimado):** Varias pruebas en una sola liga y un informe que cruza lo declarado con lo asociado.

## Ediciones
- **Aesteros Campus (Universidades):** Investigación real desde el aula. Licencia por programa académico y periodo, con roles de docente y alumno, plantillas y capacitación de FRSKO.
- **Aesteros Pro (Agencias y equipos de investigación):** Antes de elegir, compara. Baterías integradas, informes con tu propia marca y co-marca.
- **Aesteros Lite (Negocios pequeños):** ¿Cuál de los dos? Pregúntale a la percepción. Autoservicio con plantillas (en lista de espera).

## Mapa de páginas públicas
''' + '\n'.join(f'- [{r["t"]}]({r["u"]}): {r["d"]}' for r in ROWS if r['v']!='entrar') + '\n'

MANIFEST=json.dumps({
    "name": "Aesteros",
    "short_name": "Aesteros",
    "description": META_MAP['inicio']['d'],
    "start_url": "/",
    "display": "standalone",
    "background_color": "#0B0907",
    "theme_color": "#0B0907",
    "lang": "es-MX",
    "icons": [
        {"src": "/logo/png/aesteros-favicon-claro-32.png", "sizes": "32x32", "type": "image/png"},
        {"src": "/logo/png/aesteros-favicon-claro-64.png", "sizes": "64x64", "type": "image/png"},
        {"src": "/logo/png/aesteros-icono-claro-1024.png", "sizes": "1024x1024", "type": "image/png", "purpose": "any maskable"}
    ]
}, ensure_ascii=False, indent=2)+'\n'

for base_dir in (ROOT_DIR, os.path.join(ROOT_DIR,'sitio')):
    open(os.path.join(base_dir,'sitemap.xml'),'w').write(SMAP)
    open(os.path.join(base_dir,'robots.txt'),'w').write(ROBOTS)
    open(os.path.join(base_dir,'llms.txt'),'w').write(LLMS_TXT)
    open(os.path.join(base_dir,'llm.txt'),'w').write(LLMS_TXT)
    open(os.path.join(base_dir,'site.webmanifest'),'w').write(MANIFEST)

home_out = open(os.path.join(ROOT_DIR,'index.html')).read()
print(len(home_out)//1024,'KB',home_out.count('—')+home_out.count('–'),f'{len(ROWS)} routes built')

