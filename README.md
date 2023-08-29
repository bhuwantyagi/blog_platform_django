# Blog Platform for Shyftlabs Assignment

## Table of Contents
1. Project Structure
2. Prerequisites
3. Installation
4. How to Run
5. Usage
6. Tests

```
-blog-platform-shyftlabs

    |- backend
        |- backend
            |- __init__.py
            |- settings.py
            |- urls.py
        |- blog
            |- migrations
                |- __init__.py
                |- 0001_initial.py
            |- __init__.py
            |- admin.py
            |- apps.py
            |- models.py
            |- schema.py
            |- tests.py
            |- utils.py
        |- manage.py
```

## Prerequisites
1. Python 3.x
2. Django 4.x
3. PostgreSQL



## Installation

Clone the Repository

```
git clone https://github.com/bhuwantyagi/blog_platform_shyftlabs.git
```

Navigate To Directory
```
cd blog_platform_shyftlabs
cd backend
```
Create python environment and activate it
```
python -m venv venv

for mac:
source venv/bin/activate
```

Install Requirements
```
pip install -r requirements.txt
```


Update settings.py
Open ```backend/settings.py``` and update the DATABASE and other configurations if necessary.




## How to Run

Initialize the Database

```
python manage.py migrate
```

Create Superuser (Optional)

```
python manage.py createsuperuser
```

Run the Development Server

```
python manage.py runserver
```

The API will be available at http://127.0.0.1:8000/graphql.


## Usage
### Endpoints
Admin Interface: http://127.0.0.1:8000/admin/
GraphQL Endpoint: http://127.0.0.1:8000/graphql/

### Authentication
To create a JWT token, use the createUser mutation. Tokens will be needed to authenticate other GraphQL queries/mutations.

### GraphQL Queries and Mutations
You can use the built-in GraphQL IDE available at the /graphql/ endpoint to execute queries and mutations.

Create User

```
mutation {
  createUser(username: "testuser", email: "testuser@gmail.com", password: "testpassword") {
    user {
      username
    }
    token
  }
}
```

Create Post

```
mutation {
  createPost(token: "your_token", title: "New Post", content: "This is a new post") {
    post {
      title
    }
    success
    errors
  }
}

```

... and many more. Refer to blog/schema.py for the full list of queries and mutations.


## Test
Run the following command to execute the tests:

```
python manage.py test
```
