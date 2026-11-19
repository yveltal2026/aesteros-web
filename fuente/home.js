
(function(){
var AE=window.AE={};
var root=document.documentElement,$=function(s,c){return (c||document).querySelector(s)},$$=function(s,c){return Array.prototype.slice.call((c||document).querySelectorAll(s))};
var reduce=matchMedia('(prefers-reduced-motion: reduce)').matches;
var canAnim=!reduce&&window.gsap&&window.ScrollTrigger;
var finePtr=matchMedia('(hover:hover) and (pointer:fine)').matches;
function small(){return innerWidth<=820}
function clamp(x){return x<0?0:x>1?1:x}
function ease(x){x=clamp(x);return x*x*(3-2*x)}
var CH=['c-hero','c-mirada','c-asocia','c-precio','c-sellos'].map(function(i){return document.getElementById(i)});
var P=[0,0,0,0,0],PR=[0,0,0,0,0],view='inicio',S={s:0,f:0,light:0,chap:0};
function prog(el){var r=el.getBoundingClientRect(),t=r.height-innerHeight;return t>0?clamp(-r.top/t):0}

/* ---------- pruebas en miniatura (funcionan con o sin movimiento) ---------- */
(function(){
  var wrap=$('#demo-heat .canvas-wrap'),cv=$('#heat'),go=$('#heat-go'),bar=$('#heat-bar'),out=$('#heat-out');
  var W=64,H=40,g=cv.getContext('2d'),I,run=false,px=-1,py=-1,t0,last,aoi;
  var A=[['el titular',.04,.2,.45,.57],['el producto',.72,.07,.93,.93],['el botón',.04,.63,.32,.8],['el precio',.52,.62,.66,.85],['el logotipo',.04,.04,.18,.15]];
  cv.width=W;cv.height=H;
  function paint(){var im=g.createImageData(W,H),d=im.data,m=.3,i;for(i=0;i<I.length;i++)if(I[i]>m)m=I[i];
    for(i=0;i<I.length;i++){var n=Math.min(1,I[i]/m),k=Math.min(1,n*1.6);d[i*4]=20+235*k;d[i*4+1]=17+159*k;d[i*4+2]=12-12*k;d[i*4+3]=255*(.64-.5*n)}
    g.putImageData(im,0,0)}
  function move(e){var r=wrap.getBoundingClientRect();px=(e.clientX-r.left)/r.width;py=(e.clientY-r.top)/r.height}
  function tick(now){if(!run)return;var dt=Math.min(.05,(now-last)/1000);last=now;var el=(now-t0)/5000;
    if(px>=0&&px<=1&&py>=0&&py<=1){var cx=px*W,cy=py*H,x,y;for(y=Math.max(0,cy-7|0);y<Math.min(H,cy+8);y++)for(x=Math.max(0,cx-7|0);x<Math.min(W,cx+8);x++){var q=((x+.5-cx)*(x+.5-cx)+(y+.5-cy)*(y+.5-cy))/14;I[y*W+x]+=dt*Math.exp(-q)}
      aoi.t+=dt;A.forEach(function(a,k){if(px>=a[1]&&px<=a[3]&&py>=a[2]&&py<=a[4])aoi.v[k]+=dt})}
    paint();bar.style.width=Math.min(100,el*100)+'%';
    if(el>=1)return end();requestAnimationFrame(tick)}
  function end(){run=false;wrap.classList.remove('run');go.textContent='Repetir';go.hidden=false;
    if(aoi.t<.4){out.textContent='No detectamos movimiento sobre el anuncio. Inténtalo otra vez.';return}
    var o=A.map(function(a,k){return [a[0],Math.round(aoi.v[k]/aoi.t*100)]}).sort(function(a,b){return b[1]-a[1]});
    var tx=o[0][1]>0?'Tu cursor pasó más tiempo en <b>'+o[0][0]+' ('+o[0][1]+' %)</b>'+(o[1][1]>0?' y en '+o[1][0]+' ('+o[1][1]+' %)':'')+'.':'Tu cursor casi no tocó las áreas del anuncio.';
    out.innerHTML=tx+' En el estudio de ejemplo, la mirada de 52 personas fue primero al titular. Aquí seguimos tu cursor; en un estudio real, la cámara estima la mirada.';AE.blip&&AE.blip('ok')}
  go.addEventListener('click',function(){I=new Float32Array(W*H);aoi={t:0,v:[0,0,0,0,0]};px=.5;py=.5;run=true;go.hidden=true;wrap.classList.add('run');wrap.focus();out.textContent='Mueve el cursor, el dedo o las flechas sobre el anuncio…';t0=last=performance.now();requestAnimationFrame(tick)});
  wrap.addEventListener('pointermove',move);wrap.addEventListener('pointerdown',move);
  wrap.addEventListener('keydown',function(e){if(!run)return;var s=.06;if(e.key==='ArrowLeft'){e.preventDefault();px=Math.max(0,px-s)}else if(e.key==='ArrowRight'){e.preventDefault();px=Math.min(1,px+s)}else if(e.key==='ArrowUp'){e.preventDefault();py=Math.max(0,py-s)}else if(e.key==='ArrowDown'){e.preventDefault();py=Math.min(1,py+s)}});
})();
(function(){
  var word=$('#rt-word'),L=$('#rt-l'),R=$('#rt-r'),go=$('#rt-go'),bar=$('#rt-bar'),out=$('#rt-out');
  var base=[['Fresca',0],['Pura',0],['Química',1],['Limpia',0],['Sintética',1],['Viva',0]],q,i,t0,rts,err,on=false,wait=false;
  function next(){if(i>=q.length)return end();wait=true;word.className='rt-word';word.textContent='+';
    setTimeout(function(){if(!on)return;word.textContent=q[i][0];wait=false;t0=performance.now()},520+Math.random()*380)}
  function ans(side){if(!on||wait)return;var rt=performance.now()-t0;wait=true;
    if(side===q[i][1]){rts.push(rt);i++;bar.style.width=(i/q.length*100)+'%';next()}
    else{err++;word.className='rt-word bad';word.textContent='×';i++;bar.style.width=(i/q.length*100)+'%';setTimeout(next,480)}}
  function end(){on=false;L.disabled=R.disabled=true;go.hidden=false;go.textContent='Repetir';word.className='rt-word';word.textContent='Listo';
    if(!rts.length){out.textContent='Ninguna respuesta correcta esta vez. Inténtalo otra vez.';return}
    var m=Math.round(rts.reduce(function(a,b){return a+b},0)/rts.length);
    out.innerHTML='Tu promedio: <b>'+m+' ms</b> en '+rts.length+' respuestas'+(err?', con '+err+(err>1?' errores':' error'):'')+'. Una prueba completa junta cientos de respuestas como estas, y de la diferencia entre tiempos sale la fuerza de la asociación.';AE.blip&&AE.blip('ok')}
  go.addEventListener('click',function(){q=base.slice().sort(function(){return Math.random()-.5});i=0;rts=[];err=0;on=true;go.hidden=true;L.disabled=R.disabled=false;bar.style.width='0';out.textContent='Responde lo más rápido que puedas.';next()});
  L.addEventListener('click',function(){ans(0)});R.addEventListener('click',function(){ans(1)});
  document.addEventListener('keydown',function(e){if(!on||e.metaKey||e.ctrlKey||e.altKey)return;var k=e.key.toLowerCase();if(k==='e'){e.preventDefault();ans(0)}else if(k==='i'){e.preventDefault();ans(1)}});
})();

/* ---------- sonido opcional: lo borroso suena filtrado y se abre al enfocar ---------- */
(function(){
  var b=$('#snd'),lab=$('span',b),ctx,filt,master,buf={},ready=false,on=false,BASE=(document.querySelector('base')||{}).href||'';
  function load(n){return fetch(BASE+'snd/'+n+'.mp3').then(function(r){if(!r.ok)throw 0;return r.arrayBuffer()}).then(function(a){return new Promise(function(ok,no){ctx.decodeAudioData(a,ok,no)})}).then(function(d){buf[n]=d})}
  function play(n,g){if(!on||!buf[n])return;var s=ctx.createBufferSource(),v=ctx.createGain();s.buffer=buf[n];v.gain.value=g||.5;s.connect(v);v.connect(master);s.start()}
  AE.blip=function(n){play(n,.45)};
  AE.tone=function(f){if(on&&filt)filt.frequency.setTargetAtTime(750*Math.pow(24,clamp(f)),ctx.currentTime,.25)};
  function fail(){on=false;want=false;b.setAttribute('aria-pressed','false');b.disabled=true;lab.textContent='Sin sonido aquí';b.title='El sonido no está disponible en este visor'}
  var want=false,started=false;
  function mark(){b.setAttribute('aria-pressed',on?'true':'false')}
  function start(){
    if(!want)return;
    try{
      if(!ctx){var C=window.AudioContext||window.webkitAudioContext;ctx=new C();master=ctx.createGain();master.gain.value=.8;master.connect(ctx.destination);filt=ctx.createBiquadFilter();filt.type='lowpass';filt.frequency.value=900;filt.Q.value=.3;filt.connect(master)}
      var p=ctx.resume();if(p&&p.catch)p.catch(function(){});
      if(ctx.state!=='running'&&!started){setTimeout(function(){if(ctx.state==='running')go()},250)}else go();
    }catch(e){fail()}
  }
  function go(){on=want;mark();if(started)return;started=true;
    if(!ready){ready=true;Promise.all(['base','foco','sello','logo','ok','menu'].map(load)).then(function(){play('logo',.85);var s=ctx.createBufferSource(),v=ctx.createGain(),t0=ctx.currentTime+2.6;s.buffer=buf.base;s.loop=true;v.gain.setValueAtTime(0,ctx.currentTime);v.gain.setValueAtTime(0,t0);v.gain.linearRampToValueAtTime(.4,t0+3.5);s.connect(v);v.connect(filt);s.start(t0)}).catch(fail)}}
  mark();
  b.addEventListener('click',function(){
    want=!want;try{localStorage.setItem('ae-snd',want?'1':'0')}catch(e){}
    if(!want){on=false;mark();if(ctx)ctx.suspend();return}
    start();if(ctx&&started){on=true;mark();ctx.resume()}
  });
})();

/* ---------- cursor propio: un punto difuso sobre lo interactivo ---------- */
if(finePtr&&!reduce){(function(){
  var c=$('#cur'),x=0,y=0,tx=0,ty=0,sc=.22,ts=.22,op=0,seen=false;root.classList.add('hascur');
  addEventListener('pointermove',function(e){tx=e.clientX;ty=e.clientY;if(!seen){seen=true;x=tx;y=ty}op=1;ts=e.target.closest&&e.target.closest('a,button,input,label,.canvas-wrap')?1:.22},{passive:true});
  document.addEventListener('pointerleave',function(){op=0});
  (function loop(){x+=(tx-x)*.22;y+=(ty-y)*.22;sc+=(ts-sc)*.16;c.style.transform='translate3d('+x+'px,'+y+'px,0) scale('+sc+')';c.style.opacity=op*(sc>.5?.8:1);requestAnimationFrame(loop)})();
})()}


/* ---------- antes y después, y la pregunta que se enfoca ---------- */
(function(){
  var tabs=$$('.ba-tabs [role=tab]');
  function pick(t,f){tabs.forEach(function(x){var on=x===t;x.setAttribute('aria-selected',on?'true':'false');x.tabIndex=on?0:-1;var p=document.getElementById(x.getAttribute('aria-controls'));p.hidden=!on;if(on){p.classList.remove('go');void p.offsetWidth;p.classList.add('go')}});if(f)t.focus()}
  tabs.forEach(function(t,i){t.addEventListener('click',function(){pick(t)});t.addEventListener('keydown',function(e){if(e.key==='ArrowRight'||e.key==='ArrowLeft'){e.preventDefault();pick(tabs[(i+(e.key==='ArrowRight'?1:tabs.length-1))%tabs.length],true)}})});
  var sq=$('#sq'),st=$('.stage'),inp=$('#f-preg'),chips=$$('.ask .chip'),esp=$('#f-espera'),sbtn=$('#f-demo button[type="submit"]'),tm;
  function show(q,fromInput){if(!q)q='Elige una pregunta o escribe la tuya.';sq.textContent=q;sq.classList.remove('foc');st.classList.remove('foc');void sq.offsetWidth;clearTimeout(tm);tm=setTimeout(function(){sq.classList.add('foc');st.classList.add('foc')},fromInput?260:60)}
  chips.forEach(function(c){c.addEventListener('click',function(){chips.forEach(function(x){x.setAttribute('aria-pressed',x===c?'true':'false')});inp.value=c.textContent;show(c.textContent);AE.blip&&AE.blip('foco')})});
  inp.addEventListener('input',function(){chips.forEach(function(x){x.setAttribute('aria-pressed','false')});show(inp.value.trim(),true)});
  if(st&&inp){st.addEventListener('click',function(){inp.focus()})}
  function syncBtn(){if(sbtn&&esp)sbtn.textContent=esp.checked?'Unirme a la lista de espera':'Pedir una demostración'}
  if(esp){esp.addEventListener('change',syncBtn);syncBtn()}
  st.classList.add('foc');
})();

/* ---------- Producto y Método: función ---------- */
(function(){
  var pv=$('#v-producto');if(!pv)return;
  // revelados (sirven aunque la vista esté oculta al cargar)
  var rv=$$('[data-rv]');
  if('IntersectionObserver' in window&&!reduce){var io=new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting){e.target.classList.add('in');io.unobserve(e.target)}})},{rootMargin:'0px 0px -10% 0px',threshold:.08});rv.forEach(function(e){io.observe(e)})}else rv.forEach(function(e){e.classList.add('in')});
  // audiencia
  $$('.ausel button').forEach(function(b){b.addEventListener('click',function(){pv.dataset.au=b.dataset.set;$$('.ausel button').forEach(function(x){x.setAttribute('aria-pressed',x===b?'true':'false')})})});
  // riel de pasos
  var rb=$$('.rail button'),sp=$$('.sp');
  rb.forEach(function(b){b.addEventListener('click',function(){document.getElementById(b.dataset.to).scrollIntoView({behavior:reduce?'auto':'smooth',block:'start'})})});
  if('IntersectionObserver' in window){var so=new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting)rb.forEach(function(b){if(b.dataset.to===e.target.id)b.setAttribute('aria-current','step');else b.removeAttribute('aria-current')})})},{rootMargin:'-45% 0px -50% 0px'});sp.forEach(function(e){so.observe(e)})}
  // áreas de interés
  var AO=[['52 %','94 %','0,6 s','1,8 s'],['24 %','81 %','1,1 s','1,2 s'],['12 %','46 %','2,4 s','0,5 s'],['5 %','22 %','3,1 s','0,3 s']],dd=$$('#aoi-out dd'),ab=$$('.aoi');
  function aoi(b){ab.forEach(function(x){x.setAttribute('aria-pressed',x===b?'true':'false')});AO[+b.dataset.k].forEach(function(v,i){dd[i].textContent=v})}
  ab.forEach(function(b){b.addEventListener('click',function(){aoi(b)});b.addEventListener('pointerenter',function(e){if(e.pointerType==='mouse')aoi(b)});b.addEventListener('focus',function(){aoi(b)})});
  // grupos de la asociación
  var G=[[.58,.41,.75,52,'Todos'],[.81,.58,1.04,21,'Quienes ya compran Brisa'],[.42,.20,.64,31,'Quienes no la compran']],df=$('#d-fill'),db=$('#d-band'),dt=$('#d-dot'),dout=$('#d-out'),gb=$$('.grp button');
  function nx(v){return 30+v/1.2*70}function nf(v){return v.toFixed(2).replace('.',',')}
  function grp(k){var g=G[k];df.style.width=(nx(g[0])-30)+'%';db.style.left=(nx(g[1])-4)+'%';db.style.width=(nx(g[2])-nx(g[1])+8)+'%';dt.style.left=nx(g[0])+'%';
    dout.innerHTML='<b>+'+nf(g[0])+'</b>'+g[4]+': Brisa se asocia con «natural». Intervalo de '+nf(g[1])+' a '+nf(g[2])+', con '+g[3]+' personas.';gb.forEach(function(x,i){x.setAttribute('aria-pressed',i===k?'true':'false')})}
  gb.forEach(function(b,i){b.addEventListener('click',function(){grp(i)})});grp(0);
  // precio
  var pin=$('#pr-in'),pval=$('#pr-val'),pmk=$('#pr-mk'),pout=$('#pr-out');
  function lg(p,c,k){return 1/(1+Math.exp(-(p-c)/k))}function pc(x){return Math.round(x*100)+' %'}
  function price(){var p=+pin.value;pval.textContent='$'+p.toFixed(2).replace('.',',');pmk.style.left=((p-10)/26*100)+'%';
    var caro=lg(p,23,2.5),barato=1-lg(p,19,2.5),t=p<17.4?'Por debajo del rango: empieza a generar duda por barato.':p>24?'Por encima del rango: empieza a perder a quien lo ve caro.':'Dentro del rango aceptable.';
    pout.innerHTML='<b>'+t+'</b>Lo considera caro: '+pc(caro)+'. Lo considera barato: '+pc(barato)+'.'}
  pin.addEventListener('input',price);price();
  // arma tu estudio
  var Q={mira:[['Seguimiento ocular','con personas'],['Análisis visual con IA','para descartar versiones antes']],emo:[['Video con lectura del rostro','con personas']],asoc:[['Asociación implícita','con personas']],ab:[['Variantes implícitas','con personas'],['Seguimiento ocular','con personas']],precio:[['Encuestas y precio','con personas']],sitio:[['Recorrido web','simulación'],['Auditoría SEO','sin participantes']]},
      out=$('#arma-out'),qb=$$('.aq .chip');
  function arma(){var sel=qb.filter(function(b){return b.getAttribute('aria-pressed')==='true'}),seen={},L=[];
    sel.forEach(function(b){Q[b.dataset.q].forEach(function(t){if(!seen[t[0]]){seen[t[0]]=1;L.push(t)}})});
    if(!L.length){out.innerHTML='<p class="aempty">Tu estudio aparece aquí.</p>';return}
    var people=L.some(function(t){return t[1]==='con personas'});if(L.length>1)L.push(['Baterías e informe','todo en una liga y una sola lectura']);
    out.innerHTML='<h3>Tu estudio: '+(L.length>1?(L.length-1)+' herramientas y un informe':'1 herramienta')+'</h3><ul>'+L.map(function(t,i){return '<li style="animation-delay:'+(i*.12)+'s">'+t[0]+'<span>'+t[1]+'</span></li>'}).join('')+'</ul><p class="an2">'+(people?'Cuánta gente hace falta lo calcula la plataforma según el margen de error que aceptes. ':'')+'Cada resultado sale con su sello y su margen de error.</p><a class="btn" href="#inicio" data-go="demo" id="arma-go">Pedir una demostración con este estudio</a>';
    $('#arma-go').addEventListener('click',function(){var f=$('#f-preg'),tx='Quiero saber: '+sel.map(function(b){return b.textContent.toLowerCase()}).join(', ')+'.';if(f){f.value=tx;f.dispatchEvent(new Event('input',{bubbles:true}))}})}
  qb.forEach(function(b){b.addEventListener('click',function(){b.setAttribute('aria-pressed',b.getAttribute('aria-pressed')==='true'?'false':'true');arma();AE.blip&&AE.blip('foco')})});
  // acordeón: una abierta a la vez
  var ac=$$('.acc');ac.forEach(function(d){d.addEventListener('toggle',function(){if(d.open)ac.forEach(function(x){if(x!==d)x.open=false})})});
  // Método: tocar para leer lo difuso, y la línea del recorrido
  $$('.sn').forEach(function(c){c.addEventListener('click',function(){c.classList.toggle('open')})});
  var tl=$('#tl'),tf=$('#tl-fill');
  function tline(){if(!tl||!tl.offsetParent)return;var r=tl.getBoundingClientRect();tf.style.transform='scaleY('+clamp((innerHeight*.62-r.top)/r.height)+')'}
  addEventListener('scroll',tline,{passive:true});addEventListener('resize',tline);AE.tline=tline;
})();

