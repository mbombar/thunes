Cloner le depot avec le submodule :

```
git clone --recurse-submodules https://gogs.paulon.org/mikachu/MathoosHouse.git
```

Installer virtualenv et activer le venv :

```
sudo apt install virtualenv
cd MathoosHouse
virtualenv -p python3 .env
source .env/bin/activate
```

Installer les dépendances :

```
pip3 install django
pip3 install django-bootstrap4
pip3 install django-icons
pip3 install django-bootstrap-datepicker-plus
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
sudo ln -s /var/www/MathoosHouse/WebUtils/MathoosHouse.nginx ./
cd ../sites-enabled/
sudo ln -s ../sites-available/MathoosHouse .
rm default ## ça c'est parce que le serveur web écoute tout le monde

cd /etc/uwsgi/apps-available/
sudo ln -s /var/www/MathoosHouse/WebUtils/MathoosHouse.uwsgi ./
cd ../apps-enabled/
sudo ln -s ../apps-available/MathoosHouse ./MathoosHouse.ini
sudo chown -R www-data /var/www/MathoosHouse/
```


/!\ ne pas oublier le .ini dans le apps-enabled ....


On démarre le serveur web :

```
sudo systemctl restart nginx.service uwsgi.service
```

et normalement, it works ! \o/