# k8s 常用command

kubectl exec: 在pod中执行命令

kubectl cluster-info

kubectl get nodes/pods

kubectl describe pod/nodes/svc

kubectl expose rc

// 通过yaml创建k8s资源

kubectl create -f this_is_a_test.yaml

// 打开并编辑资源的yaml文件

kubectl edit <type> <resoure_name>

// 获取pod的yaml配置信息

kubectl get pod test_pod -o yaml

// 获取pod的日志

kubectl logs <name>

// 如果一个pod中包含多个container

kubectl logs <pod_name> -c <container_name>

// 获取上一个容器的log

kubectl logs <pod_name> --previous

// 将pod的端口绑定到本机指定端口

kubectl port-forward <pod_name> <local_port>:<pod_port>

// 查看资源的label

kubectl get po --show-labels
kubectl get po -L <label_name_1>,<label_name_2>

// 删除当前namespace下的所有资源(太危险了，不应该使用)

kubectl delete all --all

k run test --image=benjilee5453/test --port=5000 

k expose pod test --type NodePort --port 8080
> 这里的port指的是需要绑定的pod的端口。
minikube service hello-minikube --url

source <(kubectl completion zsh) # zsh kubuctl 命令自动补全