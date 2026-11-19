"""Ilustraciones de Aesteros: sólo puntos (sólido, difuso, hueco), cápsulas, medios puntos y líneas de puntos."""
import math,random,re
STOPS=[(0,'#FFA200',1),(.25,'#FFA800',.996),(.375,'#FFAB00',.906),(.5,'#FFAE00',.714),(.625,'#FFB000',.47),(.75,'#FFB000',.233),(.875,'#FFB000',.062),(1,'#FFB000',0)]
class Il:
    def __init__(s,w=240,h=180): s.w,s.h,s.e,s.n=w,h,[],0
    def _a(s,x,cls=''):
        s.e.append(x.replace('<%','<').replace('%%',f' class="{cls}" style="--i:{s.n}"')); s.n+=1; return s
    def S(s,x,y,r,o=1): return s._a(f'<circle%% cx="{x:.1f}" cy="{y:.1f}" r="{r:.1f}" fill="currentColor"'+(f' opacity="{o}"' if o<1 else '')+'/>','so')
    def D(s,x,y,r,o=1): return s._a(f'<circle%% cx="{x:.1f}" cy="{y:.1f}" r="{r*1.42:.1f}" fill="url(#GID)"'+(f' opacity="{o}"' if o<1 else '')+'/>','df')
    def H(s,x,y,r,sw=3,dot=False,o=1): return s._a(f'<circle%% cx="{x:.1f}" cy="{y:.1f}" r="{r:.1f}" fill="none" stroke="currentColor" stroke-width="{sw}"'+(f' stroke-dasharray="0.1 {sw*2.1:.1f}" stroke-linecap="round"' if dot else '')+(f' opacity="{o}"' if o<1 else '')+'/>','ho')
    def cap(s,x1,y1,x2,y2,w=8,o=1,dot=False): return s._a(f'<line%% x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="currentColor" stroke-width="{w}" stroke-linecap="round"'+(f' stroke-dasharray="0.1 {w*2.4:.1f}"' if dot else '')+(f' opacity="{o}"' if o<1 else '')+'/>','ca')
    def half(s,x,by,w,hollow=False,sw=3): 
        d=f'M{x-w:.1f} {by:.1f}A{w:.1f} {w:.1f} 0 0 1 {x+w:.1f} {by:.1f}'
        return s._a(f'<path%% d="{d}Z" fill="currentColor"/>' if not hollow else f'<path%% d="{d}" fill="none" stroke="currentColor" stroke-width="{sw}" stroke-linecap="round"/>','hf')
    def rect(s,x,y,w,h,rx,sw=4): return s._a(f'<rect%% x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="none" stroke="currentColor" stroke-width="{sw}"/>','ho')
    def person(s,x,y,r,hollow=False):
        w=r*1.75; by=y+r*1.45+w
        if hollow: s.H(x,y,r-1.5,3); s.half(x,by,w-1.5,True,3)
        else: s.S(x,y,r); s.half(x,by,w)
        return s
    def svg(s,uid,ink=None,cls='ilsvg'):
        g=''.join(f'<stop offset="{o}" stop-color="{c}"'+(f' stop-opacity="{a}"' if a<1 else '')+'/>' for o,c,a in STOPS)
        body=''.join(s.e).replace('GID','g'+uid)
        st=f' style="color:{ink}"' if ink else ''
        return f'<svg class="{cls}" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {s.w} {s.h}"{st}><defs><radialGradient id="g{uid}">{g}</radialGradient></defs>{body}</svg>'
def comparar():
    i=Il()
    for gx,dif in ((76,False),(164,True)):
        for a in range(3):
            for b in range(3):
                x,y=gx+(a-1)*24,90+(b-1)*24
                if dif and a==1 and b==1: i.D(x,y,10)
                else: i.S(x,y,7)
    return i
def atencion():
    i=Il(); fx,fy=152,84
    for a in range(9):
        for b in range(6):
            x,y=32+a*22,35+b*22; d=math.hypot(x-fx,y-fy)
            if d<14: continue
            if d<64: i.S(x,y,2.4+6.2*math.exp(-(d/44)**2))
            else: i.H(x,y,2.6,1.5,o=.75)
    return i.D(fx,fy,15)
