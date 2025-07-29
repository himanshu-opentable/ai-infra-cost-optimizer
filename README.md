# AI Infrastructure Cost Optimizer

A comprehensive solution for optimizing Kubernetes infrastructure costs through intelligent resource analysis and automated Horizontal Pod Autoscaler (HPA) configuration. This project combines a custom MCP (Model Context Protocol) server for Prometheus metrics collection with AI-driven cost optimization prompts.

## 🏗️ Architecture

The project consists of two main components:

### 1. Custom Prometheus MCP Server (`custom-prometheus-mcp-server/`)
A Model Context Protocol server that provides AI agents with direct access to Prometheus metrics for Kubernetes services.

**Key Features:**
- Dynamic environment-based Prometheus URL construction
- Asynchronous metric collection for CPU, memory, and pod count
- Real-time performance monitoring and reporting
- Support for multiple Kubernetes environments

### 2. Cost Optimizer Prompt (`cost-optimizer-prompt/`)
A detailed AI prompt framework for Site Reliability Engineers (SREs) to perform systematic Kubernetes service optimization.

**Key Features:**
- Iterative analysis across multiple environments
- Mathematical justification for resource allocation
- Automatic HPA configuration generation
- Cost optimization analysis with before/after comparisons

## 🚀 Getting Started

### Prerequisites
- Python 3.13 or higher
- Access to Prometheus endpoints
- Kubernetes cluster with appropriate monitoring setup

### Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd ai-infra-cost-optimizer
```

2. Install the MCP server dependencies:
```bash
cd custom-prometheus-mcp-server
pip install -r requirements.txt  # or use pyproject.toml
```

### MCP Server Usage

#### As an MCP Server
```python
python mcp_server.py
```

#### Standalone Testing
```bash
python main.py -e prod-sc2
```

### Using the Cost Optimizer Prompt

The cost optimizer prompt (`cost-optimizer-prompt/costOptimizer.md`) is designed to be used with AI agents capable of:
- Reading Kubernetes YAML configurations
- Accessing Prometheus metrics via the MCP server
- Performing mathematical calculations for resource optimization

## 📊 Metrics Collected

The system collects the following key metrics:

- **CPU Utilization**: Maximum CPU usage per pod over specified time periods
- **Memory Utilization**: Peak memory consumption with utilization percentages
- **Pod Count**: Maximum concurrent pod instances for scaling analysis

## 🎯 Optimization Targets

### Service Classification
- **Latency-Sensitive Services**: Target 55-65% CPU utilization
- **Batch/Cron Jobs**: Target ~80% CPU utilization

### Core Requirements
- **Guaranteed QoS**: Resource limits equal to requests
- **High Availability**: Minimum 3 replicas for production
- **Memory Safety**: Sub-75% average memory utilization
- **CPU-based Scaling**: HPA configured for CPU metrics only

## 🔧 Configuration

### Prometheus URLs
The system constructs Prometheus URLs dynamically:
```
https://prometheus.central-{env}.k8s.otenv.com
```

### Environment Support
- `prod-sc2` (Production South Central 2)
- `stage-sc3` (Staging South Central 3)
- Custom environments via configuration

## 📁 Project Structure

```
ai-infra-cost-optimizer/
├── README.md
├── cost-optimizer-prompt/
│   └── costOptimizer.md          # AI prompt for cost optimization
└── custom-prometheus-mcp-server/
    ├── main.py                   # Standalone test script
    ├── mcp_server.py            # MCP server implementation
    ├── prometheus_utils.py       # Prometheus query utilities
    └── pyproject.toml           # Python dependencies
```

## 🛠️ API Reference

### MCP Server Tool

#### `get_service_metrics`
Retrieves comprehensive performance metrics for a Kubernetes service.

**Parameters:**
- `namespace`: Kubernetes namespace (e.g., 'production', 'staging')
- `service_name`: Exact service name (e.g., 'api-gateway')
- `days`: Lookback period in days (default: 7)
- `env`: Target environment (default: 'prod-sc2')

**Returns:**
Formatted performance report with CPU, memory, and pod count metrics.

## 🔒 Security

- SSL verification disabled for internal Prometheus endpoints
- Environment-based URL validation
- No credential storage in code

## 📋 Best Practices

1. **Resource Allocation**: Always set limits equal to requests for Guaranteed QoS
2. **Scaling Strategy**: Use mathematical justification based on metric volatility
3. **Environment Isolation**: Test changes in staging before production deployment
4. **Monitoring**: Maintain observability throughout the optimization process

## 🤝 Contributing

This project is designed for infrastructure teams optimizing Kubernetes costs. Contributions should focus on:
- Enhanced metric collection capabilities
- Additional optimization strategies
- Improved AI prompt effectiveness
- Extended environment support

## 📄 License

[License information to be added]

## 📞 Support

For questions or issues:
1. Review the troubleshooting section in the cost optimizer prompt
2. Verify Prometheus connectivity and permissions
3. Check environment-specific configurations