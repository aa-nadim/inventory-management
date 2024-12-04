# inventory-management

A Django-based application for managing and storing property information using Django admin. This project allows for efficient handling of property details, including images, locations, policies and amenities 

## Table of Contents

1. [Project Overview](#project-overview)
2. [Features](#features)
3. [Technologies Used](#technologies-used)
4. [Prerequisites](#prerequisites)
5. [Project Structure](#project-structure)
6. [Getting Started](#getting-started)
   - [Installation](#installation)
   - [Database Configuration](#database-configuration)
   - [Running the Application](#running-the-application)
7. [Usage](#usage)
8. [Database Schema](#database-schema)


## Project Overview

This Django application is designed to store and manage property information efficiently. It utilizes Django's powerful admin interface for CRUD operations and includes custom models to handle various aspects of property data, such as images, locations, and amenities.

## Features

- **Property Management**: Store and manage detailed property information.
- **Image Handling**: 
- **Location Management**: 
- **Amenity Tracking**: 
- **Django Admin Interface**: 

## Technologies Used

- Backend: Python, Django
- Database: PostgreSQL
- ORM: Django ORM

## Prerequisites

Ensure you have the following installed:
- Python 3.x
- PostgreSQL
- Docker
- Git

## Getting Started

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/aa-nadim/inventory-management.git
   cd inventory-management
   ```

2. Set up a virtual environment:
   ```bash
   python3 -m venv .venv 
   source .venv/bin/activate   # On Windows use `source .venv/bin/activate`
   ```

3. Install the dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### Database Configuration

1. Create a `config.py` file in the DjangoAssignment root directory and add your PostgreSQL credentials:

   ```python
   # config.py
   DB_USERNAME = 'your_username'
   DB_PASSWORD = 'your_password'
   DB_HOST = 'localhost'
   DB_PORT = 'port'
   DJANGO_DBNAME = 'django_project_database_name'
   SECRET_KEY = 'your SECRET_KEY'
   ```

2. Create a `.env` file in the DjangoAssignment root directory and add your PostgreSQL credentials:

   ```
      DB_USERNAME=your_username
      DB_PASSWORD=your_password
      DB_HOST=localhost
      DB_PORT=port
      DJANGO_DBNAME=django_project_database_name
      SECRET_KEY=your_SECRET_KEY
   ```

3. Ensure PostgreSQL is running and create the necessary databases:

   ```bash
   psql -U your_username
   CREATE DATABASE django_project_database_name;
   ```

### Running the Application

   ```bash
   docker-compose up --build -d
   ```
1. Apply migrations:
   ```bash
   docker exec -it inventoryManagement python manage.py makemigrations
   docker exec -it inventoryManagement python manage.py migrate
   ```

2. Create a superuser:
   ```bash
   docker exec -it inventoryManagement python manage.py createsuperuser
   ```

3. Start the development server:
   ```bash
   docker exec -it inventoryManagement python manage.py runserver 0.0.0.0:8000
   ```


## Usage

1. `http://localhost:8000`

2. `http://localhost:8000/signup/`

3. Access the admin panel at `http://localhost:8000/admin/` and log in with your superuser credentials.


### Database Schema

The project includes the following models:

### Command-Line Utility for Sitemap Generation

To generate a sitemap.json file for all country locations.
   ```bash
   docker exec -it inventoryManagement python manage.py generate_sitemap
   ```

#### amenities field 
   ```
   [
      "Free Wi-Fi",
      "Air Conditioning",
      "Swimming Pool",
      "Pet-Friendly",
      "Room Service",
      "Gym Access"
   ]
   ```
#### policy field
   ```
   {
      "pet_policy": {
         "en": "Pets are not allowed.",
         "ar": "لا يُسمح بالحيوانات الأليفة."
      },
      "smoking_policy": {
         "en": "Smoking is prohibited indoors.",
         "ar": "التدخين ممنوع داخل المبنى."
      }
   }
   ```


## Testing Instructions

   ```bash
   docker exec -it inventoryManagement pytest --cov=properties --cov-report=term-missing
   docker exec -it inventoryManagement pytest --cov=properties --cov-report=html:coverage_report
   ```

   Open the `coverage_report/index.html` file in a web browser to view the detailed coverage report.


## Contributing

Fork the project
   Create your feature branch (git checkout -b feature/NewFeature)
   Commit your changes (git commit -m 'Add some NewFeature')
   Push to the branch (git push origin feature/NewFeature)
   Open a Pull Request

## License