def muestra():
    i=Il(); sel={(1,1),(4,0),(6,2),(2,3),(5,4)}
    for a in range(8):
        for b in range(5):
            x,y=36+a*24,42+b*24
            i.D(x,y,7.5) if (a,b) in sel else i.S(x,y,6)
    return i
def asociacion():
    i=Il(); i.S(46,90,17); i.H(194,90,15.5,3)
    for k in range(6): i.S(78+k*14,90,1.8+k*.9,o=.35+.13*k)
    return i.D(166,90,8.5)
def encuesta():
    i=Il()
    for r,(y,pick) in enumerate(((52,3),(90,1),(128,4))):
        for k in range(5):
            x=64+k*28
            if k==pick: i.D(x,y,9) if r==1 else i.S(x,y,8)
            else: i.H(x,y,7,2.5)
    return i
def ocular():
    i=Il()
    i._a('<path%% d="M44 90Q120 22 196 90Q120 158 44 90Z" fill="none" stroke="currentColor" stroke-width="5" stroke-linejoin="round"/>','ho')
    i.S(120,90,24); i.D(133,78,8)
    return i
def vistazo():
    i=Il(); P=[(48,124,5,'h'),(92,60,10,'s'),(138,108,5.5,'s'),(180,56,14,'d'),(206,130,4,'s')]
    d='M'+' L'.join(f'{x} {y}' for x,y,_,_ in P)
    i._a(f'<path%% d="{d}" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linejoin="round" opacity=".45"/>','ca')
    for x,y,r,k in P: {'h':lambda:i.H(x,y,r,2.5),'s':lambda:i.S(x,y,r),'d':lambda:i.D(x,y,r)}[k]()
    return i
def seo():
    i=Il(); i.rect(46,30,148,30,15,3.5); i.S(64,45,5)
    for k,(y,l) in enumerate(((84,96),(110,120),(136,70))):
        i.D(58,y,7.5) if k==0 else i.H(58,y,5.5,2.5)
        i.cap(78,y,78+l,y,8,o=1 if k==0 else .55)
    return i
def informe():
    i=Il()
    for k,(y,l) in enumerate(((48,112),(78,84),(108,98),(138,58))):
        i.D(56,y,8.5) if k==0 else i.S(56,y,5.5)
        i.cap(80,y,80+l,y,9,o=1 if k==0 else .5)
    return i
def margen():
    i=Il()
    for x,h in ((42,9),(94,14),(146,20),(198,27)): i.D(x,90,h,.9); i.S(x,90,7)
    return i
def nitido():
    i=Il()
    for k in range(5):
        x=38+k*41
        if k<4: i.D(x,90,17-3.4*k,1-.12*k)
        if k>0: i.S(x,90,2+3*k)
    return i
def vacio():
    i=Il()
    for x in (70,120,170): i.H(x,104,16,3,dot=True)
    return i.D(120,52,9)
def sinres():
    i=Il(); i.H(106,82,34,6); i.cap(133,109,160,136,9)
    for x in (92,106,120): i.S(x,82,3.2)
    return i
def error():
    i=Il()
    for k,x in enumerate((60,100,140,180)):
        if k==2: i.H(x,76,10,2.5,dot=True); i.D(x,124,11)
        else: i.S(x,76,11)
    return i
def sinconexion():
    i=Il(); i.cap(34,90,90,90,3)
    for x in (34,62,90): i.S(x,90,8)
    for x in (161,167,189,195): i.S(x,90,1.5,o=.7)
    for x in (150,178,206): i.H(x,90,7,2.5)
    return i.D(120,90,5.5)
def encampo():
    i=Il()
    for k in range(5):
        x=48+k*36
        i.person(x,86,9,hollow=k not in(0,))
        if k in (1,3): i.D(x,52,6.5)
    return i
