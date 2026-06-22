# -*- coding: utf-8 -*-
import json
data = json.load(open('climate_data.json', encoding='utf-8'))
DATA_JS = json.dumps(data, ensure_ascii=False)
LOGO = open('/sessions/trusting-laughing-thompson/mnt/.claude/skills/bump-design-system/assets/logo-bump-on-dark.svg', encoding='utf-8').read().strip()

HTML = r"""<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="utf-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1"/>
<title>Bump &mdash; Risques climatiques en France (projections)</title>
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/leaflet.min.css"/>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
<style>
:root{
 --navy:#214281; --navy-deep:#0E1C37; --navy600:#2B55A6; --navy100:#D6E1F5;
 --coral:#FF5D5D; --ink:#121721; --body:#252A37; --desc:#6C7485;
 --border:#D2D6DD; --bg:#FDFDFD; --sunken:#F4F5F6;
 --pos:#08744C; --warn:#CF6110; --neg:#BF1137; --info:#14658A;
 --r-md:8px; --r-lg:12px; --shadow:0 1px 2px rgba(0,0,0,.08);
}
*{box-sizing:border-box}
html,body{margin:0}
body{font-family:'Inter',system-ui,-apple-system,Segoe UI,Roboto,sans-serif;color:var(--body);background:var(--sunken)}
header{background:var(--navy-deep);color:#FDFDFD;padding:13px 22px;display:flex;align-items:center;
 justify-content:space-between;flex-wrap:wrap;gap:12px}
.brand{display:flex;align-items:center;gap:16px}
.brand svg{height:26px;width:auto;display:block}
.brand .divider{width:1px;height:30px;background:rgba(255,255,255,.22)}
.brand .ttl{line-height:1.25}
.eyebrow{color:var(--coral);font-size:11px;font-weight:700;letter-spacing:1.2px;text-transform:uppercase}
.brand h1{font-size:17px;margin:1px 0 0;font-weight:700;letter-spacing:.2px;color:#FDFDFD}
.brand .sub{font-size:12px;color:#AEB8CC;margin-top:1px}
.tag{background:var(--coral);color:#fff;font-size:10px;font-weight:700;border-radius:254px;
 padding:5px 12px;text-transform:uppercase;letter-spacing:.6px;cursor:pointer}
.wrap{display:flex;height:calc(100vh - 60px);min-height:540px}
#side{width:354px;min-width:312px;background:var(--bg);border-right:1px solid var(--border);overflow-y:auto;padding:18px}
#mapcol{flex:1;position:relative;display:flex;flex-direction:column;background:var(--sunken)}
#map{flex:1}
.ctrlbar{display:flex;gap:12px;flex-wrap:wrap;align-items:flex-end;padding:12px 16px;
 background:var(--bg);border-bottom:1px solid var(--border)}
.field{display:flex;flex-direction:column}
.ctrlbar label{font-size:10.5px;text-transform:uppercase;letter-spacing:.7px;color:var(--desc);
 font-weight:700;margin-bottom:4px}
select{font-family:inherit;font-size:14px;padding:8px 11px;border:1px solid var(--border);border-radius:var(--r-md);
 background:#fff;color:var(--ink);min-width:158px;cursor:pointer;font-weight:500}
select:focus{outline:2px solid var(--navy);outline-offset:1px}
h2{font-size:13px;margin:0 0 8px;color:var(--navy);text-transform:uppercase;letter-spacing:.6px;font-weight:700}
.figure{font-size:12.5px;line-height:1.55;color:var(--body);background:var(--sunken);
 border:1px solid var(--border);border-radius:var(--r-lg);padding:11px 13px;margin-bottom:14px}
.confbox{font-size:12px;line-height:1.5;color:var(--body);background:#FFF7ED;border:1px solid #F8D78F;
 border-left:4px solid var(--warn);border-radius:var(--r-md);padding:9px 11px;margin-bottom:14px}
.cbadge{display:inline-block;font-size:10px;font-weight:700;border-radius:254px;padding:2px 9px;margin-left:4px;color:#fff}
.cb-Elevee{background:var(--pos)} .cb-Moyenne{background:var(--warn)} .cb-Faible{background:var(--neg)}
.legend{margin:6px 0 16px}
.legend .row{display:flex;align-items:center;gap:9px;font-size:12.5px;margin:4px 0;color:var(--body)}
.sw{width:18px;height:18px;border-radius:5px;border:1px solid rgba(0,0,0,.12);flex:0 0 auto}
.gradbar{height:16px;border-radius:6px;border:1px solid rgba(0,0,0,.1);margin:6px 0 4px}
.gradticks{display:flex;justify-content:space-between;font-size:11px;color:var(--desc)}
.sources{font-size:11.5px;color:var(--desc);line-height:1.55}
.sources b{color:var(--ink)}
.card{background:var(--bg);border:1px solid var(--border);border-radius:var(--r-lg);box-shadow:var(--shadow);padding:14px;margin-top:14px}
#deptinfo h3{margin:0 0 2px;font-size:16px;color:var(--ink);font-weight:700}
#deptinfo .reg{font-size:11.5px;color:var(--desc);margin-bottom:10px}
.tempcallout{display:flex;align-items:baseline;gap:8px;background:#FFF1F1;border:1px solid #FFD2D2;
 border-radius:var(--r-md);padding:8px 12px;margin-bottom:12px}
.tempcallout .big{font-size:24px;font-weight:700;color:var(--coral);line-height:1}
.tempcallout .lbl{font-size:11.5px;color:var(--desc)}
.bar{display:flex;align-items:center;gap:9px;margin:6px 0;font-size:12.5px}
.bar .nm{width:118px;flex:0 0 auto;color:var(--body)}
.track{flex:1;height:11px;background:var(--sunken);border-radius:6px;overflow:hidden;border:1px solid var(--border)}
.fill{height:100%}
.bar .vl{width:74px;text-align:right;flex:0 0 auto;font-variant-numeric:tabular-nums;color:var(--ink);font-weight:600}
.note{font-size:11px;color:#8A93A6;margin-top:10px;font-style:italic;line-height:1.5}
.leaflet-tooltip.dt{font-size:12px;font-weight:500;border:none;border-radius:8px;box-shadow:0 2px 10px rgba(14,28,55,.25);color:var(--ink)}
.leaflet-tooltip.dt b{color:var(--navy)}
.foot{font-size:11px;color:var(--desc);padding:8px 16px;background:var(--bg);border-top:1px solid var(--border)}
.hactions{display:flex;align-items:center;gap:12px}
.btn-about{font-family:inherit;font-size:12.5px;font-weight:600;color:#FDFDFD;background:rgba(255,255,255,.08);
 border:1px solid rgba(255,255,255,.28);border-radius:254px;padding:7px 14px;cursor:pointer}
.btn-about:hover{background:rgba(255,255,255,.16);border-color:var(--coral)}
.overlay{display:none;position:fixed;inset:0;background:rgba(14,28,55,.55);z-index:1000;padding:24px;
 backdrop-filter:blur(2px)}
.overlay.open{display:flex;align-items:flex-start;justify-content:center}
.modal{background:var(--bg);max-width:880px;width:100%;max-height:90vh;border-radius:16px;
 box-shadow:0 12px 48px rgba(14,28,55,.4);display:flex;flex-direction:column;margin:auto}
.modal-head{display:flex;align-items:center;justify-content:space-between;padding:18px 24px;
 border-bottom:1px solid var(--border);background:var(--navy-deep);border-radius:16px 16px 0 0}
.modal-head h2{margin:0;color:#FDFDFD;font-size:18px;text-transform:none;letter-spacing:.2px}
.btn-close{background:none;border:none;color:#FDFDFD;font-size:28px;line-height:1;cursor:pointer;padding:0 4px}
.btn-close:hover{color:var(--coral)}
.modal-body{padding:8px 28px 28px;overflow-y:auto;font-size:13.5px;line-height:1.62;color:var(--body)}
.modal-body h3{color:var(--navy);font-size:15px;margin:22px 0 8px;font-weight:700}
.modal-body h4{color:var(--ink);font-size:13.5px;margin:16px 0 4px;font-weight:700}
.modal-body p{margin:8px 0}
.modal-body ul{margin:8px 0;padding-left:20px}
.modal-body li{margin:4px 0}
.modal-body a{color:var(--navy600);word-break:break-word}
.modal-body .eyebrow2{color:var(--coral);font-size:11px;font-weight:700;letter-spacing:1px;text-transform:uppercase;margin-top:24px}
.mtable{width:100%;border-collapse:collapse;margin:10px 0;font-size:12.5px}
.mtable th,.mtable td{border:1px solid var(--border);padding:6px 9px;text-align:left;vertical-align:top}
.mtable th{background:var(--sunken);color:var(--navy);font-weight:700}
.mtable td.c{text-align:center;font-variant-numeric:tabular-nums}
.legalbox{background:var(--sunken);border:1px solid var(--border);border-left:4px solid var(--coral);
 border-radius:var(--r-lg);padding:16px 18px;margin-top:14px;font-size:12.5px;color:var(--body)}
.legalbox h4{margin-top:12px}
.legalbox h4:first-child{margin-top:0}
.scaleinline{display:inline-flex;gap:4px;vertical-align:middle;margin:0 4px}
.scaleinline span{width:16px;height:16px;border-radius:4px;display:inline-block}
@media(max-width:800px){.wrap{flex-direction:column;height:auto}#side{width:100%;border-right:none;border-bottom:1px solid var(--border)}#map{height:62vh}.brand .sub{display:none}}
</style>
</head>
<body>
<header>
 <div class="brand">
   __LOGO__
   <div class="divider"></div>
   <div class="ttl">
     <div class="eyebrow">Adaptation climatique</div>
     <h1>Risques climatiques en France &mdash; projections futures</h1>
     <div class="sub">Exposition par d&eacute;partement &middot; trajectoire de r&eacute;f&eacute;rence TRACC &middot; horizons 2050 &amp; 2100</div>
   </div>
 </div>
 <div class="hactions">
   <button id="aboutBtn" class="btn-about" type="button">&#9432;&nbsp; &Agrave; propos, m&eacute;thode &amp; limites</button>
   <span class="tag" id="tagWarn" title="Ouvrir la m&eacute;thode">&#9888; Synth&egrave;se indicative</span>
 </div>
</header>

<div id="aboutOverlay" class="overlay" role="dialog" aria-modal="true" aria-labelledby="aboutTtl">
 <div class="modal">
   <div class="modal-head">
     <h2 id="aboutTtl">&Agrave; propos &amp; m&eacute;thodologie</h2>
     <button id="aboutClose" class="btn-close" type="button" aria-label="Fermer">&times;</button>
   </div>
   <div class="modal-body" id="aboutBody"></div>
 </div>
</div>

<div class="wrap">
 <aside id="side">
   <h2 id="riskTitle">Synth&egrave;se multi-risques</h2>
   <div class="figure" id="riskFigure"></div>
   <div class="confbox" id="riskConf"></div>
   <div class="legend" id="legend"></div>
   <div class="sources" id="riskSources"></div>
   <div class="card" id="deptinfo">
     <h3 id="dInfoTitle">Cliquez un d&eacute;partement</h3>
     <div class="reg" id="dInfoReg">Survolez pour comparer, cliquez pour le d&eacute;tail complet.</div>
     <div id="dInfoBars"></div>
     <div class="note" id="dInfoNote"></div>
   </div>
 </aside>

 <div id="mapcol">
   <div class="ctrlbar">
     <div class="field">
       <label for="riskSel">Risque</label>
       <select id="riskSel"></select>
     </div>
     <div class="field">
       <label for="hzSel">Horizon (sous-filtre)</label>
       <select id="hzSel"></select>
     </div>
     <div class="field" style="margin-left:auto">
       <label>&nbsp;</label>
       <span id="status" style="font-size:12px;color:var(--desc)"></span>
     </div>
   </div>
   <div id="map"></div>
   <div class="foot">Classes d'exposition 1 (tr&egrave;s faible) &rarr; 5 (tr&egrave;s &eacute;lev&eacute;), sauf <b>Hausse des temp&eacute;ratures</b> en &deg;C. Submersion = littoral ; enneigement = massifs. M&eacute;thode et sources dans le panneau de gauche.</div>
 </div>
</div>

<script src="https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/leaflet.min.js"></script>
<script>
const DATA = __DATA__;
const COLORS = {1:'#08744C',2:'#6FA63C',3:'#E6A817',4:'#CF6110',5:'#BF1137'};
const NA = '#E2E5EA';
const LABELS = {1:'Très faible',2:'Faible',3:'Modéré',4:'Élevé',5:'Très élevé'};
const RISK_NAMES = {global:'Synthèse',temperature:'Hausse temp.',chaleur:'Chaleur',secheresse:'Sécheresse',feux:'Feux de forêt',inondations:'Inondations',submersion:'Submersion',argiles:'Argiles (RGA)',montagne:'Enneigement'};
// rampe temperature (degC) -> couleurs Bump (warn/neg)
const TSTOPS=[[2.3,[252,227,176]],[2.9,[242,166,90]],[3.5,[207,97,16]],[4.1,[191,17,55]],[4.7,[122,14,38]]];
const TMIN=2.3, TMAX=4.7;
let curRisk='global', curHz='2050', geo=null, layer=null, selected=null;

function tempColor(v){
 if(v<=TSTOPS[0][0]) v=TSTOPS[0][0]; if(v>=TSTOPS[TSTOPS.length-1][0]) v=TSTOPS[TSTOPS.length-1][0];
 for(let i=0;i<TSTOPS.length-1;i++){const a=TSTOPS[i],b=TSTOPS[i+1];
   if(v>=a[0]&&v<=b[0]){const t=(v-a[0])/(b[0]-a[0]);
     const c=a[1].map((ch,k)=>Math.round(ch+(b[1][k]-ch)*t));
     return 'rgb('+c[0]+','+c[1]+','+c[2]+')';}}
 return 'rgb(122,14,38)';
}
const isTemp=()=>curRisk==='temperature';

const riskSel=document.getElementById('riskSel');
DATA.risks_order.forEach(r=>{const o=document.createElement('option');o.value=r;o.textContent=DATA.meta[r].label;riskSel.appendChild(o);});
const hzSel=document.getElementById('hzSel');
Object.keys(DATA.horizons).forEach(h=>{const o=document.createElement('option');o.value=h;o.textContent=DATA.horizons[h];hzSel.appendChild(o);});
riskSel.value=curRisk; hzSel.value=curHz;
riskSel.onchange=e=>{curRisk=e.target.value;refresh();};
hzSel.onchange=e=>{curHz=e.target.value;refresh();};

function valFor(code){const d=DATA.departements[code];if(!d)return null;const v=d.risks[curHz][curRisk];return (v===undefined)?null:v;}
function colorFor(code){const v=valFor(code);if(v===null||v===undefined)return NA;return isTemp()?tempColor(v):(COLORS[Math.round(v)]||NA);}
function valText(v){if(v===null||v===undefined)return 'non concerné';if(isTemp())return '+'+v.toFixed(1)+' °C';if(curRisk==='global')return v+' / 5';return LABELS[Math.round(v)]+' ('+v+')';}

const map=L.map('map',{minZoom:5,maxZoom:9,scrollWheelZoom:true}).setView([46.6,2.5],6);
L.tileLayer('https://cartodb-basemaps-{s}.global.ssl.fastly.net/light_nolabels/{z}/{x}/{y}.png',
 {attribution:'&copy; OpenStreetMap, &copy; CARTO',subdomains:'abcd'}).addTo(map);

const GEO_URLS=[
 'https://cdn.jsdelivr.net/gh/gregoiredavid/france-geojson@master/departements-version-simplifiee.geojson',
 'https://raw.githubusercontent.com/gregoiredavid/france-geojson/master/departements-version-simplifiee.geojson'
];
const st=document.getElementById('status');
(async function load(){
 st.textContent='Chargement du fond de carte…';
 for(const u of GEO_URLS){try{const r=await fetch(u);if(!r.ok)continue;geo=await r.json();break;}catch(e){}}
 if(!geo){st.textContent='⚠ Fond de carte indisponible (connexion internet requise au 1er chargement).';return;}
 draw(); st.textContent='';
})();

function style(f){return{fillColor:colorFor(f.properties.code),weight:1,color:'#fff',fillOpacity:.86};}
function draw(){
 if(layer) layer.remove();
 layer=L.geoJSON(geo,{style,onEachFeature:(f,l)=>{
   const c=f.properties.code, d=DATA.departements[c];
   l.bindTooltip('<b>'+(d?d.nom:f.properties.nom)+'</b> ('+c+')<br>'+RISK_NAMES[curRisk]+' : '+valText(valFor(c)),{className:'dt',sticky:true});
   l.on('mouseover',()=>l.setStyle({weight:2.5,color:'#214281'}));
   l.on('mouseout',()=>l.setStyle({weight:1,color:'#fff'}));
   l.on('click',()=>showDept(c));
 }}).addTo(map);
}
function refresh(){
 const m=DATA.meta[curRisk];
 document.getElementById('riskTitle').textContent=m.label;
 document.getElementById('riskFigure').textContent=m.figure;
 document.getElementById('riskConf').innerHTML='<b>Fiabilit&eacute; de la spatialisation :</b> <span class="cbadge cb-'+m.confiance+'">'+m.confiance+'</span><br>'+m.prov;
 document.getElementById('riskSources').innerHTML='<b>Sources :</b><br>'+m.sources.map(s=>'&bull; '+s).join('<br>');
 buildLegend();
 if(layer){layer.setStyle(style);layer.eachLayer(l=>{const c=l.feature.properties.code,d=DATA.departements[c];
   l.setTooltipContent('<b>'+(d?d.nom:'')+'</b> ('+c+')<br>'+RISK_NAMES[curRisk]+' : '+valText(valFor(c)));});}
 if(selected) showDept(selected);
}
function buildLegend(){
 const el=document.getElementById('legend');
 if(isTemp()){
   const g='linear-gradient(90deg,'+TSTOPS.map(s=>'rgb('+s[1].join(',')+') '+((s[0]-TMIN)/(TMAX-TMIN)*100).toFixed(0)+'%').join(',')+')';
   el.innerHTML='<b style="font-size:12px">Légende &mdash; '+DATA.meta[curRisk].unit+'</b>'
     +'<div class="gradbar" style="background:'+g+'"></div>'
     +'<div class="gradticks"><span>+2,3°C</span><span>+3,5°C</span><span>+4,5°C</span></div>';
   return;
 }
 let h='<b style="font-size:12px">Légende &mdash; '+DATA.meta[curRisk].unit+'</b>';
 for(let i=5;i>=1;i--) h+='<div class="row"><span class="sw" style="background:'+COLORS[i]+'"></span>'+i+' &middot; '+LABELS[i]+'</div>';
 if(curRisk==='submersion'||curRisk==='montagne') h+='<div class="row"><span class="sw" style="background:'+NA+'"></span>Non concerné</div>';
 el.innerHTML=h;
}
function showDept(code){
 selected=code; const d=DATA.departements[code]; if(!d)return;
 document.getElementById('dInfoTitle').textContent=d.nom+' ('+code+')';
 document.getElementById('dInfoReg').textContent='Horizon '+DATA.horizons[curHz];
 const rk=d.risks[curHz];
 let h='<div class="tempcallout"><span class="big">+'+rk.temperature.toFixed(1)+'°C</span><span class="lbl">hausse de temp&eacute;rature moyenne<br>vs 1900 ('+DATA.horizons[curHz]+')</span></div>';
 ['chaleur','secheresse','feux','inondations','submersion','argiles','montagne'].forEach(r=>{
   const v=rk[r];
   if(v===undefined){h+='<div class="bar"><span class="nm">'+RISK_NAMES[r]+'</span><div class="track"></div><span class="vl" style="color:#aab3c5">n.c.</span></div>';return;}
   h+='<div class="bar"><span class="nm">'+RISK_NAMES[r]+'</span><div class="track"><div class="fill" style="width:'+(v/5*100)+'%;background:'+COLORS[Math.round(v)]+'"></div></div><span class="vl">'+LABELS[Math.round(v)]+'</span></div>';
 });
 const g=rk.global;
 h+='<div class="bar" style="margin-top:9px;border-top:1px dashed var(--border);padding-top:9px"><span class="nm"><b>Indice global</b></span><div class="track"><div class="fill" style="width:'+(g/5*100)+'%;background:'+COLORS[Math.round(g)]+'"></div></div><span class="vl"><b>'+g+'/5</b></span></div>';
 document.getElementById('dInfoBars').innerHTML=h;
 document.getElementById('dInfoNote').textContent='n.c. = non concerné (submersion hors littoral ; enneigement hors massif). Classes = synthèse des gradients officiels, non une mesure ponctuelle.';
}
refresh();

// ---------- A propos & methodologie ----------
const ABOUT = `
<p><b>Cette carte donne une lecture comparative et indicative de l'exposition de chaque d&eacute;partement m&eacute;tropolitain aux principaux al&eacute;as du changement climatique</b>, &agrave; deux horizons (2050 et 2100). Ce n'est <b>pas</b> une mesure par d&eacute;partement, ni une donn&eacute;e officielle&nbsp;: c'est une <b>synth&egrave;se d'expert</b> qui projette des <b>chiffres nationaux</b> (souvent officiels) sur le territoire selon des gradients documment&eacute;s.</p>

<div class="legalbox" style="border-left-color:var(--warn);background:#FFF7ED;border-color:#F8D78F">
<h4>&#9888; Avertissement m&eacute;thodologique &mdash; &agrave; lire avant tout</h4>
<ul>
<li><b>Les classes 1&ndash;5 ne sont pas des donn&eacute;es mesur&eacute;es.</b> Ce sont des jugements d'expert agr&eacute;g&eacute;s par macro-r&eacute;gion. Le caract&egrave;re &laquo;&nbsp;reproductible&nbsp;&raquo; du calcul ne le rend pas exact.</li>
<li><b>Une seule note par d&eacute;partement masque l'essentiel</b>&nbsp;: le risque r&eacute;el se joue &agrave; la commune (plateau vs fond de vall&eacute;e, ville vs campagne). La maille d&eacute;partementale est trop grossi&egrave;re pour une d&eacute;cision individuelle.</li>
<li><b>Les chiffres nationaux sont sourc&eacute;s&nbsp;; leur spatialisation, non.</b> Citer M&eacute;t&eacute;o-France/BRGM &agrave; c&ocirc;t&eacute; d'une classe ne signifie pas que ces organismes l'ont produite. Voir la colonne &laquo;&nbsp;Fiabilit&eacute;&nbsp;&raquo;.</li>
<li><b>L'indice global est non pond&eacute;r&eacute;</b> et m&eacute;lange des al&eacute;as de natures diff&eacute;rentes&nbsp;: &agrave; lire comme un rep&egrave;re, pas comme un niveau de risque.</li>
<li><b>Aucune incertitude n'est affich&eacute;e.</b> Les projections ont des fourchettes larges&nbsp;; une classe unique en donne une fausse impression de pr&eacute;cision.</li>
</ul>
</div>

<h4>Ce que cette carte n'est PAS</h4>
<ul>
<li>Un &eacute;tat des risques r&eacute;glementaire (ERP/ERRIAL), un PPRN, ni un substitut &agrave; G&eacute;orisques.</li>
<li>Une pr&eacute;vision&nbsp;: la TRACC est une trajectoire d'adaptation <b>volontairement haute</b> (&laquo;&nbsp;et si on rate +2&nbsp;&deg;C&nbsp;&raquo;), pas le sc&eacute;nario le plus probable.</li>
<li>Un calcul de risque complet&nbsp;: elle d&eacute;crit l'al&eacute;a, pas l'exposition r&eacute;elle des personnes/biens ni la vuln&eacute;rabilit&eacute;.</li>
<li>Exhaustive&nbsp;: voir les al&eacute;as manquants en section 5.</li>
</ul>

<h3>1. Maille, horizons et r&eacute;f&eacute;rentiel</h3>
<ul>
<li><b>Maille :</b> 96 d&eacute;partements de France m&eacute;tropolitaine (Corse incluse). L'outre-mer n'est pas couvert par ce fond de carte. Pour une analyse &agrave; la commune, l'outil de r&eacute;f&eacute;rence est <i>Climadiag Commune</i> (M&eacute;t&eacute;o-France).</li>
<li><b>Horizons :</b> 2050 et 2100, align&eacute;s sur la <b>TRACC</b> (Trajectoire de R&eacute;chauffement de r&eacute;f&eacute;rence pour l'Adaptation au Changement climatique), inscrite au code de l'environnement (d&eacute;cret du 23/01/2026) : <b>+2,7&nbsp;&deg;C en 2050</b> et <b>+4&nbsp;&deg;C en 2100</b> en moyenne en France hexagonale et Corse (vs 1900).</li>
<li><b>Projections climatiques :</b> issues du portail <b>DRIAS &mdash; les futurs du climat</b> (M&eacute;t&eacute;o-France, en lien avec IPSL / CERFACS / CNRM), maille de r&eacute;f&eacute;rence 8&nbsp;km.</li>
</ul>

<h3>2. &Eacute;chelle de lecture</h3>
<p>Tous les al&eacute;as d'impact sont exprim&eacute;s en <b>classes d'exposition de 1 &agrave; 5</b> :
<span class="scaleinline"><span style="background:#08744C"></span><span style="background:#6FA63C"></span><span style="background:#E6A817"></span><span style="background:#CF6110"></span><span style="background:#BF1137"></span></span>
1&nbsp;=&nbsp;tr&egrave;s faible, 2&nbsp;=&nbsp;faible, 3&nbsp;=&nbsp;mod&eacute;r&eacute;, 4&nbsp;=&nbsp;&eacute;lev&eacute;, 5&nbsp;=&nbsp;tr&egrave;s &eacute;lev&eacute;.
Seule la couche <b>Hausse des temp&eacute;ratures</b> est exprim&eacute;e en <b>degr&eacute;s Celsius</b> (&eacute;chelle continue d&eacute;di&eacute;e). Les couches <b>Submersion</b> (littoral) et <b>Enneigement</b> (massifs) ne concernent que les d&eacute;partements pertinents ; les autres sont indiqu&eacute;s &laquo;&nbsp;non concern&eacute;&nbsp;&raquo;.</p>

<h3>3. Principe de classement</h3>
<p>Les chiffres <b>nationaux</b> affich&eacute;s (multiplicateurs, jours suppl&eacute;mentaires, pourcentages&hellip;) proviennent directement des sources officielles. Les <b>classes d&eacute;partementales</b> sont d&eacute;duites en projetant ces tendances sur le territoire selon les <b>gradients spatiaux document&eacute;s</b> par ces m&ecirc;mes sources, via une grille de 9 macro-r&eacute;gions climatiques, compl&eacute;t&eacute;e d'ajustements (&laquo;&nbsp;overrides&nbsp;&raquo;) factuels :</p>
<ul>
<li><b>Submersion marine :</b> uniquement les d&eacute;partements littoraux, class&eacute;s selon la vuln&eacute;rabilit&eacute; document&eacute;e (zones basses : Camargue, Marais poitevin, Charente-Maritime, Gironde, Hauts-de-France&hellip;).</li>
<li><b>Enneigement :</b> uniquement les d&eacute;partements de massif (Alpes, Pyr&eacute;n&eacute;es, Massif central, Jura, Vosges, Corse).</li>
<li><b>Retrait-gonflement des argiles :</b> classe abaiss&eacute;e sur les massifs cristallins (Bretagne granitique, hautes Alpes/Pyr&eacute;n&eacute;es, Vosges, Corse) et relev&eacute;e &agrave; 5 sur les d&eacute;partements identifi&eacute;s par le BRGM (Loiret, Loir-et-Cher, Lot-et-Garonne, Haute-Garonne&hellip;).</li>
<li><b>Horizon 2100 :</b> la plupart des al&eacute;as progressent d'un cran (extension vers le nord de la chaleur et des feux notamment), dans la limite de la classe 5.</li>
</ul>

<h4>Composition des 9 macro-r&eacute;gions</h4>
<table class="mtable">
<tr><th>Macro-r&eacute;gion</th><th>D&eacute;partements</th></tr>
<tr><td>M&eacute;diterran&eacute;e</td><td>06, 11, 13, 2A, 2B, 30, 34, 66, 83, 84</td></tr>
<tr><td>Provence / Alpes du Sud</td><td>04, 05</td></tr>
<tr><td>Sud-Ouest / Garonne-Aquitaine</td><td>09, 12, 24, 31, 32, 33, 40, 46, 47, 64, 65, 81, 82</td></tr>
<tr><td>Centre-Ouest atlantique</td><td>16, 17, 19, 23, 79, 85, 86, 87</td></tr>
<tr><td>Vall&eacute;e du Rh&ocirc;ne / Auvergne-Alpes</td><td>01, 03, 07, 15, 26, 38, 42, 43, 48, 63, 69, 73, 74</td></tr>
<tr><td>Ouest (Bretagne, Normandie, Pays de la Loire)</td><td>14, 22, 27, 29, 35, 44, 49, 50, 53, 56, 61, 72</td></tr>
<tr><td>Bassin parisien / Centre-Val de Loire</td><td>18, 21, 28, 36, 37, 41, 45, 58, 71, 75, 77, 78, 89, 91, 92, 93, 94, 95</td></tr>
<tr><td>Nord / Hauts-de-France / Normandie est</td><td>02, 59, 60, 62, 76, 80</td></tr>
<tr><td>Grand Est / Franche-Comt&eacute;</td><td>08, 10, 25, 39, 51, 52, 54, 55, 57, 67, 68, 70, 88, 90</td></tr>
</table>

<h4>Classes de base par macro-r&eacute;gion (horizon 2050)</h4>
<table class="mtable">
<tr><th>Macro-r&eacute;gion</th><th class="c">Chaleur</th><th class="c">S&eacute;cher.</th><th class="c">Feux</th><th class="c">Inond.</th><th class="c">Argiles*</th><th class="c">&Delta;T (&deg;C)</th></tr>
<tr><td>M&eacute;diterran&eacute;e</td><td class="c">5</td><td class="c">5</td><td class="c">5</td><td class="c">4</td><td class="c">4</td><td class="c">+3,0</td></tr>
<tr><td>Provence / Alpes Sud</td><td class="c">4</td><td class="c">4</td><td class="c">4</td><td class="c">4</td><td class="c">2</td><td class="c">+3,0</td></tr>
<tr><td>Sud-Ouest / Garonne</td><td class="c">4</td><td class="c">4</td><td class="c">4</td><td class="c">3</td><td class="c">5</td><td class="c">+2,8</td></tr>
<tr><td>Centre-Ouest atlant.</td><td class="c">3</td><td class="c">3</td><td class="c">3</td><td class="c">3</td><td class="c">4</td><td class="c">+2,6</td></tr>
<tr><td>Rh&ocirc;ne / Auvergne-Alpes</td><td class="c">4</td><td class="c">4</td><td class="c">3</td><td class="c">4</td><td class="c">3</td><td class="c">+2,9</td></tr>
<tr><td>Ouest</td><td class="c">2</td><td class="c">3</td><td class="c">2</td><td class="c">3</td><td class="c">3</td><td class="c">+2,4</td></tr>
<tr><td>Bassin parisien</td><td class="c">3</td><td class="c">3</td><td class="c">3</td><td class="c">3</td><td class="c">5</td><td class="c">+2,7</td></tr>
<tr><td>Nord / Hauts-de-France</td><td class="c">2</td><td class="c">2</td><td class="c">2</td><td class="c">3</td><td class="c">3</td><td class="c">+2,5</td></tr>
<tr><td>Grand Est / Franche-Comt&eacute;</td><td class="c">3</td><td class="c">3</td><td class="c">2</td><td class="c">3</td><td class="c">4</td><td class="c">+2,8</td></tr>
</table>
<p style="font-size:12px;color:var(--desc)">*Argiles : classe de base avant ajustements d&eacute;partementaux (massifs cristallins abaiss&eacute;s, standouts BRGM relev&eacute;s &agrave; 5).</p>

<h4>Fiabilit&eacute; de la spatialisation, par risque</h4>
<table class="mtable">
<tr><th>Risque</th><th>Chiffre national</th><th>Classe par d&eacute;partement</th><th>Fiabilit&eacute;</th></tr>
<tr><td>Hausse temp&eacute;rature</td><td>Officiel (TRACC/DRIAS)</td><td>Valeur nationale modul&eacute;e par un gradient grossier</td><td>Moyenne</td></tr>
<tr><td>Chaleur</td><td>Officiel (DRIAS)</td><td>Synth&egrave;se par macro-r&eacute;gion</td><td>Moyenne</td></tr>
<tr><td>S&eacute;cheresse</td><td>Officiel (DRIAS-Eau)</td><td>Synth&egrave;se par macro-r&eacute;gion</td><td>Moyenne</td></tr>
<tr><td>Feux de for&ecirc;t</td><td>Relay&eacute; (non reverifi&eacute; sur source primaire)</td><td>Synth&egrave;se</td><td>Faible</td></tr>
<tr><td>Inondations</td><td>Qualitatif</td><td>Ph&eacute;nom&egrave;ne tr&egrave;s local &mdash; classe forc&eacute;ment grossi&egrave;re</td><td>Faible</td></tr>
<tr><td>Submersion</td><td>Officiel (GIEC/Cerema)</td><td>Littoral factuel ; niveau approxim&eacute;</td><td>Moyenne</td></tr>
<tr><td>Argiles (RGA)</td><td>Officiel (BRGM/SDES)</td><td>Donn&eacute;e fine BRGM <b>non utilis&eacute;e ici</b> ; classe approxim&eacute;e</td><td>Moyenne</td></tr>
<tr><td>Enneigement</td><td>Officiel (M&eacute;t&eacute;o-France)</td><td>Massifs factuels ; niveau = synth&egrave;se</td><td>Moyenne</td></tr>
<tr><td>Indice global</td><td>&mdash;</td><td>Moyenne <b>non pond&eacute;r&eacute;e</b> (calcul Bump)</td><td>Faible</td></tr>
</table>

<h3>4. D&eacute;tail et chiffres de r&eacute;f&eacute;rence par risque</h3>
<h4>Hausse des temp&eacute;ratures</h4>
<p>+2,7&nbsp;&deg;C (2050) et +4&nbsp;&deg;C (2100) en moyenne (TRACC). R&eacute;chauffement non uniforme : <b>+0,5 &agrave; 1&nbsp;&deg;C de plus</b> sur le quart sud-est et les zones de montagne, moindre au nord-ouest. En &eacute;t&eacute;, la hausse peut atteindre +2,6 &agrave; +5,3&nbsp;&deg;C en fin de si&egrave;cle. <i>Source : M&eacute;t&eacute;o-France / DRIAS, TRACC.</i></p>
<h4>Chaleur extr&ecirc;me &amp; canicules</h4>
<p>Jours de vague de chaleur &times;5 en moyenne, &times;6 &agrave; &times;8 sur l'arc m&eacute;diterran&eacute;en (2050). Nuits tropicales : +24&nbsp;j en moyenne, jusqu'&agrave; +74&nbsp;j &agrave; +4&nbsp;&deg;C, et 90 &agrave; 120 nuits/an sur le littoral m&eacute;diterran&eacute;en en 2100. <i>Source : M&eacute;t&eacute;o-France / DRIAS.</i></p>
<h4>S&eacute;cheresse des sols &amp; ressource en eau</h4>
<p>+24 jours de sol sec/an en moyenne (2050), +39 (2100). &Eacute;pisodes extr&ecirc;mes jusqu'&agrave; 4&ndash;5 mois au nord et 7&ndash;8 mois sur le pourtour m&eacute;diterran&eacute;en ; -10&nbsp;% de pluie l'&eacute;t&eacute; &agrave; +2,7&nbsp;&deg;C. <i>Source : M&eacute;t&eacute;o-France / DRIAS-Eau.</i></p>
<h4>Feux de for&ecirc;t</h4>
<p>Jours &agrave; risque &eacute;lev&eacute; &times;2 et surfaces br&ucirc;l&eacute;es &times;4 d'ici 2050 ; plus de 50&nbsp;% des for&ecirc;ts class&eacute;es &agrave; risque (vs ~1/3 aujourd'hui) ; extension vers le nord et saison allong&eacute;e d'1 &agrave; 2 mois. <i>Source : M&eacute;t&eacute;o-France ; IGEDD/CGAAER.</i></p>
<h4>Inondations &amp; pluies extr&ecirc;mes</h4>
<p>Intensification des pluies extr&ecirc;mes (Clausius-Clapeyron), &eacute;pisodes m&eacute;diterran&eacute;ens/c&eacute;venols plus violents, crues et ruissellement accrus ; al&eacute;a le plus marqu&eacute; sur l'arc m&eacute;diterran&eacute;en et les grands bassins (Rh&ocirc;ne, Loire, Seine, Garonne). <i>Source : ONERC, M&eacute;t&eacute;o-France / DRIAS, G&eacute;orisques.</i></p>
<h4>Submersion marine &amp; &eacute;l&eacute;vation du niveau de la mer</h4>
<p>Niveau de la mer +35 &agrave; 56&nbsp;cm &agrave; Brest en 2100 (vs 2020), jusqu'&agrave; ~1&nbsp;m possible. &Agrave; +1&nbsp;m : 1,4&nbsp;million d'habitants et 450&nbsp;000 logements menac&eacute;s ; 864 communes concern&eacute;es, dont 126 prioritaires. <i>Source : GIEC, Cerema, BRGM (sealevelrise.brgm.fr), ONERC.</i></p>
<h4>Retrait-gonflement des argiles (RGA)</h4>
<p>55&nbsp;% du territoire m&eacute;tropolitain en al&eacute;a moyen/fort (vs 48&nbsp;% en 2020) ; 12,1&nbsp;millions de maisons expos&eacute;es (61,5&nbsp;%) ; ph&eacute;nom&egrave;ne aggrav&eacute; par l'intensification des s&eacute;cheresses. <i>Source : BRGM / SDES, zonage 2026 (d&eacute;cret du 09/01/2026) ; G&eacute;orisques.</i></p>
<h4>Recul de l'enneigement (montagne)</h4>
<p>-2 mois de neige au sol en moyenne/basse altitude (2050) ; saisons de ski difficiles 1 sur 2&ndash;3 aux Pyr&eacute;n&eacute;es vers 2050 ; r&eacute;chauffement hivernal renforc&eacute; sur Alpes et Pyr&eacute;n&eacute;es. <i>Source : M&eacute;t&eacute;o-France ; ONERC.</i></p>
<h4>Indice global multi-risques</h4>
<p>Moyenne des classes d'impact applicables &agrave; chaque d&eacute;partement (chaleur, s&eacute;cheresse, feux, inondations, argiles, + submersion/enneigement le cas &eacute;ch&eacute;ant). <b>La hausse de temp&eacute;rature n'entre pas dans l'indice</b> : elle est le moteur du ph&eacute;nom&egrave;ne, pas un impact en soi.</p>

<h3>5. Limites &amp; pr&eacute;cautions de lecture</h3>
<h4>Limites de m&eacute;thode</h4>
<ul>
<li>Classes = <b>exposition relative entre territoires</b>, pas un niveau de risque absolu ni une probabilit&eacute;.</li>
<li>Une classe d&eacute;partementale <b>masque les disparit&eacute;s internes</b> (fond de vall&eacute;e vs plateau, plaine vs altitude, ville vs campagne).</li>
<li><b>Al&eacute;a &ne; risque.</b> Le risque r&eacute;el = al&eacute;a &times; exposition (population/biens) &times; vuln&eacute;rabilit&eacute;. Cette carte ne d&eacute;crit que l'al&eacute;a.</li>
<li>Le passage 2050&rarr;2100 applique une progression simple (+1 cran g&eacute;n&eacute;ralement)&nbsp;: c'est une convention, pas une mod&eacute;lisation risque par risque.</li>
<li><b>Incertitude non repr&eacute;sent&eacute;e</b>&nbsp;: les projections d&eacute;pendent du sc&eacute;nario d'&eacute;missions et de l'ensemble de mod&egrave;les&nbsp;; les valeurs ont des fourchettes que la carte n'affiche pas.</li>
</ul>
<h4>Al&eacute;as non couverts</h4>
<p>&Eacute;rosion / recul du trait de c&ocirc;te, temp&ecirc;tes et vents violents, gr&ecirc;le, qualit&eacute; de l'air / ozone, maladies vectorielles (moustique tigre), stress hydrique et conflits d'usage de l'eau, impacts agricoles et sur la biodiversit&eacute;. La liste des al&eacute;as repr&eacute;sent&eacute;s n'est donc <b>pas exhaustive</b>.</p>
<h4>P&eacute;rim&egrave;tre g&eacute;ographique</h4>
<p>France <b>m&eacute;tropolitaine uniquement</b>. L'outre-mer (Antilles, Guyane, La R&eacute;union, Mayotte), pourtant parmi les territoires les plus expos&eacute;s (cyclones, submersion, s&eacute;isme), n'est pas trait&eacute;.</p>
<h4>D&eacute;pendances techniques</h4>
<p>Le fond de carte des d&eacute;partements et les tuiles sont charg&eacute;s &agrave; l'ouverture depuis des services tiers (jsDelivr/GitHub, CARTO, Google Fonts)&nbsp;: une connexion internet est requise et la disponibilit&eacute; d&eacute;pend de ces tiers. Seules les donn&eacute;es de risque et la mise en forme sont int&eacute;gr&eacute;es au fichier.</p>

<div class="eyebrow2">Sources</div>
<h3 style="margin-top:6px">6. Sources document&eacute;es</h3>
<p style="font-size:12.5px;color:var(--body)">Distinction essentielle&nbsp;: les liens ci-dessous documentent les <b>chiffres nationaux</b>. La <b>spatialisation</b> par d&eacute;partement reste une synth&egrave;se Bump. Plusieurs chiffres ont &eacute;t&eacute; collect&eacute;s via des r&eacute;sum&eacute;s de recherche et <b>devraient &ecirc;tre reverifi&eacute;s sur les documents primaires</b> (donn&eacute;es DRIAS brutes, notice IGEDD, jeu de donn&eacute;es SDES, dossier TRACC) avant tout usage engageant.</p>
<h4>Sources primaires (officielles)</h4>
<ul>
<li>TRACC &mdash; Minist&egrave;re de la Transition &eacute;cologique : <a href="https://www.ecologie.gouv.fr/politiques-publiques/trajectoire-rechauffement-reference-ladaptation-changement-climatique-tracc" target="_blank" rel="noopener">trajectoire de r&eacute;f&eacute;rence (TRACC)</a></li>
<li>DRIAS &mdash; les futurs du climat (M&eacute;t&eacute;o-France) : <a href="https://www.drias-climat.fr/" target="_blank" rel="noopener">drias-climat.fr</a> &middot; <a href="https://www.drias-climat.fr/accompagnement/section/402" target="_blank" rel="noopener">le climat futur selon la TRACC</a> &middot; <a href="https://www.drias-climat.fr/accompagnement/sections/417" target="_blank" rel="noopener">vagues de chaleur</a></li>
<li>M&eacute;t&eacute;o-France &mdash; <a href="https://meteofrance.com/le-changement-climatique/quel-climat-futur/rechauffement-climatique-quel-climat-en-france-en-2050" target="_blank" rel="noopener">quel climat en 2050&nbsp;?</a> &middot; <a href="https://meteofrance.com/le-changement-climatique/quel-climat-futur/changement-climatique-quel-impact-sur-les-feux-de-foret" target="_blank" rel="noopener">feux de for&ecirc;t</a> &middot; <a href="https://meteofrance.com/le-changement-climatique/quel-climat-futur/changement-climatique-quel-impact-sur-lenneigement" target="_blank" rel="noopener">enneigement</a></li>
<li>M&eacute;t&eacute;o-France &mdash; <a href="https://meteofrance.com/climadiag-commune" target="_blank" rel="noopener">Climadiag Commune</a> (projections &agrave; la commune) ; DRIAS-Eau (ressource en eau)</li>
<li>Feux &mdash; <a href="https://www.adaptation-changement-climatique.gouv.fr/agir/espace-documentaire/changement-climatique-et-extension-des-zones-sensibles-aux-feux-forets" target="_blank" rel="noopener">IGEDD/CGAAER : extension des zones sensibles aux feux</a></li>
<li>Argiles &mdash; <a href="https://www.statistiques.developpement-durable.gouv.fr/nouveau-zonage-dexposition-au-retrait-gonflement-des-argiles-plus-de-104-millions-de-maisons" target="_blank" rel="noopener">SDES : zonage RGA 2026</a> &middot; <a href="https://www.georisques.gouv.fr/donnees/bases-de-donnees/retrait-gonflement-des-argiles-version-2026" target="_blank" rel="noopener">BRGM / G&eacute;orisques (carte RGA 2026)</a></li>
<li>Submersion / niveau de la mer &mdash; <a href="https://sealevelrise.brgm.fr/slr/" target="_blank" rel="noopener">BRGM &mdash; visualisation de l'&eacute;l&eacute;vation</a> ; Cerema ; ONERC ; GIEC/IPCC</li>
<li>Risques naturels &mdash; <a href="https://www.georisques.gouv.fr/" target="_blank" rel="noopener">G&eacute;orisques (Minist&egrave;re / BRGM)</a></li>
<li>Fond cartographique &mdash; d&eacute;partements : projet open data <i>france-geojson</i> (Gr&eacute;goire David) ; fonds de tuiles : OpenStreetMap &amp; CARTO.</li>
</ul>

<div class="eyebrow2">Mentions l&eacute;gales</div>
<div class="legalbox">
<h4>Nature et objet</h4>
<p>Ce document est fourni par <b>Bump Charge</b> &agrave; des fins <b>strictement informatives et p&eacute;dagogiques</b>. Il ne constitue ni un conseil juridique, assurantiel, immobilier, financier, technique ou d'ing&eacute;nierie, ni une recommandation, ni une offre, et ne saurait fonder &agrave; lui seul une quelconque d&eacute;cision.</p>
<h4>Exactitude et donn&eacute;es</h4>
<p>Les classes d'exposition r&eacute;sultent d'une <b>synth&egrave;se et d'une interpr&eacute;tation</b> par Bump de donn&eacute;es publiques de tiers. Elles sont fournies &laquo;&nbsp;en l'&eacute;tat&nbsp;&raquo;, <b>sans garantie</b> d'exactitude, d'exhaustivit&eacute;, d'actualit&eacute; ou d'ad&eacute;quation &agrave; un usage particulier. Les donn&eacute;es sources demeurent la propri&eacute;t&eacute; de leurs &eacute;metteurs respectifs (M&eacute;t&eacute;o-France, BRGM, Cerema, GIEC, services de l'&Eacute;tat, etc.) ; les marques et logos cit&eacute;s appartiennent &agrave; leurs titulaires. <b>Bump n'est ni affili&eacute; &agrave; ces organismes, ni endoss&eacute; par eux</b>, et cette carte ne constitue pas une publication officielle.</p>
<h4>Non-substitution aux dispositifs r&eacute;glementaires</h4>
<p>Cette carte <b>ne remplace pas</b> les dispositifs officiels d'information sur les risques&nbsp;: G&eacute;orisques, &eacute;tat des risques (ERP/ERRIAL), plans de pr&eacute;vention des risques (PPRN), DDRM, &eacute;tudes g&eacute;otechniques (G1&ndash;G2) et diagnostics r&eacute;glementaires. Pour toute d&eacute;cision (acquisition, construction, assurance, implantation, investissement), il convient de consulter ces sources et des <b>professionnels qualifi&eacute;s</b>.</p>
<h4>Incertitude des projections</h4>
<p>Les projections climatiques sont des <b>sc&eacute;narios</b> soumis &agrave; des incertitudes intrins&egrave;ques&nbsp;; elles peuvent &eacute;voluer avec l'&eacute;tat des connaissances scientifiques et les trajectoires r&eacute;elles d'&eacute;missions.</p>
<h4>Limitation de responsabilit&eacute;</h4>
<p>Dans la limite permise par la loi, <b>Bump Charge d&eacute;cline toute responsabilit&eacute;</b> au titre de tout pr&eacute;judice direct ou indirect r&eacute;sultant de l'utilisation, de l'interpr&eacute;tation ou de la d&eacute;pendance &agrave; cette carte ou aux d&eacute;cisions prises sur son fondement.</p>
<h4>Confidentialit&eacute; et usage</h4>
<p>Document &agrave; usage interne Bump&nbsp;; toute diffusion externe, reproduction ou r&eacute;utilisation est soumise &agrave; autorisation pr&eacute;alable de Bump Charge.</p>
<p style="margin-top:12px;color:var(--desc)">&copy; 2026 Bump Charge. Tous droits r&eacute;serv&eacute;s. &mdash; Version juin 2026.</p>
</div>
`;
const ov=document.getElementById('aboutOverlay');
document.getElementById('aboutBody').innerHTML=ABOUT;
function openAbout(){ov.classList.add('open');}
function closeAbout(){ov.classList.remove('open');}
document.getElementById('aboutBtn').onclick=openAbout;
document.getElementById('tagWarn').onclick=openAbout;
document.getElementById('aboutClose').onclick=closeAbout;
ov.addEventListener('click',e=>{if(e.target===ov)closeAbout();});
document.addEventListener('keydown',e=>{if(e.key==='Escape')closeAbout();});
</script>
</body>
</html>
"""
HTML = HTML.replace('__DATA__', DATA_JS).replace('__LOGO__', LOGO)
open('carte_risques_climatiques_france.html','w',encoding='utf-8').write(HTML)
print('HTML written, bytes:', len(HTML))
