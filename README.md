Thunes
======

# Installation

## Ansible

Voici un rôle Ansible qui déploie une instance de thunes sur un serveur sous Debian, avec une base de données postgresql, un serveur web nginx et uwsgi : https://gitlab.crans.org/bombar/ansible/-/tree/master/roles%2Fthunes

Les variables sont à définir dans le fichier d'inventaire, ou dans les variables d'hôtes.
Ce rôle ne gère pas la création de la base de données, qui peut très bien être sur un autre serveur. En revanche, il gère toute la configuration de Django : Il suffit de donner l'ip sur serveur de base de données (pouvant être localhost).

## À la main

Cloner le depot :

```
git clone https://gitea.servens.org/bombar/Thunes.git
```

Installer et activer le virtualenv :

```
sudo apt install python3-venv
cd Thunes
virtualenv -p python3 .env
source .env/bin/activate
```

Installer les dépendances :

```
pip3 install -r requirements.txt
```


Installer les migrations :

```
./manage.py migrate
```


A présent vous devrez pouvoir lancer le serveur web via un 

```
./manage.py runserver
```

Mais on va utiliser un vrai serveur web: nginx + uwsgi

```
sudo apt install nginx uwsgi uwsgi-plugin-python3

cd /etc/nginx/sites-available/
sudo ln -s /var/www/Thunes/WebUtils/Thunes.nginx ./
cd ../sites-enabled/
sudo ln -s ../sites-available/Thunes .
rm default ## ça c'est parce que le serveur web écoute tout le monde

cd /etc/uwsgi/apps-available/
sudo ln -s /var/www/Thunes/WebUtils/Thunes.uwsgi ./
cd ../apps-enabled/
sudo ln -s ../apps-available/Thunes ./Thunes.ini
sudo chown -R www-data /var/www/Thunes/
```


/!\ ne pas oublier le .ini dans le apps-enabled ....


On démarre le serveur web :

```
sudo systemctl restart nginx.service uwsgi.service
```

et normalement, it works ! \o/