def listo():
    i=Il(); i.H(118,92,42,6); i.cap(99,93,113,107,8); i.cap(113,107,139,77,8)
    return i.D(164,48,9)
def participante():
    i=Il(); i.person(60,74,13,hollow=True); i.rect(128,42,86,62,11,4); i.cap(171,104,171,122,4); i.cap(152,124,190,124,4)
    for k in range(5): i.S(82+k*12,74,1.9,o=.8)
    return i.D(170,73,10)
def equipo():
    i=Il(); i.person(84,86,11); i.person(156,86,11); i.person(120,92,13)
    return i.D(120,42,9)
def privacidad():
    i=Il(); i.H(112,92,58,3,dot=True); i.person(112,78,13,hollow=True)
    return i.D(196,44,7)
def portada1():
    i=Il(480,270); i.D(404,236,150); i.H(92,74,44,2); i.S(92,74,17)
    return i
def portada2():
    i=Il(480,270)
    for x,r,o in ((62,66,.3),(166,50,.48),(256,35,.68),(332,23,.9)): i.D(x,92,r,o)
    return i.S(404,92,15)
def portada3():
    i=Il(480,270); rnd=random.Random(5)
    for k in range(24):
        x,y,r=rnd.uniform(10,470),rnd.uniform(10,260),rnd.uniform(9,44)
        if k%5==4: i.H(x,y,r*.7,1.5,o=.35)
        else: i.D(x,y,r,rnd.uniform(.14,.5))
    return i.S(350,84,11)
SETS=[('herramientas','Herramientas','Una por prueba. Sirven de portada de cada estudio y de marca en el menú.',[
 ('asociacion','Asociación implícita',asociacion,'Un concepto conocido, uno por decidir, y la respuesta que se acerca cada vez más rápido.'),
 ('encuesta','Encuesta',encuesta,'Escalas de respuesta. Lo declarado es sólido; el promedio que resulta es difuso.'),
 ('ocular','Seguimiento ocular',ocular,'Un ojo hecho con un punto. El reflejo es lo que está mirando.'),
 ('atencion','Análisis visual con IA',atencion,'La atención se concentra alrededor de un punto. El centro es una estimación, por eso es difuso.'),
 ('vistazo','Primer vistazo',vistazo,'El recorrido de la mirada. Cada punto es una pausa; el más grande es donde se quedó.'),
 ('seo','Auditoría SEO',seo,'Una búsqueda y sus resultados. El primero es el que importa.'),
 ('informe','Informe',informe,'Una conclusión arriba y sus pruebas debajo.')]),
 ('conceptos','Conceptos','Para explicar el método en presentaciones, ayuda y capacitación.',[
 ('comparar','Comparar',comparar,'Dos grupos iguales salvo por una cosa. La diferencia es lo que se percibe.'),
 ('muestra','Muestra',muestra,'Entre todas las personas posibles, las que participaron.'),
 ('margen','Margen de error',margen,'El mismo dato con poca o mucha duda alrededor.'),
 ('nitido','De difuso a nítido',nitido,'La idea de la marca en cinco pasos: la duda se achica y el dato crece.')]),
 ('estados','Estados de la plataforma','Lo que se ve cuando no hay datos, algo falla o algo termina.',[
 ('vacio','Sin estudios todavía',vacio,'Tres lugares por llenar y una idea esperando.'),
 ('sinres','Sin resultados',sinres,'Una lupa que no encontró nada.'),
 ('error','Algo falló',error,'Un punto se salió de su lugar. Queda marcado dónde debería estar.'),
 ('sinconexion','Sin conexión',sinconexion,'La línea se corta y lo que sigue queda pendiente.'),
 ('encampo','Estudio en campo',encampo,'Participantes en fila. Quien investiga va en sólido, quienes responden ahora llevan luz.'),
 ('listo','Estudio listo',listo,'Una marca de terminado y un resultado nuevo.'),
 ('participante','Participante',participante,'Una persona frente a un estímulo. Sus datos son suyos, por eso va en contorno.'),
 ('equipo','Equipo',equipo,'Tres personas y una misma pregunta.'),
 ('privacidad','Privacidad',privacidad,'Lo de la persona queda dentro del círculo. Lo estimado se queda fuera.')])]
