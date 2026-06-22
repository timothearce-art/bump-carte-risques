# -*- coding: utf-8 -*-
"""
Construit le dataset departemental des risques climatiques (projections futures).
Methode : classes d'exposition 1-5 par macro-region climatique, calees sur les
gradients spatiaux DOCUMENTES par les sources officielles (Meteo-France/DRIAS/TRACC,
BRGM/SDES pour les argiles, Cerema/BRGM/GIEC pour la submersion). Overrides
departementaux pour les cas factuels (littoral, massifs, standouts argiles).
Aucune valeur ponctuelle par departement n'est inventee : ce sont des CLASSES
de synthese, les chiffres nationaux de reference sont fournis a part.
"""
import json

# ---- 96 departements metropolitains -> macro-region climatique ----
REGION = {
 'MED':['06','11','13','2A','2B','30','34','66','83','84'],
 'PACA_INT':['04','05'],
 'SO':['09','12','24','31','32','33','40','46','47','64','65','81','82'],
 'CO':['16','17','19','23','79','85','86','87'],
 'RA':['01','03','07','15','26','38','42','43','48','63','69','73','74'],
 'OUEST':['14','22','27','29','35','44','49','50','53','56','61','72'],
 'BP':['18','21','28','36','37','41','45','58','71','75','77','78','89','91','92','93','94','95'],
 'NORD':['02','59','60','62','76','80'],
 'EST':['08','10','25','39','51','52','54','55','57','67','68','70','88','90'],
}
NOM = {
 '01':'Ain','02':'Aisne','03':'Allier','04':'Alpes-de-Haute-Provence','05':'Hautes-Alpes',
 '06':'Alpes-Maritimes','07':'Ardeche','08':'Ardennes','09':'Ariege','10':'Aube',
 '11':'Aude','12':'Aveyron','13':'Bouches-du-Rhone','14':'Calvados','15':'Cantal',
 '16':'Charente','17':'Charente-Maritime','18':'Cher','19':'Correze','21':"Cote-d'Or",
 '22':"Cotes-d'Armor",'23':'Creuse','24':'Dordogne','25':'Doubs','26':'Drome',
 '27':'Eure','28':'Eure-et-Loir','29':'Finistere','2A':'Corse-du-Sud','2B':'Haute-Corse',
 '30':'Gard','31':'Haute-Garonne','32':'Gers','33':'Gironde','34':'Herault',
 '35':'Ille-et-Vilaine','36':'Indre','37':'Indre-et-Loire','38':'Isere','39':'Jura',
 '40':'Landes','41':'Loir-et-Cher','42':'Loire','43':'Haute-Loire','44':'Loire-Atlantique',
 '45':'Loiret','46':'Lot','47':'Lot-et-Garonne','48':'Lozere','49':'Maine-et-Loire',
 '50':'Manche','51':'Marne','52':'Haute-Marne','53':'Mayenne','54':'Meurthe-et-Moselle',
 '55':'Meuse','56':'Morbihan','57':'Moselle','58':'Nievre','59':'Nord',
 '60':'Oise','61':'Orne','62':'Pas-de-Calais','63':'Puy-de-Dome','64':'Pyrenees-Atlantiques',
 '65':'Hautes-Pyrenees','66':'Pyrenees-Orientales','67':'Bas-Rhin','68':'Haut-Rhin','69':'Rhone',
 '70':'Haute-Saone','71':'Saone-et-Loire','72':'Sarthe','73':'Savoie','74':'Haute-Savoie',
 '75':'Paris','76':'Seine-Maritime','77':'Seine-et-Marne','78':'Yvelines','79':'Deux-Sevres',
 '80':'Somme','81':'Tarn','82':'Tarn-et-Garonne','83':'Var','84':'Vaucluse',
 '85':'Vendee','86':'Vienne','87':'Haute-Vienne','88':'Vosges','89':'Yonne',
 '90':'Territoire de Belfort','91':'Essonne','92':'Hauts-de-Seine','93':'Seine-Saint-Denis',
 '94':'Val-de-Marne','95':"Val-d'Oise",
}
dept_region = {}
for r, lst in REGION.items():
    for d in lst:
        dept_region[d] = r