/* ---------- menú: el punto difuso abre lo demás; páginas nuevas ---------- */
(function(){
  var mb=$('#more'),sh=$('#sheet');
  function set(o){sh.hidden=!o;mb.setAttribute('aria-expanded',o?'true':'false');if(o){sh.classList.remove('on');void sh.offsetWidth;sh.classList.add('on');AE.blip&&AE.blip('foco')}}
  mb.addEventListener('click',function(e){e.stopPropagation();set(sh.hidden)});
  document.addEventListener('click',function(e){if(!sh.hidden&&!e.target.closest('#sheet'))set(false);else if(e.target.closest('#sheet a'))set(false)});
  document.addEventListener('keydown',function(e){if(e.key==='Escape'&&!sh.hidden){set(false);mb.focus()}});
  var MAINV=['inicio','producto','metodo',''];
  function mark(){var v=((location.hash||'').slice(1))||root.dataset.view||'inicio';mb.classList.toggle('here',MAINV.indexOf(v)<0);var sec=document.getElementById('v-'+v);v=sec&&sec.dataset.nav||v;$$('#sheet a').forEach(function(a){if(a.getAttribute('href')==='#'+v)a.setAttribute('aria-current','page');else a.removeAttribute('aria-current')})}
  addEventListener('hashchange',function(){mark();if(!sh.hidden)set(false)});addEventListener('popstate',function(){mark();if(!sh.hidden)set(false)});mark();
  // informe con tu marca
  var rep=$('#rep');$$('.sw button').forEach(function(b){b.addEventListener('click',function(){$$('.sw button').forEach(function(x){x.setAttribute('aria-pressed',x===b?'true':'false')});rep.classList.remove('sw1','sw0');void rep.offsetWidth;rep.classList.add(b.dataset.b==='1'?'sw1':'sw0')})});
  // blog: filtro por línea
  var fb=$$('.bfil button'),ps=$$('.post');fb.forEach(function(b){b.addEventListener('click',function(){fb.forEach(function(x){x.setAttribute('aria-pressed',x===b?'true':'false')});ps.forEach(function(p){p.hidden=!!b.dataset.f&&p.dataset.l!==b.dataset.f})})});
  // ayuda: puertas y búsqueda
  var dr=$$('.doors [role=tab]'),hl=$$('.hlist'),hq=$('#h-q'),hn=$('#h-none');
  function door(t){dr.forEach(function(x){x.setAttribute('aria-selected',x===t?'true':'false')});hl.forEach(function(p){p.hidden=p.id!==t.getAttribute('aria-controls')});$$('.hi').forEach(function(a){a.hidden=false});hn.hidden=true}
  dr.forEach(function(t){t.addEventListener('click',function(){hq.value='';door(t)})});
  function norm(x){return x.toLowerCase().normalize('NFD').replace(/[̀-ͯ]/g,'')}
  hq.addEventListener('input',function(){var q=norm(hq.value.trim());if(!q){door(dr.filter(function(x){return x.getAttribute('aria-selected')==='true'})[0]||dr[0]);return}var n=0;hl.forEach(function(p){var any=false;$$('.hi',p).forEach(function(a){var ok=norm(a.textContent).indexOf(q)>=0;a.hidden=!ok;if(ok){any=true;n++}});p.hidden=!any});hn.hidden=n>0});
  $$('.hi.wip').forEach(function(a){a.addEventListener('click',function(e){e.preventDefault()})});
  // entrar: maqueta
  $('#f-ent').addEventListener('submit',function(e){e.preventDefault();$('#e-msg').textContent='Esto es una maqueta: todavía no abre la plataforma.'});
  $('#f-cod').addEventListener('submit',function(e){e.preventDefault();$('#e-msg').textContent='Esto es una maqueta: los códigos de grupo se activan con la plataforma.'});
})();

