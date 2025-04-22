# 1Password Connect and Operator Helm charts

For my homelab I am exploring to use 1Password as my secrets manager. I found out that they conveniently offer sweet integration with K8s through their Connect and Operator Helm charts.

I followed [this](https://developer.1password.com/docs/k8s/helm-config/) guide. I describe the key steps below for my future reference.

1. Create a [secrets automation workflow](https://developer.1password.com/docs/connect/get-started/?deploy=kubernetes#step-1) using either the UI or CLI. Keep the credentials.json some place safe. You will need to reference the file in a future step. The process to obtain the token will also be explained, although it appears to be optional from the following instructions.
2. Add the helm repo `helm repo add 1password https://1password.github.io/connect-helm-charts/`
3. Install the chart and add the path to your credentials.json file as well as the token `helm install connect 1password/connect --set-file connect.credentials=1password-credentials.json --set operator.create=true --set operator.token.value=OP_CONNECT_TOKEN`

Et voila! That is a basic installation of 1password functionality in K8s done. 

I find it neat that 1Password uses K8s secrets which will make it easy to create the secret manifest and include it in my FluxCD workflow in my homelab.
