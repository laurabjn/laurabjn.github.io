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
        "lead": "Un dressing virtuel qui propose chaque matin une tenue adaptée à la météo, au style de chacun et à l'occasion. « Ta tenue du jour, sans y passer la matinée. »",
        "badge": ("Sur Google Play", "badge badge-live"),
        "actions": [("https://www.dressingklotho.fr/", "Voir dressingklotho.fr ↗", "btn"),
                    ("https://play.google.com/store/apps/details?id=com.laurabjn.klotho", "Google Play ↗", "btn btn-ghost"),
                    ("https://github.com/laurabjn/Klotho", "Voir le code sur GitHub ↗", "btn btn-ghost")],
        "hero_alt": "Les écrans « Ma garde-robe » et « Tenue du jour » de l'application Klotho",
        "project_h2": "Choisir sa tenue sans y passer la matinée",
        "paras": [
            "Klotho range la garde-robe à partir de simples photos, puis compose des tenues en tenant compte de la météo du jour, du style de chacun et de l'occasion : travail, rendez-vous ou soirée.",
            "L'application est gratuite, avec une offre Premium qui ajoute notamment des idées de coiffure et de maquillage assorties à chaque tenue. Elle s'accompagne d'un site de présentation avec des guides, en français et en anglais.",
            "C'est un projet personnel, que j'ai mené de l'idée jusqu'à la publication : conception, développement, abonnements et site de présentation.",
        ],
        "facts": [("Type", "Application mobile et site de présentation"), ("Plateforme", "Android"),
                  ("Technologies", "React Native et Expo"),
                  ("Modèle", "Gratuit, avec abonnement Premium"),
                  ("Vie privée", "Sans publicité, données hébergées en Europe"),
                  ("Statut", "Disponible sur Google Play")],
        "features_h2": "Un dressing qui propose, au lieu de stocker",
        "features_cols": 3,
        "features": [
            ("Un dressing en photos", "<p>Chaque pièce s'ajoute en photo. L'IA pré-remplit sa fiche : catégorie, couleurs, style et saison.</p>"),
            ("La tenue du jour", "<p>Chaque matin, une tenue adaptée à la météo de sa ville.</p>"),
            ("Pour chaque occasion", "<p>Travail, rendez-vous ou soirée. On peut imposer une pièce ou écarter celles qu'on n'aime pas.</p>"),
            ("La semaine planifiée", "<p>Les tenues se planifient dans un calendrier, avec un rappel le matin.</p>"),
            ("23 styles", "<p>Du romantique au streetwear, avec une palette de couleurs pour affiner ses goûts.</p>"),
            ("Le look complet", "<p>En Premium, une coiffure et un maquillage assortis à chaque tenue, illustrés pas à pas.</p>"),
        ],
        "gallery_h2": "L'application en images",
        "gallery_cols": 3,
        "gallery": [("klotho/k1.webp", 720, 1280, "La garde-robe, rangée par catégorie", True),
                    ("klotho/k2.webp", 720, 1280, "Des idées de tenues personnalisées", True),
                    ("klotho/k3.webp", 720, 1280, "La tenue du jour, selon la météo", True),
                    ("klotho/k4.webp", 720, 1280, "La fiche détaillée de chaque pièce", True),
                    ("klotho/k5.webp", 720, 1280, "Le calendrier des tenues de la semaine", True),
                    ("klotho/k6.webp", 720, 1280, "La création d'une tenue selon le style, l'occasion et la météo", True)],
        "tech_h2": "Ce que le projet a demandé",
        "tools": ["React Native", "Expo", "IA open source (analyse d'images)", "API météo open source", "CI/CD GitHub Actions"],
        "tech_intro": "Développée en React Native avec Expo, Klotho combine reconnaissance d'images, données météo et abonnements, dans une application qui doit rester simple à utiliser chaque matin.",
        "tech": [("IA et photos", "Analyse des photos par un modèle d'IA open source, pour remplir automatiquement la fiche de chaque vêtement."),
                 ("Météo locale", "Tenues proposées chaque matin selon la météo de la ville, grâce à une API météo open source."),
                 ("Abonnements", "Offre gratuite et Premium, avec les achats intégrés de Google Play."),
                 ("Vie privée", "Sans publicité, photos privées et données hébergées en Europe.")],
    },
    "wim": {
        "name": "Wim · World Is Mine",
        "cadre": "Projet client",
        "title": "Wim, plateforme d'échange de logements · Laura Bojon",
        "desc": "Wim (World Is Mine) : plateforme d'échange de logements entre particuliers sur iOS, Android et web, avec swipe, carte et messagerie. Projet de Laura Bojon.",
        "eyebrow": "Projet client · iOS, Android et web",
        "h1": "Wim · World Is Mine",
        "lead": "Une plateforme d'échange de logements entre particuliers : on parcourt les logements qui donnent envie, on se découvre un intérêt commun, on discute, puis on échange sa maison le temps d'un séjour.",
        "badge": ("En développement", "badge"),
        "actions": [],
        "soon": "worldismine.fr · bientôt en ligne",
        "hero_alt": "L'application Wim : une fiche logement à Florence et le logo de l'application",
        "project_h2": "Échanger sa maison, simplement et en confiance",
        "paras": [
            "Wim met en relation des personnes qui souhaitent échanger leur logement. L'application mobile et le site web offrent la même expérience, en français et en anglais.",
            "Sur mobile, la découverte des logements se fait par swipe : quand deux personnes s'intéressent mutuellement à leurs logements, un match se crée et une conversation s'ouvre. Vérification d'identité et avis après chaque séjour installent la confiance.",
        ],
        "facts": [("Type", "Application mobile et site web"), ("Plateformes", "iOS, Android et web"),
                  ("Langues", "Français et anglais"),
                  ("Technologies", "React Native, Next.js, NestJS, PostgreSQL"),
                  ("Méthode", "Sprints de trois semaines, développement piloté par les tests"),
                  ("Statut", "En développement")],
        "features_h2": "Une plateforme complète",
        "features_cols": 2,
        "features": [
            ("Swipe et matching", "<p>On aime ou on passe. Quand l'intérêt est réciproque, un match se crée, avec des dates proposées selon les disponibilités de chacun.</p>"),
            ("Recherche et carte", "<p>Recherche par lieu, capacité, dates et type de logement, avec les résultats en liste ou sur une carte interactive.</p>"),
            ("Fiches logements", "<p>Photos, équipements, possibilité d'échanger aussi sa voiture, et recommandations locales du propriétaire : restaurants, visites, conseils pratiques.</p>"),
            ("Messagerie en temps réel", "<p>Une conversation s'ouvre après chaque match, avec traduction automatique des messages, statuts de lecture et possibilité de bloquer un utilisateur.</p>"),
            ("Recommandations personnalisées", "<p>Les logements proposés tiennent compte des préférences, de la géographie, des dates et de l'historique, avec des critères réglables.</p>"),
            ("Confiance", "<p>Vérification d'identité, badge « Profil vérifié » et avis obligatoires après chaque séjour.</p>"),
            ("Abonnements et parrainage", "<p>Abonnement mensuel ou annuel avec paiement en ligne, et un système de parrainage.</p>"),
            ("Notifications et administration", "<p>Notifications pour les matchs, les messages et les rappels, et un espace d'administration pour la modération.</p>"),
        ],
        "gallery_h2": "L'application en images",
        "gallery_cols": 3,
        "gallery": [("wim/ecran.webp", 421, 988, "La découverte des logements par swipe", False),
                    ("wim/fiche.webp", 421, 988, "La fiche d'un logement et ses disponibilités", False),
                    ("wim/carte.webp", 421, 988, "La recherche sur carte", False),
                    ("wim/profil.webp", 421, 988, "Un profil vérifié et ses logements", False),
                    ("wim/conversation.webp", 421, 988, "Une conversation traduite automatiquement", False),
                    ("wim/messages.webp", 421, 988, "La liste des conversations et des demandes", False)],
        "tech_h2": "Une architecture pensée pour durer",
        "tech_intro": "Le projet est découpé en sprints de trois semaines, avec une démo à la fin de chacun. Les règles les plus sensibles, comme le matching, les blocages et les avis, sont développées en TDD : les tests d'abord, le code ensuite.",
        "tech_tags": [("Mobile et web", ["React Native", "Next.js", "Monorepo partagé"]),
                      ("Back-end", ["NestJS", "API REST", "WebSockets", "JWT"]),
                      ("Données", ["PostgreSQL", "Sauvegardes quotidiennes", "RGPD"]),
                      ("Qualité", ["Clean Architecture", "TDD (Jest, Supertest)", "Docker", "GitHub Actions"])],
    },
    "freyage": {
        "name": "FreyAge",
        "cadre": "Projet personnel",
        "title": "FreyAge, site vitrine beauté près de Bordeaux · Laura Bojon",
        "desc": "FreyAge : site vitrine d'une maquilleuse et esthéticienne près de Bordeaux, avec demande de rendez-vous en ligne et cartes cadeaux payées par Stripe.",
        "eyebrow": "Projet personnel · Site web",
        "h1": "FreyAge",
        "lead": "Le site de FreyAge, activité de maquillage à Mérignac et de soins du visage à Bruges : prestations et tarifs, portfolio, formules mariage, cartes cadeaux et demande de rendez-vous en ligne.",
        "badge": ("En ligne", "badge badge-live"),
        "actions": [("https://freyage.fr/", "Voir freyage.fr ↗", "btn"),
                    ("https://github.com/laurabjn/freyage-site", "Voir le code sur GitHub ↗", "btn btn-ghost")],
        "hero_alt": "Le site FreyAge sur ordinateur et sur mobile",
        "project_h2": "Présenter les prestations et faciliter la prise de rendez-vous",
        "paras": [
            "FreyAge propose du maquillage, des formules mariée, des cours d'auto-maquillage, des soins du visage et du plasma froid, à Mérignac et à Bruges, près de Bordeaux. Le site présente chaque prestation avec son tarif, un portfolio et les formules mariage.",
            "Les clientes peuvent demander un rendez-vous en quelques étapes, offrir une carte cadeau réglée en ligne ou commander des produits de soin. Le site change aussi d'apparence au fil des fêtes et des saisons.",
            "C'est un projet personnel, dont j'ai conçu et développé le site de A à Z, du design jusqu'au paiement en ligne.",
        ],
        "facts": [("Type", "Site vitrine de plusieurs pages"),
                  ("Fonctions", "Rendez-vous en ligne, cartes cadeaux, portfolio"),
                  ("Paiement", "Cartes cadeaux réglées par carte bancaire avec Stripe"),
                  ("Hébergement", "GitHub Pages"),
                  ("Statut", "En ligne")],
        "features_h2": "Un site qui accompagne jusqu'au rendez-vous",
        "features_cols": 3,
        "features": [
            ("Prestations et tarifs", "<p>Un catalogue clair par catégorie (maquillage, cours, soins du visage, plasma froid, press-on), avec le prix et le lieu de chaque prestation.</p>"),
            ("Demande de rendez-vous", "<p>Un formulaire en trois étapes : la prestation, jusqu'à deux jours de préférence, puis les coordonnées, avec un récapitulatif de la durée et du tarif.</p>"),
            ("Cartes cadeaux", "<p>Montant personnalisable, paiement en ligne par carte bancaire et code envoyé par e-mail, valable six mois.</p>"),
            ("Formules mariage", "<p>Deux formules détaillées avec leurs options, et une demande de devis dédiée.</p>"),
            ("Thèmes saisonniers", "<p>Couleurs et décorations changent automatiquement pour Noël, la Saint-Valentin, la fête des mères, Halloween et chaque saison.</p>"),
            ("Référencement local", "<p>Pages dédiées aux soins du visage à Bruges, au plasma froid et au maquillage pour toutes les carnations, FAQ et lien vers les avis Google.</p>"),
        ],
        "gallery_h2": "Le site en images",
        "gallery_cols": 3,
        "gallery": [("freyage/accueil.webp", 476, 992, "La page d'accueil sur mobile", False),
                    ("freyage/prestations.webp", 476, 992, "Les prestations et leurs tarifs", False),
                    ("freyage/mariage.webp", 476, 992, "Les formules mariage", False),
                    ("freyage/rdv.webp", 476, 992, "La demande de rendez-vous en trois étapes", False),
                    ("freyage/carte-cadeau.webp", 476, 992, "L'offre de cartes cadeaux", False),
                    ("freyage/portfolio.webp", 476, 992, "Le portfolio, filtrable par style", False)],
        "tech_h2": "Ce que le projet a demandé",
        "tools": ["HTML / CSS", "JavaScript", "Stripe", "Formspree", "Cloudflare Turnstile", "Cloudflare Web Analytics", "GitHub Pages"],
        "tech_intro": "Un site rapide et facile à faire évoluer, qui reçoit des demandes de rendez-vous et des paiements sans serveur à maintenir.",
        "tech": [("Rendez-vous", "Formulaire en plusieurs étapes, envoyé par Formspree et protégé par le captcha Cloudflare Turnstile."),
                 ("Paiement", "Cartes cadeaux réglées en ligne avec Stripe, sans aucune donnée bancaire sur le site."),
                 ("Performance", "Site statique en HTML, CSS et JavaScript, hébergé sur GitHub Pages."),
                 ("Suivi", "Mesure d'audience sans cookies avec Cloudflare Web Analytics.")],
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
    if "tech_tags" in p:
        groups = "".join(f'\n          <div class="stack-group"><p class="stack-label">{t}</p><ul class="tags">' + "".join(f"<li>{x}</li>" for x in tags) + "</ul></div>" for t, tags in p["tech_tags"])
    else:
        groups = "".join(f'\n          <div class="stack-group"><p class="stack-label">{t}</p><p class="stack-text">{d}</p></div>' for t, d in p["tech"])
    tools = ""
    if p.get("tools"):
        tools = ('\n      <div class="tools"><p class="stack-label">Outils utilisés</p><ul class="tags">'
                 + "".join(f"<li>{t}</li>" for t in p["tools"]) + "</ul></div>")
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

  <section class="section" aria-labelledby="fonctions-titre">
    <div class="wrap">
      <div class="section-head">
        <p class="eyebrow">Fonctionnalités</p>
        <h2 id="fonctions-titre">{p['features_h2']}</h2>
      </div>
      <div class="services-grid{cols_cls}">{feats}
      </div>
    </div>
  </section>

  <section class="section section-alt" aria-labelledby="captures-titre">
    <div class="wrap">
      <div class="section-head">
        <p class="eyebrow">Captures d'écran</p>
        <h2 id="captures-titre">{p['gallery_h2']}</h2>{note}
      </div>
      <div class="gallery" style="--cols: {p['gallery_cols']}">{figs}
      </div>
    </div>
  </section>

  <section class="section" aria-labelledby="technique-titre">
    <div class="wrap">
      <div class="section-head">
        <p class="eyebrow">Technique</p>
        <h2 id="technique-titre">{p['tech_h2']}</h2>
        <p class="section-intro">{p['tech_intro']}</p>
      </div>
      <div class="stack-grid">{groups}
      </div>{tools}
      <div class="cta-panel">
        <div class="cta-text">
          <h3>Un projet similaire ?</h3>
          <p>Application mobile, site ou outil sur mesure, le premier échange est gratuit et sans engagement.</p>
        </div>
        <div class="cta-actions">
          <a class="btn" href="/#contact">Parler de votre projet</a>
          <a class="btn btn-ghost" href="https://cal.com/laurabojon/appel-decouverte" target="_blank" rel="noopener">Réserver un appel gratuit</a>
        </div>
      </div>
    </div>
  </section>

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