/* ---------- menú: la pastilla ámbar viaja entre secciones (420 ms, curva trasladar) ---------- */
(function(){
  var navs=$$('.dock nav'),last={};
  function place(anim){navs.forEach(function(n,k){var p=$('.pil',n),a=$('a[aria-current="page"]',n);
    if(!n.offsetParent){last[k]=null;return}
    if(!a){p.style.opacity=0;last[k]=null;return}
    var x=a.offsetLeft,w=a.offsetWidth,o=last[k];p.style.opacity=1;p.style.left=x+'px';p.style.width=w+'px';
    if(anim&&o&&!reduce&&p.animate&&(o[0]!==x||o[1]!==w)){var l=Math.min(o[0],x),r=Math.max(o[0]+o[1],x+w);
      p.animate([{left:o[0]+'px',width:o[1]+'px',filter:'blur(0px)'},{left:(l+(r-l)*.14)+'px',width:(r-l)*.72+'px',filter:'blur(3.5px)',offset:.5},{left:x+'px',width:w+'px',filter:'blur(0px)'}],{duration:420,easing:'cubic-bezier(.65,0,.35,1)'});AE.blip&&AE.blip('menu')}
    last[k]=[x,w];if(n.scrollWidth>n.clientWidth)n.scrollTo({left:x-n.clientWidth/2+w/2,behavior:anim?'smooth':'auto'})})}
  AE.pill=place;addEventListener('resize',function(){place(false)});
  if(document.fonts&&document.fonts.ready)document.fonts.ready.then(function(){place(false)});
  addEventListener('hashchange',function(){requestAnimationFrame(function(){place(true)})});
  document.addEventListener('click',function(e){if(e.target.closest('a[href^="#"]'))requestAnimationFrame(function(){requestAnimationFrame(function(){place(true)})})});
  requestAnimationFrame(function(){place(false)});
})();

