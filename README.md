# PyInsights

A CLI tool To query CloudWatch Logs Insights.

## Usage

### 1. Write Configuration

write configuration to `pyinsights.yml` like:

```yaml
version: '1.0'
log_group_name:
  - '/ecs/sample'
pattern: 'field @message | filter @message like /ERROR/'
duration: '30m'
limit: 10
```

### 2. Execute command

```bash
pyinsights -c pyinsights.yml -p aws_profile -r region
```
