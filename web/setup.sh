#!/bin/bash

kubectl create namespace web
kubectl create -f config/*.yaml -n web