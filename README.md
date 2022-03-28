# django-k8-sample
This is a sample django project deployable to Oracle Kubernetes Engine


Commands ran: 

```shell
ubuntu@dalquintubuntuarm:~/REPOS/django-k8-sample$ source venv/bin/activate
ubuntu@dalquintubuntuarm:~/REPOS/django-k8-sample$ mkdir web
(venv) ubuntu@dalquintubuntuarm:~/REPOS/django-k8-sample$ cd web/
(venv) ubuntu@dalquintubuntuarm:~/REPOS/django-k8-sample/web$ django-admin startproject django_k8s_sample .

```
For testing the deployment: 

```shell
cd /home/ubuntu/REPOS/django-k8-sample/web
/home/ubuntu/REPOS/django-k8-sample/venv/bin/gunicorn django_k8s.wsgi:application
```

# For Docker. 

1. Create file `.dockerignore`inside web directory and copy all the contents from `.gitignore`into it
2. Create the `Dockerfile`file in web directory and set the content
3. Create file `entrypoint.sh` with it's corresponding content

4. Write the `docker-compose.yaml`file
5. Run `docker-compose up` This will build the image
    Note: You can run `docker system prune -a` to wipe out all
    You can stop the container by running `docker-compose down`
    You can force the re-build of image by running `docker-compose up --build`
6. If everything goes fine, when opening `http://localhost:8020` will show something like this

![image](./img/django_ok.png)


7. Access the folllwing site: 
    `http://localhost:8020/admin/login/?next=/admin/`


You will see something like this: 

![](./img/django_login.png)

Pass on User and Password located at .env under `DJANGO_SUPERUSER_USERNAME` and `DJANGO_SUPERUSER_PASSWORD`

8. You will see something like this now: 

![](./img/django_admin.png)


# Pushing the image to OCIR 

Follow instructions in this link: https://www.oracle.com/webfolder/technetwork/tutorials/obe/oci/registry/index.html


1. For your user, create an auth-token

![](./img/ocir_token.png)

2. Select a region where you will do the deployment. In my case sa-santiago-1

3. Create a repository: (in this case `django-sample-app-k8s` and `django-sample-nginx-k8s`)

![](./img/ocir_registry.png)

4. Login into OCIR with docker CLI

`docker login sa-santiago-1.ocir.io``

Username: <tenancy-namespace>/oracleidentitycloudservice/john.doe@domain.com
Password: auth-token from step 1. 

Example

```shell
(venv) ubuntu@dalquintubuntuarm:~/REPOS/django-k8-sample/k8s_deployment/nginx$ docker login sa-santiago-1.ocir.io
Username: idhkis4m3p5e/oracleidentitycloudservice/denny.alquinta@oracle.com
Password: 
WARNING! Your password will be stored unencrypted in /home/ubuntu/.docker/config.json.
Configure a credential helper to remove this warning. See
https://docs.docker.com/engine/reference/commandline/login/#credentials-store

