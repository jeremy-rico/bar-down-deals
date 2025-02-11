# Bar Down Deals

A web application which scrapes the web for the best deals on hockey equipment.

# Project structure

# Tech Stack

- Scraper: Scrapy + Playwright
- Web Server: FastAPI
- Frontend: ReactJS
- Database: PostgreSQL

# TODO

1. properly install psycopg2 instead of psycopg2-binary in
   scraper/requirements.txt

# Notes

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
   - Otherwise you will need to create a custom security group
3. Accessing the database
   - See the #PostgresSQL Section

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

## PostgreSQL

### Installing

Since we used RDS to manage our database, we didn't have to manually install
a postgres server. However, if in the future you want to run a local postgres
instance see: https://www.postgresql.org/docs/16/tutorial-install.html for
installation instructions

### Acessing the database

In order to start using our database, we need to connect to it.

1. Installing psql on EC2
   - Use `yum search "postgres"` to find the version of postgres offered by
     yum
   - Once you find the version use `yum install -y postgres16` (my latest
     version offered was 16)
   - Note that the search results on literally return a 'postgres16' package,
     but if there are any that start with 'postgresXX' then you can do `yum
install postgresXX`
2. Accessing the database

   - You will need to use the following information to connect to the database

   1. Host: RDS -> Databases -> Endpoint
   2. User: User name you assigned at cretion
   3. Password: Password you assigned at creation
   4. Database name: postgres (or your database name)
   5. Post: 5432 (default)

   - A note on the password, I recommend letting AWS auto generate the password
     and then storing in SMM. You can then securly store the password and get it
     at anytime in the SMM console.
   - After you have all this info, use the following line to connect to the
     database:

   ```bash
   psql -h <endpoint> -U <user> -d <database_name>
   ```

   - If it is your first time connecting to the database the the database_name
     will ALWAYS be 'postgres'. After you have created a database, you will use
     the name of that database when connecting. A server can have multiple
     databases. Usually one per project.

### Creating the database and SQL queries.

- Read the [postgres docs](https://www.postgresql.org/docs/16/). They are quite good and will get you started creating databases, tables, data types, and writing queries.

## FastAPI

FastAPI has some [amazing docs](https://fastapi.tiangolo.com/tutorial/). You can
find most all FastAPI related information there. These notes will stick to
things that only directly relate to this project.

### Setting up a dev environment

In order to test out the apis in development you have to do two things.

1. Open up port 8000 in the EC2's security group.
   a. Navigate to the security group
   b. add new inbound rule
   c. Type: Custom TCP
   Port Range: 8000
   Source: My IP
   d. Save rules

2. Set up FastAPI dev server to listen on all ports

   ```bash
   fastapi dev main.py --host 0.0.0.0
   ```

3. Use your EC2's public IPv4 address in a browser
   ```
   <my.ec2.public.ipv4>:8000
   ```
