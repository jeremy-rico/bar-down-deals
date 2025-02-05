# bar-down-deals

A web application which scrapes the web for the best deals on hockey equipment.

# Web scraping

For now I have decided to use Scrapy as my main scraping engine with assist from
Playwright as needed.

# Notes from this project

## AWS

### Setting up EC2 and S3 communication

Scrapy docs use botocore with long term AWS credentials. This is only necessary
if you are running scrapy locally. Since I am running it on an EC2 instance, I
can use automatically generated short turn credentials for better security with
IAM Roles. Below are the steps I took to connect the EC2 instance with my S3
bucket:

1. Create an S3 Bucket

2. Create an IAM Role for the EC2 instance.

   - Go to IAM Console -> Roles -> Create new rolw
   - Choose AWS Service -> EC2
   - Select AmazonS3FullAccess (or write a custom policy)
   - Set name and create role

3. Assign IAM Role to EC2 instance

   - Select EC2 Instance -> Actions -> Security -> Modify IAM Role
   - Choose the role created in Step 2
   - Update IAM role

4. Ensure connection using the AWS CLI
   - SSH on to the instance
   ```bash
   aws s3 ls s3://bucket-name
   ```
   - If the bucket is empty, this will return nothing. You can move things to
     the bucket to test using the s3 CLI. See the documentation here:
     https://docs.aws.amazon.com/cli/latest/reference/s3/
