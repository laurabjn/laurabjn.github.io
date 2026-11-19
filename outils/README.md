# Outils du site

Scripts qui ont servi à construire le site. Ils ne sont pas nécessaires à son fonctionnement : les pages publiées sont du HTML statique, modifiable directement.

Les images d'origine (logo, bannière, captures des projets) sont sauvegardées dans `OneDrive\Sauvegarde site-vitrine\sources`.

## `pages/` : générateurs de pages

- `build-projects.py` : pages projet (`projets/<nom>/`). Contenu, fonctionnalités, galeries et technologies sont dans le dictionnaire `PROJECTS`.
- `build-content.py` : pages service (`services/<nom>/`) et articles (`articles/<nom>/`). Contenu dans `SERVICES` et `ARTICLES`.

Utilisation, depuis ce dossier : `python pages/build-content.py ..` puis vérifier le résultat avant de publier.
Attention : régénérer une page écrase les modifications faites à la main dans son HTML. Modifiez plutôt le générateur, ou abandonnez le générateur et éditez le HTML.

## `images/` : compositions d'images (Python + Pillow)

- `compose-hero.py` : les trois applications du haut de page (`assets/hero-projets.webp`) et l'image de partage (`assets/partage.jpg`).
- `project-images.py`, `klotho-full.py`, `compose-freyage-wim.py` : vignettes, galeries et images de partage des projets.
- `fiche-google.py` : images de la fiche Google Business Profile.
- `fonts.py` : téléchargement des polices hébergées avec le site (`assets/fonts/`).

Ces scripts attendent les dossiers d'images d'origine en arguments (voir leurs premières lignes).

## `verifications/` : tests dans Chrome (Node.js)

- `check.mjs` : débordements horizontaux de 320 à 1440 px et captures pleine page.
- `audit.mjs` : temps d'affichage sur mobile en 4G lente, poids de la page, balises SEO, libellés des champs.
- `shot-section.mjs` : capture d'une section précise à plusieurs largeurs.
- `cookies-test.mjs` : liste des cookies et du stockage déposés par le site en ligne.

Exemple : `node verifications/check.mjs "C:/Program Files/Google/Chrome/Application/chrome.exe" "https://laurabojon.fr/" dossier-captures`

## `sauvegarder-github.ps1` : sauvegarde de tous les dépôts GitHub

Chaque dimanche à 20 h (ou au démarrage suivant si l'ordinateur était éteint), la tâche planifiée « Sauvegarde GitHub (laurabjn) » :
1. met à jour une copie de chaque dépôt dans `%USERPROFILE%\Sauvegardes\miroirs-github` ;
2. en fait un fichier unique avec tout l'historique dans `OneDrive\Sauvegardes GitHub\<dépôt>.bundle` ;
3. note le résultat dans `OneDrive\Sauvegardes GitHub\journal.txt`.

Restaurer un dépôt : `git clone "C:\Users\laura\OneDrive\Sauvegardes GitHub\Klotho.bundle" Klotho`

Lancer une sauvegarde à la main : `powershell -ExecutionPolicy Bypass -File outils\sauvegarder-github.ps1`