/* ---------- confianza: tres demostraciones ---------- */
(function(){
  var ni=$('#n-in');if(!ni)return;var nb=$('#n-band'),nd=$('#n-dot'),nv=$('#n-val'),no=$('#n-out'),E=.24,SD=.625;
  function nx(v){return 22+v/1*72}function f(v){return (v<0?'−':'+')+Math.abs(v).toFixed(2).replace('.',',')}
  function upd(){var n=+ni.value,h=1.96*SD/Math.sqrt(n),lo=E-h,hi=E+h,weak=lo<=0;nv.textContent=n;nd.style.left=nx(E)+'%';nb.style.left=Math.max(0,nx(lo)-3)+'%';nb.style.width=Math.min(100,nx(hi)+3)-Math.max(0,nx(lo)-3)+'%';
    nb.classList.toggle('weak',weak);no.className='nout'+(weak?' weak':'');no.innerHTML=weak?'<b>Aún no se puede afirmar.</b> Diferencia de '+f(E)+', de '+f(lo)+' a '+f(hi)+'. El margen cruza el cero.':'<b>Se sostiene.</b> Diferencia de '+f(E)+', de '+f(lo)+' a '+f(hi)+'.'}
  ni.addEventListener('input',upd);upd();
  var R=[['Greenwald, Nosek y Banaji (2003)','Algoritmo de puntuación mejorado.'],['Brooke (1996)','Escala de usabilidad de 10 frases.'],['Van Westendorp (1976)','Medidor de sensibilidad al precio.']],rc=$('#r-card'),ra=$('#r-a'),rb=$('#r-b'),bs=$$('.rchips button');
  bs.forEach(function(b){b.addEventListener('click',function(){bs.forEach(function(x){x.setAttribute('aria-pressed',x===b?'true':'false')});var r=R[+b.dataset.r];ra.textContent=r[0];rb.textContent=r[1];rc.classList.remove('go');void rc.offsetWidth;rc.classList.add('go')})});
})();
if(!canAnim){AE.view=function(){};return}
root.classList.add('anim');
gsap.registerPlugin(ScrollTrigger);
var mm=gsap.matchMedia();

