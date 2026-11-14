
import json
from pathlib import Path

# Locate and load the OpenAPI specification
spec_path = Path("openapi.json")

with spec_path.open("r", encoding="utf-8") as file:
    api_spec = json.load(file)  # Convert JSON into a Python dictionary

print(api_spec["info"])  # Display API name, version, and description

# Extract all API endpoints
paths = api_spec["paths"]

# Loop through endpoints and display their HTTP methods
for endpoint, methods in paths.items():
    for method in methods:
        print(f"{method.upper()} {endpoint}")

# Define endpoints that are approved for public access
PUBLIC_ENDPOINTS = {("/", "get")}

# Review each endpoint for documented authentication requirements
for endpoint, methods in paths.items():
    for method, details in methods.items():
        security = details.get("security")  # Check for authentication documentation

        if (endpoint, method) in PUBLIC_ENDPOINTS:
            print(f"PASS: {method.upper()} {endpoint} is approved as public")

        elif security:
            print(f"PASS: {method.upper()} {endpoint} has authentication documented")

        else:
            print(f"FINDING: {method.upper()} {endpoint} is missing authentication")

# Retrieve the documented responses for the department endpoint
department_responses = paths["/department/{department_name}"]["get"]["responses"]

# Verify that the endpoint documents a 403 Forbidden response
if "403" in department_responses:
    print("PASS: Department endpoint documents 403 Forbidden")
else:
    print("FINDING: Department endpoint is missing 403 Forbidden documentation")
