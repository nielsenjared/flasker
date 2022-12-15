# Flasker = Flask + Docker




### Build the Image
```sh
docker build -t flasker:v0 .
```

Don't forget the `.`


### Run the App
```sh
docker run flasker:v0
```


## Docker

https://docs.docker.com/docker-hub/

Sign in to Docker Hub.

Click Create a Repository on the Docker Hub welcome page.

https://hub.docker.com/

Name it <your-username>/flasker.

```sh
docker build -t nielsenjared/flasker .
```


```sh
docker run nielsenjared/flasker
```

### Access Tokens
If you haven't yet, you will need to set up access tokens with Docker Hub. Do so under settings in the UI, then run: 
```
docker login -u nielsenjared
```

And at the `Password` prompt paste in your access token. 


## GitHub Actions

### Build Image on GitHub

Create a new Action and select the Docker Image workflow. 


TODO 


### Publish Changes to Docker Hub