/* ---------- capítulos fijos ---------- */
function chapter(el,build){var tl=gsap.timeline({defaults:{ease:'power2.out'},scrollTrigger:{trigger:el,start:'top top',end:'bottom bottom',scrub:1.1,invalidateOnRefresh:true}});build(tl,el);tl.set({},{},1);return tl}
function inOut(tl,els){tl.fromTo(els,{autoAlpha:0,y:28,filter:'blur(12px)'},{autoAlpha:1,y:0,filter:'blur(0px)',duration:.12,stagger:.02,ease:'power1.out'},0).to(els,{autoAlpha:0,y:-18,filter:'blur(8px)',duration:.07,ease:'power1.inOut'},.93)}
function steps(tl,el,at){$$('.st',el).forEach(function(s,k){tl.fromTo(s,{autoAlpha:0,y:16,filter:'blur(8px)'},{autoAlpha:1,y:0,filter:'blur(0px)',duration:.07,ease:'power1.out'},at[k]);if(k<at.length-1)tl.to(s,{autoAlpha:0,y:-14,filter:'blur(6px)',duration:.055,ease:'power1.inOut'},at[k+1]-.06)})}
chapter(CH[0],function(tl,el){
  tl.to($('.hintw',el),{autoAlpha:0,duration:.06},.02);tl.to($('.hero-in',el),{autoAlpha:0,y:-90,filter:'blur(16px)',duration:.3,ease:'power1.in'},.12)
    .fromTo($('.mark',el),{autoAlpha:0,scale:.92,filter:'blur(22px)'},{autoAlpha:1,scale:1,filter:'blur(0px)',duration:.24},.56)
    .to($('.mark',el),{autoAlpha:0,filter:'blur(14px)',duration:.1,ease:'power1.in'},.9)});
chapter(CH[1],function(tl,el){
  inOut(tl,[$('.cx',el),$('.vis',el)]);steps(tl,el,[.05,.36,.64]);
  tl.fromTo($('.heatcss',el),{opacity:0},{opacity:1,duration:.16},.3)
    .fromTo($('polyline',el),{strokeDashoffset:1},{strokeDashoffset:0,duration:.16,ease:'none'},.64);
  $$('.nodes g',el).forEach(function(g,k){tl.fromTo(g,{scale:0,transformOrigin:'50% 50%'},{scale:1,duration:.03,ease:'back.out(2)'},.64+k*.07)});
  $$('.tag',el).forEach(function(t,k){tl.fromTo(t,{autoAlpha:0,filter:'blur(8px)'},{autoAlpha:1,filter:'blur(0px)',duration:.04},.66+k*.07)})});
