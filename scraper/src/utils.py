# import boto3


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