COVERS=[('portada-informe','Portada de informe',portada1,'Un resplandor grande que entra por la esquina y un punto nítido con su órbita.'),
 ('portada-capitulo','Portada de capítulo',portada2,'Profundidad de campo: de muy desenfocado a nítido.'),
 ('portada-evento','Fondo para eventos',portada3,'Luces fuera de foco y un solo punto en foco.')]

def _path(i,d,sw=6,o=1): return i._a(f'<path%% d="{d}" fill="none" stroke="currentColor" stroke-width="{sw}" stroke-linecap="round" stroke-linejoin="round"'+(f' opacity="{o}"' if o<1 else '')+'/>','ho')
def tiny(i,x1,y1,x2,y2,n,r=1.8,o=.8):
    for k in range(n): t=(k+.5)/n; i.S(x1+(x2-x1)*t,y1+(y2-y1)*t,r,o)
    return i
# primeros pasos
def paso1():
    i=Il(); _path(i,'M98 70A22 22 0 1 1 120 92L120 104',7); i.S(120,124,5.5); return i.D(166,52,8.5)
def paso2():
    i=Il()
    for k,x in enumerate((48,96,144,192)):
        if k==2: i.H(x,96,21,2,o=.6); i.S(x,96,14); i.D(x,54,5.5)
        else: i.H(x,96,13,3)
    return i
def paso3():
    i=Il(); i.person(58,80,12)
    for x,y in ((176,40),(194,90),(176,140)): tiny(i,84,90,x-16,y+4,5); i.person(x,y-6,7.5,hollow=True)
    return i.D(218,82,5)
def paso4():
    i=Il(); i.rect(68,28,104,124,13,4); i.D(94,58,9); i.cap(114,58,150,58,7)
    for y,x2 in ((88,150),(108,136),(128,146)): i.cap(90,y,x2,y,6,o=.5)
    return i
# pagos y planes
def plan1():
    i=Il(); i.H(120,90,40,2.5,o=.7); i.S(120,90,20); return i.D(120+40*.707,90-40*.707,6.5)
def plan2():
    i=Il()
    for r,o in ((36,.8),(54,.55),(72,.32)): i.H(120,90,r,2.5,o=o)
    i.S(120,90,20); i.S(120-36,90,4); i.S(120+54*.5,90+54*.866,4)
    return i.D(120+72*.766,90-72*.643,7.5)
def plan3():
    i=Il()
    for k in range(6):
        x=36+k*23
        i.D(x,90,8.5) if k==5 else i.S(x,90,7)
    i.cap(172,62,172,118,5)
    for x in (192,214): i.H(x,90,6.5,2.5,dot=True)
    return i
def plan4():
    i=Il(); i.rect(52,54,124,82,13,4); i.cap(54,80,174,80,9); i.S(76,112,5); i.H(148,112,8,2.5,dot=True)
    return i.D(198,42,8.5)
# participante
def part1():
    i=Il(); i.person(64,80,12); i.person(176,80,12,hollow=True); tiny(i,86,74,108,74,3); return i.D(124,72,9.5)
def part2():
    i=Il(); i.rect(48,30,144,98,13,4); i.S(120,30,4.5); i.cap(120,128,120,146,4); i.cap(98,148,142,148,4)
    for x,y in ((68,50),(172,50),(68,108),(172,108)): i.H(x,y,5,2.5)
    return i.D(120,79,10)
def part3():
    i=Il(); i.H(116,92,46,4); i.cap(104,72,104,112,13); i.cap(128,72,128,112,13); return i.D(170,46,7)
def part4():
    i=Il(); i.person(84,84,13,hollow=True); tiny(i,112,84,172,56,5); return i.D(186,50,11)
# módulos
def mod1():
    i=Il()
    for a,x in enumerate((56,128)):
        for b,y in enumerate((30,94)):
            i.rect(x,y,56,56,11,3.5); i.D(x+28,y+28,9) if (a,b)==(1,0) else i.S(x+28,y+28,5)
    return i
