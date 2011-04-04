#/bin/sh

mysqldump -umossaic_django -pV13nna --add-drop-table --no-data mossaic_django | grep ^DROP | mysql -umossaic_django -pV13nna mossaic_django

python manage.py syncdb
