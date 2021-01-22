# django-dynamodb-crudapp
THIS IS DJANGO_BLOG_CRUD APP DESGINED USING AWS DYNAMODB AS THE BACKEND USING 'boto3'.

In order to use this you must  first install boto3 on your device.

STEPS TO RUN THE APP:

1: Clone the repo.

2: Create a dynamodb table in aws with three fields- blogid,title,body.

3: Give your aws credentials,region of dynamodb and name of the dynamobd table in the __init__ fucntion of dynamodbcrud class in views.py.

4: python3 manage.py runserver.
