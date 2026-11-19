"""Génère les pages service (/services/…) et les articles (/articles/…) du site."""
import json, os, re, sys

SITE = sys.argv[1]
BASE = "https://laurabojon.fr"
DATE_ISO, DATE_FR = "2026-11-19", "19 novembre 2026"
TVA = "Prix nets : TVA non applicable, article 293 B du CGI."

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

PROJ = {
    "klotho": ("Klotho", "Projet personnel · Application Android"),
    "wim": ("Wim · World Is Mine", "Projet client · iOS, Android et web"),
    "freyage": ("FreyAge", "Projet personnel · Site web"),
}


def head(title, desc, path, og_image, og_type, ld):
    assert len(title) <= 60, (title, len(title))
    assert len(desc) <= 155, (desc, len(desc))
    url = f"{BASE}{path}"
    lds = "\n".join(f'<script type="application/ld+json">\n{json.dumps(x, ensure_ascii=False, indent=2)}\n</script>' for x in ld)
    return f"""<!doctype html>
<html lang="fr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{title}</title>
<meta name="description" content="{desc}">
<meta name="author" content="Laura Bojon">
<meta name="robots" content="index, follow, max-image-preview:large">
<link rel="canonical" href="{url}">
<meta property="og:type" content="{og_type}">
<meta property="og:locale" content="fr_FR">
<meta property="og:site_name" content="Laura Bojon">
<meta property="og:url" content="{url}">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:image" content="{BASE}{og_image}">
<meta name="twitter:card" content="summary_large_image">
<meta name="theme-color" content="#F8F3F0">
<link rel="icon" href="/favicon.png" type="image/png">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
<link rel="preload" href="/assets/fonts/jost-normal-300-600.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="/assets/fonts/cormorant-garamond-normal-500.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="/styles.css">
<script>document.documentElement.classList.add('js');</script>
<script src="/script.js" defer></script>
{lds}
</head>
<body id="haut">
{HEADER}

<main id="contenu">"""


def tail():
    return f"""</main>

{FOOTER}
<!-- Mesure d'audience Cloudflare Web Analytics : sans cookie ni stockage dans le navigateur -->
<script type="module" src="https://static.cloudflareinsights.com/beacon.min.js" data-cf-beacon='{{"token": "bc12e6fb880b4ea7b53782594dba30e6"}}'></script>
</body>
</html>
"""