chapter(CH[2],function(tl,el){
  inOut(tl,[$('.cx',el),$('.vis',el)]);steps(tl,el,[.05,.38,.68]);
  var box=$('.iat',el);
  $$('.words span',el).forEach(function(w,k){var t=.12+k*.088,d=+w.dataset.d;
    tl.fromTo(w,{autoAlpha:0,scale:.82,x:0,filter:'blur(12px)'},{autoAlpha:1,scale:1,filter:'blur(0px)',duration:.04,ease:'power1.out'},t)
      .to(w,{x:function(){return d*box.clientWidth*.3},autoAlpha:0,scale:.72,filter:'blur(6px)',duration:.045,ease:'power1.inOut'},t+.045)
      .fromTo($(d<0?'.side.l':'.side.r',el),{scale:1},{scale:1.04,duration:.02,yoyo:true,repeat:1,transformOrigin:d<0?'0 50%':'100% 50%',ease:'sine.inOut'},t+.075)});
  tl.fromTo($$('.hl',el),{autoAlpha:0},{autoAlpha:1,duration:.05,stagger:.03},.36);
  var o={v:0},dn=$('#dnum');
  tl.fromTo($('.res',el),{autoAlpha:0,y:20,filter:'blur(10px)'},{autoAlpha:1,y:0,filter:'blur(0px)',duration:.06},.68)
    .fromTo(o,{v:0},{v:.58,duration:.1,ease:'power1.out',onUpdate:function(){dn.textContent='+'+o.v.toFixed(2).replace('.',',')}},.68)});
chapter(CH[3],function(tl,el){
  inOut(tl,[$('.cx',el),$('.vis',el)]);steps(tl,el,[.05,.36,.66]);
  tl.fromTo($('.plot svg',el),{clipPath:'inset(-10% 100% -10% 0%)'},{clipPath:'inset(-10% 0% -10% 0%)',duration:.2,ease:'none'},.34)
    .fromTo($('.leg',el),{autoAlpha:0},{autoAlpha:1,duration:.06},.34)
    .fromTo($('.rng',el),{scaleX:0,opacity:0},{scaleX:1,opacity:1,duration:.1},.66)
    .fromTo([$('.rg',el),$$('.axis span',el)[1],$$('.axis span',el)[2]],{autoAlpha:0},{autoAlpha:1,duration:.05},.7)
    .fromTo($('.opt',el),{autoAlpha:0,filter:'blur(8px)'},{autoAlpha:1,filter:'blur(0px)',duration:.06},.78)});
chapter(CH[4],function(tl,el){
  tl.fromTo($('.top',el),{autoAlpha:0,y:46,filter:'blur(18px)'},{autoAlpha:1,y:0,filter:'blur(0px)',duration:.12},0);
  $$('.sl',el).forEach(function(s,k){tl.fromTo(s,{autoAlpha:0,y:30,filter:'blur(12px)'},{autoAlpha:1,y:0,filter:'blur(0px)',duration:.1},.14+k*.1)})});

/* ---------- tramo claro: revelados y galería horizontal ---------- */
$$('.lite .hd,.lite .demo,.lite .aud-c,.lite .tri>div,.lite .ba-tabs,.lite .ask,.snp').forEach(function(el){
  gsap.from(el,{y:44,autoAlpha:0,filter:'blur(12px)',duration:.9,ease:'power3.out',clearProps:'filter,transform',scrollTrigger:{trigger:el,start:'top 90%',once:true}})});
$$('.tc').forEach(function(el,k){ScrollTrigger.create({trigger:el,start:'top 86%',once:true,onEnter:function(){setTimeout(function(){el.classList.add('in')},(k%3)*140)}})});
$$('.ba-p').forEach(function(p){ScrollTrigger.create({trigger:'#antes',start:'top 70%',once:true,onEnter:function(){p.classList.add('go')}})});
$$('.tgr h3,.proof').forEach(function(el){gsap.from(el,{y:30,autoAlpha:0,filter:'blur(10px)',duration:.9,ease:'power3.out',clearProps:'filter,transform',scrollTrigger:{trigger:el,start:'top 90%',once:true}})});