def mod2():
    i=Il(); i.cap(76,90,104,90,3); i.cap(136,90,164,90,3); i.S(58,90,16); i.H(120,90,14.5,3); return i.D(182,90,13)
def mod3():
    i=Il(); i.cap(98,36,142,36,4,o=.35); i.cap(88,48,152,48,4,o=.6); i.rect(70,60,100,74,11,4); i.S(96,84,7); return i.D(142,104,10)
def mod4():
    i=Il()
    for a in range(4):
        for b in range(3):
            x,y=66+a*36,36+b*46; sel=(a,b) in((1,0),(2,2)); i.person(x,y,6.5,hollow=not sel)
            if (a,b)==(2,2): i.D(x,y-16,4.5)
    return i
def mod5():
    i=Il(); i.rect(40,44,68,92,12,4); i.rect(132,44,68,92,12,4); i.S(74,90,13); tiny(i,112,90,128,90,2,1.6); return i.D(166,90,14)
def mod6():
    i=Il(); i.S(62,90,14)
    for k,(x,y) in enumerate(((178,44),(194,90),(178,136))):
        tiny(i,82,90+(y-90)*.12,x-14,y-(y-90)*.1,5)
        i.D(x,y,8.5) if k==1 else i.H(x,y,8,2.5)
    return i
SETS+=[('modulos','Módulos','Las secciones de la plataforma. Van en el menú, en las pantallas de inicio de cada sección y en la ayuda.',[
 ('mod-estudios','Estudios',mod1,'Cada tarjeta es un estudio. Uno ya tiene resultado.'),
 ('mod-baterias','Baterías',mod2,'Varias pruebas encadenadas: hecha, pendiente y la que da el resultado.'),
 ('mod-estimulos','Biblioteca de estímulos',mod3,'Imágenes apiladas. Lo que se va a mostrar.'),
 ('mod-participantes','Participantes',mod4,'El panel completo y quienes ya respondieron.'),
 ('mod-comparacion','Comparación',mod5,'Dos versiones lado a lado. Una se percibe distinta.'),
 ('mod-compartir','Exportar y compartir',mod6,'Un resultado que sale hacia varias personas.')]),
 ('pasos','Primeros pasos','El recorrido de bienvenida, en cuatro pantallas.',[
 ('paso-pregunta','Plantea tu pregunta',paso1,'Todo estudio empieza con una duda.'),
 ('paso-prueba','Elige la prueba',paso2,'Varias opciones y una que encaja.'),
 ('paso-invita','Invita participantes',paso3,'De quien investiga hacia quienes responden.'),
 ('paso-informe','Lee el informe',paso4,'Una página con la conclusión arriba.')]),
 ('planes','Pagos y planes','El mismo dibujo crece con el plan. Los avisos de cobro no asustan.',[
 ('plan-gratuito','Plan gratuito',plan1,'Un punto con una sola órbita.'),
 ('plan-pago','Plan de pago',plan2,'El mismo punto con más alcance.'),
 ('plan-limite','Límite alcanzado',plan3,'Llegaste al tope. Lo que sigue queda del otro lado.'),
 ('plan-rechazado','Pago rechazado',plan4,'El pago no entró. Queda marcado dónde falta.')]),
 ('participante','Lado del participante','Lo que ve quien responde un estudio. Van solas, sin datos ni cifras, para no influir.',[
 ('part-bienvenida','Bienvenida',part1,'Alguien te invita a mirar algo.'),
 ('part-calibracion','Calibración de cámara',part2,'Mira el punto del centro; las esquinas vienen después.'),
 ('part-pausa','Pausa',part3,'El estudio espera. Nada se pierde.'),
 ('part-gracias','Gracias',part4,'Lo que diste ya va en camino.')])]
