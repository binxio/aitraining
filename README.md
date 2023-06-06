# AI Training

## Instructions

docker buildx build . --platform linux/amd64 -t <yourname>-myfirstai
docker tag <yourname>-myfirstai gcr.io/<projectid>/<yourname>-myfirstai
docker push gcr.io/<projectid>/<yourname>-myfirstai
gcloud run deploy <yourname>-myfirstai --image gcr.io/<projectid>/<yourname>-myfirstai --platform managed --region us-east1 --allow-unauthenticated
