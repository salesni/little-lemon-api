# Little Lemon DRF API

## Project Description

Little Lemon DRF API is a Django REST framework project for managing orders, menu items, and other related data for a restaurant application.


## Installation Instructions

### Prerequisites

Before you begin, ensure you have the following installed on your machine:

- Python 3.8+
- pip (Python package installer)
- Virtualenv

### Setup Instructions

1. **Clone the Repository**

   Clone the project repository to your local machine using the following command:
    ```bash
   git clone repoURL
   cd api_final_project
   ```

2. **Create a Virtual Environment**
   ```bash
   python -m venv venv
   ```
   - On Windows:
    ```bash
   venv\Scripts\activate
   ```
   - On macOS and Linux:
    ```bash
   source venv/bin/activate
   ```

3. **Install Dependencies**

    Install the project dependencies listed in the requirements.txt file:   
   ```bash
   pip install -r requirements.txt
    ```

4. **Run Migrations**

    Apply the database migrations to set up the database schema:   
   ```bash
   python manage.py migrate
   ```

5. **Create a Superuser**

   Create a superuser account to access the Django admin interface:  
   ```bash
   python manage.py createsuperuser
   ```
6. **Start the Development Server**

   Run the development server to start the application:
   ```bash
   python manage.py runserver
   ```
   The application will be available at http://127.0.0.1:8000/.

# CURRENT USERS
- **Customer:**   customer@example.com  paswd: 12345
- **Delivery Crew:**   delivery_crew@skere.com.com  paswd: 12345
- **Manager:**   superuser@gmail.com  pswd: 12345

# Usage
## API Endpoints
### Menu Items

- GET /api/menu-items/: Retrieve a list of all menu items.
- POST /api/menu-items/: Create a new menu item (Manager only).
- GET /api/menu-items/{id}/: Retrieve details of a specific menu item.
- PUT /api/menu-items/{id}/: Update a specific menu item (Manager only).
- DELETE /api/menu-items/{id}/: Delete a specific menu item (Manager only).

### Cart

- GET /api/cart/: Retrieve the current user's cart items.
- POST /api/cart/: Add an item to the cart.
- DELETE /api/cart/{id}/: Remove an item from the cart.

### Orders

- GET /api/orders/: Retrieve a list of orders (Manager and Delivery Crew can view all, Customers can view their own).
- POST /api/orders/: Create a new order from the current user's cart items.
- GET /api/orders/{id}/: Retrieve details of a specific order.
- PUT /api/orders/{id}/: Update a specific order (Manager can assign delivery crew, Delivery Crew can update status).
- DELETE /api/orders/{id}/: Delete a specific order (Manager only).

## Permissions
### Manager

- Can manage all menu items.
- Can view and delete all orders.
- Can assign delivery crew to orders.

### Customer

- Can view and manage their own cart.
- Can create orders from their cart items.
- Can view their own orders.

### Delivery Crew

- Can view orders assigned to them.
- Can update the status of orders assigned to them.