/* ---------- puntos en WebGL ---------- */
var GL=(function(){
  var cv=document.getElementById('gl'),gl;
  try{gl=cv.getContext('webgl',{alpha:true,premultipliedAlpha:true,antialias:false,powerPreference:'high-performance'})}catch(e){}
  if(!gl)return null;
  var N=small()?5000:((navigator.hardwareConcurrency||4)>4?15000:9000);
  var VS='precision mediump float;attribute vec3 aP;attribute vec3 aA;uniform vec2 uR;uniform float uF,uD,uG;varying float vG,vK;void main(){vec2 p=aP.xy/(uR*.5);p.y=-p.y;gl_Position=vec4(p,0.,1.);float d=1.+aP.z*.4;gl_PointSize=uD*aA.x*mix(11.,2.5,uF)*d;vG=aA.y*uG;vK=aA.z;}';
  var FS='precision mediump float;uniform float uF,uA,uL;varying float vG,vK;void main(){float r=length(gl_PointCoord-.5)*2.;float a=smoothstep(1.,mix(0.,.72,uF),r)*mix(.075,.74,uF*uF)*uA*(.55+.45*vK);vec3 c=mix(vec3(1.,.69,0.),vec3(.85,.576,.353),vG);c=mix(c,vec3(.93,.52,0.),uL);gl_FragColor=vec4(c*a,a);}';
  function sh(t,s){var o=gl.createShader(t);gl.shaderSource(o,s);gl.compileShader(o);return o}
  var pr=gl.createProgram();gl.attachShader(pr,sh(gl.VERTEX_SHADER,VS));gl.attachShader(pr,sh(gl.FRAGMENT_SHADER,FS));gl.linkProgram(pr);
  if(!gl.getProgramParameter(pr,gl.LINK_STATUS))return null;
  gl.useProgram(pr);
  var U={};['uR','uF','uD','uG','uA','uL'].forEach(function(n){U[n]=gl.getUniformLocation(pr,n)});
  var pos=new Float32Array(N*3),att=new Float32Array(N*3),rnd=new Float32Array(N),ph=new Float32Array(N),sp=new Float32Array(N),loc=new Float32Array(N*3),SH=[],i;
  function gs(){var u=0,v=0;while(!u)u=Math.random();v=Math.random();return Math.sqrt(-2*Math.log(u))*Math.cos(6.2832*v)}
  for(i=0;i<N;i++){att[i*3]=.6+Math.random()*.9;att[i*3+1]=i%5<3?0:1;att[i*3+2]=Math.random();rnd[i]=Math.random();ph[i]=Math.random()*6.2832;sp[i]=.4+Math.random()*1.1;loc[i*3]=gs();loc[i*3+1]=gs();loc[i*3+2]=gs()}
  var bp=gl.createBuffer(),ba=gl.createBuffer(),lp=gl.getAttribLocation(pr,'aP'),la=gl.getAttribLocation(pr,'aA');
  gl.bindBuffer(gl.ARRAY_BUFFER,ba);gl.bufferData(gl.ARRAY_BUFFER,att,gl.STATIC_DRAW);gl.enableVertexAttribArray(la);gl.vertexAttribPointer(la,3,gl.FLOAT,false,0,0);
  gl.bindBuffer(gl.ARRAY_BUFFER,bp);gl.bufferData(gl.ARRAY_BUFFER,pos,gl.DYNAMIC_DRAW);gl.enableVertexAttribArray(lp);gl.vertexAttribPointer(lp,3,gl.FLOAT,false,0,0);
  gl.enable(gl.BLEND);gl.blendFunc(gl.ONE,gl.ONE_MINUS_SRC_ALPHA);gl.clearColor(0,0,0,0);
  var W=0,H=0,dpr=1,FAR=1200,c0=[0,0],R0=100,mx=0,my=0,tmx=0,tmy=0;
  function box(el){var x=0,y=0,w=el.offsetWidth,h=el.offsetHeight,pin=el.closest('.pin');while(el&&el!==pin){x+=el.offsetLeft;y+=el.offsetTop;el=el.offsetParent}return {x:x-W/2,y:y-H/2,w:w,h:h}}
  var CURV=__CURV__,CK=['tb','bc','ca','dc'];
  function build(){
    W=innerWidth;H=innerHeight;dpr=Math.min(devicePixelRatio||1,small()?1.5:2);cv.width=W*dpr;cv.height=H*dpr;gl.viewport(0,0,cv.width,cv.height);
    FAR=Math.max(W,H)*.8;var sm=small(),m=Math.min(W,H),k,a,b,q,t,u,r,g;
    c0=sm?[0,-H*.24]:[W*.24,-H*.02];R0=m*(sm?.17:.2);
    for(k=0;k<6;k++)if(!SH[k])SH[k]=new Float32Array(N*3);
    var lg=box($('.mark .word')),ad=box($('#ad')),hi=box($('#hist')),pl=box($('#plot')),ho=$$('.hole').map(box);
    var cl=[[.235,.39,.1,.085,.5],[.82,.5,.035,.17,.25],[.175,.715,.06,.03,.12],[.1,.1,.04,.025,.07],[.585,.735,.03,.035,.06]];
    for(i=0;i<N;i++){a=i*3;
      // 1: el punto nítido
      r=Math.min(1,Math.abs(gs())*.42)*lg.w*.0592;t=Math.random()*6.2832;SH[1][a]=lg.x+lg.w*.1833+Math.cos(t)*r;SH[1][a+1]=lg.y+lg.h*.488+Math.sin(t)*r;SH[1][a+2]=(Math.random()-.5)*.3;
      // 2: instantes de mirada sobre el anuncio
      u=Math.random();q=0;for(k=0;k<cl.length;k++){q+=cl[k][4];if(u<q)break}k=Math.min(k,cl.length-1);
      SH[2][a]=ad.x+ad.w*Math.min(.985,Math.max(.015,cl[k][0]+gs()*cl[k][2]));SH[2][a+1]=ad.y+ad.h*Math.min(.98,Math.max(.02,cl[k][1]+gs()*cl[k][3]));SH[2][a+2]=(Math.random()-.5);
      // 3: dos distribuciones de tiempos de respuesta
      g=att[a+1];var mu=g?.6125:.39,sd=g?.1:.085,hh=g?.68:.9;t=gs();t=Math.max(-2.6,Math.min(2.6,t));b=Math.exp(-t*t/2);
      SH[3][a]=hi.x+hi.w*Math.min(1,Math.max(0,mu+t*sd));SH[3][a+1]=hi.y+hi.h-Math.random()*b*hh*hi.h;SH[3][a+2]=(Math.random()-.5)*.6;
      // 4: cuatro curvas de precio
      q=CURV[CK[i%4]];t=Math.random()*(q.length-1);k=t|0;u=t-k;
      SH[4][a]=pl.x+pl.w*(q[k][0]+(q[k+1][0]-q[k][0])*u)/1000+gs()*2.2;SH[4][a+1]=pl.y+pl.h*(q[k][1]+(q[k+1][1]-q[k][1])*u)/400+gs()*2.2;SH[4][a+2]=(Math.random()-.5)*.5;
      // 5: los tres sellos: disco, punto difuso, aro
      k=i%3;b=ho[k];r=b.w/2;t=Math.random()*6.2832;
      if(k===0)r*=Math.sqrt(Math.random());else if(k===1)r*=Math.min(1.5,Math.abs(gs())*.55);else r*=.86+Math.random()*.12;
      SH[5][a]=b.x+b.w/2+Math.cos(t)*r;SH[5][a+1]=b.y+b.h/2+Math.sin(t)*r;SH[5][a+2]=(Math.random()-.5)*.3;
    }
    gl.uniform2f(U.uR,W,H);gl.uniform1f(U.uD,dpr);
  }
  addEventListener('pointermove',function(e){tmx=e.clientX/innerWidth-.5;tmy=e.clientY/innerHeight-.5},{passive:true});
  var shown=true;
  function draw(time,s,f,alpha,light,it){
    if(alpha<=.002){if(shown){gl.clear(gl.COLOR_BUFFER_BIT);shown=false}return}shown=true;
    mx+=(tmx-mx)*.06;my+=(tmy-my)*.06;
    var si=Math.min(4,Math.floor(s)),fr=Math.min(1,s-si),A=SH[si],B=SH[si+1],T=time*.001,cs=Math.cos(T*.22),sn=Math.sin(T*.22),amp=3+10*(1-f),par=24,a,t,x,y,z,ax,ay,az,w,arc;
    for(var i=0;i<N;i++){a=i*3;
      if(si===0){x=loc[a];z=loc[a+2];ax=c0[0]+(x*cs-z*sn)*R0;ay=c0[1]+loc[a+1]*R0;az=(x*sn+z*cs)*.5;if(it<1){var q=it*1.75-.75*rnd[i];q=q<0?0:q>1?1:q;q=1-(1-q)*(1-q)*(1-q);var fr0=FAR*(.75+.6*sp[i]),sw2=(1-q)*1.4;ax=ax*q+(c0[0]+Math.cos(ph[i]+sw2)*fr0)*(1-q);ay=ay*q+(c0[1]+Math.sin(ph[i]+sw2)*fr0)*(1-q)}}else{ax=A[a];ay=A[a+1];az=A[a+2]}
      t=fr*1.7-.7*rnd[i];t=t<0?0:t>1?1:t;t=t*t*(3-2*t);arc=Math.sin(t*3.1416)*(24+50*rnd[i])*(si<2?1.6:1);
      w=T*sp[i]+ph[i];
      x=ax+(B[a]-ax)*t+Math.cos(ph[i])*arc+Math.sin(w)*amp;y=ay+(B[a+1]-ay)*t+Math.sin(ph[i])*arc+Math.cos(w*.9)*amp;z=az+(B[a+2]-az)*t;
      pos[a]=x+mx*z*par;pos[a+1]=y+my*z*par;pos[a+2]=z}
    gl.bindBuffer(gl.ARRAY_BUFFER,bp);gl.bufferSubData(gl.ARRAY_BUFFER,0,pos);
    gl.uniform1f(U.uF,f);gl.uniform1f(U.uA,alpha);gl.uniform1f(U.uL,light);gl.uniform1f(U.uG,Math.max(0,1-Math.abs(s-3)));
    gl.clear(gl.COLOR_BUFFER_BIT);gl.drawArrays(gl.POINTS,0,N);
  }
  return {build:build,draw:draw};
})();
if(GL)root.classList.add('gl');