Login Succeeded
```

5. Rebuild the image and Tag it

`$ docker-compose up --build`

5.1 Get the name of the image: 

```shell
(venv) ubuntu@dalquintubuntuarm:~/REPOS/django-k8-sample/k8s_deployment$ docker image ls
REPOSITORY         TAG             IMAGE ID       CREATED          SIZE
django-nginx-k8s   v0.0.1          21c339a04fe3   20 seconds ago   19.9MB
django-app-k8s     v0.0.1          4ac1b0e88b46   27 seconds ago   582MB
mysql              oracle          bf5b46dfe369   3 days ago       486MB
python             3.8.5-alpine    da3ea875dbcd   18 months ago    41.9MB
nginx              1.19.0-alpine   d918ec5de862   22 months ago    19.9MB
```

Now tag it
`docker tag django-app-k8s:v0.0.1 sa-santiago-1.ocir.io/idhkis4m3p5e/django-sample-app-k8s:v0.0.1`

and

`docker tag django-nginx-k8s:v0.0.1 sa-santiago-1.ocir.io/idhkis4m3p5e/django-sample-nginx-k8s:v0.0.1`


It'll look like this: 

```shell
(venv) ubuntu@dalquintubuntuarm:~/REPOS/django-k8-sample/k8s_deployment$ docker image ls
REPOSITORY                                                   TAG             IMAGE ID       CREATED              SIZE
django-nginx-k8s                                             v0.0.1          21c339a04fe3   About a minute ago   19.9MB
sa-santiago-1.ocir.io/idhkis4m3p5e/django-sample-nginx-k8s   v0.0.1          21c339a04fe3   About a minute ago   19.9MB
sa-santiago-1.ocir.io/idhkis4m3p5e/django-sample-app-k8s     v0.0.1          4ac1b0e88b46   About a minute ago   582MB
django-app-k8s                                               v0.0.1          4ac1b0e88b46   About a minute ago   582MB
mysql                                                        oracle          bf5b46dfe369   3 days ago           486MB
python                                                       3.8.5-alpine    da3ea875dbcd   18 months ago        41.9MB
nginx                                                        1.19.0-alpine   d918ec5de862   22 months ago        19.9MB
```

6. Now push the image by running: 

`docker push sa-santiago-1.ocir.io/idhkis4m3p5e/django-sample-nginx-k8s:v0.0.1`

and

`docker push sa-santiago-1.ocir.io/idhkis4m3p5e/django-sample-app-k8s:v0.0.1`

```shell
(venv) ubuntu@dalquintubuntuarm:~/REPOS/django-k8-sample/k8s_deployment$ docker push sa-santiago-1.ocir.io/idhkis4m3p5e/django-sample-nginx-k8s:v0.0.1
The push refers to repository [sa-santiago-1.ocir.io/idhkis4m3p5e/django-sample-nginx-k8s]
cd891328faf6: Pushed 
6e4a39e7acca: Pushed 
8f6d0026c2cc: Mounted from idhkis4m3p5e/django-nginx-k8s 
6276c65fe4d5: Mounted from idhkis4m3p5e/django-nginx-k8s 
c52b0b636089: Mounted from idhkis4m3p5e/django-nginx-k8s 
f2683d3e7323: Mounted from idhkis4m3p5e/django-nginx-k8s 
678a0785e7d2: Mounted from idhkis4m3p5e/django-nginx-k8s 
v0.0.1: digest: sha256:59083bfdef1240443ff2cd877c283f92a9ba5c28748b736ecfb57c772401a622 size: 1774
(venv) ubuntu@dalquintubuntuarm:~/REPOS/django-k8-sample/k8s_deployment$ docker push sa-santiago-1.ocir.io/idhkis4m3p5e/django-sample-app-k8s:v0.0.1
The push refers to repository [sa-santiago-1.ocir.io/idhkis4m3p5e/django-sample-app-k8s]
2a72c0f0aa5e: Pushed 
6faa2d4f8e86: Pushed 
42f9113c3ae7: Pushed 
deb0abe52b59: Pushed 
412cd8383a90: Pushed 
0c5b2785074b: Mounted from idhkis4m3p5e/django-app-k8s 
27da86305d5e: Mounted from idhkis4m3p5e/django-app-k8s 
798cb960efb8: Mounted from idhkis4m3p5e/django-app-k8s 
8691b6bf9361: Mounted from idhkis4m3p5e/django-app-k8s 
e2f13739ad41: Mounted from idhkis4m3p5e/django-app-k8s 
v0.0.1: digest: sha256:bd99d9ee1729a126cc255a52531c34097c47b51d74a1da2ef1762a264d0dfa9c size: 2423
```


After image is pushed, you will see it on OCIR like this: 

![](./img/ocir_image_push.png)


# Add secrets for production deployment

1. Execute the following to generate secrets based on a file

`kubectl create secret generic django-k8s-web-prod-env --from-env-file=web/.env`

Something like this will appear: 

```shell
(venv) ubuntu@dalquintubuntuarm:~/REPOS/django-k8-sample$ kubectl create secret generic django-k8s-web-prod-env --from-env-file=web/.env
secret/django-k8s-web-prod-env created
```

2. To verify secret got created correctly, run: 

`kubectl get secret django-k8s-web-prod-env -o YAML`

```shell
(venv) ubuntu@dalquintubuntuarm:~/REPOS/django-k8-sample$ kubectl get secret django-k8s-web-prod-env -o YAML
apiVersion: v1
data:
  DEBUG: MQ==
  DJANGO_SECRET_KEY: Zml4X3RoaXNfbGF0ZXI=
  DJANGO_SUPERUSER_EMAIL: ZHJhbHF1aW50YUBnbWFpbC5jb20=
  DJANGO_SUPERUSER_PASSWORD: ZDNubnk0bHF1MW5UYQ==
  DJANGO_SUPERUSER_USERNAME: ZGFscXVpbnQ=
  MYSQL_DB: ZGphbmdv
  MYSQL_HOST: MTAuMC4yLjE5Ng==
  MYSQL_PASSWORD: VzNsYzBtMzEu
  MYSQL_PORT: MzMwNg==
  MYSQL_READY: MQ==
  MYSQL_ROOT_PASSWORD: VzNsYzBtMzEu
kind: Secret
metadata:
  creationTimestamp: "2022-03-24T20:56:23Z"
  name: django-k8s-web-prod-env
  namespace: default
  resourceVersion: "49606"
  uid: 0f0f0856-799d-46c5-b62e-f2edc3a040ee