# ---- niveaux par macro-region (horizon 2050 ; +1 -> 2100, plafond 5) ----
# 1 tres faible / 2 faible / 3 modere / 4 eleve / 5 tres eleve
LVL = {                # chaleur, secheresse, feux, inondations, argiles
 'MED':      {'chaleur':5,'secheresse':5,'feux':5,'inondations':4,'argiles':4},
 'PACA_INT': {'chaleur':4,'secheresse':4,'feux':4,'inondations':4,'argiles':2},
 'SO':       {'chaleur':4,'secheresse':4,'feux':4,'inondations':3,'argiles':5},
 'CO':       {'chaleur':3,'secheresse':3,'feux':3,'inondations':3,'argiles':4},
 'RA':       {'chaleur':4,'secheresse':4,'feux':3,'inondations':4,'argiles':3},
 'OUEST':    {'chaleur':2,'secheresse':3,'feux':2,'inondations':3,'argiles':3},
 'BP':       {'chaleur':3,'secheresse':3,'feux':3,'inondations':3,'argiles':5},
 'NORD':     {'chaleur':2,'secheresse':2,'feux':2,'inondations':3,'argiles':3},
 'EST':      {'chaleur':3,'secheresse':3,'feux':2,'inondations':3,'argiles':4},
}
# au moins quel risque progresse fortement vers 2100 (extension feux/chaleur nord)
PLUS2100 = {'chaleur':1,'secheresse':1,'feux':1,'inondations':1,'argiles':1}

# ---- Hausse de la temperature moyenne annuelle (degC vs 1900) ----
# National TRACC : +2,7C en 2050, +4,0C en 2100. Gradient documente DRIAS :
# +0,5 a 1C de plus sur le quart sud-est et la montagne, moindre au nord-ouest.
TEMP_OFFSET = {'MED':0.3,'PACA_INT':0.3,'SO':0.1,'CO':-0.1,'RA':0.2,
               'OUEST':-0.3,'BP':0.0,'NORD':-0.2,'EST':0.1}
def temp_val(reg, hz):
    base = 2.7 if hz == '2050' else 4.0
    mult = 1.0 if hz == '2050' else 1.3
    return round(base + TEMP_OFFSET[reg]*mult, 1)

# ---- overrides factuels argiles (BRGM) : crystallin = faible ; standouts = tres fort ----
ARGILE_LOW = {'29':1,'22':2,'56':2,'2A':2,'2B':2,'05':2,'73':2,'74':2,'04':2,
              '65':2,'09':2,'66':3,'15':2,'43':2,'63':3,'48':2,'88':2,'68':2,'90':2,'38':3}
ARGILE_HIGH = {'45':5,'41':5,'47':5,'31':5,'82':5,'32':4,'18':4,'37':4,'86':4}

# ---- submersion marine (littoral uniquement) : classe de vulnerabilite ----
SUBMERSION = {
 '17':5,'85':5,'13':5,'30':5,'80':5,'62':5,'59':5,'44':5,'33':5,'34':5,'11':5,
 '50':4,'14':4,'76':4,'56':4,'29':4,'66':4,
 '22':3,'35':3,'40':3,'64':3,'83':3,'06':3,
 '2A':2,'2B':2,
}
# ---- montagne / enneigement (departements de massif) ----
MONTAGNE = {
 '73':5,'74':5,'05':5,'38':5,'65':5,'09':4,'04':4,
 '06':4,'66':4,'64':4,'31':3,'15':4,'43':4,'63':4,'88':4,'39':4,'25':4,'2A':3,'2B':3,
 '12':3,'48':3,'07':3,'26':3,'68':3,'01':3,'42':3,'70':2,'90':2,'19':2,'23':2,'69':2,
}

