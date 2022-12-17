# Flasker = Flask + Docker

TODO


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


Open the repository Settings, and go to Secrets > Actions.

Create a new secret named `DOCKER_HUB_USERNAME` and your Docker ID as value.


Create a new Personal Access Token (PAT) for Docker Hub.

TODO create an Access Token for GitHub


Add the PAT as a second secret in your GitHub repository, with the name DOCKER_HUB_ACCESS_TOKEN.


Go to your repository on GitHub and then select the Actions tab.

Select set up a workflow yourself.

This takes you to a page for creating a new GitHub actions workflow file in your repository, under .github/workflows/main.yml by default.

In the editor window, copy and paste the following YAML configuration.
```yml
name: ci

on:
  push:
    branches:
      - "main"

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      -
        name: Checkout
        uses: actions/checkout@v3
      -
        name: Login to Docker Hub
        uses: docker/login-action@v2
        with:
          username: ${{ secrets.DOCKER_HUB_USERNAME }}
          password: ${{ secrets.DOCKER_HUB_ACCESS_TOKEN }}
      -
        name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v2
      -
        name: Build and push
        uses: docker/build-push-action@v3
        with:
          context: .
          file: ./Dockerfile
          push: true
          tags: ${{ secrets.DOCKER_HUB_USERNAME }}/clockbox:latest
```

    name: the name of this workflow.
    on.push.branches: specifies that this workflow should run on every push event for the branches in the list.
    jobs: creates a job ID (build) and declares the type of machine that the job should run on.

The previous YAML snippet contains a sequence of steps that:

    Checks out the repository on the build machine.
    Signs in to Docker Hub, using the Docker Login action and your Docker Hub credentials.
    Creates a BuildKit builder instance using the Docker Setup Buildx action.

    Builds the container image and pushes it to the Docker Hub repository, using Build and push Docker images.

    The with key lists a number of input parameters that configures the step:
        context: the build context.
        file: filepath to the Dockerfile.
        push: tells the action to upload the image to a registry after building it.
        tags: tags that specify where to push the image.

Run the workflow

Save the workflow file and run the job.

    Select Start commit and push the changes to the main branch.

    After pushing the commit, the workflow starts automatically.

    Go to the Actions tab. It displays the workflow.

    Selecting the workflow shows you the breakdown of all the steps.

    When the workflow is complete, go to your repositories on Docker Hub.

    If you see the new repository in that list, it means the GitHub Actions successfully pushed the image to Docker Hub!



## Kubernetes

### Create a Kubernetes Cluster with EKS

```sh
eksctl create cluster --name flaskernetes --region us-east-1
```


After the cluster is created, check it out 
https://console.aws.amazon.com/cloudformation/


Take a look at your nodes: 
```sh
kubectl get nodes -o wide
```


Take a look at the workloads running on the cluster: 
```sh
kubectl get pods -A -o wide
```


#### Create a Namespace

```sh
kubectl create namespace flask
```





### Creating s Kubernetes Deployment Manifest 

TODO
`eks-deployment.yml`

TODO 

Apply the deployment manifest
TODO
```sh
kubectl apply -f eks-deployment.yml 
```



Create a service manifest
TODO `eks-service.yml`

Apply the service manifest: 
```sh
kubectl apply -f eks-service.yaml
```


View the resources in the `flask` namespace: 
```
kubectl get all -n flaskernetes
```











Create a `k8s` folder and the following files: 

* flask-pod.yml

* flask-pod.yml

* flask-service.yml





Confirm the pod is running:
```sh
kubectl get pod -n flask
```


### Deploy your manifest to your k8s cluster Using kubectl

TODO


### Deploying Kubernetes w/ GitHub Actions

https://github.com/marketplace/actions/kubernetes-action







## Clean Up

```sh
eksctl delete cluster --name flaskernetes --region us-east-1 --fargate
```




## Resources

* https://www.digitalocean.com/community/meetup-kits/getting-started-with-containers-and-kubernetes-a-digitalocean-workshop-kit

* https://docs.docker.com/build/ci/github-actions/

* https://docs.github.com/en/actions/learn-github-actions/finding-and-customizing-actions

* https://github.com/marketplace/actions/publish-docker

* https://github.com/marketplace/actions/docker-login

* https://docs.github.com/en/actions/creating-actions/creating-a-docker-container-action

* https://docs.github.com/en/actions/publishing-packages/publishing-docker-images

* https://github.com/marketplace/actions/build-and-push-docker-images

* https://www.digitalocean.com/community/tutorials/how-to-make-a-web-application-using-flask-in-python-3












