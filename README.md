# redis-printer

`
docker network create my_app &&
docker run -d -p 6379:6379 --net my_app --name redis1 redis 
docker build -f DockerFile -t docker-printer:1.0 . &&
docker build -f DockerFileFlask -t docker-printer-api:1.0 . &&
docker run --net my_app --name console  docker-printer:1.0 &&
docker run -d -p 5000:5000 --net my_app --name api  docker-printer-api:1.0
`

curl -d time=12 -d msg="Hello World"  http://localhost:5000/echo

