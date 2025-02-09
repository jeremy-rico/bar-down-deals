import boto3


def get_ssm_param(name, default="", secure=False):
    """
    Fetch parameters from AWS SSM parameter store
    """
    ssm = boto3.client("ssm", region_name="us-west-1")
    try:
        param = ssm.get_parameter(Name=name, WithDecryption=secure)
        return param["Parameter"]["Value"]
    except:
        return default


def cleanPrice(s: str):
    """
    Remove dollar symbol from string
    """
    if s.startswith("$"):
        return s[1 : len(s)]
    return s


def cleanBrand(s: str):
    """
    Clean scraped brand string
    """
    if s.lower().startswith("by"):
        return s.split()[-1]
    return s
