import asyncio
import argparse

# Assuming your script is saved as 'prometheus_utils.py'
from prometheus_utils import (
    initialize_prometheus_client,
    get_max_cpu_utilization,
    get_max_memory_utilization,
    get_max_pod_count,
)

async def main():
    """
    Main function to parse arguments and run the metric fetching tasks.
    """
    # Set up the command-line argument parser
    parser = argparse.ArgumentParser(description="Test script for fetching Prometheus metrics.")
    parser.add_argument(
        "-e", "--env", 
        type=str, 
        required=True, 
        help="The target environment (e.g., 'prod-sc2')."
    )
    args = parser.parse_args()

    # Hardcoded values as requested
    namespace = "restaurant"
    service_name = "service-restaurant-cache-populator"
    env = args.env
    
    print("--- 🚀 Starting Prometheus Metrics Test ---")
    print(f"Environment: {env}")
    print(f"Namespace:   {namespace}")
    print(f"Service:     {service_name}")
    print("------------------------------------------\n")

    try:
        # Initialize the global Prometheus client
        initialize_prometheus_client(env=env)

        # Run all metric-gathering tasks concurrently for efficiency
        print("\nFetching metrics for the last 7 days...\n")
        
        # Create tasks for each async function call
        tasks = [
            get_max_cpu_utilization(namespace=namespace, service_name=service_name),
            get_max_memory_utilization(namespace=namespace, service_name=service_name),
            get_max_pod_count(namespace=namespace, service_name=service_name),
        ]

        # Wait for all tasks to complete
        max_cpu, max_mem, max_pods = await asyncio.gather(*tasks)

        # --- Display the results ---
        print("\n--- 📊 Final Results ---")
        if max_cpu is not None:
            print(f"Maximum CPU Utilization:    {max_cpu:.2f}%")
        else:
            print("Maximum CPU Utilization:    Not available")

        if max_mem is not None:
            print(f"Maximum Memory Utilization: {max_mem:.2f}%")
        else:
            print("Maximum Memory Utilization: Not available")

        if max_pods is not None:
            print(f"Maximum Pod Count:          {max_pods}")
        else:
            print("Maximum Pod Count:          Not available")
            
        print("------------------------\n")

    except Exception as e:
        print(f"❌ An unexpected error occurred in the main script: {e}")


if __name__ == "__main__":
    asyncio.run(main())