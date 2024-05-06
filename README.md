## Vendor Management System with Performance Metrics

#### Clone the Project Repository
```
  git clone https://github.com/bkumar28/vms.git
```
 
#### Python Version Requirement
 - Python 3.9.4

#### Create a Virtual Environment
```
 virtualenv venv -p python3
```

#### Activate the Virtual Environment

```
 source venv/bin/activate
```
#### Navigate to the Project Directory (vms)

```
 cd vms/
```

#### Install Dependencies

```
 pip3 install -r requirements.txt
```

#### Navigate to the SRC Directory (src)

```
 cd src/
```

#### Run Migration Command

```
 python manage.py migrate
```

#### Create a Super Admin User

```
  python manage.py createsuperuser
>>>  username : super_admin
>>>  email_address : kumar.bhart28@gmail.com
>>>  password : admin@1234
>>>  password (again): admin@1234
```

## Running the Application

#### Run the Test Suite
```
coverage run manage.py test -v 2
```

#### Code Coverage Report
```
coverage report
```

#### Run the Django Server
```
 python3 manage.py runserver
```

## Accessing API Documentation

#### Swagger Documentation
To access the Swagger documentation and interact with the API endpoints, simply open your web browser and navigate to the Swagger UI URL provided for your API. From there, you can explore the available endpoints and make requests directly within the Swagger interface.

Open your web browser and navigate to:

```
http://127.0.0.1:8000/swagger
```

#### API Documentation
Explore the API documentation to gain insights into API endpoints, including details such as response data, response status codes, payload structure, and required fields along with their data types. This documentation serves as a comprehensive guide to understanding how to interact with the API effectively.

Explore API details at:

```
http://127.0.0.1:8000/api-doc
```