# Fruit Store Website - Backend

## _The Server-Side Solution for Fresh Produce_

[![Django](https://www.djangoproject.com/m/img/logos/django-logo-negative.png)](https://www.djangoproject.com/)

[![Build Status](https://travis-ci.org/yourusername/fruit-store-backend.svg?branch=main)](https://travis-ci.org/yourusername/fruit-store-backend)

The backend for the Fruit Store website is designed to manage server-side operations for a seamless online shopping experience for fresh fruits and vegetables. Built with Django, it handles user authentication, product management, and more, making the application a fullstack solution.

- **Develop the backend to manage product listings**
- **Secure user authentication and registration**
- **API endpoints for frontend integration**
- ✨ **Robust & Scalable** ✨

## Features

- **User Registration and Login:** Secure user registration, login, and account management.
- **Product Management:** CRUD (Create, Read, Update, Delete) operations for managing fruit and vegetable listings.
- **Shopping Cart:** Comprehensive shopping cart management for adding, updating, and removing items.
- **Order Processing:** Functionality to handle order creation, processing, and tracking.
- **API Endpoints:** RESTful API endpoints for frontend integration and external communication.
- **Product Search and Filters:** Search functionality and filters for users to find products easily.
- **Wishlist:** Option for users to save and manage their favorite products.
- **Review and Ratings:** Feature to allow users to leave reviews and ratings for products.
- **Checkout System:** Secure checkout process including payment integration.

This backend is built with Django to provide a powerful, scalable server-side solution for the Fruit Store. As [Django Documentation](https://www.djangoproject.com/) writes:

> Django is a high-level Python Web framework that encourages rapid development and clean, pragmatic design. It’s designed to help developers take applications from concept to completion as swiftly as possible.

## Tech

The backend uses several technologies and libraries:

- [Django](https://www.djangoproject.com/) - High-level Python Web framework
- [Python](https://www.python.org/) - Programming language for backend development
- [HTML](https://developer.mozilla.org/en-US/docs/Web/HTML) - The skeleton of the website
- [CSS](https://developer.mozilla.org/en-US/docs/Web/CSS) - Styles for the site
- [JavaScript](https://developer.mozilla.org/en-US/docs/Web/JavaScript) - Client-side functionality
- [PostgreSQL/MySQL](https://www.postgresql.org/) - Database for data storage (configure in `settings.py`)

## Current Status

**Features Implemented:**

- **Index Page:** Basic routing and homepage setup.
- **Accounts Page:** User registration and login functionality.
- **Product Management Page:** Initial wiring completed; some product cards still in progress.

**Future Work:**

- **Product Management Integration:** Finalize integration of product management features.
- **Rewiring and Integration:** Complete the rewiring of HTML pages, navigation to use Django templates, and ensure JavaScript functions properly with Django.
- **Shopping Cart Functionality:** Develop and integrate comprehensive shopping cart management.
- **Additional API Endpoints:** Create and implement additional API endpoints as needed.
- **Frontend Integration:** Ensure seamless integration with the frontend.
- **Extensive Development:** Address a range of significant tasks across various components to ensure full functionality and integration, covering all remaining aspects of backend development.

## Secret Key Setup

To ensure the security of your Django project, you must set a `SECRET_KEY` in your environment variables. This key is critical for various cryptographic operations in Django, including session management, password hashing, and more.

### Creating the `.env` File

1. **Create a `.env` File:**
   - Create a `.env` file in the root of your project directory. The `.env` file should reside outside the 'src' directory where `requirements.txt` and `.env.example` are located.
   - Use the `.env.example` file as a guide. Copy its contents into your new `.env` file and replace any placeholder values as needed.

2. **How to Set the Secret Key:**
   - **Option 1: Generate a Secret Key Online:**
     - Use an online generator like [Django Secret Key Generator](https://djecrety.ir/) to generate a secure key.
   - **Option 2: Generate a Secret Key Using the Project's Utility Function:**
     - Use the `generateSessionKey()` function found in the `utils` module of this project to generate a secure key.

### Setting the Secret Key in `.env`

Once you have your secret key, add it to the `.env` file as follows:



# Fruit Store Website - Backend

The backend for the Fruit Store website is designed to manage server-side operations for a seamless online shopping experience for fresh fruits and vegetables. Built with Django, it handles user authentication, product management, and more, making the application a fullstack solution.

- **Develop the backend to manage product listings**
- **Secure user authentication and registration**
- **API endpoints for frontend integration**
- ✨ **Robust & Scalable** ✨

## Features

- **User Registration and Login:** Secure user registration, login, and account management.
- **Product Management:** CRUD (Create, Read, Update, Delete) operations for managing fruit and vegetable listings.
- **Shopping Cart:** Comprehensive shopping cart management for adding, updating, and removing items.
- **Order Processing:** Functionality to handle order creation, processing, and tracking.
- **API Endpoints:** RESTful API endpoints for frontend integration and external communication.
- **Product Search and Filters:** Search functionality and filters for users to find products easily.
- **Wishlist:** Option for users to save and manage their favorite products.
- **Review and Ratings:** Feature to allow users to leave reviews and ratings for products.
- **Checkout System:** Secure checkout process including payment integration.


## Tech

The backend uses several technologies and libraries:

- [Django](https://www.djangoproject.com/) - High-level Python Web framework
- [Python](https://www.python.org/) - Programming language for backend development
- [HTML](https://developer.mozilla.org/en-US/docs/Web/HTML) - The skeleton of the website
- [CSS](https://developer.mozilla.org/en-US/docs/Web/CSS) - Styles for the site
- [JavaScript](https://developer.mozilla.org/en-US/docs/Web/JavaScript) - Client-side functionality
- [PostgreSQL/MySQL](https://www.postgresql.org/) - Database for data storage (configure in `settings.py`)

## Current Status

**Features Implemented:**

- **Index Page:** Basic routing and homepage setup.
- **Accounts Page:** User registration and login functionality.
- **Product Management Page:** Initial wiring completed; some product cards still in progress.

**Future Work:**

- **Product Management Integration:** Finalize integration of product management features.
- **Rewiring and Integration:** Complete the rewiring of HTML pages, navigation to use Django templates, and ensure JavaScript functions properly with Django.
- **Shopping Cart Functionality:** Develop and integrate comprehensive shopping cart management.
- **Additional API Endpoints:** Create and implement additional API endpoints as needed.
- **Frontend Integration:** Ensure seamless integration with the frontend.
- **Extensive Development:** Address a range of significant tasks across various components to ensure full functionality and integration, covering all remaining aspects of backend development.

## Secret Key Setup

To ensure the security of your Django project, you must set a `SECRET_KEY` in your environment variables. This key is critical for various cryptographic operations in Django, including session management, password hashing, and more.

### Creating the `.env` File

1. **Create a `.env` File:**
   - Create a `.env` file in the root of your project directory. The `.env` file should reside outside the 'src' directory where `requirements.txt` and `.env.example` are located.
   - Use the `.env.example` file as a guide. Copy its contents into your new `.env` file and replace any placeholder values as needed.

2. **How to Set the Secret Key:**
   - **Option 1: Generate a Secret Key Online:**
     - Use an online generator like [Django Secret Key Generator](https://djecrety.ir/) to generate a secure key.
   - **Option 2: Generate a Secret Key Using the Project's Utility Function:**
     - Use the `generateSessionKey()` function found in the `utils` module of this project to generate a secure key.

### Setting the Secret Key in `.env`

Once you have your secret key, add it to the `.env` file as follows:

```plaintext
SECRET_KEY='your_generated_secret_key_here'
```

## Django Application Setup with PostgreSQL

### Database Setup with PostgreSQL

1. **Download and Install PostgreSQL:**
   - Visit the [PostgreSQL download page](https://www.postgresql.org/download/) and install PostgreSQL for your operating system.

2. **Create a Database:**
   - After installing PostgreSQL, use a tool like pgAdmin (often included with PostgreSQL) or the `psql` command-line tool to create a new database for your application.

3. **Configure Your Application:**
   - Copy the following `.env.example` file to the `.env` and replace it with your postgresl setup:
    
   - Update the `.env` file with your database configuration:
     ```plaintext
     DB_NAME=your_database_name
     DB_USER=your_database_user
     DB_PASSWORD=your_database_password
     DB_HOST=localhost
     DB_PORT=5432
     ```

Your application should now be set up with PostgreSQL.

## Overview


Overview
To set up the backend environment, follow these instructions:

```bash
# Clone the repository
git clone https://github.com/EgbieAndersonUku1/Fullstack-fruit-and-veg.git .
# The period at the end specifies that the repository should be cloned into the current directory.

# Set up a virtual environment
python3 -m venv venv

# Activate the virtual environment you should see (venv) in front of the path 
# For Unix or MacOS
source venv/bin/activate
# For Windows
venv\Scripts\activate

# Navigate to the src folder (make sure you are in the same directory as requirements.txt)
cd src

# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Run the development server
python manage.py runserver

# Navigate to the application
http://127.0.0.1:8000/
```
