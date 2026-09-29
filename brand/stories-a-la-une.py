# -*- coding: utf-8 -*-
"""Stories « à la une » : 8 thèmes, 3 ou 4 stories chacun, plus 8 couvertures.

Tout le texte vient des pages du site (mêmes chiffres, mêmes prix, mêmes
mentions). Aucun nombre n'est ajouté ici.
"""
import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))

I = {
 'doc':'<path d="M7 3h7l5 5v13H7z"/><path d="M14 3v5h5M10 13h6M10 17h6"/>',
 'reseau':'<circle cx="6" cy="12" r="2.5"/><circle cx="18" cy="6" r="2.5"/><circle cx="18" cy="18" r="2.5"/><path d="M8.2 10.9l7.6-3.8M8.2 13.1l7.6 3.8"/>',
 'envoi':'<path d="M4 12l16-8-6 16-3-7z"/><path d="M11 13l9-9"/>',
 'loupe':'<circle cx="10.5" cy="10.5" r="6.5"/><path d="M20 20l-4.8-4.8"/>',
 'cloche':'<path d="M6 16V11a6 6 0 0 1 12 0v5l1.5 2h-15z"/><path d="M10 20.5a2 2 0 0 0 4 0"/>',
 'oui':'<path d="M5 12.5l4.5 4.5L19 7.5"/>',
 'non':'<path d="M6.5 6.5l11 11M17.5 6.5l-11 11"/>',
 'euro':'<path d="M17 6.5a6.5 6.5 0 1 0 0 11M4 10.5h9M4 13.5h9"/>',
 'facture':'<path d="M7 3h10v18l-2.5-1.5L12 21l-2.5-1.5L7 21z"/><path d="M10 8h4M10 12h4"/>',
 'bouclier':'<path d="M12 3l7 3v6c0 4.5-3 7.5-7 9-4-1.5-7-4.5-7-9V6z"/><path d="M8.8 12.2l2.2 2.2 4.2-4.4"/>',
 'cible':'<circle cx="12" cy="12" r="8.5"/><circle cx="12" cy="12" r="4.5"/><circle cx="12" cy="12" r="1"/>',
 'equipe':'<circle cx="9" cy="8" r="3"/><circle cx="17" cy="9" r="2.5"/><path d="M3 20c0-3.3 2.7-6 6-6s6 2.7 6 6M15 14.2c3 .1 5.5 2.5 5.5 5.8"/>',
 'fusee':'<path d="M12 15l-3-3c1-4 4-8 10-9-1 6-5 9-9 10z"/><path d="M9 12l-4 1-1 4 4-1M12 15l-1 4 4-1 1-4"/><circle cx="15" cy="9" r="1.2"/>',
 'repere':'<path d="M12 21s-6.5-5.6-6.5-11a6.5 6.5 0 0 1 13 0c0 5.4-6.5 11-6.5 11z"/><circle cx="12" cy="10" r="2.5"/>',
 'calc':'<rect x="5" y="3" width="14" height="18" rx="2.5"/><path d="M8.5 7.5h7M8.5 12h.01M12 12h.01M15.5 12h.01M8.5 16h.01M12 16h.01M15.5 16h.01"/>',
 'calendrier':'<rect x="4" y="5" width="16" height="15" rx="2"/><path d="M4 10h16M9 3v4M15 3v4"/>',
 'tel':'<path d="M5 4h4l2 5-2.5 1.5a11 11 0 0 0 5 5L15 13l5 2v4a1 1 0 0 1-1 1A16 16 0 0 1 4 5a1 1 0 0 1 1-1z"/>',
 'balance':'<path d="M12 4v16M8 20h8M5 7h14"/><path d="M5 7l-3 6h6zM19 7l-3 6h6z"/>',
 'horloge':'<circle cx="12" cy="12" r="8.5"/><path d="M12 7v5l3 2"/>',
 'courbe':'<path d="M4 19h16"/><path d="M5 15l4-4 3 3 6-7"/><path d="M14 7h4v4"/>',
 'etiquette':'<path d="M3 12V4h8l10 10-8 8z"/><circle cx="7.5" cy="8.5" r="1.5"/>',
 'boussole':'<circle cx="12" cy="12" r="8.5"/><path d="M15.5 8.5l-2 5-5 2 2-5z"/>',
 'bas':'<path d="M12 4v15M6 13l6 6 6-6"/>',
}
def svg(k): return f'<svg viewBox="0 0 24 24">{I[k]}</svg>'
def icone(k, c=''): return f'<div class="icone {c}">{svg(k)}</div>'

