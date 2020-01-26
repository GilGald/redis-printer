# redis-printer

in project directory run:
```
docker network create my_app &&
docker run -d -p 6379:6379 --net my_app --name redis1 redis 
docker build -f DockerFile -t docker-printer:1.0 . &&
docker build -f DockerFileFlask -t docker-printer-api:1.0 . &&
docker run -d -p 5000:5000 --net my_app --name api  docker-printer-api:1.0 &&
docker run --net my_app --name console docker-printer:1.0 

```
run post call like this:
```curl -d time=12 -d msg="Hello World"  http://localhost:5000/echo```

you should see the output in the console container logs

# Demo server is down and up again steps:
in case the server is down we add a few messages and then the server runs again it should print them



remove the console container :
```
docker container rm  console
```
post a few messages :

```
curl -d time=12 -d msg="Hello World"  http://localhost:5000/echo
```

run console container :
(for demo purposes will call it console2)
```
docker run --net my_app --name console2 docker-printer:1.0 
```

you should see the messages printed on console2 logs
