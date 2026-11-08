from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer

app = FastAPI(title="Insurance Company API")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

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


def get_current_user(token: str = Depends(oauth2_scheme)):
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

@app.get("/department/{department_name}")
def access_department(
    department_name: str,
    current_user: dict = Depends(get_current_user)
):
    if current_user["department"] != department_name:
        raise HTTPException(
            status_code=403,
            detail="Access denied: You are not authorized for this department"
        )

    return {
        "message": "Access granted",
        "username": current_user["username"],
        "department": department_name
    }
