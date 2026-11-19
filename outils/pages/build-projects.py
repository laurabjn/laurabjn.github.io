"""Génère les pages projet détaillées du site (projets/<slug>/index.html)."""
import json, os, sys

SITE = sys.argv[1]
BASE = "https://laurabojon.fr"


def lst(items):
    return '<ul class="feature-list">' + "".join(f"<li>{i}</li>" for i in items) + "</ul>"


PROJECTS = {
    "klotho": {
        "name": "Klotho",
        "cadre": "Projet personnel",
        "title": "Klotho, application de dressing virtuel · Laura Bojon",
        "desc": "Klotho : application Android de dressing virtuel qui propose chaque matin une tenue selon la météo, le style et l'occasion. Un projet de Laura Bojon.",
        "eyebrow": "Projet personnel · Application Android",
        "h1": "Klotho",
        "lead": "Un dressing virtuel qui propose chaque matin une tenue selon la météo, le style et l'occasion. Un projet personnel que j'ai mené de l'idée jusqu'à la publication sur Google Play.",
        "badge": ("Sur Google Play", "badge badge-live"),
        "actions": [("https://www.dressingklotho.fr/", "Voir dressingklotho.fr ↗", "btn"),
                    ("https://play.google.com/store/apps/details?id=com.laurabjn.klotho", "Google Play ↗", "btn btn-ghost"),
                    ("https://github.com/laurabjn/Klotho", "Voir le code sur GitHub ↗", "btn btn-ghost")],
        "hero_alt": "Les écrans « Ma garde-robe » et « Tenue du jour » de l'application Klotho",
        "project_h2": "Choisir sa tenue sans y passer la matinée",
        "paras": [
            "Klotho range la garde-robe à partir de simples photos et propose chaque matin une tenue adaptée à la météo, au style et à l'occasion. L'application est gratuite, avec une offre Premium.",
            "Même pour un projet personnel, j'ai travaillé comme pour un client : un cahier des charges et un backlog avant la première ligne de code, puis un développement par sprints, testé à chaque étape.",
        ],
        "facts": [("Type", "Application mobile et site de présentation"), ("Plateforme", "Android"),
                  ("Modèle", "Gratuit, avec abonnement Premium"),
                  ("Méthode", "Backlog découpé en sprints, développement piloté par les tests"),
                  ("Statut", "Disponible sur Google Play")],
        "method_first": True,
        "features_h2": "L'essentiel de l'application",
        "features_cols": 3,
        "features": [
            ("Un dressing en photos", "<p>Chaque pièce s'ajoute en photo, et l'IA pré-remplit sa fiche.</p>"),
            ("La tenue du jour", "<p>Chaque matin, une tenue adaptée à la météo de sa ville.</p>"),
            ("Le look complet", "<p>En Premium, une coiffure et un maquillage assortis à chaque tenue.</p>"),
        ],
        "gallery_h2": "L'application en images",
        "gallery_cols": 3,
        "gallery": [("klotho/k1.webp", 720, 1280, "La garde-robe, rangée par catégorie", True),
                    ("klotho/k3.webp", 720, 1280, "La tenue du jour, selon la météo", True),
                    ("klotho/k6.webp", 720, 1280, "La création d'une tenue selon le style, l'occasion et la météo", True)],
        "tech_eyebrow": "Ma méthode",
        "tech_h2": "Comment j'ai mené le projet",
        "tech_intro": "Tout a été cadré avant de coder, puis développé par petites étapes testées, jusqu'à la publication sur Google Play.",
        "tech_cols": 3,
        "tech": [("Un cahier des charges et un backlog", "Le cahier des charges fixe les objectifs et les parcours. Le backlog les découpe en user stories, chacune avec ses critères d'acceptation."),
                 ("L'essentiel d'abord", "La première version se concentre sur le dressing, la météo et les tenues. La reconnaissance des vêtements par IA et le planning de la semaine étaient prévus pour une étape suivante."),
                 ("Dix sprints", "Des fondations jusqu'à la stabilisation : compte, dressing, photos, préférences, météo, moteur de tenues, historique… Chaque sprint a un objectif clair."),
                 ("Les tests avant le code", "Les règles du moteur de tenues sont d'abord écrites sous forme de tests : à 30 °C, pas de doudoune ; une pièce au lavage n'apparaît jamais ; une pièce imposée figure dans toutes les tenues."),
                 ("Une vérification à chaque évolution", "Chaque évolution passe par une branche et une pull request. Les tests et les contrôles de qualité se lancent automatiquement avant de l'intégrer."),
                 ("Une stabilisation avant la sortie", "Le dernier sprint est consacré à la performance, au RGPD et à la recette du parcours complet, avant la publication sur Google Play.")],
    },
    "wim": {
        "name": "Wim · World Is Mine",
        "cadre": "Projet client",
        "title": "Wim, plateforme d'échange de logements · Laura Bojon",
        "desc": "Wim (World Is Mine) : plateforme d'échange de logements entre particuliers sur iOS, Android et web, avec swipe, carte et messagerie. Projet de Laura Bojon.",
        "eyebrow": "Projet client · iOS, Android et web",
        "h1": "Wim · World Is Mine",
        "lead": "Une plateforme d'échange de logements entre particuliers, sur iOS, Android et le web, que je développe pour un client, des fondations techniques jusqu'à la mise en ligne.",
        "badge": ("En développement", "badge"),
        "actions": [],
        "soon": "worldismine.fr · bientôt en ligne",
        "hero_alt": "L'application Wim : une fiche logement à Florence et le logo de l'application",
        "project_h2": "Échanger sa maison, simplement et en confiance",
        "paras": [
            "Wim met en relation des particuliers qui souhaitent échanger leur logement le temps d'un séjour. L'application mobile et le site web offrent la même expérience, en français et en anglais.",
            "Le projet s'appuie sur un cahier des charges détaillé, validé avec le client, qui décrit chaque fonctionnalité de la première version. Il me sert de référence pour planifier, développer et valider chaque étape.",
        ],
        "facts": [("Type", "Application mobile et site web"), ("Plateformes", "iOS, Android et web"),
                  ("Langues", "Français et anglais"),
                  ("Méthode", "Sprints de trois semaines, développement piloté par les tests"),
                  ("Statut", "En développement")],
        "method_first": True,
        "features_h2": "L'essentiel de la plateforme",
        "features_cols": 3,
        "features": [
            ("Swipe et matching", "<p>Quand deux personnes s'intéressent mutuellement à leurs logements, un match se crée.</p>"),
            ("Messagerie traduite", "<p>Une conversation s'ouvre après chaque match, avec traduction automatique des messages.</p>"),
            ("Confiance", "<p>Vérification d'identité et avis après chaque séjour.</p>"),
        ],
        "gallery_h2": "L'application en images",
        "gallery_cols": 3,
        "gallery": [("wim/ecran.webp", 421, 988, "La découverte des logements par swipe", False),
                    ("wim/fiche.webp", 421, 988, "La fiche d'un logement et ses disponibilités", False),
                    ("wim/conversation.webp", 421, 988, "Une conversation traduite automatiquement", False)],
        "tech_eyebrow": "Ma méthode",
        "tech_h2": "Comment je mène le projet",
        "tech_intro": "Un projet de plusieurs mois demande de l'organisation et de la rigueur. Voici comment je le conduis, du cahier des charges jusqu'à la mise en ligne.",
        "tech_cols": 3,
        "tech": [("Un cahier des charges de référence", "Il décrit chaque fonctionnalité de la première version. Une fonctionnalité est livrée quand elle le respecte, qu'elle est testée et qu'elle fonctionne sur iOS, Android et le web."),
                 ("Des sprints de trois semaines", "Un sprint par grand ensemble : comptes, logements, calendrier, recherche, matching, messagerie… Une démo à la fin de chacun permet au client de suivre l'avancement et d'ajuster les priorités."),
                 ("Les tests avant le code", "Les règles sensibles, comme le matching, les blocages et les avis, sont développées en TDD : j'écris d'abord le test, puis le code."),
                 ("Des vérifications automatiques", "À chaque envoi de code, les tests et les contrôles de qualité se lancent seuls, pour qu'une nouvelle fonctionnalité n'en casse pas une autre."),
                 ("Une base pensée pour durer", "Les règles métier sont indépendantes des outils techniques, et l'application mobile et le site partagent une base de code commune : moins de doublons, la même expérience partout."),
                 ("Une marge pour les imprévus", "Le dernier sprint est réservé aux tests finaux, aux corrections et aux vérifications RGPD avant la mise en production.")],
    },
    "freyage": {
        "name": "FreyAge",
        "cadre": "Projet personnel",
        "title": "FreyAge, site vitrine beauté près de Bordeaux · Laura Bojon",
        "desc": "FreyAge : site vitrine d'une maquilleuse et esthéticienne près de Bordeaux, avec demande de rendez-vous en ligne et cartes cadeaux payées par Stripe.",
        "eyebrow": "Projet personnel · Site web",
        "h1": "FreyAge",
        "lead": "Le site de FreyAge, activité de maquillage et de soins du visage près de Bordeaux. Je l'ai conçu et développé de A à Z, et je le fais évoluer au rythme de l'activité.",
        "badge": ("En ligne", "badge badge-live"),
        "actions": [("https://freyage.fr/", "Voir freyage.fr ↗", "btn"),
                    ("https://github.com/laurabjn/freyage-site", "Voir le code sur GitHub ↗", "btn btn-ghost")],
        "hero_alt": "Le site FreyAge sur ordinateur et sur mobile",
        "project_h2": "Présenter les prestations et faciliter la prise de rendez-vous",
        "paras": [
            "FreyAge propose du maquillage, des formules mariée et des soins du visage à Mérignac et à Bruges. Le site présente les prestations et leurs tarifs, et permet de demander un rendez-vous ou d'offrir une carte cadeau en ligne.",
            "J'ai mis en ligne une première version simple, puis je l'ai enrichie par petites étapes, en partant des besoins réels de l'activité.",
        ],
        "facts": [("Type", "Site vitrine de plusieurs pages"),
                  ("Fonctions", "Rendez-vous en ligne, cartes cadeaux, portfolio"),
                  ("Paiement", "Cartes cadeaux réglées par carte bancaire avec Stripe"),
                  ("Hébergement", "GitHub Pages"),
                  ("Méthode", "Première version rapide, puis évolutions par petites étapes"),
                  ("Statut", "En ligne")],
        "method_first": True,
        "features_h2": "L'essentiel du site",
        "features_cols": 3,
        "features": [
            ("Prestations et tarifs", "<p>Chaque prestation avec son prix et son lieu.</p>"),
            ("Demande de rendez-vous", "<p>Un formulaire en trois étapes, avec un récapitulatif de la durée et du tarif.</p>"),
            ("Cartes cadeaux", "<p>Un montant au choix, réglé en ligne par carte bancaire.</p>"),
        ],
        "gallery_h2": "Le site en images",
        "gallery_cols": 3,
        "gallery": [("freyage/accueil.webp", 476, 992, "La page d'accueil sur mobile", False),
                    ("freyage/prestations.webp", 476, 992, "Les prestations et leurs tarifs", False),
                    ("freyage/rdv.webp", 476, 992, "La demande de rendez-vous en trois étapes", False)],
        "tech_eyebrow": "Ma méthode",
        "tech_h2": "Comment je fais évoluer le site",
        "tech_intro": "Un site vitrine n'est jamais vraiment terminé : il doit suivre l'activité, rester à jour et facile à trouver sur Google.",
        "tech_cols": 3,
        "tech": [("Une première version, puis des évolutions", "Le site a été mis en ligne avec l'essentiel, puis enrichi par petites étapes. Chaque changement est publié séparément et peut être annulé facilement."),
                 ("Partir des besoins réels", "Les évolutions viennent du terrain : deux jours de préférence pour les rendez-vous, acompte pour les tarifs variables, parrainage, offres de Noël…"),
                 ("Des tarifs à jour en un seul endroit", "Prestations, tarifs et coordonnées sont réunis dans un seul fichier. Un petit outil les recopie dans chaque page, pour éviter les oublis et les doublons."),
                 ("Le référencement local dès le départ", "Des pages dédiées aux prestations clés et aux villes, des données structurées pour Google, une rubrique conseils et un suivi dans la Search Console."),
                 ("Aucun serveur à maintenir", "Un site statique, des paiements par Stripe et des formulaires par Formspree : peu de frais, peu de maintenance et aucune donnée bancaire sur le site."),
                 ("Le respect de la vie privée", "Mesure d'audience sans cookies et formulaires protégés contre le spam : aucun bandeau de cookies à accepter.")],
    },
}

