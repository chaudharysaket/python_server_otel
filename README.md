# python_server_otel
Server to collect payload from OTEL

## Python environment
```shell
pipenv --python 3.11 
pipenv shell #activate shell
exit #exit the shell
```

## Production deployment
```
gunicorn -w 4 -b 0.0.0.0:4317 app:app
```
