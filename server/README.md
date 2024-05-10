## run locally with hot reload

```flask --app server.py --debug run --host=0.0.0.0```

## run with docker

```docker image build -t flask_docker . && docker run -p 5000:5000 -d flask_docker```