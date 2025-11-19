Flask + Pytest + Ruff + Git Hooks + GitHub Actions

Objectifs

Créer une simple liste de tâches avec Flask (une liste items conservée en mémoire), puis :

    - Exécuter des tests automatisés localement avec pytest

    - Utiliser ruff pour l’analyse statique du code (lint)

    - Configurer un pre-push hook Git : lancer automatiquement ruff + pytest avant chaque git push local

    - Pousser le projet sur GitHub et utiliser GitHub Actions (CI) pour exécuter automatiquement ruff + pytest à chaque push / pull request

Tout code qui doit être poussé (en local) ou fusionné (sur GitHub) doit d’abord passer les tests et le lint.

Cela garantit une qualité de code stable et évite les erreurs causées par des négligences humaines.

Arborescence finale du projet (version simplifiée) :

workflows/
├─ app/
│  ├─ app.py
│  ├─ __init__.py
│  └─ pyproject.toml        # ruff setting
├─ templates/
│  └─ index.html
├─ static/
│  └─ style.css
├─ tests/
│  └─ test_unit_example.py  # pytest 
├─ .github/
│  └─ workflows/
│     └─ ci.yml             # GitHub Actions workflow
├─ requirements.txt
└─ .gitignore

1. Environnement local : environnement virtuel et dépendances

Un environnement virtuel Python (.venv) a été créé pour isoler les dépendances du projet. 
Après activation de l'environnement, Flask, pytest et Ruff ont été installés puis ajoutés au fichier requirements.txt. 
Une difficulté rencontrée fut l’absence d’activation du venv, rendant pytest introuvable.

2. Application Flask et structure du projet

Le fichier principal (app/myapp.py) contient les routes Flask pour afficher, ajouter, supprimer et mettre à jour des éléments. 
Comme les dossiers templates/ et static/ se trouvaient à la racine du projet, il a fallu indiquer explicitement leur chemin lors de l’initialisation de Flask.

Le fichier app/__init__.py rend le dossier app utilisable comme package Python, permettant :
from app import app, items

3. Tests automatisés avec pytest

Le fichier tests/test_unit_example.py contient les tests. 
Pour les besoins du CI GitHub, il a fallu ajouter le chemin du projet à sys.path, car l’environnement du runner GitHub ne détecte pas automatiquement le package app.
Pour éviter une erreur Ruff (E402), la ligne d’importation a été annotée avec # noqa: E402.

4. Analyse statique avec Ruff

Une configuration moderne a été écrite dans pyproject.toml. Des avertissements ont été résolus en migrant vers la syntaxe [tool.ruff] et [tool.ruff.lint]. 
Certaines règles (telles que E402 dans les tests) ont été ignorées au cas par cas.

5. Git et hook local pre-push

Un hook pre-push a été mis en place pour lancer Ruff puis pytest avant chaque push. S’il échoue, le push est annulé. 
Une difficulté particulière provenait des différences entre PowerShell et Bash sous Windows, ce qui a nécessité une version PowerShell du hook.

6. GitHub : branches, Pull Requests et merge

Le développement a été réalisé sur une branche dédiée (feature/my-change). Une fois les tests et le lint passés, une Pull Request a été créée puis fusionnée dans main. 
GitHub affiche clairement les commits mergés.

7. Intégration continue (CI) avec GitHub Actions

Le fichier .github/workflows/ci.yml exécute automatiquement deux jobs :
- Lint (Ruff)
- Tests (pytest)
Les dépendances sont installées via requirements.txt. 
Des erreurs initiales sont apparues lorsque Flask n’était pas installé ou lorsque Python ne trouvait pas le module app. Ces problèmes ont été résolus en ajoutant requirements.txt et en ajustant sys.path dans les tests.

8. Résultat final et bonnes pratiques

Le pipeline complet fonctionne désormais :
- Ruff valide le code ;
- pytest valide les tests ;
- GitHub Actions exécute automatiquement les deux ;
- le hook local empêche un push si un problème est détecté.

Bonnes pratiques identifiées :
- Toujours créer un environnement virtuel ;
- Garder une structure claire (app/, tests/, templates/, static/) ;
- Utiliser sys.path intelligemment dans des environnements CI ;
- Configurer Ruff dans pyproject.toml ;
- Utiliser des branches et PR pour un workflow propre ;
- Automatiser via CI pour une qualité constante.





