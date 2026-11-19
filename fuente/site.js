(function(){
var V=[].map.call(document.querySelectorAll('main > .view'),function(e){return e.id.slice(2)}),MAIN=['inicio','producto','metodo'];
var META=window.__AE_META__||{},P2V=window.__AE_P2V__||{};
function setMeta(name){
  var m=META[name]||META.inicio;if(!m)return;
  document.title=m.t;
  var d=document.querySelector('meta[name="description"]');if(d)d.setAttribute('content',m.d);
  var ogt=document.querySelector('meta[property="og:title"]');if(ogt)ogt.setAttribute('content',m.t);
  var ogd=document.querySelector('meta[property="og:description"]');if(ogd)ogd.setAttribute('content',m.d);
  var ogu=document.querySelector('meta[property="og:url"]');if(ogu)ogu.setAttribute('content',m.u);
  var twt=document.querySelector('meta[name="twitter:title"]');if(twt)twt.setAttribute('content',m.t);
  var twd=document.querySelector('meta[name="twitter:description"]');if(twd)twd.setAttribute('content',m.d);
  var can=document.querySelector('link[rel="canonical"]');if(can)can.setAttribute('href',m.u);
  var rob=document.querySelector('meta[name="robots"]');if(rob)rob.setAttribute('content',name==='entrar'?'noindex, nofollow':'index, follow');
}
function show(name,target){
  if(V.indexOf(name)<0)name='inicio';
  V.forEach(function(v){document.getElementById('v-'+v).hidden=v!==name});
  document.documentElement.dataset.view=name;document.documentElement.dataset.mode=MAIN.indexOf(name)<0?'mas':'main';var cur=document.getElementById('v-'+name).dataset.nav||name;setMeta(name);if(window.AE&&AE.view)AE.view(name);
  document.querySelectorAll('.dock nav a').forEach(function(a){if(a.dataset.v===cur)a.setAttribute('aria-current','page');else a.removeAttribute('aria-current')});
  var el=target&&document.getElementById(target);
  if(el){if(el.tagName==='DETAILS')el.open=true;el.scrollIntoView({block:'start',behavior:'instant'});var f=el.querySelector('input');if(target==='espera'){var c=document.getElementById('f-espera');if(c){c.checked=true;c.dispatchEvent(new Event('change'))}}}
  else window.scrollTo({top:0,behavior:'instant'});
}
function curView(){
  var h=(location.hash||'').slice(1);
  if(h&&V.indexOf(h)>=0)return h;
  var p=(location.pathname||'/').replace(/\/index\.html$/,'').replace(/\/+$/,'')||'/';
  if(P2V[p])return P2V[p];
  return h||'inicio';
}
function route(){show(curView())}
document.addEventListener('click',function(e){var a=e.target.closest('a[data-go],a[href^="#"]');if(!a)return;var hr=a.getAttribute('href')||'';if(hr.charAt(0)!=='#')return;var name=hr.slice(1);if(V.indexOf(name)<0)return;e.preventDefault();var m=META[name];if(m&&m.p&&location.protocol!=='file:'){if(location.pathname!==m.p||location.hash){history.pushState({v:name},'',m.p)}}else if(location.hash!=='#'+name){history.pushState({v:name},'','#'+name)}show(name,a.dataset.go);window.dispatchEvent(new Event('hashchange'))});
window.addEventListener('hashchange',route);window.addEventListener('popstate',route);route();
var f=document.getElementById('f-demo');
[document.getElementById('f-nombre'),document.getElementById('f-correo')].forEach(function(el){if(!el)return;el.addEventListener('input',function(){el.removeAttribute('aria-invalid');var m=document.getElementById('f-msg');if(m)m.textContent=''})});
f.addEventListener('submit',function(e){e.preventDefault();var m=document.getElementById('f-msg'),n=document.getElementById('f-nombre'),c=document.getElementById('f-correo');
  if(!n.value.trim()){n.setAttribute('aria-invalid','true');m.textContent='Falta tu nombre.';n.focus();return}
  if(!/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(c.value)){c.setAttribute('aria-invalid','true');m.textContent='Revisa el correo: falta algo, como la arroba o el dominio.';c.focus();return}
  m.textContent='Esto es una maqueta: el formulario todavía no envía nada. Tus datos no salieron de esta página.'});
})();

