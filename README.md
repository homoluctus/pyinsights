# PyInsights

![PyPI - Python Version](https://img.shields.io/pypi/pyversions/pyinsights)
![PyPI](https://img.shields.io/pypi/v/pyinsights?color=blue)
![GitHub](https://img.shields.io/github/license/homoluctus/pyinsights)

A CLI tool To query CloudWatch Logs Insights.

## ToC

- [Usage](#Usage)
  - [Write Configuration](#Write%20Configuration)
  - [Execute command](#Execute%20command)
- [Configuration](#Configuration)
- [CLI Options](#CLI%20Options)
- [Environment Variable](#Environment%20Variable)

## Usage

### Write Configuration

Write configuration to `pyinsights.yml` like:

```yaml
version: '1.0'
log_group_name:
  - '/ecs/sample'
query_string: 'field @message | filter @message like /ERROR/'
duration: '30m'
limit: 10
```

I wrote examples, so see [examples folder](https://github.com/homoluctus/pyinsights/tree/master/examples).

### Execute command

```bash
pyinsights -c pyinsights.yml -p aws_profile -r region
```

## Configuration

|Parameter|Type|Required|Description|
|:--:|:--:|:--:|:--|
|version|string|true|Choose configuration version from ['1.0']|
|log_group_name|array|true|Target log group names to query|
|query_string|string|true|Pattern to query|
|duration|string or object|true||
||string||Specify hours, minutes or seconds from now<br>Unit: hours = `h`, minutes = `m`, seconds = `s`|
||object||Specify `start_time` and `end_time`<br>Datetime format must be `YYYY-MM-DD HH:MM:SS`|
|limit|integer|false|The number of log to fetch|

## CLI Options

|Option|Required|Description|
|:--:|:--:|:--|
|-c, --config|true|Specify yaml configuration by absolute or relative path|
|-f, --format|false|Choose from json or table|
|-p, --profile|false|AWS profile name|
|-r, --region|false|AWS region|
|-v, --version|false|Show version|

## Environment Variable

If `profile` and `region` options are not specified, AWS Credentials must be set as environment variables.

- AWS_ACCESS_KEY_ID
- AWS_SECRET_ACCESS_KEY
- AWS_DEFAULT_REGION

Please see [Environment Variable Configuration](https://boto3.amazonaws.com/v1/documentation/api/latest/guide/configuration.html#environment-variable-configuration) for the detail.
