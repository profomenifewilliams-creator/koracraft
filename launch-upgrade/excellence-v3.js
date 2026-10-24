/* KoraCraft Studio Edition 03: routed navigation, skeleton bubbles and card links */
(function(){
'use strict';
var doc=document,body=doc.body;
if(!body||body.dataset.excellenceVersion!=='3')return;
var reduced=window.matchMedia&&window.matchMedia('(prefers-reduced-motion: reduce)').matches;
var loader=doc.createElement('div');
loader.className='kc-route-loader';
loader.setAttribute('aria-hidden','true');
loader.innerHTML='<div class="kc-loader-content" role="status" aria-live="polite"><div class="kc-loader-logo"><span class="kc-loader-mark">K✳</span><span>KoraCraft<small>AFRICA\'S CREATIVE MARKET</small></span></div><div class="kc-loader-bubbles" aria-hidden="true"><i></i><i></i><i></i></div><div class="kc-loader-caption">WEAVING YOUR NEXT PAGE <span class="kc-load-dot"></span><span class="kc-load-dot"></span><span class="kc-load-dot"></span></div><div class="kc-skeleton-stack" aria-hidden="true"><div class="kc-skeleton-row"><span class="kc-skeleton-thumb"></span><span class="kc-skeleton-lines"><i class="kc-skeleton-line"></i><i class="kc-skeleton-line short"></i></span></div><div class="kc-skeleton-row"><span class="kc-skeleton-thumb"></span><span class="kc-skeleton-lines"><i class="kc-skeleton-line"></i><i class="kc-skeleton-line short"></i></span></div></div></div>';
doc.body.appendChild(loader);
function startLoader(){loader.classList.add('is-active');body.classList.add('kc-nav-loading');loader.setAttribute('aria-hidden','false');}
function navigate(url){startLoader();window.setTimeout(function(){window.location.assign(url);},reduced?0:110);}
window.addEventListener('pageshow',function(){loader.classList.remove('is-active');body.classList.remove('kc-nav-loading');loader.setAttribute('aria-hidden','true');});
doc.addEventListener('click',function(event){
 if(event.defaultPrevented||event.button!==0||event.metaKey||event.ctrlKey||event.shiftKey||event.altKey)return;
 var card=event.target.closest('.product-card');
 if(card&&!event.target.closest('a,button,input,select,textarea,form,label,[data-add],[data-wish]')){
   var detail=card.querySelector('.product-info h3 a[href]');
   if(detail){event.preventDefault();navigate(detail.href);return;}
 }
 var link=event.target.closest('a[href]');
 if(!link||link.hasAttribute('download')||link.target&&link.target!=='_self'||link.dataset.noLoader==='true'||event.target.closest('[data-no-loader]'))return;
 if(link.getAttribute('href').trim().charAt(0)==='#')return;
 var url;
 try{url=new URL(link.href,window.location.href);}catch(_){return;}
 if(url.origin!==window.location.origin||!/^https?:$/.test(url.protocol))return;
 if(url.pathname===window.location.pathname&&url.search===window.location.search&&url.hash)return;
 if(link.href===window.location.href)return;
 event.preventDefault();navigate(url.href);
},false);
doc.addEventListener('submit',function(event){
 var form=event.target;
 if(!(form instanceof HTMLFormElement)||form.target&&form.target!=='_self'||form.dataset.noLoader==='true')return;
 if(form.dataset.kcLoadingStarted==='1')return;
 form.dataset.kcLoadingStarted='1';startLoader();
},false);
doc.addEventListener('click',function(event){
 var close=event.target.closest('[data-close="cart-drawer"]');
 if(close){var go=close.closest('.cart-empty');if(go){var link=doc.createElement('a');link.href='/shop/';link.className='btn-primary';link.textContent='Explore products';close.replaceWith(link);}}
},true);
// Product cards behave like dedicated product pages when tapped outside their controls.
Array.prototype.forEach.call(doc.querySelectorAll('.product-card'),function(card){
 card.setAttribute('tabindex','0');card.setAttribute('role','link');
 card.setAttribute('aria-label','Open '+((card.dataset.name||'product')));
 card.addEventListener('keydown',function(event){if(event.key==='Enter'||event.key===' '){if(event.target.closest('a,button,input,select,textarea'))return;var a=card.querySelector('.product-info h3 a[href]');if(a){event.preventDefault();navigate(a.href);}}});
});
})();
