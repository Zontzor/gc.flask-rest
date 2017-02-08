from app import app

@app.route("/glucose_coach/api/v1.0")
def index():  
    return """
* Denotes authentication required
 
Available API endpoints:

GET /users/<username> - List a user *
POST /users - Add a user
PUT /users - Update a users info *
GET /users/usernames/<username> - Get a username

GET /users/<username>/bgreadings - Get a users blood glucose results *
POST /users/<username>/bgreadings - Add a user blood glucose result *
PUT /users/<username>/bgreadings/<bg_id> - Alter a users bg reading *

GET /users/<username>/insdosages - Get a users insulin dosage values *
POST /users/<username>/insdosages - Add a user insulin dosage value *
PUT /users/<username>/insdosages/<ins_id> - Alter a users insulin dosage value *
""" 