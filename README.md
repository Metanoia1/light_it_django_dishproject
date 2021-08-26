[dishp.herokuapp.com](https://dishp.herokuapp.com)

# DOCKER LECTION
```
git clone https://github.com/Metanoia1/light_it_django_dishproject.git

```
```
cd light_it_django_dishproject

```
```
git checkout docker_lection

```
```
sudo apt-get update && apt-get install -y python3-dev libpq-dev gcc libmemcached-dev zlib1g-dev
```
ACTIVATE YOUR VIRTUAL ENV AND:
```
pip install -r requirements.txt
```
```
python manage.py migrate
```
```
python manage.py createsuperuser
```
```
docker-compose build

```
```
docker-compose up

```
