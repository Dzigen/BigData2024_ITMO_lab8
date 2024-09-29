# creating namespace
kubectl create -f k8s/project_namespace.yaml

kubectl create serviceaccount spark --namespace=default
kubectl create clusterrolebinding spark-operator-role --clusterrole=cluster-admin --serviceaccount=default:spark --namespace=default
helm repo add spark-operator https://kubeflow.github.io/spark-operator
helm install spark-operator/spark-operator --namespace lab8 --set sparkJobNamespace=default --set webhook.enable=true --generate-name

# creating pv
kubectl create -f k8s/shared_pv.yaml
kubectl create -f k8s/mysql_pv.yaml
#kubectl create -f k8s/configs_pv.yaml

# creating pvc
kubectl create -f k8s/shared_pvc.yaml -n lab8
kubectl create -f k8s/mysql_pvc.yaml -n lab8
#kubectl create -f k8s/configs_pvc.yaml -n lab8

# creating configmap and secret
kubectl create -f k8s/mysql_secret.yaml -n lab8
kubectl create -f k8s/mysql_config.yaml -n lab8

# deploy mysql app
kubectl create -f k8s/mysql.yaml -n lab8
# deploy model app
kubectl create -f k8s/model.yaml -n lab8
# deploy datamart app
kubectl create -f k8s/datamart.yaml -n lab8