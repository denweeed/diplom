# InflationCalcAPI

**InflationCalcAPI** is a REST service developed for calculating the inflation of a product basket. Using this service, you can analyze price changes for different products and determine the overall inflation rate.

## Features

- Supports inflation calculation based on product data, their prices, and quantities.
- Accounts for price changes from different periods for accurate inflation calculation.
- Simple and intuitive interface using FastAPI.
- Stores product and price data in MongoDB for convenient management and access to information.

## Prerequisites

- Docker: [Install Docker](https://docs.docker.com/get-docker/)
- Docker Compose: [Install Docker Compose](https://docs.docker.com/compose/install/)

## Usage

1. Clone the repository: `git clone https://github.com/denweeed/diplom`
2. Navigate to the project directory: `cd diplom`
3. Build and start the Docker containers: `docker-compose up -d` 

The API server and MongoDB database will be started in separate containers.

4. Open your browser and go to `http://localhost:8000/docs` to view the API documentation.
5. Use API requests to send product data and receive inflation calculations.

# How it works

The InflationCalcAPI project is a REST service that calculates the inflation rate of a product basket. It utilizes the FastAPI framework for building the API and MongoDB for data storage.

Here's an overview of how the project works:

1. The API exposes several endpoints that allow users to interact with the service.
2. When the API receives a request to calculate the inflation rate, it retrieves the product basket data from the MongoDB database.
3. The API then performs the necessary calculations to determine the inflation rate based on the provided product basket.
4. The calculated inflation rate is returned as a response to the client.
5. Users can also send requests to add or update product data in the database using the appropriate API endpoints.
6. The project is set up to run in a Docker container, ensuring easy deployment and scalability.

# Running the Project

To run this project and get it up and running, follow these steps:

1. Make sure Docker containers are running by executing the command `docker-compose up -d`.
2. Open your browser and go to `http://localhost:8000/docs` to view the API documentation.
3. Use API requests to send product data and receive inflation calculations.

Note: Before running the project, make sure you have installed the necessary dependencies and properly configured the project.

# Running Tests

To run tests for this project, follow these steps:

1. Make sure the Docker containers are running by executing the command `docker-compose up -d`.
2. Navigate to the project directory in your terminal.
3. Run the following command to execute the tests:

   ```bash
   docker-compose exec app pytest
   
4. Review the test results to ensure that all tests have passed successfully.

## Authors

InflationCalcAPI is developed by a team of developers:

- Developer Name 1 - [@denweeed](https://github.com/denweeed)
- Developer Name 2 - [@belimenkon](https://github.com/belimenkon)
- 