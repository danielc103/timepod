import datetime, argparse

from kubernetes import client, config

# Set up parser for arguments being passed in
parser = argparse.ArgumentParser()
parser.add_argument('--namespace', '-n', required=True, help='namespace of scaler to be applied')
args = parser.parse_args()

# Load cluster config
# change to config.load_kube_config() for local testing
config.load_incluster_config()

# Set kubenetes client to use app library
v1 = client.AppsV1Api()

# Returns the digit of the current minute
def get_minute_val():
    now = datetime.datetime.now()
    return now.minute % 10

# Updates the supplied deployment's replicas using last digit of current time
def update_deployment_replicas(deplyoment):
    print('scaling deployment {} from {} pods to {} pods'.format(deplyoment.metadata.name, deplyoment.spec.replicas , get_minute_val()))
    deplyoment.spec.replicas = get_minute_val()
    v1.patch_namespaced_deployment(
        deplyoment.metadata.name,
        "default",
        body=deplyoment
    )

# simple annotation check to apply change
def check_annotaions(deployment):
    if 'daniel.me/auto-scale' in deployment.metadata.annotations:
        try:
            update_deployment_replicas(deployment)
        except:
            print("somethings broken")
    else:
        print("{} : does not contain correct annotation....gon get".format(deployment.metadata.name))


def main():
    namespace = args.namespace
    deploys = v1.list_namespaced_deployment(namespace, watch=False)
    if not deploys.items:
        print('There are no deployments with found')
    for item in deploys.items:
        check_annotaions(item)

if __name__ == '__main__':
    main()