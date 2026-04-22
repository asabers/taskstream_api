TaskStream API
A task management backend built with FastAPI, SQLAlchemy, and SQLite. This repository contains the core logic for user registration and task lifecycle management.

Environment Setup (WSL Native)
For optimal performance, it is recommended to run this project within a native WSL file system.

Project Architecture
The codebase follows a standard Router-Service-Database pattern to maintain a clean separation of concerns.

src/main.py
Docstring:

Handles the FastAPI application initialization, global dependencies, and the transport layer. Defines RESTful endpoints for user registration and task management.

src/services/task_service.py
Docstring:

Encapsulates all business logic and database interactions. This service layer ensures the API remains agnostic of the underlying storage implementation.

Testing
The project uses Pytest for automated quality assurance.



