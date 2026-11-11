import json
from pathlib import Path

spec_path = Path("openapi.json")

with spec_path.open("r", encoding="utf-8") as file:
    api_spec = json.load(file)

print(api_spec["info"])

paths = api_spec["paths"]

for endpoint, methods in paths.items():
    for method in methods:
        print(f"{method.upper()} {endpoint}")

PUBLIC_ENDPOINTS = {("/", "get")}

for endpoint, methods in paths.items():
    for method, details in methods.items():
        security = details.get("security")

        if (endpoint, method) in PUBLIC_ENDPOINTS:
            print(f"PASS: {method.upper()} {endpoint} is approved as public")

        elif security:
            print(f"PASS: {method.upper()} {endpoint} has authentication documented")

        else:
            print(f"FINDING: {method.upper()} {endpoint} is missing authentication")


department_responses = paths["/department/{department_name}"]["get"]["responses"]

if "403" in department_responses:
    print("PASS: Department endpoint documents 403 Forbidden")
else:
    print("FINDING: Department endpoint is missing 403 Forbidden documentation")