(function(){
var V=[].map.call(document.querySelectorAll('main > .view'),function(e){return e.id.slice(2)}),MAIN=['inicio','producto','metodo'];
function show(name,target){
  if(V.indexOf(name)<0)name='inicio';
  V.forEach(function(v){document.getElementById('v-'+v).hidden=v!==name});
  document.documentElement.dataset.view=name;document.documentElement.dataset.mode=MAIN.indexOf(name)<0?'mas':'main';var cur=document.getElementById('v-'+name).dataset.nav||name;if(window.AE&&AE.view)AE.view(name);
  document.querySelectorAll('.dock nav a').forEach(function(a){if(a.dataset.v===cur)a.setAttribute('aria-current','page');else a.removeAttribute('aria-current')});
  var el=target&&document.getElementById(target);
  if(el){if(el.tagName==='DETAILS')el.open=true;el.scrollIntoView({block:'start',behavior:'instant'});var f=el.querySelector('input');if(target==='espera'){var c=document.getElementById('f-espera');if(c)c.checked=true}}
  else window.scrollTo({top:0,behavior:'instant'});
}
function route(){show((location.hash||'#inicio').slice(1))}
document.addEventListener('click',function(e){var a=e.target.closest('a[data-go]');if(!a)return;e.preventDefault();var name=a.getAttribute('href').slice(1);if(location.hash!=='#'+name){history.replaceState(null,'','#'+name)}show(name,a.dataset.go)});
window.addEventListener('hashchange',route);route();
var f=document.getElementById('f-demo');
f.addEventListener('submit',function(e){e.preventDefault();var m=document.getElementById('f-msg'),n=document.getElementById('f-nombre'),c=document.getElementById('f-correo');
  if(!n.value.trim()){m.textContent='Falta tu nombre.';n.focus();return}
  if(!/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(c.value)){m.textContent='Revisa el correo: falta algo, como la arroba o el dominio.';c.focus();return}
  m.textContent='Esto es una maqueta: el formulario todavía no envía nada. Tus datos no salieron de esta página.'});
})();
