# creating namespace
kubectl create -f k8s/project_namespace.yaml

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