def pastille(t): return f'<div class="pastille">{t}</div>'

def carte(ic, titre, texte, c='c1'):
    return f'''<div class="carte carte-ligne">{icone(ic, c)}<div><h3>{titre}</h3><p>{texte}</p></div></div>'''

def num(n, titre, texte, c='c1'):
    return f'''<div class="carte carte-ligne"><div class="num {c}">{n}</div><div><h3>{titre}</h3><p>{texte}</p></div></div>'''

def coche(oui, titre, detail=''):
    m = 'marque-oui' if oui else 'marque-non'
    d = f'<small>{detail}</small>' if detail else ''
    return f'<div class="coche"><span class="{m}">{svg("oui" if oui else "non")}</span><div>{titre}{d}</div></div>'

def etape(quand, quoi, point='var(--blanc)'):
    return f'<div class="etape" style="--point:{point}"><div class="quand">{quand}</div><div class="quoi">{quoi}</div></div>'

def tarif(nom, detail, prix):
    return f'<div class="tarif-ligne"><div><b>{nom}</b><small>{detail}</small></div><span class="prix">{prix}</span></div>'

def sticker(ic, titre, sous, c='c1', barre=False):
    cls = 'sticker barre' if barre else 'sticker'
    return f'<div class="{cls}">{icone(ic, c)}<div><b>{titre}</b><span>{sous}</span></div></div>'

LIEN = f'''<div class="lien-ici">{svg("bas")}Touchez le lien</div><div class="place-lien"></div>'''

# Décor dans les bandes que l'interface d'Instagram recouvre (haut et bas).
DECO = '''  <div class="deco rond" style="width:520px;height:520px;right:-170px;top:-250px;background:var(--c1)"></div>
  <div class="deco rond" style="width:150px;height:150px;right:330px;top:70px;background:var(--c3);border:5px solid var(--encre)"></div>
  <div class="deco points" style="width:300px;height:150px;left:70px;top:90px"></div>
  <div class="deco rond" style="width:430px;height:430px;left:-150px;bottom:-210px;background:var(--c2)"></div>
  <div class="deco rond" style="width:120px;height:120px;right:130px;bottom:120px;background:var(--c1);border:5px solid var(--encre)"></div>
'''
DECO_PLEIN = '''  <div class="deco rond" style="width:620px;height:620px;right:-240px;top:-330px;background:var(--c2-plein,var(--c2));opacity:.6"></div>
  <div class="deco rond" style="width:140px;height:140px;left:110px;top:110px;background:var(--c3);border:5px solid var(--encre)"></div>
  <div class="deco points" style="width:320px;height:170px;right:80px;bottom:110px"></div>
'''

def story(theme, nom, i, n, corps, plein=False, centre=True):
    cls = f'story theme-{theme}' + (' pleine' if plein else '')
    if centre:
        corps = corps.replace('<!--bloc-->', '<div class="bloc">', 1) + ('</div>' if '<div class="bloc">' in corps.replace('<!--bloc-->', '<div class="bloc">', 1) else '')
    logo = '<img class="logo" src="../logo-header-light.png" alt="Pilotia">'
    return f'''<div class="{cls}" data-nom="{nom}">
{DECO_PLEIN if plein else DECO}  <div class="zone">
{corps}
  </div>
  <div class="pied">{logo}<span class="compteur">{i} / {n}</span></div>
</div>
'''

S = []   # (theme, nom, corps, plein)

