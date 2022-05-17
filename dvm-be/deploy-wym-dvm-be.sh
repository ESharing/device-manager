kubectl delete -f nodeport-service-wym-dvm-be.yaml
kubectl delete -f nodeport-deployment-wym-dvm-be.yaml
./dockerbuild-wym-dvm-be.sh
kubectl apply -f nodeport-deployment-wym-dvm-be.yaml
kubectl apply -f nodeport-service-wym-dvm-be.yaml

