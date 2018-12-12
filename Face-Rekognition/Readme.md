## Implementing-AWS-Rekognition
### Requirments
```
1. AWS account 
2. Access to Amazon Rekognition service
3. Access to Amazon S3
4. IAM user
5. AWS CLI
6. Python (or java, or php)
```
## Step 1:

Click [here](https://aws.amazon.com/console/) to Login or signup for the AWS account. 

If you are signing up for a new account, you will need to proivde you credit card details.

But, do not worry Amazon provides the services for free for a year.

Amazon free - tire includes both Rekognition and S3 service for a year. 

So, you wont be charge untill you cross the free tire limits you can read more about it [here](https://aws.amazon.com/free/?sc_channel=PS&sc_campaign=acquisition_US&sc_publisher=google&sc_medium=ACQ-P%7CPS-GO%7CBrand%7CDesktop%7CSU%7CCore%7CCore%7CUS%7CEN%7CText&sc_content=Brand_Free_e&sc_detail=aws%20free%20tier&sc_category=Core&sc_segment=293614486743&sc_matchtype=e&sc_country=US&s_kwcid=AL!4422!3!293614486743!e!!g!!aws%20free%20tier&ef_id=EAIaIQobChMIi7Dozsua3wIVBglpCh0U6wR5EAAYASAAEgJiMfD_BwE:G:s)

## Step 2:

### Creating a IAM user

This will be the IAM user which we will be using for the API call

Once you logged in, In the find services, search for IAM users

Click on Users tab in the left side, now click on add user

Provides the user details, for example give the user name as face-reko

Select Programmatic access in the access type and click Next.

Next is the permissions settings. Make sure you click the THIRD box on the screen, that says ‘Attach existing policies directly’.

Then, on the ‘Filter: Policy Type’ search box below that, type in ‘rekognition’.

Choose ‘AmazonRekognitionFullAccess’ from the list by placing a check mark next to it.

Do the same for Amazon S3 and choose AmazonS3FullAccess from the list.

Almost Done! Now click on Next review, make sure you have access for both Rekognition and S3 services and Click create user.

Now we the a new IAM user
```
Now this page is IMPORTANT. Make a note of the AWS Key and Secret that you are given on this page, as we will need to incorporate it into our application below. Download the csv file credentials or copy the access key and security key.
```
For reference the key looks something like this
### Credentials
```
AWS_KEY=AX3BC4ASDLF324TLKSD09SLJK
AWS_SECRET=T37SFNLASOIASDFNnslxGHIDS/DFKLG
```
They appear as just random strings

## Step 3:

### Installing AWS CLI

Make sure you have python installed, we will be using python to perform API calls in this project

Open command prompt and type
```
pip install awscli
```
### Add credentials to aws configuration 

To add you IAM user credentials to the AWS CLI configuration enter
```
aws configure
```
Now enter you IAM user Access key and then Security key
For region enter the appropriate region for your IAM user Example: us-east-2
And for the output format enter json.

Now enter 
```
aws configure list 
```
to verify your credentials your output should look like this, but with you last 4 values of credentials.

```
      Name                    Value             Type    Location
      ----                    -----             ----    --------
   profile                <not set>             None    None
access_key     ****************N5XA shared-credentials-file
secret_key     ****************jPTy shared-credentials-file
    region                us-east-2      config-file    ~/.aws/config
```

Now it time to test out the services!











