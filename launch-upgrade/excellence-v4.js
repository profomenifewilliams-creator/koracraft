/* KoraCraft Studio Edition 04: account and door entrance */
(function(){
'use strict';
var doc=document,body=doc.body;if(!body)return;
var page=doc.querySelector('[data-kc-storefront]');if(!page)return;
var reduced=window.matchMedia&&window.matchMedia('(prefers-reduced-motion: reduce)').matches;
var shopName=page.getAttribute('data-storefront-name')||'Maker Store';
var overlay=doc.createElement('div');overlay.className='kc-store-door-overlay';overlay.setAttribute('role','dialog');overlay.setAttribute('aria-modal','true');overlay.setAttribute('aria-label','Opening '+shopName);
overlay.innerHTML='<button type="button" class="kc-door-skip">Skip intro ↗</button><div class="kc-door-stage" aria-hidden="true"><div class="kc-door-arch"></div><div class="kc-door-top-label"><span class="kc-door-brand">KORACRAFT · MAKER STORE</span><span class="kc-door-flowers">✳</span><span class="kc-door-shop-name"></span></div><div class="kc-door-leaf kc-door-left"><span class="kc-door-inlay"></span><span class="kc-door-knob"></span></div><div class="kc-door-leaf kc-door-right"><span class="kc-door-inlay"></span><span class="kc-door-knob"></span></div><div class="kc-door-sill"></div><div class="kc-door-overlay-caption">A PLACE MADE BY HANDS · OPENING YOUR STORE</div></div>';
overlay.querySelector('.kc-door-shop-name').textContent=shopName;doc.body.appendChild(overlay);body.classList.add('kc-store-entry-active');
var finished=false;function finish(){if(finished)return;finished=true;overlay.classList.add('is-leaving');body.classList.remove('kc-store-entry-active');window.setTimeout(function(){if(overlay.parentNode)overlay.parentNode.removeChild(overlay);},reduced?0:520);}
overlay.querySelector('.kc-door-skip').addEventListener('click',finish);
if(reduced){finish();return;}window.setTimeout(function(){overlay.classList.add('is-opening');},180);window.setTimeout(finish,1850);
})();
