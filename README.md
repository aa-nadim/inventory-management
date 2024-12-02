# inventory-management

________________For Env_____________________

____________________________For Linux
```
      python3 -m venv .venv
      source .venv/bin/activate
      deactivate
```
____________________________For Windows
```
      python -m venv .venv
      source .venv/Scripts/activate 
      deactivate
```

__________________________installation
```
pip install -r requirements.txt
```

_________________________Docker
```
docker volume ls
docker-compose down -v
docker volume rm $(docker volume ls -q)
docker-compose build
docker-compose up -d
```

_________________________db

```
docker exec -it inventoryManagement python manage.py runserver 0.0.0.0:8000

docker exec -it inventoryManagement python manage.py makemigrations
docker exec -it inventoryManagement python manage.py migrate

docker exec -it inventoryManagement python manage.py migrate app zero

docker exec -it inventoryManagement python manage.py migrate properties zero

docker exec -it inventoryManagement python manage.py migrate unapply

```

## Create Superuser and Property Owners Group:
```
docker exec -it inventoryManagement python manage.py createsuperuser

docker exec -it inventoryManagement python manage.py create_property_owners_group

```


docker exec -it postgres_container_name bash
docker exec -it postgres_db bash
psql -U your_db_user
\c postgres
DROP DATABASE your_db_name;
CREATE DATABASE your_db_name;
\q

python manage.py migrate
python manage.py createsuperuser