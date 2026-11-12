from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import HTTPBearer
import logging
from datetime import datetime, timezone

logging.basicConfig(
    filename="audit.log",
    level=logging.INFO,
    format="%(message)s"
)

def log_access_attempt(username, requested_department, result):
    timestamp = datetime.now(timezone.utc).isoformat()

    logging.info(
        "Timestamp=%s | User=%s | Department=%s | Result=%s",
        timestamp,
        username,
        requested_department,
        result
    )

app = FastAPI(title="Kani's Insurance Company API")

oauth2_scheme = HTTPBearer()

USERS = {
    "john_token": {
        "username": "john",
        "department": "IT"
    },
    "sarah_token": {
        "username": "sarah",
        "department": "HR"
    },
    "michelle_token": {
        "username": "michelle",
        "department": "Security"
    }
}


def get_current_user(credentials = Depends(oauth2_scheme)):
    token = credentials.credentials

    user = USERS.get(token)
    if user is None:
        raise HTTPException(
            status_code=401,
            detail="Invalid authentication token"
        )
    return user


@app.get("/me")
def read_current_user(current_user: dict = Depends(get_current_user)):
    return current_user

@app.get("/")
def home():
    return {"message": "Insurance Company API is running"}

@app.get(
    "/department/{department_name}",
    responses={403: {"description": "Forbidden"}}
)
def access_department(
    department_name: str,
    current_user: dict = Depends(get_current_user)
):

    if current_user["department"] != department_name:

        log_access_attempt(
            current_user["username"],
            department_name,
            "DENIED"
        )

        raise HTTPException(
            status_code=403,
            detail="Access denied: You are not authorized for this department"
        )

    log_access_attempt(
        current_user["username"],
        department_name,
        "GRANTED"
    )

    return {
        "message": "Access granted",
        "username": current_user["username"],
        "department": department_name
    }