/* ---------- un solo ciclo: lee el avance, pinta el cielo, mueve los puntos, abre el filtro ---------- */
var IT0=0,ITD=3400,intro=(root.dataset.view||'inicio')==='inicio'&&scrollY<40;if(intro)root.classList.add('wait');function endIntro(fast){if(!intro)return;intro=false;root.classList.remove('wait');root.classList.add('opened');if(fast)IT0=-1e9}
if(intro){['pointerdown','keydown','wheel','touchstart'].forEach(function(n){addEventListener(n,function(){endIntro(true)},{passive:true,once:true})});addEventListener('scroll',function(){if(scrollY>30)endIntro(true)},{passive:true})}
var sky=$('#sky'),sel=CH[4],holes=$$('.hole'),lastChap=-1,lastL=-1,built=false;
function mix(a,b,t){return Math.round(a+(b-a)*t)}
function frame(time){
  requestAnimationFrame(frame);
  if(view!=='inicio'||document.hidden)return;
  if(GL&&!built){GL.build();built=true}
  if(!IT0)IT0=time;var it=clamp((time-IT0)/ITD);if(intro&&it>.86)endIntro(false);if(!GL&&intro&&it>.3)endIntro(false);
  var dt=Math.min(.05,(time-(frame.t||time))/1000);frame.t=time;var kk=1-Math.exp(-dt*5.5);for(var i=0;i<5;i++){var raw=prog(CH[i]);PR[i]=raw;P[i]+=(raw-P[i])*(Math.abs(raw-P[i])>.6?1:kk)}
  AE.dbg={raw:PR.slice(),p:P.slice()};
  var s=ease(P[0]/.8)+ease(P[1]/.2)+ease(P[2]/.26)+ease(P[3]/.26)+ease(P[4]/.34),fr=s-Math.floor(s);
  var f=s<1?ease(s)*ease(s):1-(s<2?.82:.6)*Math.sin(Math.PI*Math.min(1,fr));if(s>=5)f=1;
  var L=ease((P[4]-.36)/.24),out=ease((P[4]-.82)/.14);
  if(L!==lastL){lastL=L;sky.style.backgroundColor='rgb('+mix(11,255,L)+','+mix(9,247,L)+','+mix(7,230,L)+')';
    var k=mix(255,20,L)+','+mix(247,17,L)+','+mix(230,12,L),ca=mix(255,122,L)+','+mix(176,62,L)+','+mix(0,18,L);sel.style.setProperty('--ink','rgb('+k+')');sel.style.setProperty('--mut','rgba('+k+',.72)');sel.style.setProperty('--amber','rgb('+ca+')')}
  if(GL){for(i=0;i<3;i++)holes[i].style.opacity=out;GL.draw(time,s,f*(it<1?1:1),(1-out)*(small()?.5+.5*clamp(s):1)*(1-.62*ease((P[1]-.6)/.06)*(1-ease((P[1]-.97)/.03)))*(1-.66*ease((P[3]-.5)/.08)*(1-ease((P[3]-.97)/.03))),L,it)}
  var chap=Math.min(5,Math.round(s));
  if(chap!==lastChap){if(lastChap>=0&&AE.blip)AE.blip(chap===5?'sello':'foco');lastChap=chap}
  if(AE.tone)AE.tone(f);
}
var rz;addEventListener('resize',function(){clearTimeout(rz);rz=setTimeout(function(){built=false},180)});
if(document.fonts&&document.fonts.ready)document.fonts.ready.then(function(){built=false;ScrollTrigger.refresh()});
addEventListener('load',function(){built=false;ScrollTrigger.refresh()});
AE.view=function(n){if(n===view&&lastChap>=-1&&AE.on)return;AE.on=1;view=n;if(AE.tline)setTimeout(AE.tline,60);if(n==='inicio'){built=false;lastL=-1;requestAnimationFrame(function(){ScrollTrigger.refresh()})}};
AE.view(root.dataset.view||'inicio');
requestAnimationFrame(frame);
})();
