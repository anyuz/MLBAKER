#!/bin/bash
kubectl create namespace db
cat <<EOF | kubectl create -f -
apiVersion: v1
kind: Secret
metadata:
  name: mongodb
  namespace: db
type: Opaque
stringData:
  mongodb-root-password: $(head -c 24 /dev/random | base64)
EOF

helm install stable/mongodb \
     --name mongodb --namespace db \
     -f config/helm-mongodb.yaml