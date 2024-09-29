# deploy model app
kubectl create -f k8s/model.yaml -n lab8
# deploy datamart app
kubectl create -f k8s/datamart.yaml -n lab8