# ── 1. Pilotia ───────────────────────────────────────────────────────────
T = 'pilotage'
S += [(T, 'pilotia-1', f'''
    {pastille('Bienvenue')}
    <div class="h1">Pilotia, <span class="surligne">c'est quoi</span> ?</div>
    <div class="texte">Un accompagnement de gestion pour les <strong>petites entreprises</strong> et les <strong>futurs indépendants</strong>.</div>
    <!--bloc--><div class="pile">
      {sticker('equipe', 'PME et commerces', 'Vous tournez, mais quelque chose freine')}
      {sticker('fusee', 'Futurs indépendants', 'Vous voulez vous lancer sans faux départ', 'c3')}
    </div>''', False),
 (T, 'pilotia-2', f'''
    {pastille("Ce qu'on fait")}
    <div class="h2">Trois piliers, <span class="couleur">un seul interlocuteur</span></div>
    <!--bloc--><div class="pile">
      {carte('loupe', 'Diagnostic &amp; gestion', 'Marges, organisation, processus : ce qui coûte sans se voir.')}
      {carte('facture', 'Gestion administrative &amp; Peppol', 'Facture électronique, encaissements, relances.', 'c2')}
      {carte('reseau', 'Présence digitale', 'Réseaux sociaux, visibilité locale, image de marque.', 'c3')}
    </div>''', False),
 (T, 'pilotia-3', f'''
    {pastille('La méthode')}
    <div class="h2">4 étapes, <span class="couleur">toujours les mêmes</span></div>
    <!--bloc--><div class="frise">
      {etape('1. Écouter', 'Un appel découverte gratuit', 'var(--c3)')}
      {etape('2. Diagnostiquer', 'Sur vos chiffres réels', 'var(--c2)')}
      {etape('3. Décider', '3 à 5 priorités chiffrées', 'var(--c1)')}
      {etape('4. Piloter', 'Un suivi mensuel, si vous le voulez')}
    </div>''', False),
 (T, 'pilotia-4', f'''
    {pastille('Ce qui guide')}
    <div class="h2">Chiffré, réaliste, et c'est vous qui décidez.</div>
    <!--bloc--><div class="pile">
      {carte('loupe', 'Transparence', 'Pas de jargon : chaque conclusion expliquée.')}
      {carte('cible', 'Réalisme', 'Un plan à la mesure de votre temps et de vos moyens.', 'c3')}
    </div>
    {LIEN}''', True),
]

# ── 2. Peppol ────────────────────────────────────────────────────────────
T = 'peppol'
S += [(T, 'peppol-1', f'''
    {pastille('Depuis le 1<sup>er</sup> janvier 2026')}
    <div class="h1">Vos factures PDF <span class="surligne">ne comptent plus.</span></div>
    <div class="texte">Entre entreprises belges assujetties à la TVA, la facture passe désormais par <strong>Peppol</strong>.</div>
    <!--bloc--><div class="stickers">
      {sticker('doc', 'Facture PDF', 'par e-mail', 'c3', barre=True)}
      <svg class="sticker-fleche" viewBox="0 0 64 40"><path d="M4 20h52M42 6l14 14-14 14"/></svg>
      {sticker('envoi', 'Peppol', 'structurée')}
    </div>''', False),
 (T, 'peppol-2', f'''
    {pastille('Ce qui a changé')}
    <div class="h2">Trois choses <span class="couleur">à savoir</span></div>
    <!--bloc--><div class="pile">
      {carte('doc', 'Le PDF ne compte plus', 'La facture doit être structurée, lisible par un logiciel.')}
      {carte('envoi', 'Envoyer et recevoir', "L'obligation vaut dans les deux sens : clients et fournisseurs.", 'c2')}
      {carte('equipe', 'Les particuliers restent à part', 'Les factures aux particuliers ne sont pas visées.', 'c3')}
    </div>''', False),
 (T, 'peppol-3', f'''
    {pastille("Ce qu'on met en place")}
    <div class="h2">De la mise en règle <span class="couleur">au paiement reçu</span></div>
    <!--bloc--><div class="pile" style="gap:22px">
      {num(1, 'Le bon outil', 'Pas le plus cher. Parfois celui de votre comptable suffit.')}
      {num(2, "L'inscription", 'Et les premiers envois faits ensemble.', 'c2')}
      {num(3, 'Des conditions qui protègent', 'Délai, intérêts de retard, acompte.', '')}
      {num(4, 'Un suivi des encaissements', 'Qui vous doit quoi, et quand relancer.')}
    </div>''', False),
 (T, 'peppol-4', f'''
    {pastille('Mise en règle Peppol')}
    <div class="h2">Vos factures en règle, et payées à l'heure.</div>
    <div class="texte">Outil, inscription, modèles, conditions de paiement et relances. <strong>Sur devis.</strong></div>
    <!--bloc-->{LIEN}''', True),
]

