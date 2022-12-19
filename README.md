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

TODO what's the naming convention? 
```
system+cluster-unique-id
```

```sh
kubectl create namespace eks-flasker
```





### Creating Kubernetes Deployment Manifest

TODO
`eks-deployment.yml`

TODO 

Apply the deployment manifest
TODO
```sh
kubectl apply -f eks-flasker-deployment.yml 
```

The response will be:
```sh
deployment.apps/flaskernetes created
```


### Creating Kubernetes Service Manifest


TODO `eks-flasker-service.yml`

Apply the service manifest: 
```sh
kubectl apply -f eks-flasker-service.yml
```


The response will be:
```
service/flaskernetes created
```



### View Resources and Details 

View the resources in the `flask` namespace: 
```
kubectl get all -n eks-flasker
```

The output will be something like:
```sh
NAME                               READY   STATUS    RESTARTS   AGE
pod/flaskernetes-9fffc5965-4vbm7   1/1     Running   0          3m21s
pod/flaskernetes-9fffc5965-r7kcc   1/1     Running   0          3m21s
pod/flaskernetes-9fffc5965-v77pm   1/1     Running   0          3m21s

NAME                   TYPE        CLUSTER-IP      EXTERNAL-IP   PORT(S)   AGE
service/flaskernetes   ClusterIP   10.100.86.236   <none>        80/TCP    41s

NAME                           READY   UP-TO-DATE   AVAILABLE   AGE
deployment.apps/flaskernetes   3/3     3            3           3m21s

NAME                                     DESIRED   CURRENT   READY   AGE
replicaset.apps/flaskernetes-9fffc5965   3         3         3       3m21s
```





View the details: 

```sh
kubectl -n eks-flasker describe service flaskernetes
```

The output will be something like:
```sh
Name:              flaskernetes
Namespace:         eks-flasker
Labels:            app=flasker
Annotations:       <none>
Selector:          app=flasker
Type:              ClusterIP
IP Family Policy:  SingleStack
IP Families:       IPv4
IP:                10.100.86.236
IPs:               10.100.86.236
Port:              <unset>  80/TCP
TargetPort:        80/TCP
Endpoints:         192.168.14.25:80,192.168.27.249:80,192.168.62.16:80
Session Affinity:  None
Events:            <none>
```


View the details of a pod:
```sh
kubectl -n eks-flasker describe pod flaskernetes-5dd7b949b5-6zg8h
```

Replace the alphanumeric values with those from one your pods listed above. 

The output will be similar to the following:
```sh
Name:             flaskernetes-9fffc5965-4vbm7
Namespace:        eks-flasker
Priority:         0
Service Account:  default
Node:             ip-192-168-32-138.ec2.internal/192.168.32.138
Start Time:       Mon, 19 Dec 2022 14:35:25 -0500
Labels:           app=flasker
                  pod-template-hash=9fffc5965
Annotations:      kubernetes.io/psp: eks.privileged
Status:           Running
IP:               192.168.62.16
IPs:
  IP:           192.168.62.16
Controlled By:  ReplicaSet/flaskernetes-9fffc5965
Containers:
  nginx:
    Container ID:   docker://322a63337994cedc885474656198ca2e80ade7526c30a38783f57d43cc12ef6a
    Image:          public.ecr.aws/nginx/nginx:1.21
    Image ID:       docker-pullable://public.ecr.aws/nginx/nginx@sha256:3aac7c736093ce043a17d6e83ef5addb8be321b5b6b93879141e51474448ca65
    Port:           80/TCP
    Host Port:      0/TCP
    State:          Running
      Started:      Mon, 19 Dec 2022 14:35:29 -0500
    Ready:          True
    Restart Count:  0
    Environment:    <none>
    Mounts:
      /var/run/secrets/kubernetes.io/serviceaccount from kube-api-access-mrztr (ro)
Conditions:
  Type              Status
  Initialized       True 
  Ready             True 
  ContainersReady   True 
  PodScheduled      True 
Volumes:
  kube-api-access-mrztr:
    Type:                    Projected (a volume that contains injected data from multiple sources)
    TokenExpirationSeconds:  3607
    ConfigMapName:           kube-root-ca.crt
    ConfigMapOptional:       <nil>
    DownwardAPI:             true
QoS Class:                   BestEffort
Node-Selectors:              kubernetes.io/os=linux
Tolerations:                 node.kubernetes.io/not-ready:NoExecute op=Exists for 300s
                             node.kubernetes.io/unreachable:NoExecute op=Exists for 300s
Events:
  Type    Reason     Age    From               Message
  ----    ------     ----   ----               -------
  Normal  Scheduled  7m43s  default-scheduler  Successfully assigned eks-flasker/flaskernetes-9fffc5965-4vbm7 to ip-192-168-32-138.ec2.internal
  Normal  Pulling    7m42s  kubelet            Pulling image "public.ecr.aws/nginx/nginx:1.21"
  Normal  Pulled     7m39s  kubelet            Successfully pulled image "public.ecr.aws/nginx/nginx:1.21" in 2.831763339s
  Normal  Created    7m39s  kubelet            Created container nginx
  Normal  Started    7m39s  kubelet            Started container nginx
```

## Root a Pod

```
kubectl exec -it flaskernetes-9fffc5965-4vbm7 -n eks-flasker -- /bin/bash
```

This will ssh you into a pod as root. 

### Hit the Server 

TODO
```
curl flaskernetes
```

The output will be similar to the following: 
```sh
<!DOCTYPE html>
<html>
<head>
<title>Welcome to nginx!</title>
<style>
html { color-scheme: light dark; }
body { width: 35em; margin: 0 auto;
font-family: Tahoma, Verdana, Arial, sans-serif; }
</style>
</head>
<body>
<h1>Welcome to nginx!</h1>
<p>If you see this page, the nginx web server is successfully installed and
working. Further configuration is required.</p>

<p>For online documentation and support please refer to
<a href="http://nginx.org/">nginx.org</a>.<br/>
Commercial support is available at
<a href="http://nginx.com/">nginx.com</a>.</p>

<p><em>Thank you for using nginx.</em></p>
</body>
</html>
```


### TODO DNS
```sh
cat /etc/resolv.conf
```

TODO
```sh
nameserver 10.100.0.10
search eks-flasker.svc.cluster.local svc.cluster.local cluster.local ec2.internal
options ndots:5
```

10.100.0.10 is automatically assigned as the nameserver for all pods deployed to the cluster.



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