type: Opaque
```

# Generate django deployment

1. Generate an OCIR Secret to later embed into yaml file

run: `kubectl create secret docker-registry ocirsecret --docker-server=sa-santiago-1.ocir.io --docker-username='idhkis4m3p5e/oracleidentitycloudservice/denny.alquinta@oracle.com' --docker-password='YOUR_AUTH_TOKEN' --docker-email='denny.alquinta@oracle.com'`

You'll see something like this: 

```shell
(venv) ubuntu@dalquintubuntuarm:~/REPOS/django-k8-sample$ kubectl create secret docker-registry ocirsecret --docker-server=sa-santiago-1.ocir.io --docker-username='idhkis4m3p5e/oracleidentitycloudservice/denny.alquinta@oracle.com' --docker-password='YOUR_AUTH_TOKEN' --docker-email='denny.alquinta@oracle.com'
secret/ocirsecret created
```


2. Create the yaml file django-k8s-web.yaml

3. Deploy the container: 

`kubectl apply -f k8s_deployment/apps/django-k8s-web.yaml`


4. If everything went fine, this is what you should get: 

![](./img/k8_ok.png)


# Database side

1. Pre-create a MySQL Database and get credetials and coordinates
2. Connect into database and create the django DB for later usage. To do so: 

`mysql --host=10.0.2.196 --user=root --password=W3lc0m31.`

```shell
mysql> show databases;
+--------------------+
| Database           |
+--------------------+
| information_schema |
| mysql              |
| performance_schema |
| sys                |
+--------------------+
4 rows in set (0.00 sec)

mysql> CREATE DATABASE django;
Query OK, 1 row affected (0.01 sec)

mysql> show databases;
+--------------------+
| Database           |
+--------------------+
| django             |
| information_schema |
| mysql              |
| performance_schema |
| sys                |
+--------------------+
5 rows in set (0.00 sec)
```


# Finishing

If everything went fine, a LBaaS Should have been created as below: 

![](./img/lbaas_public.png)

and if accessing to this, you'll see this: 


![](./img/django_login_k8.png)



For do rollout deployment: 

`kubectl rollout status deployment/django-k9s-web`


---

# To create an application

1. Make sure your host has the MySQL Client files and binaries. In the case of ubuntu: 

```shell
Step 0: sudo apt install python3-dev build-essential

Step 1: sudo apt install libssl1.1

Step 2: sudo apt install libssl1.1=1.1.1f-1ubuntu2

Step 3: sudo apt install libssl-dev

Step 4: sudo apt install libmysqlclient-dev

Step 5: pip3 install mysqlclient
```

2. Then re-run `dependencies.sh`

3. Now run: (Based on: https://docs.djangoproject.com/en/4.0/intro/tutorial01/)

`python3 manage.py startapp polls`


4. Create a file under `polls/urls.py` that looks like this: 

```python
from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
]
```

5. Modify file `django_k8s/urls.py` to look like this: 

```python
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('polls/', include('polls.urls')),
    path('admin/', admin.site.urls),
]
```

6. Rebuild, retag and push the image: 

`docker tag django-k8s:v0.0.2 sa-santiago-1.ocir.io/idhkis4m3p5e/django-example:v0.0.2`
`docker push sa-santiago-1.ocir.io/idhkis4m3p5e/django-example:v0.0.2`


It'll look like this: 

```shell
(venv) ubuntu@dalquintubuntuarm:~/REPOS/django-k8-sample/web/polls$ docker image ls
REPOSITORY                                          TAG            IMAGE ID       CREATED         SIZE
django-k8s                                          v0.0.2         a5e481cfe439   2 minutes ago   582MB
sa-santiago-1.ocir.io/idhkis4m3p5e/django-example   v0.0.2         a5e481cfe439   2 minutes ago   582MB
mysql                                               oracle         00c014d8ea9c   13 hours ago    486MB
python                                              3.8.5-alpine   da3ea875dbcd   18 months ago   41.9MB
(venv) ubuntu@dalquintubuntuarm:~/REPOS/django-k8-sample/web/polls$ docker push sa-santiago-1.ocir.io/idhkis4m3p5e/django-example:v0.0.2
The push refers to repository [sa-santiago-1.ocir.io/idhkis4m3p5e/django-example]
cc9f1bced2fd: Pushed 
f5d27dd3a9b7: Pushed 
81bb673d2af6: Pushed 
6b8c463dd40c: Pushed 
50391f846464: Pushed 
0c5b2785074b: Layer already exists 
27da86305d5e: Layer already exists 
798cb960efb8: Layer already exists 
8691b6bf9361: Layer already exists 
e2f13739ad41: Layer already exists 
v0.0.2: digest: sha256:0126c15ccb3b830efdf47dd09b69fc27896fe84ac72c5309a298722f3ca1806c size: 2423
```


7. If everything went fine, then the deploy will look like this: 

![](./img/polls.png)