# ── 3. Impayés ───────────────────────────────────────────────────────────
T = 'payeurs'
S += [(T, 'impayes-1', f'''
    {pastille('Facture impayée')}
    <div class="h1">Un client paie <span class="surligne">en retard</span> ?</div>
    <div class="texte">Avant de relancer, une question : <strong>professionnel ou particulier</strong> ? Les règles ne sont pas les mêmes.</div>
    <!--bloc--><div class="stickers">
      {sticker('horloge', 'Échéance', 'dépassée', 'c3')}
      {sticker('cloche', 'On relance', 'mais comment ?')}
    </div>''', False),
 (T, 'impayes-2', f'''
    {pastille('Deux régimes')}
    <div class="h2">Pro ou particulier : <span class="couleur">pas la même règle</span></div>
    <!--bloc--><div class="pile">
      {carte('facture', 'Client professionnel', 'Intérêts de retard au taux légal, plus une indemnité forfaitaire de 40 € pour frais de recouvrement.')}
      {carte('equipe', 'Client particulier', 'Premier rappel gratuit, puis au moins 14 jours avant le moindre frais. Pénalités plafonnées par un barème légal.', 'c3')}
    </div>
    <div class="mention" style="margin-top:28px">Informations générales, pas un avis juridique.</div>''', False),
 (T, 'impayes-3', f'''
    {pastille("Dans l'ordre")}
    <div class="h2">Cinq étapes, <span class="couleur">pas une de plus</span></div>
    <!--bloc--><div class="frise serree">
      {etape('1', 'Vérifier votre propre dossier', 'var(--c3)')}
      {etape('2', 'Téléphoner', 'var(--c2)')}
      {etape('3', 'Écrire, avec une date', 'var(--c1)')}
      {etape('4', 'Mise en demeure formelle')}
      {etape('5', 'Décider, avec un avocat si besoin', 'var(--encre)')}
    </div>''', False),
 (T, 'impayes-4', f'''
    {pastille('Le mieux')}
    <div class="h2">Le retard se prévient avant la facture.</div>
    <!--bloc--><div class="pile">
      {carte('envoi', 'Facturer le jour même', 'Par Peppol, avec une trace.', 'c3')}
      {carte('cloche', 'Relancer sans y penser', 'Un calendrier écrit une fois.', 'c2')}
    </div>
    {LIEN}''', True),
]

# ── 4. Affacturage ───────────────────────────────────────────────────────
T = 'affacturage'
S += [(T, 'affacturage-1', f'''
    {pastille('Affacturage')}
    <div class="h1">Facturé aujourd'hui, <span class="surligne">payé tout de suite.</span></div>
    <div class="texte">Vos clients paient à 30 ou 60 jours. <strong>Vos salaires, eux, n'attendent pas.</strong></div>
    <!--bloc--><div class="stickers">
      {sticker('facture', 'Facture', 'envoyée', 'c3')}
      <svg class="sticker-fleche" viewBox="0 0 64 40"><path d="M4 20h52M42 6l14 14-14 14"/></svg>
      {sticker('euro', 'Avance', 'sur votre compte')}
    </div>''', False),
 (T, 'affacturage-2', f'''
    {pastille('Comment ça marche')}
    <div class="h2">En <span class="couleur">trois temps</span></div>
    <!--bloc--><div class="pile">
      {num(1, 'Vous facturez', "Votre client professionnel, comme d'habitude.", '')}
      {num(2, "Vous recevez l'avance", "La plus grande partie du montant, sans attendre l'échéance.", 'c2')}
      {num(3, 'Le client paie', 'Vous recevez le solde, moins la rémunération du partenaire.')}
    </div>''', False),
 (T, 'affacturage-3', f'''
    {pastille("C'est pour vous si")}
    <div class="h2">Quatre <span class="couleur">bons signes</span></div>
    <!--bloc--><div>
      {coche(True, 'Vous facturez des entreprises')}
      {coche(True, 'Vos clients paient à 30, 45 ou 60 jours')}
      {coche(True, 'Vos factures sont acceptées', 'Un travail livré et non contesté')}
      {coche(True, 'Vous facturez régulièrement')}
    </div>''', False),
 (T, 'affacturage-4', f'''
    {pastille('Étude gratuite')}
    <div class="h2">On vérifie, on prépare, on présente.</div>
    <div class="texte">Un avis franc : si ce n'est pas la bonne solution, <strong>on vous le dit.</strong></div>
    <!--bloc-->{LIEN}
    <div class="mention">Pilotia n'accorde aucun financement : le partenaire financier décide. Pilotia peut être rémunéré par le partenaire, vous en êtes informé avant toute signature. Réservé aux entreprises.</div>''', True),
]