RISK_META = {
 'global':{'label':'Indice de synthese (indicatif)','unit':'indice moyen NON PONDERE (1-5)',
   'figure':"AVERTISSEMENT : moyenne arithmetique NON PONDEREE des classes d'aleas applicables (chaleur, secheresse, feux, inondations, argiles + submersion/montagne). Melanger un alea geotechnique (argiles) et des aleas climatiques a poids egal n'a pas de sens physique : a lire comme un simple reperage relatif, pas comme un niveau de risque. La hausse de temperature n'y entre pas (moteur, pas impact).",
   'sources':['Indice construit par Bump (ponderation = aucune, choix discutable)']},
 'temperature':{'label':'Hausse des temperatures','unit':'degC vs 1900 (moyenne annuelle)',
   'figure':"Trajectoire de reference TRACC : +2,7C en 2050 et +4,0C en 2100 en moyenne en France hexagonale et Corse (vs 1900). Rechauffement non uniforme : +0,5 a 1C de plus sur le quart sud-est et les zones de montagne, moindre au nord-ouest. En ete, la hausse peut atteindre +2,6 a +5,3C a la fin du siecle.",
   'sources':['Meteo-France / DRIAS - le climat futur selon la TRACC','TRACC (decret 23/01/2026)']},
 'chaleur':{'label':'Chaleur extreme & canicules','unit':'classe 1-5',
   'figure':"Jours de vague de chaleur x5 en moyenne (x6 a x8 sur l'arc mediterraneen) en 2050 (+2,7C). Nuits tropicales : jusqu'a +24 j en moyenne, +74 j a +4C ; jusqu'a 90-120 nuits/an sur le littoral mediterraneen en 2100. +20 a 35 jours >35C a l'interieur, +10 a 20 sur les littoraux.",
   'sources':['Meteo-France / DRIAS - les futurs du climat','TRACC (decret 23/01/2026)']},
 'secheresse':{'label':'Secheresse des sols & ressource en eau','unit':'classe 1-5',
   'figure':"+24 jours de sol sec/an en moyenne en 2050, +39 en 2100. Secheresses extremes jusqu'a 4-5 mois dans le Nord, 7-8 mois sur le pourtour mediterraneen. -10% de pluie l'ete a +2,7C.",
   'sources':['Meteo-France / DRIAS-Eau','TRACC']},
 'feux':{'label':'Feux de foret','unit':'classe 1-5',
   'figure':"Jours a risque eleve x2 et surfaces brulees x4 d'ici 2050. >50% des forets classees a risque (vs ~1/3 aujourd'hui). Extension vers le nord et saison +1 a 2 mois.",
   'sources':['Meteo-France','IGEDD/CGAAER - extension des zones sensibles aux feux']},
 'inondations':{'label':'Inondations & pluies extremes','unit':'classe 1-5',
   'figure':"Pluies extremes plus intenses (Mediterranee, episodes cevenols), crues et ruissellement accrus. Alea le plus marque sur l'arc mediterraneen et les grands bassins (Rhone, Loire, Seine, Garonne).",
   'sources':['ONERC','Meteo-France / DRIAS','Georisques']},
 'submersion':{'label':'Submersion marine & elevation du niveau de la mer','unit':'classe 1-5 (littoral)',
   'figure':"Niveau de la mer : +35 a 56 cm a Brest en 2100 (vs 2020), jusqu'a ~1 m possible. A +1 m : 1,4 M d'habitants et 450 000 logements menaces ; 864 communes concernees dont 126 prioritaires. Camargue, Marais poitevin, Charente-Maritime, Gironde, Hauts-de-France parmi les plus exposes.",
   'sources':['GIEC','Cerema','BRGM - sealevelrise.brgm.fr','ONERC']},
 'argiles':{'label':'Retrait-gonflement des argiles (RGA)','unit':'classe 1-5',
   'figure':"55% du territoire metropolitain en alea moyen/fort (vs 48% en 2020) ; 12,1 M de maisons exposees (61,5%). Departements les plus exposes : Loiret, Loir-et-Cher, Lot-et-Garonne, Haute-Garonne (50-70% du territoire). Aggrave par l'intensification des secheresses.",
   'sources':['BRGM / SDES - zonage 2026 (decret 09/01/2026)','Georisques']},
 'montagne':{'label':'Recul de l\'enneigement (montagne)','unit':'classe 1-5 (massifs)',
   'figure':"-2 mois de neige au sol en moyenne/basse altitude en 2050 (+2,7C). Saisons de ski difficiles 1 sur 2-3 aux Pyrenees vers 2050. Rechauffement hivernal renforce sur Alpes et Pyrenees.",
   'sources':['Meteo-France','ONERC - dossier montagne']},
}

