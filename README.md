# Vendor Management API

This is a Django-based RESTful API for managing vendors and purchase orders.

## Setup Instructions

1. **Clone the Repository:**
git clone https://github.com/Anirudh5d/Vendor-management.git

2. **Install Dependencies:**
pip install -r requirements.txt

3. **Run Migrations:**
python manage.py migrate

4. **Start the Development Server:**
python manage.py runserver


## API Endpoints

### Vendor Management

- **List/Create Vendors:** `GET /api/vendors/` (List all vendors) | `POST /api/vendors/` (Create a new vendor)
- **Retrieve/Update/Delete Vendor:** `GET /api/vendors/<vendor_id>/` | `PUT /api/vendors/<vendor_id>/` | `DELETE /api/vendors/<vendor_id>/`

### Purchase Order Management

- **List/Create Purchase Orders:** `GET /api/purchase_orders/` (List all purchase orders) | `POST /api/purchase_orders/` (Create a new purchase order)
- **Retrieve/Update/Delete Purchase Order:** `GET /api/purchase_orders/<po_id>/` | `PUT /api/purchase_orders/<po_id>/` | `DELETE /api/purchase_orders/<po_id>/`

### Vendor Performance Evaluation

- **Retrieve Vendor Performance Metrics:** `GET /api/vendors/<vendor_id>/performance/`

## Authentication

- **Authentication Type:** Token-based authentication
- **Obtaining Authentication Token:** Use the provided username and password to obtain an authentication token. Send a POST request to `/api-token-auth/` with the username and password in the request body to obtain the token.

## Testing

- Use tools like Postman or Django's testing framework to test the API endpoints.
- Write test cases to cover various scenarios, including valid requests, invalid requests, and edge cases.
- Run the test suite regularly to ensure the functionality and reliability of the endpoints.
