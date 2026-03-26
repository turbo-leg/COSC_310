# COSC_310 Project 

#Overview
This project currently contains the backend system for a food delivery app. The app has 8 core functionalities:
- User Authentication
- Menu Management
- Search Functionality
- Order Management
- Delivery System
- Order Tracking
- Payment Processing
- Notifications


# Setup
Clone the repo
Run `docker-compose up --build -d`
The API will be available at `http://localhost:8000`
`http://localhost:8000/docs` is much easier to use Tobi highly recommends it

## API Endpoints
GET /users - Get all users
GET /users/{user_id} - Get a specific user
POST /users - Create a new user
DELETE /users/{user_id} - Delete a user

## Database
CSV file

## Reminders
I added a comment at the top of every file to explain what it does. Read it and let me know if you have any questions

## Testing
Testing is completed through `pytest `
The CI pipeline uses both `pylint` and  `pytest`

## Notes
Testing reports/evidence are found in `/testing-documents`
Scrum documents are found in `/scrum-documents`

