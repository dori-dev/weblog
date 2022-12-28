# Weblog

Advanced and modern weblog.

#

# How to Run Project

## Download Codes

```
git clone https://github.com/dori-dev/weblog.git
```

```
cd weblog
```

## Build Virtual Environment

```
python -m venv env
```

```
source env/bin/activate
```

## Install Project Requirements

```
pip install -r requirements.txt
```

## Change .Env Files

set your environment variables in `.env.local` to `.env.production`.<br>
<br>

## Set STATE Variable

if you doesn't set `STATE` environ variable, project run with `debug=False`

```
export STATE=LOCAL
```

## Create Extension

```
psql -U postgres db_name
```

```sql
CREATE EXTENSION pg_trgm;
```

## Migrate Models

```
python manage.py makemigrations blog
```

```
python manage.py migrate
```

## Add Super User

```
python manage.py createsuperuser
```

## Run Project

```
python manage.py runserver
```

## Open On Browser

Blog Page: [127.0.0.1:8000/blog](http://127.0.0.1:8000/blog/)<br>
Admin Page: [127.0.0.1:8000/admin](http://127.0.0.1:8000/admin/)

#

## Links

Download Source Code: [Click Here](https://github.com/dori-dev/weblog/archive/refs/heads/master.zip)

My Github Account: [Click Here](https://github.com/dori-dev/)
