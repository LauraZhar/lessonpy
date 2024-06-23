import sys
import os
import pytest
import requests

# Добавляем путь к директории проекта
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

from db import EmployeeDB

class EmployeeAPI:
    def __init__(self, base_url, headers):
        self.base_url = base_url
        self.headers = headers

    def create_employee(self, employee_data):
        response = requests.post(f"{self.base_url}/employee", json=employee_data, headers=self.headers)
        response.raise_for_status()
        return response.json()

    def update_employee(self, employee_id, update_data):
        response = requests.patch(f"{self.base_url}/employee/{employee_id}", json=update_data, headers=self.headers)
        response.raise_for_status()
        return response.json()

    def get_employee(self, employee_id):
        response = requests.get(f"{self.base_url}/employee/{employee_id}", headers=self.headers)
        response.raise_for_status()
        return response.json()

    def delete_employee(self, employee_id):
        response = requests.delete(f"{self.base_url}/employee/{employee_id}", headers=self.headers)
        response.raise_for_status()

@pytest.fixture(scope="module")
def db():
    db_instance = EmployeeDB()
    yield db_instance
    db_instance.close()

@pytest.fixture(scope="module")
def setup_test_company(db):
    new_company = {
        "name": "Test Company",
        "description": "A company for testing purposes",
        "is_active": True
    }
    company_id = db.insert_company(new_company)
    yield company_id
    db.delete_employees_by_company_id(company_id)
    db.delete_company(company_id)

@pytest.fixture(scope="module")
def headers():
    auth_url = "https://x-clients-be.onrender.com/auth/login"
    auth_data = {
        "username": "raphael",
        "password": "cool-but-crude"
    }
    response = requests.post(auth_url, json=auth_data)
    token = response.json()["userToken"]
    return {
        "Content-Type": "application/json",
        "x-client-token": token
    }

@pytest.fixture(scope="module")
def employee_api(headers):
    return EmployeeAPI(base_url="https://x-clients-be.onrender.com", headers=headers)

def test_employee_crud_operations(employee_api, db, setup_test_company):
    company_id = setup_test_company

    # Создание нового сотрудника (insert)
    new_employee = {
        "firstName": "John",
        "lastName": "Doe",
        "middleName": "Michael",
        "companyId": company_id,
        "email": "john.doe@example.com",
        "phone": "1234567890",
        "birthdate": "1990-01-01",
        "isActive": True
    }
    create_response = employee_api.create_employee(new_employee)
    print(f"Create employee response: {create_response}")
    employee_id = create_response["id"]

    # Проверка созданного сотрудника в базе данных
    db_employee = db.select_employee(employee_id)
    print(f"Database employee: {db_employee}")
    assert db_employee is not None
    assert db_employee["id"] == employee_id
    assert db_employee["first_name"] == "John"
    assert db_employee["last_name"] == "Doe"
    assert db_employee["middle_name"] == "Michael"
    assert db_employee["phone"] == "1234567890"
    assert db_employee["is_active"] == True

    # Обновление сотрудника (update)
    updated_data = {
        "lastName": "Smith"
    }
    update_response = employee_api.update_employee(employee_id, updated_data)
    print(f"Update employee response: {update_response}")

    # Проверка обновленного сотрудника в базе данных
    db_updated_employee = db.select_employee(employee_id)
    print(f"Database updated employee: {db_updated_employee}")
    assert db_updated_employee["last_name"] == "Smith"

    # Удаление сотрудника (delete)
    db.delete_employee(employee_id)

    # Проверка, что сотрудник удален из базы данных
    db_deleted_employee = db.select_employee(employee_id)
    print(f"Database deleted employee: {db_deleted_employee}")
    assert db_deleted_employee is None
