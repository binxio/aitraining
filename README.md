# AI Training

## Deploying the Flask WebApp to GCP Cloud Run:

```
gcloud auth login
gcloud config set project <projectid>
gcloud auth configure-docker 
docker buildx build . --platform linux/amd64 -t <yourname>-myfirstai
docker tag <yourname>-myfirstai gcr.io/<projectid>/<yourname>-myfirstai
docker push gcr.io/<projectid>/<yourname>-myfirstai
gcloud run deploy <yourname>-myfirstai \
  --image gcr.io/<projectid>/<yourname>-myfirstai \
  --platform managed --region us-east1 --allow-unauthenticated
```

Note that you might need to configure the API key as an environment variable.

## Local testing

```
python3 app.py
```


