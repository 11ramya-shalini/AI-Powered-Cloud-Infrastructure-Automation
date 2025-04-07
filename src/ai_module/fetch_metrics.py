import requests

def get_cpu_metrics(prometheus_url="http://localhost:9090"):
    # query: CPUacross all pods
    query = 'sum(rate(container_cpu_usage_seconds_total[1m])) by (pod)'
    response = requests.get(f"{prometheus_url}/api/v1/query", params={'query': query})

    if response.status_code == 200:
        results = response.json()['data']['result']
        pod_cpu = {item['metric']['pod']: float(item['value'][1]) for item in results}
        return pod_cpu
    else:
        print(f"Failed to fetch metrics. Status code: {response.status_code}")
        return {}
