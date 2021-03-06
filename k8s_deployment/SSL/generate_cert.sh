#!/bin/bash

kubectl delete secret tls-secret
openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout tls.key -out tls.crt -subj "/CN=test.ocitestdomain.co.uk" 
kubectl create secret tls tls-secret --key tls.key --cert tls.crt