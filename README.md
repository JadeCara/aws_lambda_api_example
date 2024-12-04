## Python AWS Lambda Setup With local run Option

To run this locally you can either set up a local dynamodb instance, instructions [here](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/DynamoDBLocal.html).

Or make a couple dynamodb tables to support the back end. I added the scripts I used to create these tables in the `app/awscli.sh` [file](https://github.com/JadeCara/aws_lambda_api_example/blob/a5569b2dd3500fcb24fb299388f1e08a85594296/app/awscli.sh)

### To run locally:
Clone this repo. 

>[!TIP]
> Make sure your aws config is set up!

Create your dynamodb tables

Navigate into the project directory

run ```sh uvicorn app.main:app --reload```

>[!TIP]
> Once that is running docs can be found at http://127.0.0.1:8000/docs where they are kindly generated for us by FastApi using openapi. 


Curl Commands for all api calls can be found there or in the docstrings on the routes. 