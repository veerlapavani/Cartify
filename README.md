Cartify – E-Commerce Web Application

Cartify is a Django-based e-commerce web application that allows users to browse products, add items to a shopping cart, place orders, and manage their purchases.

Features
User registration and login
Product catalog with categories and brands
Product search and product details
Shopping cart and quantity updates
Checkout and order placement
Order history and order details
Admin dashboard and order management
REST API for products and orders
MySQL database integration
Technologies Used
Backend: Python, Django
API: Django REST Framework
Frontend: HTML, CSS, JavaScript, Bootstrap
Database: MySQL
Tools: PyCharm, Git, GitHub
Installation and Setup

Clone the repository:

git clone https://github.com/veerlapavani/Cartify.git
cd Cartify

Create and activate a virtual environment:

python -m venv venv

Windows PowerShell:

.\venv\Scripts\Activate.ps1

Install dependencies:

pip install django djangorestframework mysqlclient Pillow python-dotenv
Configure your .env file with your Django secret key and local MySQL database credentials. Do not commit this file to GitHub.

Create the database in MySQL and apply migrations:

python manage.py migrate

Start the development server:

python manage.py runserver
Open http://127.0.0.1:8000/ in your browser.
API Endpoints
Method	Endpoint	Purpose
GET	/api/products/	List products
GET	/api/products/1/	View product details
POST	/api/products/create/	Create a product (admin)
PUT/PATCH	/api/products/1/update/	Update a product (admin)
DELETE	/api/products/1/delete/	Delete a product (admin)
GET	/api/my-orders/	View your orders
GET	/api/orders/1/	View an order
GET	/api/admin/orders/	Admin order list

Note: Replace 1 with the relevant product or order ID. Some endpoints require authentication or administrator permissions.

Project Purpose

This project was developed to practice full-stack web development, database integration, authentication, e-commerce workflows, and REST API development.
