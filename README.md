# ModSum

## Setup Docker

```
git clone https://github.com/jkszymczak/ModSum
docker compose up # starting both services
docker compose up ref # start only ref site on port 8000
docker compose up broken # start only broken site on port 7000

jmeter -n -t load_test/load_test.jmx -Jport {port on which start load testing} -l {log file}

```

## Apps

```
localhost:8000 - Working App
localhost:7000 - Testing App
```


## Tests
Remember to install Docker.
On Windows you maybe should run docker desktop 

