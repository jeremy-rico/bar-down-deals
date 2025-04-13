import boto3


def get_ssm_param(name, default="", secure=False) -> str:
    """
    Fetch parameters from AWS SSM parameter store

    Args:
        name: name of ssm param
        secure: bool if ssm param is encrypted

    Returns:
        Value of ssm param
    """
    ssm = boto3.client("ssm", region_name="us-west-1")
    try:
        param = ssm.get_parameter(Name=name, WithDecryption=secure)
        return param["Parameter"]["Value"]
    except:
        return default
