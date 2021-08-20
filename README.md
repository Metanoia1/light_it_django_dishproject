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
ACTIVATE YOUR ENV AND:
```
pip install -r requirements.txt

```
```
python manage.py makemigrations

```
```
python manage.py migrate 

```
```
python manage.py createsuperuser

```

```
docker build -f Dockerfile --tag app:latest .

```

```
docker run -d -p 8082:8000 app

```
[127.0.0.1:8082](http://127.0.0.1:8082)