TYPES = {"klotho": "Application Android", "wim": "iOS, Android et web", "freyage": "Site web"}

HEADER = """<a class="skip-link" href="#contenu">Aller au contenu</a>

<header class="site-header">
  <div class="wrap header-inner">
    <a class="brand" href="/">
      <img class="brand-logo" src="/assets/logo-lb.png" width="189" height="176" alt="">
      <span class="brand-text">
        <span class="brand-name">Laura Bojon</span>
        <span class="brand-tagline">Développeuse web et mobile</span>
      </span>
    </a>
    <button class="nav-toggle" id="nav-toggle" type="button" aria-expanded="false" aria-controls="menu">
      <span class="nav-toggle-bars" aria-hidden="true"></span>
      <span class="visually-hidden">Menu</span>
    </button>
    <nav class="site-nav" id="menu" aria-label="Navigation principale">
      <ul>
        <li><a href="/#services">Services</a></li>
        <li><a href="/#methode">Méthode</a></li>
        <li><a href="/#projets">Projets</a></li>
        <li><a href="/#apropos">À propos</a></li>
        <li><a href="/#faq">FAQ</a></li>
        <li><a href="/articles/">Articles</a></li>
      </ul>
      <a class="btn btn-small" href="/#contact">Me contacter</a>
    </nav>
  </div>
</header>"""