# ── 5. Diagnostic ────────────────────────────────────────────────────────
T = 'diagnostic'
S += [(T, 'diagnostic-1', f'''
    {pastille('Diagnostic express')}
    <div class="h1">Où en est <span class="surligne">vraiment</span> votre entreprise ?</div>
    <!--bloc--><div class="stickers">
      {sticker('horloge', '3 minutes', 'chrono', 'c3')}
      {sticker('loupe', '8 questions', 'sans inscription')}
    </div>''', False),
 (T, 'diagnostic-2', f'''
    {pastille('4 thèmes')}
    <div class="h2">Passés <span class="couleur">au crible</span></div>
    <!--bloc--><div class="grille">
      <div class="carte">{icone('euro', 'c1')}<h3 style="margin-top:22px">Finances</h3></div>
      <div class="carte">{icone('equipe', 'c2')}<h3 style="margin-top:22px">Personnel</h3></div>
      <div class="carte">{icone('reseau', 'c3')}<h3 style="margin-top:22px">Présence digitale</h3></div>
      <div class="carte">{icone('courbe', '')}<h3 style="margin-top:22px">Trésorerie</h3></div>
    </div>
    <div class="texte">Le résultat n'est visible <strong>que par vous</strong>.</div>''', False),
 (T, 'diagnostic-3', f'''
    {pastille('Gratuit')}
    <div class="h2">Le diagnostic donne une direction. L'appel donne un plan.</div>
    <!--bloc-->{LIEN}''', True),
]

# ── 6. Outils ────────────────────────────────────────────────────────────
T = 'outils'
S += [(T, 'outils-1', f'''
    {pastille('Gratuits')}
    <div class="h1">Des calculateurs, <span class="surligne">pas du doigt mouillé.</span></div>
    <div class="texte"><strong>Neuf outils gratuits</strong> sur le site, pour poser vos chiffres en quelques minutes.</div>
    <!--bloc--><div class="stickers">
      {sticker('calc', 'Calculer', 'vos vrais chiffres', 'c3')}
      {sticker('courbe', 'Anticiper', 'votre point bas')}
    </div>''', False),
 (T, 'outils-2', f'''
    {pastille('Lequel pour vous ?')}
    <div class="h2">Neuf outils, <span class="couleur">trois familles</span></div>
    <!--bloc--><div class="pile">
      {carte('fusee', 'Indépendants', 'Cotisations sociales, franchise TVA.', 'c3')}
      {carte('courbe', 'Entreprises', "Trésorerie, marge, taux horaire, délai d'encaissement, coût d'un salarié.")}
      {carte('loupe', 'Tout le monde', 'Diagnostic express, calendrier de contenu.', 'c2')}
    </div>''', False),
 (T, 'outils-3', f'''
    {pastille('Les chiffres sont posés')}
    <div class="h2">Et maintenant ? On en parle.</div>
    <div class="texte">Tous les outils sont sur le site, <strong>en libre accès</strong>.</div>
    <!--bloc-->{LIEN}''', True),
]

# ── 7. Lancement ─────────────────────────────────────────────────────────
T = 'independant'
S += [(T, 'lancement-1', f'''
    {pastille('Devenir indépendant')}
    <div class="h1">Se lancer, <span class="surligne">sur des bases solides.</span></div>
    <!--bloc--><div class="pile">
      {coche(False, 'Des démarches mal comprises', 'Statut, TVA, assurances : dans quel ordre ?')}
      {coche(False, 'Des charges sous-estimées', 'Cotisations trimestrielles, TVA à mettre de côté')}
      {coche(False, 'Zéro visibilité au lancement', 'Invisible pendant des mois')}
    </div>''', False),
 (T, 'lancement-2', f'''
    {pastille('Les documents fournis')}
    <div class="h2">Un cadre clair <span class="couleur">pour démarrer</span></div>
    <!--bloc--><div class="grille">
      <div class="carte">{icone('doc', 'c1')}<h3 style="margin-top:22px">Guide des statuts</h3></div>
      <div class="carte">{icone('euro', 'c2')}<h3 style="margin-top:22px">Checklist des charges</h3></div>
      <div class="carte">{icone('bouclier', 'c3')}<h3 style="margin-top:22px">Checklist administrative</h3></div>
      <div class="carte">{icone('reseau', 'c1')}<h3 style="margin-top:22px">Kit premiers clients</h3></div>
    </div>
    <div class="mention" style="margin-top:28px">Le choix du statut se fait toujours avec un comptable agréé.</div>''', False),
 (T, 'lancement-3', f'''
    {pastille('Formule lancement')}
    <div class="h2">3 séances pour partir du bon pied.</div>
    <div class="texte">Démarches administratives, repères financiers, premiers pas commerciaux. <strong>390&nbsp;€.</strong></div>
    <!--bloc-->{LIEN}''', True),
]

