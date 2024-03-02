# Thesis Project: Design and Implementation of a RESTful API for Attendance Verification

## Introduction

This thesis introduces an attendance verification system designed within the REST (Representational State Transfer) architectural paradigm, an abstract model crucial for the design of distributed information systems established in the early 21st century. Focused on the creation of a REST-compliant application programming interface (API), this work aims to serve as an educational example, illustrating the principles of REST API design and its application in modern microservices-based information systems. Such systems are notably used in cutting-edge technologies, including 5G networks.

## Objectives

The goal is to provide an exhaustive exploration and practical example of the design and implementation process of a modern REST API, in line with contemporary standards and best practices. The system developed for this thesis could be instrumental in teaching both students and IT professionals about advanced programming techniques related to REST API creation, offering value in both academic research and practical applications.

## Theoretical Background and Design Principles

### Microservices and Their Design

The thesis elaborates on the general principles behind the creation and design of microservices, providing the necessary foundation to understand their architectural and operational advantages.

### REST API Interfaces

It delves into the specifics of REST API interfaces, discussing their objectives, benefits, and design best practices. Core concepts such as URI identifiers, CRUD operations, and the significance of HTTP response codes are thoroughly examined.

## System Design and Implementation

This section introduces the attendance verification system's architecture, detailing the selected technologies, implementation choices, and the functionalities of its constituent microservices and APIs. The system illustrates the application of REST principles in a practical setting, emphasizing microservices architecture for efficient, scalable solutions.

### Key Features

- **Token Generation and Management**: Facilitates the creation and verification of unique tokens for meeting authentication.
- **Participant Registration**: Enables participants to register for meetings using personal information along with a token for verification.

### Tools and Techniques

- **Flask**: A lightweight framework chosen for its simplicity and flexibility in building web applications in Python.
- **MySQL and XAMPP**: For efficient data storage and management within a microservices architecture.
- **Postman**: Utilized for testing the functionality and integration of RESTful APIs.
- **Development Environments**: The project leverages IntelliJ IDEA and Visual Studio Code, supporting robust development features and ease of use.

## Detailed Endpoint Descriptions

The system comprises two microservices, each offering a suite of endpoints to support its operations:

### Microservice 1: Token Generation and Management

- **`GET /generate-token`**: Generates and returns a random token, optionally with a password.
- **`POST /generate-token`**: Stores the generated token and password in the database.
- **`GET /tokens`**, **`GET /token/<int:id>`**: Facilitates token retrieval and management operations.

### Microservice 2: Participant Registration

- **`GET, POST /register-to-room`**: Handles the registration process, allowing for both the fetching of the registration form (`GET`) and the submission of registration data (`POST`).
- **`GET /students`**: Retrieves information on all registered participants, with filtering and sorting capabilities.
- **`GET, DELETE /student/<int:id>`**, **`POST /student/<int:id>`**: Supports operations on individual participant records.

## Practical Applications and Conclusion

The thesis underscores the importance of RESTful APIs in the development of scalable, efficient, and modern software systems. By providing a detailed account of both the theoretical underpinnings and practical implementation of a RESTful service, this work aims to bridge the gap between academic knowledge and real-world application, offering valuable insights for both educational and professional development in the field of software engineering.


