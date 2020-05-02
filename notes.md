## Convert entrypoint.sh CRLF (Windows) to LF (Unix) 
docker-compose up -d --build

## Create table:
docker-compose exec users python manage.py recreate_db

## Ensure the users table was created:
docker-compose exec users-db psql --username=postgres --dbname=users_dev

$ docker-compose exec users-db psql --username=postgres --dbname=users_dev
psql (12.2)
Type "help" for help.

users_dev=# \l
                                 List of databases
    Name    |  Owner   | Encoding |  Collate   |   Ctype    |   Access privileges
------------+----------+----------+------------+------------+-----------------------
 postgres   | postgres | UTF8     | en_US.utf8 | en_US.utf8 |
 template0  | postgres | UTF8     | en_US.utf8 | en_US.utf8 | =c/postgres          +
            |          |          |            |            | postgres=CTc/postgres
 template1  | postgres | UTF8     | en_US.utf8 | en_US.utf8 | =c/postgres          +
            |          |          |            |            | postgres=CTc/postgres
 users_dev  | postgres | UTF8     | en_US.utf8 | en_US.utf8 |
 users_prod | postgres | UTF8     | en_US.utf8 | en_US.utf8 |
 users_test | postgres | UTF8     | en_US.utf8 | en_US.utf8 |
(6 rows)

users_dev=# \c users_dev
You are now connected to database "users_dev" as user "postgres".
users_dev=# \dt
         List of relations
 Schema | Name  | Type  |  Owner
--------+-------+-------+----------
 public | users | table | postgres
(1 row)

users_dev=# \q

Alex@alex-pc MINGW64 ~/Documents/Projects/flask-react-aws (master)
$

## Populate the database table:
```
$ docker-compose exec users python manage.py seed_db  
$ docker-compose exec users-db psql --username=postgres --dbname=users_dev  
# \l  
# \dt  
# \c users_dev  
users_dev=# select * from users;  
 id |   username    |        email        |                           password                           | active |       created_date
----+---------------+---------------------+--------------------------------------------------------------+--------+---------------------------
  1 | michael       | hermanmu@gmail.com  | $2b$04$w.ZoLAl6RPb08tZuNK/KSOXQskr7QYCf.jS0lxpoF9E8VGTrrRbRq | t      | 2020-05-01 13:54:29.28865
  2 | michaelherman | michael@mherman.org | $2b$04$fb5vwkA/1JNsyvNqXrkkcO8YGM1cthucVdd8dz/7xFgtUKnBUzqze | t      | 2020-05-01 13:54:29.28865
(2 rows)
```
docker-compose up

http://192.168.99.100:5001/ping 
``` 
{
    "status": "success",
    "message": "pong!!"
}
```
http://192.168.99.100:5001/users  
```
[
    {
        "id": 1,
        "username": "michael",
        "email": "hermanmu@gmail.com",
        "created_date": "2020-05-01T13:54:29.288650"
    },
    {
        "id": 2,
        "username": "michaelherman",
        "email": "michael@mherman.org",
        "created_date": "2020-05-01T13:54:29.288650"
    }
]
```

docker-compose.yml:
```
REACT_APP_USERS_SERVICE_URL=http://192.168.99.100:5001
```

Next Step: add swagger according to https://mherman.org/presentations/microservices-flask-docker/#1

## References:
https://mherman.org/blog/dockerizing-a-react-app/  
https://testdriven.io/blog/dockerizing-flask-with-postgres-gunicorn-and-nginx/  
https://mherman.org/presentations/microservices-flask-docker/#1  
https://github.com/testdrivenio/flask-microservices-users  
https://github.com/testdrivenio/flask-microservices-main  
https://github.com/testdrivenio/flask-microservices-client  
https://github.com/testdrivenio/flask-microservices-main/tree/master/nginx  
https://github.com/testdrivenio/flask-microservices-main/tree/master/e2e  
https://github.com/testdrivenio/flask-microservices-swagger  
https://github.com/wsargent/docker-cheat-sheet  
https://hub.packtpub.com/how-to-build-12-factor-design-microservices-on-docker-part-1/  









	  
