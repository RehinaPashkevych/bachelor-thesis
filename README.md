# Thesis Project: A REST-compilant Application Programming Interface (RESTfull API): An Educational Example

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


## Repository Contents

This repository contains all the materials and codebase for the thesis project on the design and implementation of a RESTful API for attendance verification within a microservices architecture. Below is a detailed overview of the repository's structure and the purpose of each item:

### `material-dydaktyczny/`

- Contains educational material and interactive examples demonstrating the principles of REST API, microservices design, and implementation strategies used in the project. These notebooks serve as a practical guide for understanding and applying the concepts discussed in the thesis.  The materials are written in Polish.

### `room/`

- This directory houses the code for the Room microservice, responsible for generating and managing tokens and passwords used for meeting authentication. It includes all the necessary Flask routes, models, and utilities to support its operations.

### `student/`

-  Contains the implementation of the Student microservice, which facilitates participant registration for meetings using personal information along with a generated token for verification. This microservice also handles the validation of tokens and passwords in coordination with the Room microservice.

### `Praca_dyplomowa-pdf.pdf`

-  The complete text of the thesis in PDF format, providing a comprehensive account of the project's motivation, theoretical background, objectives, system design, implementation details, and the practical applications of the developed RESTful API. The thesis are written in Polish.


### `diploma-score-exam-gpa.pdf`

-  The scan from my diploma supplements shows my GPA (4,07), the grade of the diploma thesis (5) and the grade for diploma examination (4,63).





