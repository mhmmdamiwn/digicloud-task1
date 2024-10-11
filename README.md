# RSS Scraper Microservices Project

This project is a Python-based RSS scraper built with a microservices architecture using Docker, RabbitMQ, MySQL, and Nameko. It is designed to fetch, parse, and manage RSS feeds with authentication and feed management capabilities.

## Table of Contents
- [Project Overview](#project-overview)
- [Architecture](#architecture)
- [Technologies Used](#technologies-used)
- [Setup Instructions](#setup-instructions)
- [Services Overview](#services-overview)
  - [Auth Service](#auth-service)
  - [Feed Service](#feed-service)
  - [API Gateway](#api-gateway)
- [API Documentation](#api-documentation)
- [Running Unit Tests](#running-unit-tests)

## Project Overview

This microservices application is responsible for:
- Authenticating users.
- Fetching and updating RSS feeds.
- Exposing endpoints for interacting with the feeds and managing user authentication.

## Architecture

The project uses the following services:
- **Auth Service**: Manages user registration and authentication.
- **Feed Service**: Handles RSS feed scraping and parsing.
- **API Gateway**: Exposes endpoints for the client to interact with both the Auth and Feed services.

All services communicate using RabbitMQ as the message broker.

## Technologies Used

- **Programming Language**: Python
- **Microservices Framework**: Nameko
- **Database**: MySQL
- **Message Broker**: RabbitMQ
- **Unit Testing**: pytest
- **Containerization**: Docker
- **HTTP Client**: aiohttp

## Setup Instructions

### Prerequisites
- Docker
- Docker Compose

### Steps to Run the Project

1. **Clone the Repository**
   ```bash
   git clone https://github.com/mhmmdamiwn/digicloud-task1.git
   cd digicloud-task1 

2. **Build and Start Docker Containers**
   ```bash
   docker-compose up --build

3. **Check the Logs Make sure all services are running properly**
   ```bash
   docker-compose logs -f


## Services Overview

### Auth Service
- **Purpose**: Manages user registration and authentication.
- **Endpoints**:
  - **POST /register**: Register a new user.
  - **POST /login**: Login a user and return a JWT token.

### Feed Service
- **Purpose**: Handles RSS feed scraping and parsing, as well as feed management.
- **Endpoints**:
  - **GET /feeds**: List all feeds for a logged-in user.
  - **POST /feeds**: Allow a user to follow a new feed.
  - **POST /feeds/update**: Trigger feed updates (asynchronously or synchronously).

### Bookmark Service
- **Purpose**: Manages bookmarks for feed items.
- **Endpoints**:
  - **POST /bookmarks**: Add a bookmark for a feed item.
  - **GET /bookmarks**: List all bookmarks for a user.

### API Gateway
- **Purpose**: Exposes endpoints for the client to interact with both the Auth and Feed services, acting as a centralized interface.
- **Endpoints**: All endpoints listed above are routed through the API Gateway.

## API Documentation

### Auth Service Endpoints

- **POST /register**
  - **Description**: Register a new user.
  - **Request Body**: 
    ```json
    {
      "username": "your_username",
      "password": "your_password"
    }
    ```
  - **Response**:
    - **200 OK**: 
      ```json
      {
        "message": "User registered successfully."
      }
      ```
    - **400 Bad Request**: 
      ```json
      {
        "message": "Error message."
      }
      ```

- **POST /login**
  - **Description**: Login a user and return a JWT token.
  - **Request Body**: 
    ```json
    {
      "username": "your_username",
      "password": "your_password"
    }
    ```
  - **Response**:
    - **200 OK**: 
      ```json
      {
        "token": "your_jwt_token"
      }
      ```
    - **401 Unauthorized**: 
      ```json
      {
        "message": "Invalid credentials."
      }
      ```

### Feed Service Endpoints

- **GET /feeds**
  - **Description**: List all feeds for a logged-in user.
  - **Headers**: `Authorization: Bearer your_jwt_token`
  - **Response**:
    - **200 OK**: 
      ```json
      [
        {
          "id": 1,
          "url": "http://example.com/feed",
          "title": "Feed Title",
          "last_updated": "2023-10-01T12:00:00Z"
        },
        ...
      ]
      ```
    - **401 Unauthorized**: 
      ```json
      {
        "message": "Unauthorized"
      }
      ```

- **POST /feeds**
  - **Description**: Allow a user to follow a new feed.
  - **Headers**: `Authorization: Bearer your_jwt_token`
  - **Request Body**: 
    ```json
    {
      "feed_url": "http://example.com/feed"
    }
    ```
  - **Response**:
    - **200 OK**: 
      ```json
      {
        "message": "Feed followed successfully."
      }
      ```
    - **400 Bad Request**: 
      ```json
      {
        "message": "Error message."
      }
      ```

- **POST /feeds/update**
  - **Description**: Trigger feed update (async or sync based on payload).
  - **Request Body**: 
    ```json
    {
      "asynchronous": true
    }
    ```
  - **Response**:
    - **200 OK**: 
      ```json
      {
        "message": "Feed update triggered."
      }
      ```
    - **400 Bad Request**: 
      ```json
      {
        "message": "Error message."
      }
      ```

### Bookmark Service Endpoints

- **POST /bookmarks**
  - **Description**: Add a bookmark for a feed item.
  - **Headers**: `Authorization: Bearer your_jwt_token`
  - **Request Body**: 
    ```json
    {
      "feed_item_id": "unique_feed_item_id"
    }
    ```
  - **Response**:
    - **200 OK**: 
      ```json
      {
        "message": "Bookmark added successfully."
      }
      ```
    - **401 Unauthorized**: 
      ```json
      {
        "message": "Unauthorized"
      }
      ```

- **GET /bookmarks**
  - **Description**: List all bookmarks for a user.
  - **Headers**: `Authorization: Bearer your_jwt_token`
  - **Response**:
    - **200 OK**: 
      ```json
      [
        {
          "id": 1,
          "feed_item_id": "unique_feed_item_id",
          "created_at": "2023-10-01T12:00:00Z"
        },
        ...
      ]
      ```
    - **401 Unauthorized**: 
      ```json
      {
        "message": "Unauthorized"
      }
      ```


## Running Unit Tests

### Prerequisites
Ensure you have `pytest` installed. If not, you can add it to your `requirements.txt`:

### Steps to Run Tests

1. **Navigate to Each Service Directory**
   ```bash
   cd auth_service
   pytest tests/

   cd ../feed_service
   pytest tests/

   cd ../api_gateway
   pytest tests/

2. **Running All Tests in One Command**
   ```bash
   pytest
