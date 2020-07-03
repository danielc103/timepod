# autoscaler


## simple cron job that auto scales the number of pods to be equal to the last digit of the current minute with an added annotation the deployment


### How to use
---

Deploy provided helm chart to desired namespace.

```cli
helm install scaler autoscaler
```

Helm chart contains:

* `cronjob` : cronjob resource that contains python image with script
* `service account` : this allows for setting up for correct RBAC permissions for the cronjob 
*  `role` : defines accessable apis
*  `role binding` : binds the role and rules to service account

Create a deployment using the annotation below.  There is a sample deployment in the repository you can deploy called `test-deployment.yaml`

```cli
kubectl create -f test-deployment.yaml
```

```yaml
annotations:
    'daniel.me/auto-scale': 'true'
```

### Development
---

Supplied Dockerfile for local testing.

`autoscaler.py` is a simple python script using the kubernetes-client module.  To test outside of cluster please update the following bit of code.

```python
...
# Remove load cluster command and replace with load kube config
config.load_incluster_config() 

config.load_kube_config()

```