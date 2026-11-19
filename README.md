# Site vitrine · Laura Bojon

Site statique (HTML, CSS, JavaScript), sans dépendance ni étape de compilation.

```
index.html               page d'accueil (toutes les sections)
mentions-legales.html    mentions légales et RGPD
conditions-generales.html conditions générales de prestation (devis, paiement, rétractation…)
404.html                 page affichée pour une adresse inexistante
projets/<nom>/          pages détaillées des projets (Klotho, Wim, FreyAge)
services/<nom>/         pages service (site internet, application mobile, application web)
articles/               articles de conseil (prix, obligations légales, React Native)
styles.css               styles ; polices puis couleurs du logo tout en haut
script.js                menu mobile, copie de l'e-mail, formulaire, captcha, bouton « haut de page »
assets/fonts/            polices hébergées avec le site
assets/hero-projets.webp captures des trois projets en haut de page
assets/projets/          images des cartes projets
assets/partage.jpg       image d'aperçu lors d'un partage sur les réseaux
assets/logo-lb.png       monogramme LB (en-tête et pied de page)
favicon.png              icône de l'onglet
apple-touch-icon.png     icône quand le site est ajouté à l'écran d'accueil d'un iPhone
sitemap.xml, robots.txt  référencement Google
CNAME                    domaine laurabojon.fr (ne pas supprimer)
outils/                  scripts de construction, de vérification et de sauvegarde (voir outils/README.md)
```

Pour le voir en local : ouvrez `index.html` dans un navigateur.

## À compléter avant la mise en ligne

1. **Wim** : quand worldismine.fr sera en ligne, passez son badge en « En ligne » et ajoutez le lien (voir le commentaire au-dessus de la section Projets).
2. **Engagements** : délais de la FAQ et « réponse sous 48 h ».

## Recevoir les messages du formulaire

Le formulaire est branché sur Formspree (formulaire « Site vitrine », adresse `https://formspree.io/f/mbgoyvra`, dans l'attribut `data-endpoint` du formulaire de `index.html`). Chaque demande arrive par e-mail sur laura.bojon@gmail.com et reste consultable dans le tableau de bord Formspree.

- L'offre gratuite de Formspree accepte un nombre limité de messages par mois : vérifiez la limite actuelle dans votre compte.
- Le champ caché `_gotcha` sert de piège anti-spam, et `_subject` fixe l'objet des e-mails reçus.
- Si vous videz `data-endpoint`, le formulaire revient au fonctionnement de secours : il ouvre la messagerie du visiteur avec le message prérempli.

## Hébergement et nom de domaine

- **Hébergement** : GitHub Pages (gratuit), depuis le dépôt public `laurabjn/laurabjn.github.io`, branche `main`, dossier racine. Chaque envoi sur `main` met le site à jour en une minute environ.
- **Domaine** : **laurabojon.fr**, acheté chez OVHcloud (renouvellement en novembre 2029). Le fichier `CNAME` à la racine indique ce domaine à GitHub : ne le supprimez pas. L'ancienne adresse https://laurabjn.github.io redirige automatiquement vers https://laurabojon.fr.
- **Zone DNS chez OVH** : 4 entrées A (185.199.108.153 à 185.199.111.153), 4 entrées AAAA (2606:50c0:8000::153 à 2606:50c0:8003::153) et un CNAME `www` vers `laurabjn.github.io.`. Les entrées MX et SPF servent à l'e-mail : ne les supprimez pas.
- **HTTPS** : certificat gratuit fourni par GitHub (Settings › Pages › Enforce HTTPS).

Si vous changez d'hébergeur, mettez à jour la rubrique Hébergement des mentions légales.

## Référencement Google

- `sitemap.xml` liste les pages à indexer (les mentions légales sont exclues, elles portent `noindex`). Mettez à jour `<lastmod>` après une modification importante.
- `robots.txt` autorise l'exploration et indique le sitemap.
- `index.html` contient l'adresse canonique du site et une fiche structurée (JSON-LD) qui décrit l'activité à Google.
- Search Console : propriétés « Préfixe d'URL » `https://laurabjn.github.io/` (ancienne adresse) et `https://laurabojon.fr/`, validées par les deux balises `google-site-verification` dans `index.html` (une par propriété). Ne les supprimez pas, sinon les propriétés perdent leur validation.

## Polices, images et page 404

- **Polices** : Cormorant Garamond, Cinzel et Jost sont hébergées avec le site (jeu de caractères latin), sans appel à Google Fonts : plus rapide, et aucune donnée de visiteur n'est transmise à Google.
- **Image de partage** : `assets/partage.jpg` (1200 × 630) s'affiche quand le lien du site est partagé sur LinkedIn, Facebook ou X.
- **Haut de page** : `assets/hero-projets.webp` montre trois projets réels ; à refaire si les applications changent beaucoup.
- **Page 404** : `404.html` est servie par GitHub Pages pour toute adresse inexistante, d'où ses chemins absolus (`/styles.css`…).
