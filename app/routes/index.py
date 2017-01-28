from app import app

@app.route("/glucose_coach/api/v1.0")
def index():  
    return """
Available API endpoints:

GET /users - List all users
GET /users/<username> - List a user
POST /users - Add a user
PUT /users - Update a users info
DELETE /users/<username> - Delete a user (Not available atm)

GET /users/<username>/bgreadings - Get a users blood glucose results
POST /users/<username>/bgreadings - Add a user blood glucose result
""" 