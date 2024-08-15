# Fruit Store Website - Backend

## _The Server-Side Solution for Fresh Produce_

[![Django](https://www.djangoproject.com/m/img/logos/django-logo-negative.png)](https://www.djangoproject.com/)

[![Build Status](https://travis-ci.org/yourusername/fruit-store-backend.svg?branch=main)](https://travis-ci.org/yourusername/fruit-store-backend)

The backend for the Fruit Store website is designed to manage server-side operations for a seamless online shopping experience for fresh fruits and vegetables. Built with Django, it handles user authentication, product management, and more.

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
## Branching and Repository Structure

- The **backend** branch is maintained separately from the frontend branch and will not be merged into the main branch.
- Once the backend development is complete, it will be deployed to a distinct repository, while the frontend (developed with HTML, CSS, and JavaScript) will also be hosted in a separate repository.
- The original frontend repository will concentrate solely on frontend features and will remain separate from the backend integration.



## Branching and Repository Structure

- The **backend** branch is maintained separately from the frontend branch and won't be integrated in the main brach.
- Upon completion the frontend, developed using HTML, CSS, and JavaScript, will integrate with the backend services and hosted on another repository.
- The frontend where this branch is original from will be kept at is and the rest of the features built but only for the front

## Installation

To set up the backend environment, follow these instructions:

```bash
# Clone the repository
git clone https://github.com/EgbieAndersonUku1/fruit-and-veg-store.git 

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


