import asyncio
from mcp.server.fastmcp import FastMCP
# 1. Import the new initialization function
from prometheus_utils import (
    initialize_prometheus_client,
    get_max_cpu_utilization,
    get_max_memory_utilization,
    get_max_pod_count
)

# Initialize FastMCP server
mcp = FastMCP("prometheus_monitor")


@mcp.tool()
# 2. Add the new 'env' parameter to accept the environment name
async def get_service_metrics(namespace: str, service_name: str, days: int = 7, env: str = "prod-sc2") -> str:
    """
    Provides a full performance report for a specific Kubernetes service.

    This tool fetches the maximum CPU utilization, maximum memory utilization,
    and the maximum concurrent pod count for the requested service over a
    specified number of days.

    Args:
        namespace: The Kubernetes namespace where the service is running (e.g., 'production', 'staging').
        service_name: The exact name of the service to get metrics for (e.g., 'api-gateway', 'user-database').
        days: The number of days to look back for the metrics. Defaults to 7.
        env: The target environment (e.g., 'prod-sc2', 'stage') used to construct the Prometheus URL.
    """
    # 3. Call the initialization function first
    # This sets up the correct Prometheus client in the utility module.
    initialize_prometheus_client(env=env)

    print(f"Gathering all metrics for service '{service_name}' in '{env}'...")

    # The rest of your logic remains the same
    results = await asyncio.gather(
        get_max_cpu_utilization(namespace=namespace, service_name=service_name, days=days),
        get_max_memory_utilization(namespace=namespace, service_name=service_name, days=days),
        get_max_pod_count(namespace=namespace, service_name=service_name, days=days)
    )

    max_cpu, max_mem, max_pods = results

    if all(r is None for r in results):
        return f"Could not retrieve any metrics for service '{service_name}' in namespace '{namespace}'."

    report_header = f"📈 Performance Report for Service: '{service_name}' (Last {days} Days in {env})\n"
    report_lines = ["-" * (len(report_header) - 1)]

    if max_cpu is not None:
        report_lines.append(f"  - 🧠 **Max CPU Utilization**: {max_cpu:.2f}%")
    else:
        report_lines.append("  - 🧠 **Max CPU Utilization**: Data not available")

    if max_mem is not None:
        report_lines.append(f"  - 💾 **Max Memory Utilization**: {max_mem:.2f}%")
    else:
        report_lines.append("  - 💾 **Max Memory Utilization**: Data not available")

    if max_pods is not None:
        report_lines.append(f"  - 🤖 **Max Pod Count**: {max_pods} pods")
    else:
        report_lines.append("  - 🤖 **Max Pod Count**: Data not available")

    return "\n".join([report_header] + report_lines)


if __name__ == "__main__":
    print("🚀 Starting Prometheus Monitor MCP Server...")
    mcp.run(transport='stdio')