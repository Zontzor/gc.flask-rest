"""
    Author: Alex Kiernan

    Desc: API routes
"""
from app import app


@app.route("/glucose_coach/api/v1.0")
def index():  
    return """
* Denotes authentication required
 
Available API endpoints:

GET /users/{username}                           - List a user *
POST /users                                     - Add a user
PUT /users                                      - Update a users info *
GET /users/usernames/{username}                 - Get a username

GET /users/{username}/bgreadings                - Get a users bg logs *
GET /users/{username}/bgreadings/{bg_id}        - Get a users bg log *
POST /users/{username}/bgreadings               - Add a user bg log *
PUT /users/{username}/bgreadings/{bg_id}        - Alter a users bg log *

GET /users/{username}/insdosages                - Get a users insulin log values *
GET /users/{username}/insdosages/{ins_id}       - Get a users insulin log value *
POST /users/{username}/insdosages               - Add a user insulin log value *
PUT /users/{username}/insdosages/{ins_id}       - Alter a users insulin log value *

GET /users/{username}/exerciselogs              - Get a users exercise logs *
GET /users/{username}/exerciselogs/{elog_id}    - Get a users exercise log *
POST /users/{username}/exerciselogs             - Add a user exercise log *
PUT /users/{username}/exerciselogs/{elog_id}    - Alter a users exercise log *

GET /users/{username}/foodlogs                  - Get a users food logs *
GET /users/{username}/foodlogs/{flog_id}        - Get a users food log *
POST /users/{username}/foodlogs                 - Add a user food log *
PUT /users/{username}/foodlogs/{flog_id}        - Alter a users food log *

GET /sync/{username}                            - Get a users last sync date *
POST /sync/{username}                           - Add a users last sync date *

GET /token                                      - Get a token, requires username and password
""" 