def crumbs(items):
    """items : [(nom, chemin)] ; le dernier est la page courante."""
    ld = {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": i + 1, "name": n, "item": f"{BASE}{p}"} for i, (n, p) in enumerate(items)]}
    lis = "".join(f'\n      <li><a href="{p}">{n}</a></li>' for n, p in items[:-1])
    html = f"""  <nav class="breadcrumb" aria-label="Fil d'Ariane">
    <ol class="wrap">{lis}
      <li aria-current="page">{items[-1][0]}</li>
    </ol>
  </nav>"""
    return ld, html


def project_cards(slugs):
    out = ""
    for s in slugs:
        name, typ = PROJ[s]
        out += f"""
        <a class="other-card" href="/projets/{s}/">
          <div class="thumb thumb-img"><img src="/assets/projets/{s}.webp" width="1200" height="900" alt="" loading="lazy" decoding="async"></div>
          <div class="other-body">
            <p class="project-type">{typ}</p>
            <h3>{name}</h3>
            <span class="text-link">Découvrir le projet →</span>
          </div>
        </a>"""
    return out


CTA = """      <div class="cta-panel">
        <div class="cta-text">
          <h3>{titre}</h3>
          <p>{texte}</p>
        </div>
        <div class="cta-actions">
          <a class="btn" href="/#contact">Demander un devis gratuit</a>
          <a class="btn btn-ghost" href="https://cal.com/laurabojon/appel-decouverte" target="_blank" rel="noopener">Réserver un appel gratuit</a>
        </div>
      </div>"""

# ---------------------------------------------------------------- Services

SERVICES = {
    "creation-site-internet": {
        "nav": "Création de site internet",
        "title": "Création de site internet à Bordeaux · Laura Bojon",
        "desc": "Création de site vitrine sur mesure à Bordeaux et Mérignac : rapide, adapté au mobile et bien référencé. À partir de 900 €, devis gratuit.",
        "h1": "Création de site internet",
        "lead": "Un site vitrine rapide, lisible sur mobile et bien référencé, qui présente votre activité et vous amène des contacts. Pour les particuliers et les professionnels de Bordeaux, de Mérignac et de toute la Gironde.",
        "price": "900 €", "price_label": "À partir de", "price_num": 900,
        "price_text": "Le prix dépend du nombre de pages et des fonctionnalités. La maintenance est possible ensuite à partir de 40 € par mois.",
        "offer_h2": "Ce que comprend votre site",
        "offer": [
            ("Un design sur mesure", "Pensé pour votre activité et votre image, plutôt qu'un modèle générique."),
            ("Adapté au mobile", "Lisible et agréable sur téléphone, tablette et ordinateur."),
            ("Référencement de base", "Titres, descriptions, données structurées, sitemap et déclaration à Google Search Console."),
            ("Formulaire de contact", "Protégé contre les robots, avec la réception des demandes par e-mail."),
            ("Pages obligatoires", "Mentions légales et informations RGPD, indispensables pour un site professionnel."),
            ("Mise en ligne", "Nom de domaine, hébergement et HTTPS configurés pour vous."),
        ],
        "offer_note": "Selon vos besoins, j'ajoute aussi la prise de rendez-vous, le paiement en ligne, des cartes cadeaux, une galerie, un blog ou une version anglaise.",
        "steps": [
            ("Échange", "Vous me présentez votre activité et vos objectifs. Je vous envoie un devis détaillé et gratuit."),
            ("Maquette", "Je propose l'organisation des pages et le design. Vous validez avant le développement."),
            ("Développement", "Je réalise le site et vous partage une version en ligne à tester."),
            ("Mise en ligne", "Je publie le site, le déclare à Google et vous montre comment le faire vivre."),
        ],
        "projects": ["freyage"],
        "faq": [
            ("Combien de temps faut-il pour créer un site vitrine ?", "Comptez en général 2 à 4 semaines, selon le nombre de pages et la rapidité des échanges sur les textes et les photos."),
            ("Qui fournit les textes et les photos ?", "Vous connaissez votre activité mieux que personne : vous fournissez les informations et les photos, je vous conseille sur ce qui fonctionne bien sur le web et je les mets en forme."),
            ("Le nom de domaine et l'hébergement sont-ils compris ?", "Je m'occupe de leur configuration. Le nom de domaine reste à votre nom et coûte quelques euros par an pour un .fr. Pour un site vitrine, l'hébergement peut même être gratuit."),
            ("Pourrai-je modifier mon site moi-même ?", "Oui. Selon vos besoins, je mets en place un outil simple pour modifier vos contenus et je vous forme à son utilisation."),
        ],
        "service_type": "Création de site internet",
    },
    "application-mobile": {
        "nav": "Application mobile",
        "title": "Développement d'application mobile à Bordeaux · Laura Bojon",
        "desc": "Applications mobiles iOS et Android en React Native, de la maquette à la publication sur les stores. À Bordeaux et à distance, à partir de 4 500 €.",
        "h1": "Développement d'application mobile",
        "lead": "Une application iOS et Android développée en React Native, avec une seule base de code, de la maquette jusqu'à la publication sur l'App Store et Google Play.",
        "price": "4 500 €", "price_label": "À partir de", "price_num": 4500,
        "price_text": "Pour une application simple, publiée sur les deux stores. Le devis détaille chaque fonctionnalité. Les comptes développeur restent à votre nom : 25 $ une fois chez Google, 99 $ par an chez Apple.",
        "offer_h2": "Ce que je développe pour vous",
        "offer": [
            ("iOS et Android", "Une seule base de code en React Native avec Expo, pour les deux plateformes."),
            ("Maquettes des écrans", "Les parcours et les écrans clés, validés avec vous avant le développement."),
            ("Comptes et données en ligne", "Inscription, connexion et données synchronisées entre les appareils."),
            ("Notifications", "Des notifications push envoyées au bon moment, même quand l'application est fermée."),
            ("Paiement et abonnements", "Paiement par carte avec Stripe ou achats intégrés aux stores."),
            ("Publication sur les stores", "Fiches, captures d'écran, soumission et suivi jusqu'à la validation par Apple et Google."),
        ],
        "offer_note": "Carte et géolocalisation, messagerie en temps réel, intelligence artificielle : ces fonctionnalités sont déjà dans mes projets et peuvent l'être dans le vôtre.",
        "steps": [
            ("Échange", "Nous définissons ensemble les fonctionnalités prioritaires. Je vous envoie un devis détaillé."),
            ("Maquettes", "Je dessine les écrans clés et les parcours. Vous validez avant le développement."),
            ("Développement", "Je développe par sprints de trois semaines, avec une version à tester à la fin de chacun."),
            ("Publication", "Je publie l'application sur l'App Store et Google Play, puis j'assure le suivi."),
        ],
        "projects": ["klotho", "wim"],
        "faq": [
            ("Pourquoi React Native plutôt que deux applications natives ?", "Une seule base de code pour iOS et Android réduit le budget et les délais, et les deux versions évoluent en même temps. <a href=\"/articles/react-native-ios-android/\">J'explique tout dans cet article.</a>"),
            ("Combien de temps faut-il ?", "De quelques mois à près d'un an selon les fonctionnalités. Le devis détaille le planning, sprint par sprint."),
            ("L'application m'appartient-elle ?", "Oui. Une fois le projet réglé, vous recevez le code source et la documentation, et les comptes des stores sont à votre nom."),
        ],
        "service_type": "Développement d'application mobile",
    },
    "application-web": {
        "nav": "Application web",
        "title": "Application web sur mesure à Bordeaux · Laura Bojon",
        "desc": "Applications web sur mesure à Bordeaux : espace client, réservation, back-office, tableaux de bord. Développées en Next.js et NestJS, sur devis.",
        "h1": "Application web sur mesure",
        "lead": "Espace client, outil de réservation, back-office ou tableau de bord : des outils en ligne pensés pour votre activité, qui vous font gagner du temps au quotidien.",
        "price": "Sur devis", "price_label": "", "price_num": None,
        "price_text": "Chaque outil est différent. Après un premier échange gratuit, je vous envoie une estimation détaillée, découpée par fonctionnalité.",
        "offer_h2": "Ce que je développe pour vous",
        "offer": [
            ("Espace client", "Vos clients retrouvent leurs informations, leurs documents ou leurs commandes."),
            ("Réservation et paiement", "Prise de rendez-vous, réservation de créneaux et paiement en ligne."),
            ("Back-office", "Un espace simple pour gérer vos contenus, vos commandes et vos utilisateurs."),
            ("Tableaux de bord", "Vos chiffres clés réunis au même endroit, mis à jour en continu."),
            ("Connexion à vos outils", "Paiement, e-mails, agendas : votre application dialogue avec les services que vous utilisez."),
            ("Sécurité et RGPD", "Authentification, sauvegardes et données protégées dès la conception."),
        ],
        "offer_note": "Côté technique : Next.js et React pour l'interface, NestJS et PostgreSQL pour le serveur, avec des tests automatisés et un déploiement continu.",
        "steps": [
            ("Échange", "Nous partons de vos usages réels pour définir l'outil. Je vous envoie un devis détaillé."),
            ("Conception", "Je propose les écrans et l'organisation des données. Vous validez avant le développement."),
            ("Développement", "Je développe par sprints de trois semaines, en écrivant les tests avant le code."),
            ("Mise en ligne", "Je déploie l'application, vous forme à son utilisation et reste disponible pour la faire évoluer."),
        ],
        "projects": ["wim", "freyage"],
        "faq": [
            ("Application web ou application mobile ?", "Une application web s'utilise depuis un navigateur, sur ordinateur comme sur mobile, sans passer par les stores. C'est souvent le meilleur choix pour un outil métier ou un espace client. Une application mobile est utile quand vos utilisateurs s'en servent au quotidien sur leur téléphone."),
            ("Pourrai-je faire évoluer l'outil plus tard ?", "Oui. Je l'organise pour qu'il reste facile à faire évoluer, avec des tests automatisés qui évitent de casser l'existant à chaque nouveauté."),
            ("Où sont hébergées les données ?", "Chez un hébergeur choisi ensemble selon votre projet, en Europe si vous le souhaitez."),
        ],
        "service_type": "Développement d'application web",
    },
    "maintenance": {
        "nav": "Maintenance",
        "title": "Maintenance de site internet à Bordeaux · Laura Bojon",
        "desc": "Maintenance de site internet et d'application : mises à jour, sauvegardes, sécurité et petites évolutions. À Bordeaux et à distance, dès 40 € par mois.",
        "h1": "Maintenance de site et d'application",
        "lead": "Mises à jour de sécurité, sauvegardes, corrections et petites évolutions : votre site ou votre application reste fiable, rapide et à jour après sa mise en ligne.",
        "price": "40 € par mois", "price_label": "À partir de", "price_num": 40,
        "price_text": "Pour un site vitrine. Pour une application ou un site plus complet, le prix dépend du temps nécessaire et figure au devis. Sans engagement : résiliable à tout moment avec un mois de préavis.",
        "offer_h2": "Ce que comprend la maintenance",
        "offer": [
            ("Mises à jour de sécurité", "Les bibliothèques et les services utilisés restent à jour, pour fermer les failles connues."),
            ("Sauvegardes", "Des sauvegardes régulières, et une restauration rapide en cas de problème."),
            ("Vérifications régulières", "Je vérifie que le site reste en ligne, rapide, et que le formulaire de contact fonctionne."),
            ("Petites modifications", "Textes, images, tarifs, horaires : vos contenus évoluent, dans la limite du temps inclus."),
            ("Compatibilité mobile", "Pour une application, les mises à jour nécessaires aux nouvelles versions d'iOS et d'Android."),
            ("Conseils", "Référencement, nouvelles fonctionnalités, outils : je vous aide à faire évoluer votre projet."),
        ],
        "offer_note": "Votre site ou votre application n'a pas été réalisé par moi ? Je peux aussi en reprendre la maintenance, après un premier état des lieux.",
        "steps": [
            ("État des lieux", "Je fais le point sur votre site ou votre application : technologies, hébergement, sauvegardes, points à corriger."),
            ("Formule", "Je vous propose une formule mensuelle, avec ce qu'elle comprend précisément."),
            ("Suivi", "Mises à jour, sauvegardes et vérifications ont lieu chaque mois, sans que vous ayez à y penser."),
            ("Évolutions", "Une modification à faire ? Elle est réalisée dans le temps inclus, ou chiffrée à part si elle est plus importante."),
        ],
        "projects": ["freyage", "klotho"],
        "faq": [
            ("Que se passe-t-il si mon site tombe en panne ?", "Je le remets en ligne au plus vite, à partir des sauvegardes si nécessaire. Avec un suivi régulier, les problèmes sont souvent repérés avant que vos visiteurs ne les voient."),
            ("La maintenance est-elle obligatoire ?", "Non. Votre site fonctionne sans maintenance, mais les mises à jour de sécurité et les sauvegardes évitent les mauvaises surprises, surtout avec un formulaire ou un paiement en ligne."),
            ("Puis-je arrêter quand je veux ?", "Oui. La maintenance est sans engagement : vous pouvez l'arrêter à tout moment, avec un mois de préavis."),
            ("Vous occupez-vous d'un site que vous n'avez pas créé ?", "Oui, après un état des lieux pour vérifier qu'il peut être maintenu dans de bonnes conditions."),
        ],
        "service_type": "Maintenance de site internet et d'application",
    },
}


def service_page(slug, s):
    path = f"/services/{slug}/"
    ld_c, crumb = crumbs([("Accueil", "/"), ("Services", "/#services"), (s["nav"], path)])
    service_ld = {"@context": "https://schema.org", "@type": "Service", "serviceType": s["service_type"], "name": s["h1"],
                  "description": s["desc"], "url": f"{BASE}{path}", "provider": {"@id": f"{BASE}/#activite"},
                  "areaServed": [{"@type": "City", "name": "Bordeaux"}, {"@type": "City", "name": "Mérignac"},
                                 {"@type": "AdministrativeArea", "name": "Gironde"}, {"@type": "Country", "name": "France"}]}
    if s["price_num"]:
        service_ld["offers"] = {"@type": "Offer", "priceCurrency": "EUR",
                                "priceSpecification": {"@type": "PriceSpecification", "minPrice": s["price_num"], "priceCurrency": "EUR"}}
    price_html = (f'<p class="price-label">{s["price_label"]}</p><p class="price-big">{s["price"]}</p>' if s["price_label"]
                  else f'<p class="price-big">{s["price"]}</p>')
    offer = "".join(f'\n        <article class="service"><h3>{t}</h3><p>{d}</p></article>' for t, d in s["offer"])
    steps = "".join(f'\n        <li class="step"><span class="step-num">Étape {i}</span><h3>{t}</h3><p>{d}</p></li>' for i, (t, d) in enumerate(s["steps"], 1))
    faq = "".join(f'\n        <details class="faq-item"><summary>{q}</summary><p>{a}</p></details>' for q, a in s["faq"])
    n = len(s["projects"])
    real_h2 = "Un exemple de réalisation" if n == 1 else "Des exemples de réalisations"
    return head(s["title"], s["desc"], path, f"/assets/partage.jpg", "website", [ld_c, service_ld]) + f"""
{crumb}

  <section class="project-hero">
    <div class="wrap project-hero-inner">
      <div class="project-hero-text">
        <p class="eyebrow">Service</p>
        <h1>{s['h1']}</h1>
        <p class="lead">{s['lead']}</p>
        <div class="hero-actions">
          <a class="btn" href="/#contact">Demander un devis gratuit</a>
          <a class="btn btn-ghost" href="https://cal.com/laurabojon/appel-decouverte" target="_blank" rel="noopener">Réserver un appel gratuit</a>
        </div>
      </div>
      <aside class="price-panel" aria-label="Tarif">
        {price_html}
        <p>{s['price_text']}</p>
        <p class="price-note">{TVA} <a href="/conditions-generales.html">Conditions générales</a></p>
      </aside>
    </div>
  </section>

  <section class="section section-alt" aria-labelledby="offre-titre">
    <div class="wrap">
      <div class="section-head">
        <p class="eyebrow">L'offre</p>
        <h2 id="offre-titre">{s['offer_h2']}</h2>
      </div>
      <div class="services-grid cols-3">{offer}
      </div>
      <p class="section-intro">{s['offer_note']}</p>
    </div>
  </section>

  <section class="section" aria-labelledby="etapes-titre">
    <div class="wrap">
      <div class="section-head">
        <p class="eyebrow">Méthode</p>
        <h2 id="etapes-titre">Comment se déroule le projet</h2>
      </div>
      <ol class="steps">{steps}
      </ol>
    </div>
  </section>

  <section class="section section-alt" id="realisations" aria-labelledby="real-titre">
    <div class="wrap">
      <div class="section-head">
        <p class="eyebrow">Réalisations</p>
        <h2 id="real-titre">{real_h2}</h2>
      </div>
      <div class="other-projects{' is-single' if n == 1 else ''}">{project_cards(s['projects'])}
      </div>
    </div>
  </section>

  <section class="section" aria-labelledby="faq-titre">
    <div class="wrap faq">
      <div class="section-head">
        <p class="eyebrow">Questions fréquentes</p>
        <h2 id="faq-titre">Vos questions</h2>
        <p class="section-intro">Une autre question ? <a href="/#contact">Écrivez-moi directement.</a></p>
      </div>
      <div class="faq-list">{faq}
      </div>
    </div>
  </section>

  <section class="section section-alt" aria-label="Contact">
    <div class="wrap">
{CTA.format(titre="Parlons de votre projet", texte="Le premier échange est gratuit et sans engagement. Je vous réponds sous 48 h ouvrées.")}
    </div>
  </section>
""" + tail()


# ---------------------------------------------------------------- Articles

ARTICLES = {
    "prix-site-vitrine": {
        "title": "Combien coûte un site vitrine en 2026 ? · Laura Bojon",
        "h1": "Combien coûte un site vitrine en 2026 ?",
        "desc": "Prix d'un site vitrine : ce qui fait varier le budget, les coûts à prévoir chaque année et les tarifs d'une développeuse freelance à Bordeaux.",
        "lead": "Entre un site fait soi-même et un site réalisé par une agence, les écarts de prix sont énormes. Voici ce qui fait varier le prix d'un site vitrine, et ce qu'il faut prévoir chaque année.",
        "body": """
<h2>Trois façons de créer un site vitrine</h2>
<p><strong>Le faire soi-même</strong> avec un outil en ligne (Wix, Squarespace, WordPress.com…). On paie un abonnement, mais on y passe beaucoup de temps, et le résultat dépend de son aisance avec le design, les textes et le référencement.</p>
<p><strong>Faire appel à une freelance.</strong> Vous avez une seule interlocutrice du début à la fin, un site conçu pour votre activité et un budget plus accessible qu'en agence.</p>
<p><strong>Passer par une agence.</strong> Une équipe complète (chef de projet, designer, développeurs) adaptée aux gros projets, avec un budget en conséquence.</p>

<h2>Ce qui fait varier le prix</h2>
<ul>
<li><strong>Le nombre de pages</strong> : une page unique bien construite ou un site de dix pages ne demandent pas le même travail.</li>
<li><strong>Le design</strong> : un design sur mesure prend plus de temps qu'un modèle adapté, mais il vous distingue.</li>
<li><strong>Les fonctionnalités</strong> : prise de rendez-vous, paiement en ligne, cartes cadeaux, blog ou version anglaise ajoutent du développement.</li>
<li><strong>Les contenus</strong> : des textes et des photos prêts à l'emploi font gagner du temps ; leur rédaction ou leur retouche en demande.</li>
<li><strong>Le référencement</strong> : au-delà des bases, travailler des pages ciblées sur votre ville ou vos services est un vrai chantier.</li>
</ul>

<h2>Les coûts à prévoir chaque année</h2>
<ul>
<li><strong>Le nom de domaine</strong> : quelques euros par an pour un .fr, à renouveler.</li>
<li><strong>L'hébergement</strong> : gratuit pour un site statique bien conçu, quelques euros par mois pour un site plus lourd.</li>
<li><strong>La maintenance</strong> : facultative, elle couvre les mises à jour, les sauvegardes et les petites retouches.</li>
<li><strong>L'adresse e-mail professionnelle</strong> : souvent incluse avec le nom de domaine.</li>
</ul>

<h2>Mes tarifs</h2>
<p>Chez moi, un site vitrine démarre à <strong>900 €</strong>. Ce prix comprend un design sur mesure, un site adapté au mobile, un formulaire de contact protégé, les pages obligatoires, le référencement de base et la mise en ligne. La maintenance est possible ensuite à partir de <strong>40 € par mois</strong>. Prix nets : TVA non applicable, article 293 B du CGI.</p>
<p>Pour un exemple concret, le <a href="/projets/freyage/">site de FreyAge</a> réunit prestations, portfolio, prise de rendez-vous et cartes cadeaux payées en ligne.</p>

<h2>Bien préparer son budget</h2>
<ul>
<li>Listez les pages dont vous avez besoin, et les informations à mettre sur chacune.</li>
<li>Notez deux ou trois sites que vous aimez, et ce qui vous plaît chez eux.</li>
<li>Rassemblez vos textes, votre logo et vos photos.</li>
<li>Classez les fonctionnalités entre indispensables et « plus tard » : un site peut évoluer après sa mise en ligne.</li>
</ul>
<p>Vous avez un projet ? <a href="/services/creation-site-internet/">Découvrez l'offre de création de site internet</a> ou demandez-moi un devis gratuit.</p>
""",
    },
    "mentions-obligatoires-site-professionnel": {
        "title": "Les mentions obligatoires d'un site pro · Laura Bojon",
        "h1": "Les mentions obligatoires d'un site professionnel",
        "desc": "Mentions légales, RGPD, cookies, CGV, médiateur : la liste des informations obligatoires sur le site d'une entreprise ou d'un indépendant en France.",
        "lead": "Un site professionnel doit afficher certaines informations, et les oublier peut coûter cher. Voici la liste, avec les points qui concernent particulièrement les indépendants.",
        "body": """
<h2>Les mentions légales</h2>
<p>La loi pour la confiance dans l'économie numérique impose à tout site professionnel d'indiquer :</p>
<ul>
<li><strong>Qui édite le site</strong> : nom et prénom pour une entreprise individuelle, dénomination sociale pour une société.</li>
<li><strong>L'adresse</strong> de l'entreprise, une <strong>adresse e-mail</strong> et un <strong>numéro de téléphone</strong>.</li>
<li><strong>Le numéro d'immatriculation</strong> (SIREN, et RCS selon l'activité) et, le cas échéant, le numéro de TVA intracommunautaire.</li>
<li><strong>Le directeur ou la directrice de la publication.</strong></li>
<li><strong>L'hébergeur</strong> du site : son nom, son adresse et son téléphone.</li>
</ul>

<h2>La politique de confidentialité</h2>
<p>Dès que votre site recueille des données personnelles, ne serait-ce qu'avec un formulaire de contact, le RGPD vous oblige à informer vos visiteurs :</p>
<ul>
<li>à quoi servent les données et sur quelle base légale vous les utilisez ;</li>
<li>combien de temps vous les conservez et qui les reçoit (par exemple le service qui envoie vos formulaires) ;</li>
<li>quels sont leurs droits (accès, rectification, effacement, opposition…) et comment les exercer ;</li>
<li>qu'ils peuvent adresser une réclamation à la CNIL.</li>
</ul>

<h2>Les cookies</h2>
<p>Les cookies qui ne sont pas indispensables au fonctionnement du site, notamment publicitaires, demandent le consentement préalable du visiteur, d'où les bandeaux. Certains outils de mesure d'audience sans cookies, ou configurés selon les recommandations de la CNIL, permettent de s'en passer. C'est le choix le plus simple pour un site vitrine.</p>

<h2>Si vous vendez à des particuliers</h2>
<ul>
<li><strong>Des conditions générales de vente</strong> accessibles avant toute commande.</li>
<li><strong>Des prix TTC</strong>, ou accompagnés de la mention « TVA non applicable, article 293 B du CGI » si vous êtes en franchise en base.</li>
<li><strong>Le droit de rétractation de 14 jours</strong> pour les contrats conclus à distance, sauf exceptions prévues par la loi.</li>
<li><strong>Les coordonnées d'un médiateur de la consommation</strong>, auquel tout professionnel qui vend à des particuliers doit adhérer.</li>
</ul>

<h2>Que risque-t-on ?</h2>
<p>Ne pas afficher les mentions légales est puni par la loi, jusqu'à un an d'emprisonnement et 75 000 € d'amende pour une personne physique. La CNIL peut aussi sanctionner les manquements au RGPD, et la DGCCRF contrôle l'information due aux consommateurs. En pratique, mettre son site en règle prend peu de temps : autant le faire dès la mise en ligne.</p>

<h2>La liste à vérifier</h2>
<ul>
<li>Une page « Mentions légales » complète, accessible depuis toutes les pages.</li>
<li>Une politique de confidentialité si vous recueillez des données.</li>
<li>Un bandeau de consentement seulement si vous utilisez des cookies non essentiels.</li>
<li>Des CGV, des prix clairs et un médiateur si vous vendez à des particuliers.</li>
</ul>
<p>Tous les sites que je réalise intègrent ces pages dès le départ. <a href="/services/creation-site-internet/">Découvrez l'offre de création de site internet.</a></p>
<p class="article-disclaimer">Cet article donne des repères généraux. Pour une situation particulière, rapprochez-vous d'un professionnel du droit.</p>
""",
    },
    "react-native-ios-android": {
        "title": "React Native : une appli pour iOS et Android · Laura Bojon",
        "h1": "React Native : une seule application pour iOS et Android",
        "desc": "Comment React Native permet de développer une seule application pour iOS et Android, ses avantages, ses limites et quand le choisir.",
        "lead": "Faut-il développer deux applications, une pour l'iPhone et une pour Android ? Avec React Native, une seule base de code suffit dans la plupart des cas. Voici comment ça marche, et quand ce n'est pas le bon choix.",
        "body": """
<h2>Natif ou multiplateforme</h2>
<p>Une application <strong>native</strong> est écrite dans le langage propre à chaque système : Swift pour iOS, Kotlin pour Android. Il faut donc deux applications, deux bases de code, et souvent deux équipes.</p>
<p>Une application <strong>multiplateforme</strong> est écrite une seule fois, puis fonctionne sur les deux systèmes. React Native est l'une des solutions les plus répandues pour y parvenir.</p>

<h2>React Native en deux mots</h2>
<p>React Native est un framework open source créé par Meta. On y développe en JavaScript ou en TypeScript, avec React, et l'application affiche de vrais composants natifs : ce n'est pas une page web glissée dans une application.</p>
<p><strong>Expo</strong> complète React Native avec des outils pour développer, tester, publier sur les stores et diffuser certaines mises à jour plus rapidement.</p>

<h2>Les avantages pour votre projet</h2>
<ul>
<li><strong>Un budget et des délais réduits</strong> : une seule base de code au lieu de deux.</li>
<li><strong>Les mêmes fonctionnalités en même temps</strong> sur iPhone et sur Android.</li>
<li><strong>Des évolutions plus simples</strong> : une correction profite immédiatement aux deux versions.</li>
<li><strong>Un écosystème riche</strong> : paiement, notifications, cartes, connexion à Firebase ou à votre propre serveur.</li>
</ul>

<h2>Ses limites</h2>
<p>Pour une application qui repose sur des fonctions très avancées du téléphone (réalité augmentée poussée, jeux 3D exigeants, matériel très spécifique), le natif reste parfois préférable. Certaines intégrations demandent aussi un peu de développement natif en complément. Pour la grande majorité des applications (réservation, commerce, réseau social, outil métier), React Native offre d'excellentes performances.</p>

<h2>Ce que j'en fais au quotidien</h2>
<p>Je développe toutes mes applications en React Native :</p>
<ul>
<li><a href="/projets/klotho/">Klotho</a> : un dressing virtuel avec analyse des photos par IA, météo et abonnements ;</li>
<li><a href="/projets/wim/">Wim</a> : une plateforme d'échange de logements, disponible sur iOS, Android et le web, avec du code partagé entre l'application et le site.</li>
</ul>

<h2>En résumé</h2>
<p>Si votre application doit exister sur iPhone et sur Android, React Native est souvent le choix le plus raisonnable : moins cher, plus rapide à livrer et plus simple à faire évoluer. <a href="/services/application-mobile/">Découvrez l'offre de développement d'application mobile.</a></p>
""",
    },
    "prix-application-mobile": {
        "title": "Combien coûte une application mobile ? · Laura Bojon",
        "h1": "Combien coûte une application mobile ?",
        "desc": "Prix d'une application mobile iOS et Android : ce qui fait varier le budget, les frais à prévoir après la sortie et comment commencer petit.",
        "lead": "Le prix d'une application mobile peut varier du simple au décuple. Voici ce qui le fait bouger, les frais à prévoir après la publication, et comment démarrer sans exploser son budget.",
        "body": """
<h2>Ce qui fait varier le prix</h2>
<ul>
<li><strong>Le nombre d'écrans et de fonctionnalités</strong> : une application de réservation simple et une plateforme avec messagerie, paiement et recommandations ne représentent pas le même travail.</li>
<li><strong>Les comptes utilisateurs</strong> : inscription, connexion, profil et données synchronisées entre les appareils demandent un serveur ou un service comme Firebase.</li>
<li><strong>Le paiement</strong> : paiement par carte, abonnements ou achats intégrés aux stores ajoutent du développement et des règles à respecter.</li>
<li><strong>Les fonctions du téléphone</strong> : géolocalisation, carte, appareil photo, notifications push.</li>
<li><strong>Le design</strong> : des écrans sur mesure, pensés pour votre public, prennent plus de temps qu'une interface standard.</li>
<li><strong>Un espace d'administration</strong> : pour gérer les contenus, les utilisateurs ou les commandes sans passer par un développeur.</li>
</ul>

<h2>iOS et Android : une ou deux applications ?</h2>
<p>Développer deux applications natives, une pour l'iPhone et une pour Android, coûte presque deux fois plus cher. Avec React Native, une seule base de code suffit pour les deux plateformes dans la grande majorité des cas. <a href="/articles/react-native-ios-android/">J'explique comment dans cet article.</a></p>

<h2>Les frais après la publication</h2>
<ul>
<li><strong>Les comptes développeur</strong> : 99 $ par an chez Apple, 25 $ une seule fois chez Google, à votre nom.</li>
<li><strong>Le serveur ou les services en ligne</strong> : souvent quelques euros par mois au départ, plus à mesure que le nombre d'utilisateurs grandit.</li>
<li><strong>Les commissions</strong> : les stores prélèvent une part sur les achats intégrés et les abonnements, et les prestataires de paiement prennent des frais sur chaque transaction.</li>
<li><strong>La maintenance</strong> : chaque nouvelle version d'iOS et d'Android peut demander des ajustements, et les bibliothèques utilisées doivent rester à jour.</li>
</ul>

<h2>Commencer petit : la première version</h2>
<p>Plutôt que de tout développer d'un coup, mieux vaut sortir une première version avec les fonctionnalités indispensables, la mettre entre les mains de vrais utilisateurs, puis l'enrichir. Vous dépensez moins au départ, et chaque évolution répond à un besoin constaté plutôt qu'imaginé.</p>

<h2>Mes tarifs</h2>
<p>Chez moi, une application mobile iOS et Android démarre à <strong>4 500 €</strong> pour une application simple, publiée sur les deux stores. Le devis détaille chaque fonctionnalité, et le développement avance par sprints de trois semaines, avec une version à tester à la fin de chacun. Prix nets : TVA non applicable, article 293 B du CGI.</p>
<p>Pour des exemples concrets, découvrez <a href="/projets/klotho/">Klotho</a>, un dressing virtuel avec IA et abonnements, et <a href="/projets/wim/">Wim</a>, une plateforme d'échange de logements sur iOS, Android et le web.</p>

<h2>Bien préparer son projet</h2>
<ul>
<li>Décrivez en quelques phrases le problème que l'application résout, et pour qui.</li>
<li>Listez les fonctionnalités, puis séparez l'indispensable du « plus tard ».</li>
<li>Repérez deux ou trois applications dont vous aimez le fonctionnement.</li>
<li>Prévoyez le budget des premiers mois après la sortie, pas seulement celui du développement.</li>
</ul>
<p>Vous avez une idée d'application ? <a href="/services/application-mobile/">Découvrez l'offre de développement d'application mobile</a> ou demandez-moi un devis gratuit.</p>
""",
    },
}


def words(html):
    return len(re.sub(r"<[^>]+>", " ", html).split())


def article_page(slug, a, others):
    path = f"/articles/{slug}/"
    minutes = max(2, round(words(a["body"] + a["lead"]) / 200))
    ld_c, crumb = crumbs([("Accueil", "/"), ("Articles", "/articles/"), (a["h1"], path)])
    post = {"@context": "https://schema.org", "@type": "BlogPosting", "headline": a["h1"], "description": a["desc"],
            "datePublished": DATE_ISO, "dateModified": DATE_ISO, "inLanguage": "fr-FR", "mainEntityOfPage": f"{BASE}{path}",
            "image": f"{BASE}/assets/partage.jpg",
            "author": {"@type": "Person", "name": "Laura Bojon", "url": f"{BASE}/"},
            "publisher": {"@id": f"{BASE}/#activite"}}
    cards = "".join(article_card(s, ARTICLES[s], "h3") for s in others)
    return head(a["title"], a["desc"], path, "/assets/partage.jpg", "article", [ld_c, post]) + f"""
{crumb}

  <article class="section article">
    <div class="wrap">
      <header class="section-head">
        <p class="eyebrow">Article</p>
        <h1>{a['h1']}</h1>
        <p class="article-meta">Publié le <time datetime="{DATE_ISO}">{DATE_FR}</time> · {minutes} min de lecture · Laura Bojon</p>
        <p class="lead">{a['lead']}</p>
      </header>
      <div class="prose">{a['body']}</div>
{CTA.format(titre="Un projet en tête ?", texte="Site, application mobile ou outil sur mesure, le premier échange est gratuit et sans engagement.")}
    </div>
  </article>

  <section class="section section-alt" aria-labelledby="lire-titre">
    <div class="wrap">
      <div class="section-head">
        <p class="eyebrow">À lire aussi</p>
        <h2 id="lire-titre">D'autres articles</h2>
      </div>
      <div class="article-list">{cards}
      </div>
    </div>
  </section>
""" + tail()


def article_card(slug, a, tag):
    minutes = max(2, round(words(a["body"] + a["lead"]) / 200))
    return f"""
        <a class="article-card" href="/articles/{slug}/">
          <p class="article-meta"><time datetime="{DATE_ISO}">{DATE_FR}</time> · {minutes} min</p>
          <{tag}>{a['h1']}</{tag}>
          <p>{a['lead']}</p>
          <span class="text-link">Lire l'article →</span>
        </a>"""


def articles_index():
    path = "/articles/"
    ld_c, crumb = crumbs([("Accueil", "/"), ("Articles", path)])
    cards = "".join(article_card(s, a, "h2") for s, a in ARTICLES.items())
    return head("Articles sur le web et le mobile · Laura Bojon",
                "Conseils pour votre site internet ou votre application mobile : prix, obligations légales, choix techniques. Par Laura Bojon, développeuse à Bordeaux.",
                path, "/assets/partage.jpg", "website", [ld_c]) + f"""
{crumb}

  <section class="section">
    <div class="wrap">
      <div class="section-head">
        <p class="eyebrow">Articles</p>
        <h1>Conseils pour votre projet web ou mobile</h1>
        <p class="section-intro">Prix, obligations légales, choix techniques : des repères concrets pour préparer votre site ou votre application.</p>
      </div>
      <div class="article-list">{cards}
      </div>
    </div>
  </section>
""" + tail()


def write(rel, html):
    d = os.path.join(SITE, rel)
    os.makedirs(d, exist_ok=True)
    open(os.path.join(d, "index.html"), "w", encoding="utf-8", newline="\n").write(html)
    print(f"{rel}/index.html")


for slug, s in SERVICES.items():
    write(f"services/{slug}", service_page(slug, s))
write("articles", articles_index())
for slug, a in ARTICLES.items():
    write(f"articles/{slug}", article_page(slug, a, [x for x in ARTICLES if x != slug]))
