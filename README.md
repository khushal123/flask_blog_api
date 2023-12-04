
# Flask Blog API

## Introduction
`flask_blog_api` is a RESTful API built using Flask, designed to power blog applications. This API supports functionalities such as user authentication, blog post creation, and commenting on posts.

## Prerequisites
- Python 3.11.6
- Poetry for dependency management
- Postman for API testing

## Setup Instructions
1. **Clone the Repository**: Clone this repository to your local machine.

2. **Install Dependencies**:
   Navigate to the cloned directory and run:
   ```
   poetry install
   ```

3. **Environment Setup**:
   - Copy the contents from `.env.example` to `dev.env` and `test.env`.
   - Update `dev.env` and `test.env` with appropriate values for your development and testing environments.



## Running the Project
To run the development server, execute:
```
export ENVIRONMENT=development && poetry run python run.py
```
This will start the Flask development server with the configuration specified in `dev.env`.

## Running Tests
For running tests, use:
```
export ENVIRONMENT=test && poetry run pytest tests/
```
This command will run the test suite using the configuration specified in `test.env`.

## Using the Postman Collection
Import the provided Postman collection into your Postman application to interact with the API. The collection includes pre-configured requests for registering users, logging in, creating posts, adding comments, and more.

## Contact
For any queries or contributions, please contact Khushal Chouhan at khushalsingh12@gmail.com.
