# PyInsights

![PyPI - Python Version](https://img.shields.io/pypi/pyversions/pyinsights)
![PyPI](https://img.shields.io/pypi/v/pyinsights?color=blue)
![GitHub](https://img.shields.io/github/license/homoluctus/pyinsights)

A CLI tool To query CloudWatch Logs Insights.

![usage1](https://raw.githubusercontent.com/homoluctus/pyinsights/master/images/usage1.png)

![usage2](https://raw.githubusercontent.com/homoluctus/pyinsights/master/images/usage2.png)

# ToC

<!-- TOC depthFrom:2 -->

- [Usage](#usage)
  - [Write Configuration](#write-configuration)
  - [Execute command](#execute-command)
- [Configuration](#configuration)
- [CLI Options](#cli-options)
- [Environment Variable](#environment-variable)

<!-- /TOC -->

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
||string||Specify hours, minutes or seconds from now<br>Unit:<br>hours = `h`,<br>minutes = `m`,<br>seconds = `s`,<br>days = `d`,<br>weeks = `w`|
||object||Specify `start_time` and `end_time`<br>Datetime format must be `YYYY-MM-DD HH:MM:SS`|
|limit|integer|false|The number of log to fetch|

## CLI Options

|Option|Required|Description|
|:--:|:--:|:--|
|-c, --config|true|Specify yaml configuration by absolute or relative path|
|-f, --format|false|Choose from json or table|
|-p, --profile|false|AWS profile name|
|-r, --region|false|AWS region|
|-q, --quiet|false|Suppress progress message|
|-v, --version|false|Show version|

## Environment Variable

If `profile` and `region` options are not specified, AWS Credentials must be set as environment variables.

- AWS_ACCESS_KEY_ID
- AWS_SECRET_ACCESS_KEY
- AWS_DEFAULT_REGION

Please see [Environment Variable Configuration](https://boto3.amazonaws.com/v1/documentation/api/latest/guide/configuration.html#environment-variable-configuration) for the detail.
