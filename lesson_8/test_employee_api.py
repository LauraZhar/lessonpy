import pytest
import requests

BASE_URL = "https://x-clients-be.onrender.com"
AUTH_URL = f"{BASE_URL}/auth/login"
EMPLOYEE_URL = f"{BASE_URL}/employee"
COMPANY_ID = 10157  # Замените на реальный ID компании, если требуется

# Используем логин и пароль для авторизации
AUTH_CREDENTIALS = {
    "username": "raphael",
    "password": "cool-but-crude"
}

@pytest.fixture(scope="module")
def auth_token():
    response = requests.post(AUTH_URL, json=AUTH_CREDENTIALS)
    print(f"Authorization response: {response.status_code}, {response.text}")
    try:
        response.raise_for_status()
    except requests.exceptions.HTTPError as e:
        print(f"Authorization failed: {response.text}")
        raise e
    return response.json()["userToken"]

@pytest.fixture(scope="module")
def headers(auth_token):
    return {
        "x-client-token": auth_token,
        "Content-Type": "application/json"
    }

def test_get_employees(headers):
    response = requests.get(EMPLOYEE_URL, headers=headers, params={"company": COMPANY_ID})
    print(f"Get employees response: {response.status_code}, {response.text}")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_post_employee(headers):
    new_employee = {
        "firstName": "John",
        "lastName": "Doe",
        "middleName": "Michael",
        "companyId": COMPANY_ID,
        "email": "john.doe@example.com",
        "phone": "1234567890",
        "birthdate": "1990-01-01",
        "isActive": True
    }
    response = requests.post(EMPLOYEE_URL, json=new_employee, headers=headers)
    print(f"Create employee response: {response.status_code}, {response.text}")
    try:
        response.raise_for_status()
    except requests.exceptions.HTTPError as e:
        print(f"Failed to create employee: {response.text}")
        raise e
    assert response.status_code == 201
    employee_id = response.json()["id"]

    # Убедимся, что сотрудник добавлен
    get_response = requests.get(f"{EMPLOYEE_URL}/{employee_id}", headers=headers)
    print(f"Get employee response: {get_response.status_code}, {get_response.text}")
    assert get_response.status_code == 200
    employee_data = get_response.json()
    for key in new_employee:
        if new_employee[key] is not None:
            if key in employee_data and employee_data[key] is not None:
                assert new_employee[key] == employee_data[key], f"Expected {key} to be {new_employee[key]}, but got {employee_data[key]}"

    # Удаление сотрудника для чистоты тестов
    delete_response = requests.delete(f"{EMPLOYEE_URL}/{employee_id}", headers=headers)
    print(f"Delete employee response: {delete_response.status_code}, {delete_response.text}")

def test_get_employee_by_id(headers):
    # Создание нового сотрудника для теста
    new_employee = {
        "firstName": "Jane",
        "lastName": "Doe",
        "middleName": "Marie",
        "companyId": COMPANY_ID,
        "email": "jane.doe@example.com",
        "phone": "0987654321",
        "birthdate": "1985-05-05",
        "isActive": True
    }
    post_response = requests.post(EMPLOYEE_URL, json=new_employee, headers=headers)
    print(f"Create employee response: {post_response.status_code}, {post_response.text}")
    try:
        post_response.raise_for_status()
    except requests.exceptions.HTTPError as e:
        print(f"Failed to create employee: {post_response.text}")
        raise e
    employee_id = post_response.json()["id"]

    response = requests.get(f"{EMPLOYEE_URL}/{employee_id}", headers=headers)
    print(f"Get employee by ID response: {response.status_code}, {response.text}")
    assert response.status_code == 200
    employee_data = response.json()
    for key in new_employee:
        if new_employee[key] is not None:
            if key in employee_data and employee_data[key] is not None:
                assert new_employee[key] == employee_data[key], f"Expected {key} to be {new_employee[key]}, but got {employee_data[key]}"

    # Удаление сотрудника для чистоты тестов
    delete_response = requests.delete(f"{EMPLOYEE_URL}/{employee_id}", headers=headers)
    print(f"Delete employee response: {delete_response.status_code}, {delete_response.text}")

def test_patch_employee(headers):
    # Создание нового сотрудника для теста
    new_employee = {
        "firstName": "Alice",
        "lastName": "Doe",
        "middleName": "Ann",
        "companyId": COMPANY_ID,
        "email": "alice.doe@example.com",
        "phone": "1231231234",
        "birthdate": "1980-10-10",
        "isActive": True
    }
    post_response = requests.post(EMPLOYEE_URL, json=new_employee, headers=headers)
    print(f"Create employee response: {post_response.status_code}, {post_response.text}")
    try:
        post_response.raise_for_status()
    except requests.exceptions.HTTPError as e:
        print(f"Failed to create employee: {post_response.text}")
        raise e
    employee_id = post_response.json()["id"]

    # Обновление данных сотрудника
    updated_employee = {
        "lastName": "Smith",
        "isActive": False
    }
    patch_response = requests.patch(f"{EMPLOYEE_URL}/{employee_id}", json=updated_employee, headers=headers)
    print(f"Patch employee response: {patch_response.status_code}, {patch_response.text}")
    try:
        patch_response.raise_for_status()
    except requests.exceptions.HTTPError as e:
        print(f"Failed to update employee: {patch_response.text}")
        raise e
    assert patch_response.status_code == 200

    # Убедимся, что данные обновлены
    get_response = requests.get(f"{EMPLOYEE_URL}/{employee_id}", headers=headers)
    print(f"Get updated employee response: {get_response.status_code}, {get_response.text}")
    assert get_response.status_code == 200
    employee_data = get_response.json()
    for key in updated_employee:
        if updated_employee[key] is not None:
            if key in employee_data and employee_data[key] is not None:
                assert updated_employee[key] == employee_data[key], f"Expected {key} to be {updated_employee[key]}, but got {employee_data[key]}"
            else:
                print(f"Key {key} not found or is None in response data")

    # Удаление сотрудника для чистоты тестов
    delete_response = requests.delete(f"{EMPLOYEE_URL}/{employee_id}", headers=headers)
    print(f"Delete employee response: {delete_response.status_code}, {delete_response.text}")