# Confiance + provenance : on distingue le CHIFFRE NATIONAL (souvent officiel)
# de la SPATIALISATION departementale (synthese qualitative Bump = moins fiable).
CONF = {'global':'Faible','temperature':'Moyenne','chaleur':'Moyenne','secheresse':'Moyenne',
        'feux':'Faible','inondations':'Faible','submersion':'Moyenne','argiles':'Moyenne','montagne':'Moyenne'}
PROV = {
 'global':"Calcul Bump (moyenne non ponderee). Aucune source officielle ne produit cet indice.",
 'temperature':"Chiffre national : OFFICIEL (TRACC/DRIAS). Valeur par departement : valeur nationale MODULEE par Bump selon un gradient documente mais grossier (pas une donnee station).",
 'chaleur':"Chiffre national : OFFICIEL (DRIAS). Classe par departement : SYNTHESE Bump par macro-region.",
 'secheresse':"Chiffre national : OFFICIEL (DRIAS-Eau). Classe par departement : SYNTHESE Bump.",
 'feux':"Chiffre national : relaye par Meteo-France/IGEDD (non reverifie sur source primaire). Classe : SYNTHESE Bump.",
 'inondations':"Phenomene tres local : une classe departementale est par nature grossiere. Classe : SYNTHESE Bump (a recouper avec Georisques/PPRI commune par commune).",
 'submersion':"Liste des departements littoraux : FACTUELLE. Niveau de vulnerabilite : approximation Bump (a recouper avec Cerema/TRI).",
 'argiles':"Donnee fine existante (BRGM par commune) NON utilisee ici : classe = approximation Bump. A remplacer par la donnee Georisques RGA pour fiabilite.",
 'montagne':"Massifs : FACTUELS. Niveau : synthese Bump.",
}
for k in RISK_META:
    RISK_META[k]['confiance'] = CONF.get(k,'')
    RISK_META[k]['prov'] = PROV.get(k,'')

def cap(v): return max(1, min(5, v))

depts = {}
for code, nom in NOM.items():
    reg = dept_region[code]
    base = LVL[reg]
    rec = {'nom': nom, 'region': reg, 'risks': {}}
    for hz, add in (('2050',0), ('2100',1)):
        terr = {}
        for rk in ('chaleur','secheresse','feux','inondations','argiles'):
            v = cap(base[rk] + (PLUS2100[rk] if add else 0))
            if rk == 'argiles':
                if code in ARGILE_LOW: v = ARGILE_LOW[code] + (1 if add else 0)
                if code in ARGILE_HIGH: v = ARGILE_HIGH[code]
                v = cap(v)
            terr[rk] = v
        if code in SUBMERSION:
            # le niveau de la mer monte avec le temps : 2050 < 2100
            terr['submersion'] = cap(SUBMERSION[code] - 1 + add)
        if code in MONTAGNE:
            terr['montagne'] = cap(MONTAGNE[code] + (1 if add else 0))
        # synthese = moyenne des classes d'impact applicables (hors temperature)
        vals = list(terr.values())
        terr['global'] = round(sum(vals)/len(vals), 1)
        # hausse de temperature (degC) : couche autonome, hors indice global
        terr['temperature'] = temp_val(reg, hz)
        rec['risks'][hz] = terr
    depts[code] = rec

out = {'meta': RISK_META,
       'risks_order': ['global','temperature','chaleur','secheresse','feux','inondations','submersion','argiles','montagne'],
       'horizons': {'2050':'2050 (+2,7C)','2100':'2100 (+4C)'},
       'departements': depts}

with open('climate_data.json','w',encoding='utf-8') as f:
    json.dump(out, f, ensure_ascii=False)

print('Departements:', len(depts))
print('Exemple 13 (Bouches-du-Rhone):', json.dumps(depts['13']['risks'], ensure_ascii=False))
print('Exemple 29 (Finistere):', json.dumps(depts['29']['risks'], ensure_ascii=False))
print('Exemple 45 (Loiret):', json.dumps(depts['45']['risks']['2050'], ensure_ascii=False))
print('Exemple 75 (Paris):', json.dumps(depts['75']['risks']['2050'], ensure_ascii=False))