# ── 8. Tarifs ────────────────────────────────────────────────────────────
T = 'presence'
S += [(T, 'tarifs-1', f'''
    {pastille('Tarifs')}
    <div class="h2">Pour commencer, <span class="couleur">c'est gratuit</span></div>
    <!--bloc--><div class="carte tarifs">
      {tarif('Diagnostic découverte', 'Appel de 15 minutes, sans engagement', 'Gratuit')}
      {tarif('Diagnostic express', '8 questions en ligne', 'Gratuit')}
      {tarif('Kits et outils', 'En libre accès', 'Gratuit')}
      {tarif('Affacturage', 'Étude et mise en relation', 'Gratuit')}
    </div>''', False),
 (T, 'tarifs-2', f'''
    {pastille('Entreprises en activité')}
    <div class="h2">Des formules <span class="couleur">sans petites lignes</span></div>
    <!--bloc--><div class="carte tarifs">
      {tarif('Diagnostic complet', "Rapport écrit et plan d'action", 'dès 490 €')}
      {tarif('Accompagnement mensuel', 'Sur 3, 6 ou 12 mois', 'dès 390 €/mois')}
      {tarif('Mise en règle Peppol', 'Et encaissements', 'Sur devis')}
      {tarif('Stratégie de visibilité', 'État des lieux et calendrier', '290 €')}
      {tarif('Réseaux sociaux', 'Création, publication, avis', 'dès 290 €/mois')}
    </div>''', False),
 (T, 'tarifs-3', f'''
    {pastille('Futur indépendant')}
    <div class="h2">Formule lancement : 3 séances, 390&nbsp;€.</div>
    <div class="texte">Et un premier appel <strong>gratuit</strong>, pour voir si ça a du sens pour vous.</div>
    <!--bloc-->{LIEN}''', True),
]

# ── Couvertures ──────────────────────────────────────────────────────────
COUV = [('01-pilotia', 'pilotage', 'boussole'), ('02-peppol', 'peppol', 'envoi'), ('03-impayes', 'payeurs', 'cloche'),
        ('04-affacturage', 'affacturage', 'euro'), ('05-diagnostic', 'diagnostic', 'loupe'), ('06-outils', 'outils', 'calc'),
        ('07-lancement', 'independant', 'fusee'), ('08-tarifs', 'presence', 'etiquette')]

# Numérotation par thème
from collections import Counter, defaultdict
total = Counter(n.split('-')[0] for _, n, _, _ in S)
vu = defaultdict(int)
html_st = []
for th, nom, corps, plein in S:
    g = nom.split('-')[0]; vu[g] += 1
    html_st.append(story(th, nom, vu[g], total[g], corps, plein))
html_cv = [f'<div class="couv theme-{th}" data-nom="couverture-{n}"><div class="couv-icone">{svg(ic)}</div></div>\n' for n, th, ic in COUV]

page = f'''<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="UTF-8">
<title>Stories à la une | PILOTIA</title>
<link rel="icon" href="data:,">
<link rel="stylesheet" href="services.css">
<link rel="stylesheet" href="stories.css">
</head>
<body class="stories">

<!-- Stories « à la une » : 8 thèmes et leurs couvertures. Généré ; le texte
     reprend les pages du site, aucun chiffre n'est ajouté. Rendu :
     chaque .story et chaque .couv en PNG 1080 × 1920. -->

{''.join(html_st)}
{''.join(html_cv)}
</body>
</html>
'''
open('stories-a-la-une.html', 'w', encoding='utf-8').write(page)
print(len(S), 'stories,', len(COUV), 'couvertures')
