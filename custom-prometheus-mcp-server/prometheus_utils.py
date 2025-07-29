import os
import asyncio
from datetime import datetime, timedelta
from prometheus_api_client import PrometheusConnect
from prometheus_api_client.exceptions import PrometheusApiClientException

# The global Prometheus client instance, initialized to None.
prom: PrometheusConnect | None = None

def initialize_prometheus_client(env: str):
    """
    Initializes the Prometheus client with a URL based on the environment.

    This function must be called once from the main script before any of the
    data-fetching functions are used.

    Args:
        env: The environment name (e.g., 'prod-sc2').
    """
    global prom
    # Construct the URL dynamically based on the environment
    url = f"https://prometheus.central-{env}.k8s.otenv.com"
    print(f"✅ Initializing Prometheus client for environment: {env}")
    print(f"   URL: {url}")
    prom = PrometheusConnect(url=url, disable_ssl=True)


async def get_max_cpu_utilization(namespace: str, service_name: str, days: int = 7) -> float | None:
    """
    Fetches the max CPU utilization for a service over a number of days.
    """
    if prom is None:
        raise Exception("Prometheus client not initialized. Call initialize_prometheus_client() first.")
        
    print(f"Starting CPU query for {service_name} in {namespace} over {days} days...")
    end_time = datetime.now()
    start_time = end_time - timedelta(days=days)
    query_step = "1h"

    # This query fetches the max CPU utilization per pod.
    promql_query = f"""
    max(ot:container:cpu_utilization:max_3m{{namespace="{namespace}", container!~"istio-proxy|.+-sidecar"}}) by (pod, label_app) * on (label_app) group_left(service) max(kube_service_labels{{namespace="{namespace}", service="{service_name}"}}) by (label_app)
    """
    
    try:
        result = await asyncio.to_thread(
            prom.custom_query_range,
            query=promql_query,
            start_time=start_time,
            end_time=end_time,
            step=query_step,
        )
        if not result:
            return None
            
        max_value = 0.0
        for series in result:
            for value_pair in series.get("values", []):
                current_value = float(value_pair[1])
                if current_value > max_value:
                    max_value = current_value
        return max_value
    except PrometheusApiClientException as e:
        print(f"❌ An error occurred while querying Prometheus: {e}")
        return None

async def get_max_memory_utilization(namespace: str, service_name: str, days: int = 7) -> float | None:
    """
    Fetches the max memory utilization for a service over a number of days.
    """
    if prom is None:
        raise Exception("Prometheus client not initialized. Call initialize_prometheus_client() first.")
        
    print(f"Starting memory query for {service_name} in {namespace} over {days} days...")
    end_time = datetime.now()
    start_time = end_time - timedelta(days=days)
    query_step = "1h"

    # --- MODIFIED QUERY ---
    # This query now fetches the max memory utilization per pod.
    promql_query = f"""
    max(ot:container:memory_utilization:max_3m{{namespace="{namespace}", container!~"istio-proxy|.+-sidecar"}}) by (pod, label_app) * on (label_app) group_left(service) max(kube_service_labels{{namespace="{namespace}", service="{service_name}"}}) by (label_app)
    """

    try:
        result = await asyncio.to_thread(
            prom.custom_query_range,
            query=promql_query,
            start_time=start_time,
            end_time=end_time,
            step=query_step,
        )
        if not result:
            return None

        # This logic correctly finds the max value across all series (pods).
        max_value = 0.0
        for series in result:
            for value_pair in series.get("values", []):
                current_value = float(value_pair[1])
                if current_value > max_value:
                    max_value = current_value
        return max_value
    except PrometheusApiClientException as e:
        print(f"❌ An error occurred while querying Prometheus: {e}")
        return None

async def get_max_pod_count(namespace: str, service_name: str, days: int = 7) -> int | None:
    """
    Fetches the max concurrent pod count for a service over a number of days.
    """
    if prom is None:
        raise Exception("Prometheus client not initialized. Call initialize_prometheus_client() first.")
        
    print(f"Starting pod count query for {service_name} in {namespace} over {days} days...")
    end_time = datetime.now()
    start_time = end_time - timedelta(days=days)
    query_step = "1h"

    promql_query = f"""
    count(
        kube_pod_info{{namespace="{namespace}"}}
        * on(pod) group_left(label_app)
        kube_pod_labels{{namespace="{namespace}"}}
        * on(label_app) group_left(service)
        kube_service_labels{{service="{service_name}", namespace="{namespace}"}}
    )
    """
    try:
        result = await asyncio.to_thread(
            prom.custom_query_range,
            query=promql_query,
            start_time=start_time,
            end_time=end_time,
            step=query_step,
        )
        if not result:
            return None
        max_pods = 0
        for series in result:
            for value_pair in series.get("values", []):
                current_pods = int(value_pair[1])
                if current_pods > max_pods:
                    max_pods = current_pods
        return max_pods
    except PrometheusApiClientException as e:
        print(f"❌ An error occurred while querying Prometheus: {e}")
        return None