# módulos y herramientas que llegaron con la interfaz (2.6)
def video_facial():
    i=Il(); i.rect(64,22,112,74,14,4); i.person(120,46,10,True)
    for k,x in enumerate(range(52,196,16)):
        if k==5: i.D(x,134,12)
        else: i.S(x,134,2.6+(1.6 if k in (4,6) else 0),o=.55 if k not in (4,6) else .9)
    return i
def recorrido_web():
    i=Il(); i.rect(40,26,160,128,16,4); i.cap(58,48,182,48,3,o=.4)
    i.H(66,76,6,2.5); tiny(i,74,80,112,104,4); i.S(120,108,6.5); tiny(i,128,112,160,130,3)
    return i.D(170,134,9)
def variantes():
    i=Il(); i.S(54,90,17)
    tiny(i,78,82,150,54,5,1.8,.6); tiny(i,80,90,150,90,5,1.8,.6); tiny(i,78,98,150,126,5,1.8,.6)
    i.H(172,48,11,3); i.D(174,90,10); i.H(172,132,11,3,True)
    return i
def precio():
    i=Il(); i.cap(44,150,196,150,3,o=.4)
    for k in range(7):
        x=58+k*21; i.S(x,44+k*14,3.2,o=.8); i.H(x,128-k*14,3.4,2)
    return i.D(121,86,11)
def calibracion():
    i=Il()
    for r in range(3):
        for c in range(3):
            x,y=70+c*50,40+r*50; n=r*3+c
            if n<4: i.S(x,y,7)
            elif n==4: i.D(x,y,13)
            else: i.H(x,y,7,2.5)
    return i
def calculadora():
    i=Il(); i.cap(40,152,200,152,3,o=.4)
    for c,(x,n,r) in enumerate(((66,2,15),(120,4,10),(174,6,5.5))):
        for k in range(n): i.S(x,138-k*13,4.6)
        i.D(x,138-n*13-r*1.4-4,r)
    return i
def alumnos():
    i=Il(); i.person(64,58,15)
    for k,(x,y) in enumerate(((122,70),(156,62),(190,70),(139,112),(173,112))): i.person(x,y,8,True)
    return i.D(98,36,7)
def proyectos():
    i=Il()
    _path(i,'M76 44V42a14 14 0 0 1 14-14H182a14 14 0 0 1 14 14V98a14 14 0 0 1-14 14H180',3,.35)
    _path(i,'M60 60V58a14 14 0 0 1 14-14H166a14 14 0 0 1 14 14V114a14 14 0 0 1-14 14H164',3,.6)
    i.rect(44,60,120,84,14,4); i.S(70,88,6); i.H(96,88,6,2.5); i.cap(62,118,120,118,7,o=.55)
    return i.D(140,96,10)
_h=SETS[0][3]; _v=[x for x in _h if x[0]=='vistazo'][0]; _h.remove(_v)
_h+=[('video-facial','Video con codificación facial',video_facial,'Una persona mira un video. Abajo, el tiempo; el punto con luz es el momento que más movió.'),
 ('recorrido-web','Recorrido web',recorrido_web,'Una página y el camino que alguien siguió en ella, de la entrada al clic que importa.'),
 ('variantes','Variantes implícitas',variantes,'Una sola marca y tres maneras de medir con qué se asocia.'),
 ('precio','Encuestas de precio',precio,'Dos curvas que se cruzan. El precio aceptable está donde se encuentran.'),
 ('calibracion','Laboratorio de calibración',calibracion,'Nueve puntos: cuatro listos, uno midiéndose y cuatro por venir.')]
SETS[1][3].append(('vistazo','Primer vistazo',vistazo,'El recorrido de la mirada. Es una vista dentro de seguimiento ocular y análisis visual, no una herramienta aparte.'))
[g for g in SETS if g[0]=='modulos'][0][3].extend([('mod-proyectos','Proyectos',proyectos,'Carpetas apiladas. Cada proyecto guarda sus estudios y su resultado.'),
 ('mod-calculadora','Calculadora de muestra',calculadora,'Con más personas, menos duda: la mancha se achica.'),
 ('mod-alumnos','Alumnos',alumnos,'Quien enseña va en sólido; el grupo, en contorno.')])
