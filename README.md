# COSC_310
Backend API for COSC_310
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

## Notes
The database.py functions are unimplemented