FOOTER = """<footer class="site-footer">
  <div class="wrap footer-inner">
    <div class="footer-top">
      <a class="footer-brand" href="/">
        <img class="brand-logo" src="/assets/logo-lb.png" width="189" height="176" alt="">
        <span class="brand-text">
          <span class="brand-name">Laura Bojon</span>
          <span class="brand-tagline">Développeuse web et mobile</span>
        </span>
      </a>
      <nav class="footer-links" aria-label="Liens de pied de page">
        <a href="https://www.linkedin.com/in/laura-bojon-86a7b41a1" target="_blank" rel="noopener">LinkedIn</a>
        <a href="https://github.com/laurabjn" target="_blank" rel="noopener">GitHub</a>
        <a href="https://g.page/r/CX-nBFtLMPElECE/review" target="_blank" rel="noopener">Laisser un avis Google</a>
        <a href="/articles/">Articles</a>
        <a href="/mentions-legales.html">Mentions légales</a>
        <a href="/conditions-generales.html">Conditions générales</a>
      </nav>
    </div>
    <div class="footer-legal">
      <p>© <span id="annee">2026</span> Laura Bojon EI · Tous droits réservés</p>
      <p>SIRET 989 670 385 00016</p>
    </div>
  </div>
</footer>

<a class="to-top" id="to-top" href="#haut" aria-label="Revenir en haut de la page">
  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 19V5M5.5 11.5 12 5l6.5 6.5"/></svg>
</a>"""


