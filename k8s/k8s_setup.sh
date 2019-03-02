#!/bin/bash
export KOPS_STATE_STORE=s3://anyuz-k8s-state
# export REGION=us-west-1
# ZONES=`aws ec2 describe-availability-zones --region ${REGION} | jq -r '.AvailabilityZones | map(.ZoneName) | join(",")'`
DOMAIN=anyuzdevopsinsight2018.com
ZONES=us-west-1a
NODE=6
MASTERSIZE=t2.xlarge
NODESIZE=m4.xlarge


kops create cluster \
	--name k8s.${DOMAIN} \
	--dns-zone ${DOMAIN} \
	--master-zones ${ZONES} \
	--master-size ${MASTERSIZE} \
	--zones ${ZONES} \
	--node-size ${NODESIZE}\
	--node-count ${NODE} \
	--networking weave \
	--topology private \
	--state=$KOPS_STATE_STORE \
	--yes
echo "========================================"
echo "Wait for 2min for cluster to spin up ..."
echo "========================================"
sleep 2m

echo "========================================"
echo "Validating Cluster ..."
echo "========================================"
kops validate cluster 

echo "========================================"
echo "Check API server ..."
echo "========================================"
kubectl cluster-info

echo "========================================"
echo "Install Tiller ..."
echo "========================================"
kubectl apply -f config/rbac-admin.yaml
kubectl apply -f config/rbac-tiller.yaml
helm init --service-account tiller 

helm install stable/kubernertes-dashboard \
     --name k8sdashboard --namespace kube-system \
     -f config/helm-k8sdashboard.yaml 

