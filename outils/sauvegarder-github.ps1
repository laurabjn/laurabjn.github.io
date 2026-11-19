# Sauvegarde de tous les depots GitHub de laurabjn (publics et prives).
# 1. Met a jour une copie miroir de chaque depot dans %USERPROFILE%\Sauvegardes\miroirs-github
# 2. En fait un fichier unique (bundle Git, avec tout l'historique) dans OneDrive\Sauvegardes GitHub
# Restaurer un depot :  git clone "C:\Users\laura\OneDrive\Sauvegardes GitHub\NOM.bundle" NOM
# Lance chaque semaine par la tache planifiee "Sauvegarde GitHub (laurabjn)".

$ErrorActionPreference = 'Continue'
$miroirs = Join-Path $env:USERPROFILE 'Sauvegardes\miroirs-github'
$cible = Join-Path $env:USERPROFILE 'OneDrive\Sauvegardes GitHub'
New-Item -ItemType Directory -Force -Path $miroirs, $cible | Out-Null
$journal = Join-Path $cible 'journal.txt'

$lignes = @("Sauvegarde du $((Get-Date).ToString('dd/MM/yyyy HH:mm'))")
$depots = gh repo list laurabjn --limit 200 --json name --jq '.[].name'
if ($LASTEXITCODE -ne 0 -or -not $depots) {
    $lignes += '  ERREUR  impossible de lister les depots (gh est-il connecte ? lancer : gh auth status)'
}

foreach ($nom in $depots) {
    $miroir = Join-Path $miroirs "$nom.git"
    if (Test-Path $miroir) {
        git -C $miroir remote update --prune 2>&1 | Out-Null
    } else {
        git clone --mirror --quiet "https://github.com/laurabjn/$nom.git" $miroir 2>&1 | Out-Null
    }
    if ($LASTEXITCODE -ne 0) { $lignes += "  ERREUR  $nom : copie impossible"; continue }

    $bundle = Join-Path $cible "$nom.bundle"
    git -C $miroir bundle create $bundle --all 2>&1 | Out-Null
    if ($LASTEXITCODE -ne 0) { $lignes += "  ERREUR  $nom : depot vide ou fichier impossible a creer"; continue }

    $taille = [math]::Round((Get-Item $bundle).Length / 1MB, 1)
    $lignes += "  OK      $nom ($taille Mo)"
}

$lignes += ''
Add-Content -Path $journal -Value $lignes -Encoding UTF8
$lignes