def page(slug, p):
    url = f"{BASE}/projets/{slug}/"
    assert len(p["desc"]) <= 160, (slug, len(p["desc"]))
    crumbs = {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": 1, "name": "Accueil", "item": f"{BASE}/"},
        {"@type": "ListItem", "position": 2, "name": "Projets", "item": f"{BASE}/#projets"},
        {"@type": "ListItem", "position": 3, "name": p["name"], "item": url}]}
    actions = "".join(f'\n          <a class="{c}" href="{h}" target="_blank" rel="noopener">{t}</a>' for h, t, c in p["actions"])
    actions_html = f'<div class="hero-actions">{actions}\n        </div>' if actions else f'<p class="project-soon">{p["soon"]}</p>'
    paras = "\n          ".join(f"<p>{x}</p>" for x in p["paras"])
    facts = "".join(f"\n          <div><dt>{k}</dt><dd>{v}</dd></div>" for k, v in [("Cadre", p["cadre"])] + p["facts"])
    feats = "".join(f'\n        <article class="service"><h3>{t}</h3>{body}</article>' for t, body in p["features"])
    cols_cls = " cols-3" if p["features_cols"] == 3 else ""
    figs = "".join(
        f'\n        <figure><div class="gallery-media{" is-cover" if cover else ""}"><img src="/assets/projets/{src}" width="{w}" height="{h}" alt="{cap}" loading="lazy" decoding="async"></div><figcaption>{cap}</figcaption></figure>'
        for src, w, h, cap, cover in p["gallery"])
    note = f'\n        <p class="section-intro">{p["gallery_note"]}</p>' if p.get("gallery_note") else ""
    groups = "".join(f'\n          <div class="stack-group"><p class="stack-label">{t}</p><p class="stack-text">{d}</p></div>' for t, d in p.get("tech", []))
    stack_cls = " cols-3" if p.get("tech_cols") == 3 else ""
    stack = f'\n      <div class="stack-grid{stack_cls}">{groups}\n      </div>' if groups else ""
    blocks = {
        "features": ("fonctions-titre", f"""
      <div class="section-head">
        <p class="eyebrow">Fonctionnalités</p>
        <h2 id="fonctions-titre">{p['features_h2']}</h2>
      </div>
      <div class="services-grid{cols_cls}">{feats}
      </div>"""),
        "gallery": ("captures-titre", f"""
      <div class="section-head">
        <p class="eyebrow">Captures d'écran</p>
        <h2 id="captures-titre">{p['gallery_h2']}</h2>{note}
      </div>
      <div class="gallery" style="--cols: {p['gallery_cols']}">{figs}
      </div>"""),
        "tech": ("technique-titre", f"""
      <div class="section-head">
        <p class="eyebrow">{p.get('tech_eyebrow', 'Technique')}</p>
        <h2 id="technique-titre">{p['tech_h2']}</h2>
        <p class="section-intro">{p['tech_intro']}</p>
      </div>{stack}"""),
    }
    cta = """
      <div class="cta-panel">
        <div class="cta-text">
          <h3>Un projet similaire ?</h3>
          <p>Application mobile, site ou outil sur mesure, le premier échange est gratuit et sans engagement.</p>
        </div>
        <div class="cta-actions">
          <a class="btn" href="/#contact">Parler de votre projet</a>
          <a class="btn btn-ghost" href="https://cal.com/laurabojon/appel-decouverte" target="_blank" rel="noopener">Réserver un appel gratuit</a>
        </div>
      </div>"""
    # Ordre des sections après « Le projet » : la méthode d'abord si method_first, le CTA clôt la dernière
    order = ["tech", "features", "gallery"] if p.get("method_first") else ["features", "gallery", "tech"]
    middle = "\n\n".join(
        f'  <section class="section{" section-alt" if n % 2 else ""}" aria-labelledby="{blocks[k][0]}">\n    <div class="wrap">{blocks[k][1]}{cta if n == len(order) - 1 else ""}\n    </div>\n  </section>'
        for n, k in enumerate(order))
    others = ""
    for o in (s for s in PROJECTS if s != slug):
        op = PROJECTS[o]
        others += f"""
        <a class="other-card" href="/projets/{o}/">
          <div class="thumb thumb-img"><img src="/assets/projets/{o}.webp" width="1200" height="900" alt="" loading="lazy" decoding="async"></div>
          <div class="other-body">
            <p class="project-type">{op['cadre']} · {TYPES[o]}</p>
            <h3>{op['name']}</h3>
            <span class="text-link">Découvrir le projet →</span>
          </div>
        </a>"""

    return f"""<!doctype html>
<html lang="fr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{p['title']}</title>
<meta name="description" content="{p['desc']}">
<meta name="author" content="Laura Bojon">
<meta name="robots" content="index, follow, max-image-preview:large">
<link rel="canonical" href="{url}">
<meta property="og:type" content="article">
<meta property="og:locale" content="fr_FR">
<meta property="og:site_name" content="Laura Bojon">
<meta property="og:url" content="{url}">
<meta property="og:title" content="{p['title']}">
<meta property="og:description" content="{p['desc']}">
<meta property="og:image" content="{BASE}/assets/projets/{slug}-partage.jpg">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<meta name="theme-color" content="#F8F3F0">
<link rel="icon" href="/favicon.png" type="image/png">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
<link rel="preload" href="/assets/fonts/jost-normal-300-600.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="/assets/fonts/cormorant-garamond-normal-500.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="/styles.css">
<script>document.documentElement.classList.add('js');</script>
<script src="/script.js" defer></script>
<script type="application/ld+json">
{json.dumps(crumbs, ensure_ascii=False, indent=2)}
</script>
</head>
<body id="haut">
{HEADER}

<main id="contenu">
  <nav class="breadcrumb" aria-label="Fil d'Ariane">
    <ol class="wrap">
      <li><a href="/">Accueil</a></li>
      <li><a href="/#projets">Projets</a></li>
      <li aria-current="page">{p['name']}</li>
    </ol>
  </nav>

  <section class="project-hero">
    <div class="wrap project-hero-inner">
      <div class="project-hero-text">
        <p class="eyebrow">{p['eyebrow']}</p>
        <h1>{p['h1']}</h1>
        <p class="lead">{p['lead']}</p>
        <span class="{p['badge'][1]}">{p['badge'][0]}</span>
        {actions_html}
      </div>
      <div class="project-hero-visual thumb thumb-img">
        <img src="/assets/projets/{slug}.webp" width="1200" height="900" alt="{p['hero_alt']}" fetchpriority="high" decoding="async">
      </div>
    </div>
  </section>

  <section class="section section-alt" aria-labelledby="projet-titre">
    <div class="wrap">
      <div class="about">
        <div class="about-text">
          <p class="eyebrow">Le projet</p>
          <h2 id="projet-titre">{p['project_h2']}</h2>
          {paras}
        </div>
        <dl class="fiche">{facts}
        </dl>
      </div>
    </div>
  </section>

{middle}

  <section class="section section-alt" aria-labelledby="autres-titre">
    <div class="wrap">
      <div class="section-head">
        <p class="eyebrow">Autres projets</p>
        <h2 id="autres-titre">D'autres réalisations</h2>
      </div>
      <div class="other-projects">{others}
      </div>
    </div>
  </section>
</main>

{FOOTER}
<!-- Mesure d'audience Cloudflare Web Analytics : sans cookie ni stockage dans le navigateur -->
<script type="module" src="https://static.cloudflareinsights.com/beacon.min.js" data-cf-beacon='{{"token": "bc12e6fb880b4ea7b53782594dba30e6"}}'></script>
</body>
</html>
"""


for slug, p in PROJECTS.items():
    d = f"{SITE}/projets/{slug}"
    os.makedirs(d, exist_ok=True)
    open(f"{d}/index.html", "w", encoding="utf-8", newline="\n").write(page(slug, p))
    print(f"projets/{slug}/index.html : titre {len(p['title'])} car., description {len(p['desc'])} car.")
