# Fruit Store Website - Backend

## _The Server-Side Solution for Fresh Produce_

![Home page](src/static/assets/home_page.png)

The backend for the Fruit Store website is designed to manage server-side operations for a seamless online shopping experience for fresh fruits and vegetables. Built with Django, it handles user authentication, product management, and more, making the application a fullstack solution.

- **Develop the backend to manage product listings**
- **Secure user authentication and registration**
- **API endpoints for frontend integration**
- ✨ **Robust & Scalable** ✨

## Table of Contents
- [Features](#features)
- [Tech](#tech)
- [Current Status](#current-status)
- [Secret Key Setup](#secret-key-setup)
- [Email setup](#email-setup)
- [Django Application Setup with PostgreSQL](#django-application-setup-with-postgresql)
- [Django-HTML Syntax Highlighting in VS Code](#Django-HTML-Syntax-Highlighting-in-VS-Code)
- [Create a superuser](#Creating-a-Superuser)
- [Overview](#overview)


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

## Current Status (In progress)

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
- Add responsiveness to the site so that it can handle all screen sizes as not all elements respond to different windows sizes e.g small, etc

## Email setup 

To send emails using Django, you'll need to configure its email backend. There are various email service providers, such as Mailgun and SendGrid which offer solutions for sending emails. However, on free plans, these services often place you in a sandbox environment with restrictions, such as limited sending capabilities or the need to verify recipient addresses.

A popular alternative is to use Gmail, which is free and allows you to send emails without these sandbox limitations. However, Gmail does have sending limits—typically 500 emails per day for regular accounts and 2,000 emails per day for Google Workspace accounts. To use Gmail with Django we first need to adjust our Gmail account settings to allow Django to send emails on its behalf. This includes enabling access for an `App Password` if you have two-factor authentication enabled.

### How to Generate an App Password in Gmail

To begin you need to generate an app password for Gmail, this is necessary when setting up your Google account on a device or in an application that doesn't support two-step verification. Without enabling 2-factor authentication `App passwords` will not be available.

### Step 1: Enable Two-Step Verification

1. Go to your [Google Account](https://myaccount.google.com/).
2. Navigate to the **Security** tab.
3. Under **Signing in to Google**, click on **2-Step Verification**.
4. Follow the instructions to enable Two-Step Verification.

### Step 2: Generate an App Password

1. After enabling Two-Step Verification, return to the **Security** tab in your Google Account.
2. In the search bar type in **App passwords** option and click on it when you see. If prompted, sign in again.
3. Now type in the name of the app you want to create the `authentication code` for and hit `create`
4. A popup will appear with a generate code e.g `yele liof uwkg qdvc`
5. A 16-character password will be generated. Copy this password.

### Important Notes

- **One-time Use:** The app password is a one-time code, and so you don't need to remember it, and if you ever lose it, you can generate a new one.
- **Security:** If you suspect that your account has been compromised, you can revoke the `app password` and any apps using it will have its access revoked. You can do this at any time in your Google Account under **App passwords**.

## How to use the App password to send emails

Open up the `.env.example` and copy the following block into the `.env` file

```
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'your-email@gmail.com'   # your gmail account
EMAIL_HOST_PASSWORD = 'your-app-password'  # Use the generated App Password here
```
Replace the `EMAIL_HOST_USER` and `EMAIL_HOST_PASSWORD` with your email and 16 digit app. Note, you only need to change
the last two if you are using gmail, however if you are using a different email provider you need to the entire block with their email services providers


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


SECRET_KEY='your_generated_secret_key_here'


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
4. **Run python manage.py migrate:**
   - Run the migrate command above to migrate the changes

Your application should now be set up with PostgreSQL.



### Django-HTML Syntax Highlighting in VS Code


Enhance your Django development experience by enabling **Django-HTML** syntax highlighting in Visual Studio Code (VS Code). This guide will walk you through the installation process to get the best out of your Django templates with proper syntax highlighting, auto-completion, and error checking.

## 🎯 Why Use Django-HTML Syntax Highlighting?

When working on Django projects, your HTML templates often contain Django-specific syntax, such as `{% %}` for template tags and `{{ }}` for expressions. By enabling Django-HTML syntax highlighting in VS Code, you get:

- **Improved Readability**: Clearly distinguish between HTML and Django template syntax.
- **Enhanced Development Experience**: Enjoy features like auto-completion, code snippets, and error checking tailored for Django.
- **Increased Productivity**: Quickly identify syntax errors and improve coding efficiency.

## 🚀 Getting Started

Follow these steps to set up Django-HTML syntax highlighting in VS Code:

### Step 1: Install Visual Studio Code

If you haven't already installed VS Code, download it from the [official website](https://code.visualstudio.com/) and follow the installation instructions for your operating system.

### Step 2: Install the Django Template Extension

To enable Django-HTML syntax highlighting, you'll need to install a VS Code extension. Here's how:

1. Open **Visual Studio Code**.
2. Go to the **Extensions** view by clicking on the **Extensions icon** in the sidebar or pressing `Ctrl+Shift+X` (Windows/Linux) or `Cmd+Shift+X` (Mac).
3. In the **Search bar**, type **Django**.
4. Find the extension named **"Django"** by **Baptiste Darthenay** and click **Install**.


### Step 3: Configure Syntax Highlighting

1. After installing the extension, open any `.html` file in your Django project.
2. VS Code should automatically detect the Django template syntax and apply the Django-HTML highlighting.
3. If not, manually change the language mode:
   - Click on the language mode indicator in the bottom right corner of the status bar (usually says `HTML`).
   - Select **"Django HTML"** from the dropdown list.

### Step 4: Optional - Install Additional Extensions

To further enhance your Django development experience, consider installing these additional extensions:

- **Django** by **Baptiste Darthenay** - Provides Django snippets and additional functionalities.
- **Python** by **Microsoft** - Essential for Python development, with features like IntelliSense, linting, and debugging.

## ⚙️ Troubleshooting

If you face any issues with syntax highlighting:

- Ensure that the **Django** extension is installed and enabled.
- Restart VS Code after installation.
- Verify that your template files have the correct `.html` extension.
- In VS code you can switch between templates using the bottom right corner. If you are using html VScode should
automatically detect that the templates is HTML and vice-versa with with Django-html. However, if that is not the case click on `HTML` a dropdown will now appear with `auto-detect` on top, now in the search bar enter `Django-HTML` and hit
`Enter` now any Django snippets will be highlighted with the proper colour and syntax


## 📚 Additional Resources

- [Django Documentation](https://docs.djangoproject.com/en/stable/): Official Django documentation for templates and more.
- [VS Code Django Extension Guide](https://marketplace.visualstudio.com/items?itemName=batisteo.vscode-django): Detailed guide and documentation for the Django extension.

## 🎉 Congratulations!

You now have Django-HTML syntax highlighting enabled in VS Code! 
---


## Creating a Superuser

To manage your Django application through the admin interface, you need to create a superuser. Follow these steps:

### Step 1: Create a Superuser

1. **Activate your virtual environment** (if not already activated):
   - For Unix or macOS:
     ```bash
     source venv/bin/activate
     ```
   - For Windows:
     ```bash
     venv\Scripts\activate
     ```

2. **Navigate to your project directory** (where `manage.py` is located):
   ```bash
   cd src
   ```

3. **Run the `createsuperuser` command**:
   ```bash
   python manage.py createsuperuser
   ```

4. **Enter the required details**:
   - **Username**: Choose a username for your superuser.
   - **Email address**: Provide an email address.
   - **Password**: Set a strong password and confirm it.

   After completing these prompts, Django will create your superuser account.

### Step 2: Access the Django Admin Interface

1. **Run the development server** (if it's not already running):
   ```bash
   python manage.py runserver
   ```

2. **Open the Django admin interface** in your web browser:
   ```plaintext
   http://127.0.0.1:8000/admin/
   ```

3. **Log in** with the superuser credentials you created.

Once logged in, you'll have full access to manage your Django project's data and settings through the admin interface.



## Quick Overview

```

## Overview

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


