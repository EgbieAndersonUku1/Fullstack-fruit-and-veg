# Fruit Store Website - Backend

## _The Server-Side Solution for Fresh Produce_

[![Django](https://www.djangoproject.com/m/img/logos/django-logo-negative.png)](https://www.djangoproject.com/)

[![Build Status](https://travis-ci.org/yourusername/fruit-store-backend.svg?branch=main)](https://travis-ci.org/yourusername/fruit-store-backend)

The backend for the Fruit Store website is designed to manage server-side operations for a seamless online shopping experience for fresh fruits and vegetables. Built with Django, it handles user authentication, product management, and more making the application a fullstack application

- Develop the backend to manage product listings
- Secure user authentication and registration
- API endpoints for frontend integration
- ✨ Robust & Scalable ✨

## Features

- **User Registration and Login:** Secure user registration, login, and account management.
- **Product Management:** CRUD (Create, Read, Update, Delete) operations for managing fruit and vegetable listings.
- **Shopping Cart:** Comprehensive shopping cart management for adding, updating, and removing items.
- **Order Processing:** Functionality to handle order creation, processing, and tracking.
- **API Endpoints:** RESTful API endpoints for frontend integration and external communication.
- **Product Search and Filters:** Search functionality and filters for users to find products easily.
- **Wishlist:** Option for users to save and manage their favourite products.
- **Review and Ratings:** Feature to allow users to leave reviews and ratings for products.
- **Checkout System:** Secure checkout process including payment integration.


This backend is built with Django to provide a powerful, scalable server-side solution for the Fruit Store. As [Django Documentation] writes:

> Django is a high-level Python Web framework that encourages rapid development and clean, pragmatic design. It’s designed to help developers take applications from concept to completion as swiftly as possible.



## Tech

The backend uses several technologies and libraries some have be used some have not:

- [Django] - High-level Python Web framework
- [Python] - Programming language for backend development
- [HTML] - The Skeleton of the website
- [CSS] - Beautify the site
- [JS] - Functionality
- [PostgreSQL/MySQL] - Database for data storage (configure in `settings.py`)

## Current Status

**Features Implemented:**

- **Index Page:** Basic routing and homepage setup.
- **Accounts Page:** User registration and login functionality.
- **Product Management Page:** Initial wiring completed; some product cards still in progress.

**Future Work:**

- **Product Management Integration:** Finalise integration of product management features.
- **Rewiring and Integration:** Complete the rewiring of HTML pages, navs to use Django templates and ensure JavaScript functions properly with Django.
- **Shopping Cart Functionality:** Develop and integrate comprehensive shopping cart management.
- **Additional API Endpoints:** Create and implement additional API endpoints as needed.
- **Frontend Integration:** Ensure seamless integration with the frontend.
- **Extensive Development:** Address a range of significant tasks across various components to ensure full functionality and integration, covering all remaining aspects of the backend development.
- 



### Secret Key Setup

To ensure the security of your Django project, you must set a `SECRET_KEY` in your environment variables. This key is critical for various cryptographic operations in Django, including session management, password hashing, and more.

#### Creating the `.env` File1.**Create a `.env` File:**   - Start by creating a `.env` file in the root of your project directory. The .env file
    must reside outside the 'src' directory where the `requirements.html' and `.env.example` live

   - You can use the `.env.example` file as a guide. Simply copy its contents into your new `.env` file and replace any placeholder values as needed.

2.**How to Set the Secret Key:**   - You have two options to generate the `SECRET_KEY`:

   -**Option 1: Generate a Secret Key Online:**     - You can use an online generator like [Django Secret Key Generator](https://djecrety.ir/) to generate a secure key.

   -**Option 2: Generate a Secret Key Using the Project's Utility Function:**     - Use the `generateSessionKey()` function found in the `utils` module of this project to generate a secure key.

#### Setting the Secret Key in `.env`:

Once you have your secret key, add it to the `.env` file as follows:

```bash
# Option 1: Generate Secret Key Online and add it to the .env file
# Go to https://djecrety.ir/ and generate a key, then replace 'your_generated_secret_key_here' below

SECRET_KEY='your_generated_secret_key_here'

# Option 2: Generate Secret Key using the project's utility function
# This command will generate the SECRET_KEY, which you can then copy and paste into the .env file


## Installation

To set up the backend environment, follow these instructions:

```bash
# Clone the repository
git https://github.com/EgbieAndersonUku1/Fullstack-fruit-and-veg.git . 

# Set up a virtual environment
python3 -m venv venv

# Activate the virtual environment
# For Unix or MacOS
source venv/bin/activate
# For Windows
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt


# Apply migrations
cd into the "src" folder
python manage.py migrate


# Run the development server
python manage.py runserver

# Navigation to 
http://127.0.0.1:8000/
```


