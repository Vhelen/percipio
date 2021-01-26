# Percipio

# Le but de l'outil
L'outil permet d'automatiser l'e-learning sur la plateforme Percipio.

# Son fonctionnement
L'outil va chercher vos cours assignés dans l'onglet Parcours.
Il va jouer ensuite toutes les vidéos des cours puis lancer les tests.
Pour les tests, il va enregistrer les réponses dans le fichier test_answer.json et recommencer jusqu'à avoir 100%.

# Installation
- Installer la librairie Selenium : pip install selenium
- Installer Firefox 64 bits : https://www.mozilla.org/en-US/firefox/browsers/windows-64-bit/

# Configurer le fichier de configuration conf.json
Ligne de commande :
- python3 percifiak.py -u adresse@mail.com -p votremotdepasse -b "C:\Program Files\Mozilla Firefox\firefox.exe"

Sinon vous pouvez toujours éditer le fichier conf.json directement.

Ceci est juste pour le premier lancement.
Une fois le fichier conf.json mis en place, vous pouvez lancer l'outil comme ceci : python3 percifiak.py
L'outil ira chercher automatiquement les accès à Percipio et l'emplacement de votre Firefox dans le fichier conf.json

# Aide
Pour que l'outil se lance correctement, il faut définir au premier lancement :
     - Le nom d'utilisateur (exemple : jean.dupont@gmail.com)
     - Le mot de passe associe (exemple : tonmeilleurmotdepasse)
     - La location de l'exe de firefox (exemple : C:/Program Files/Mozilla Firefox/firefox)
Ces informations sont stockees dans le fichier conf.json
Vous n'aurez pas à les remplir à chaque utilisation

-h --help Affiche l'aide
-u --username Met à jour le nom d'utilisateur
-p --password Met à jour le mot de passe de l'utilisateur
-b --browser Met à jour la location de l'exe de firefox
-d --debug Affiche la fenetre du navigateur

