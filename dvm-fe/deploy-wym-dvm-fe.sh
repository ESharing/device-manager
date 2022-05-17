kubectl delete -f nodeport-service-wym-dvm-fe.yaml
kubectl delete -f nodeport-deployment-wym-dvm-fe.yaml
./dockerbuild-wym-dvm-fe.sh
kubectl apply -f nodeport-deployment-wym-dvm-fe.yaml
kubectl apply -f nodeport-service-wym-dvm-fe.yaml

