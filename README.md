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

### RDS and EC2 Connection

RDS is AWS's Relational Database Service. It manages all the database stuff
making for high availability and automated backups. We will use this service and
connect to it from our EC2 instance

1. Creating Database Instance
   - Go to RDS -> Create Database
   - Select PostgreSQL
2. Connecting to EC2
   - When creating the RDS, you will have the option to connect it to an EC2
     instance. This will automatically create a security group for the two to
     communicate.
   - Otherwise you will need to create a custom secutiry group
3. Installing psql to test connection
   - Use `yum search "postgres"` to find the version of postgres offered by
     yum
   - Once you find the version use `yum install -y postgres16` (my latest
     version offered was 16)
4. Creating the database
   - The name you gave your RDS instance is NOT the DB_NAME.
   - On creation, RDS only creates the defauly database named 'postgres'
   - You will need to use the following information to connect to the database
     either using psycopg2 in python or psql from the terminal
   1. Host: RDS -> Databases -> Endpoint
   2. User: User name you assigned at cretion
   3. Password: Password you assigned at creation
   4. Post: 5432

### Securley storing secrets with SSM

We don't want to store our database password and host in plain text anywhere for
the project. We will use Amazon's SSM parameter store to encrypt and store them.

1. AWS Console -> SSM -> Parameter Store -> Create Parameter
   OR
   Use the AWS CLI

   ```bash
   aws ssm put-parameter --name "DB_HOST" --value "xyz" --type "SecureString"
   aws ssm put-parameter --name "DB_NAME" --value "databaseName" --type "String"
   aws ssm put-parameter --name "DB_USER" --value "postgres" --type "String"
   aws ssm put-parameter --name "DB_PASSWORD" --value "postgrespassword" --type "SecureString"
   ```

2. Add our database parameters, select SecureString for sensitive info like the
   hostname and password
3. Once added we will need to allow out EC2 to access these values.
   3a. Edit our EC2's IAM role and attach the AmazonSSMManagedInstanceCore policy
   3b. install boto3 on instance
   3c. use botos ssm.get_parameter() see: https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm/client/get_parameter.html
4. These values can now be used with psycopg2 to connect to the database
