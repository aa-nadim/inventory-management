# inventory-management

A Django-based application for managing and storing property information using Django admin. This project allows for efficient handling of property details, including images, locations, policies and amenities 

## Features

- **Property Management**: Store and manage detailed property information.
- **Django Admin Interface**: Customized admin panel for easy CRUD operations.

## Technologies Used

- Backend: Python, Django
- Database: PostgreSQL
- ORM: Django ORM
- Containerization: Docker
- Web-Based Database Management: pgAdmin

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

3. Ensure PostgreSQL is running 

### Running the Application

1. start docker
   ```bash        
   docker-compose up --build -d
   ```
2. Apply migrations:
   ```bash
   docker exec -it inventoryManagement python manage.py makemigrations
   docker exec -it inventoryManagement python manage.py migrate
   ```

3. Create a superuser:
   ```bash
   docker exec -it inventoryManagement python manage.py createsuperuser
   ```

## Usage

1. `http://localhost:8000`

2. `http://localhost:8000/signup/`  -- successful signup --> `http://localhost:8000/signup/success/`

3. Access the admin panel at `http://localhost:8000/admin/` and log in with your superuser credentials.

4. To see database in pgadmin goto `http://localhost:5050` and use `your_username`=`admin@admin.com` and `your_password`=`admin123` to login. Then connect to `localhost:5432` with `your_db_username` and `your_db_password` where `host`=`postgres_db`.


## Documentation

### Command-Line Utility for Sitemap Generation

To generate a `sitemap.json` file for all country locations.
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

