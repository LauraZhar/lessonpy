import pytest
import requests
import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import allure

# Конфигурация базы данных
DATABASE_URL = "postgresql://x_clients_db_3fmx_user:mzoTw2Vp4Ox4NQH0XKN3KumdyAYE31uq@dpg-cour99g21fec73bsgvug-a.oregon-postgres.render.com/x_clients_db_3fmx"
engine = sa.create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
metadata = sa.MetaData()

# Определение таблицы employee
employee = sa.Table(
    'employee', metadata,
    sa.Column('id', sa.Integer, primary_key=True),
    sa.Column('is_active', sa.Boolean, nullable=False, default=True),
    sa.Column('create_timestamp', sa.TIMESTAMP, nullable=False, default=datetime.now),
    sa.Column('change_timestamp', sa.TIMESTAMP, nullable=False, default=datetime.now),
    sa.Column('first_name', sa.String(20), nullable=False),
    sa.Column('last_name', sa.String(20), nullable=False),
    sa.Column('middle_name', sa.String(20)),
    sa.Column('phone', sa.String(15), nullable=False),
    sa.Column('email', sa.String(256)),
    sa.Column('avatar_url', sa.String(1024)),
    sa.Column('company_id', sa.Integer, nullable=False)
)

# API URL
BASE_URL = "https://x-clients-be.onrender.com"
AUTH_URL = f"{BASE_URL}/auth/login"
EMPLOYEE_URL = f"{BASE_URL}/employee"
COMPANY_ID = 10157 
AUTH_CREDENTIALS = {
    "username": "raphael",
    "password": "cool-but-crude"
}

class APIClient:
    """
    Класс для работы с API.

    Methods:
        authenticate(): Авторизация и получение токена.
        get_headers(token: str): Получение заголовков для авторизованного запроса.
    """
    def __init__(self):
        self.base_url = BASE_URL
        self.auth_url = AUTH_URL
        self.employee_url = EMPLOYEE_URL

    @allure.step("Авторизация пользователя")
    def authenticate(self) -> str:
        response = requests.post(self.auth_url, json=AUTH_CREDENTIALS)
        print(f"Authorization response: {response.status_code}, {response.text}")
        response.raise_for_status()
        return response.json()["userToken"]

    @staticmethod
    @allure.step("Получение заголовков для авторизованного запроса")
    def get_headers(token: str) -> dict:
        return {
            "x-client-token": token,
            "Content-Type": "application/json"
        }

class EmployeeTable:
    """
    Класс для работы с таблицей employee.

    Methods:
        create_employee(session, employee_data): Создание сотрудника в БД.
        delete_employee(session, employee_id): Удаление сотрудника из БД.
    """
    @staticmethod
    @allure.step("Создание сотрудника в базе данных")
    def create_employee(session, employee_data: dict) -> int:
        insert_stmt = employee.insert().values(employee_data).returning(employee.c.id)
        result = session.execute(insert_stmt)
        session.commit()
        return result.scalar()

    @staticmethod
    @allure.step("Удаление сотрудника из базы данных")
    def delete_employee(session, employee_id: int) -> None:
        session.execute(employee.delete().where(employee.c.id == employee_id))
        session.commit()

@pytest.fixture(scope="module")
def api_client():
    return APIClient()

@pytest.fixture(scope="module")
def auth_token(api_client):
    return api_client.authenticate()

@pytest.fixture(scope="module")
def headers(auth_token, api_client):
    return api_client.get_headers(auth_token)

@pytest.fixture(scope="module")
def db_session():
    session = Session()
    yield session
    session.close()

@pytest.fixture(scope="module")
def setup_test_data(db_session):
    new_employee = {
        "first_name": "TestFirst",
        "last_name": "TestLast",
        "middle_name": "TestMiddle",
        "phone": "1234567890",
        "email": "test@example.com",
        "company_id": COMPANY_ID,
        "is_active": True
    }
    employee_id = EmployeeTable.create_employee(db_session, new_employee)
    yield employee_id
    EmployeeTable.delete_employee(db_session, employee_id)

@allure.title("Получение списка сотрудников")
@allure.description("Тест на получение списка сотрудников для компании")
@allure.feature("Employee API")
@allure.severity(allure.severity_level.CRITICAL)
def test_get_employees(headers, setup_test_data):
    with allure.step("Отправка запроса на получение списка сотрудников"):
        response = requests.get(EMPLOYEE_URL, headers=headers, params={"company": COMPANY_ID})
        print(f"Get employees response: {response.status_code}, {response.text}")
        assert response.status_code == 200
        assert isinstance(response.json(), list)

@allure.title("Создание нового сотрудника")
@allure.description("Тест на создание нового сотрудника через API")
@allure.feature("Employee API")
@allure.severity(allure.severity_level.CRITICAL)
def test_post_employee(headers, db_session):
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
    with allure.step("Отправка запроса на создание сотрудника"):
        response = requests.post(EMPLOYEE_URL, json=new_employee, headers=headers)
        print(f"Create employee response: {response.status_code}, {response.text}")
        response.raise_for_status()
        assert response.status_code == 201
        employee_id = response.json()["id"]

    with allure.step("Проверка, что сотрудник добавлен"):
        get_response = requests.get(f"{EMPLOYEE_URL}/{employee_id}", headers=headers)
        print(f"Get employee response: {get_response.status_code}, {get_response.text}")
        assert get_response.status_code == 200
        employee_data = get_response.json()
        for key in new_employee:
            if new_employee[key] is not None:
                if key in employee_data and employee_data[key] is not None:
                    assert new_employee[key] == employee_data[key], f"Expected {key} to be {new_employee[key]}, but got {employee_data[key]}"

    with allure.step("Удаление сотрудника для чистоты тестов"):
        EmployeeTable.delete_employee(db_session, employee_id)

@allure.title("Получение сотрудника по ID")
@allure.description("Тест на получение сотрудника по ID через API")
@allure.feature("Employee API")
@allure.severity(allure.severity_level.CRITICAL)
def test_get_employee_by_id(headers, setup_test_data):
    employee_id = setup_test_data
    with allure.step("Отправка запроса на получение сотрудника по ID"):
        response = requests.get(f"{EMPLOYEE_URL}/{employee_id}", headers=headers)
        print(f"Get employee by ID response: {response.status_code}, {response.text}")
        assert response.status_code == 200
        employee_data = response.json()
        assert employee_data["id"] == employee_id
        assert employee_data["firstName"] == "TestFirst"
        assert employee_data["lastName"] == "TestLast"
        assert employee_data["phone"] == "1234567890"
        assert employee_data["email"] == "test@example.com"

@allure.title("Обновление данных сотрудника")
@allure.description("Тест на обновление данных сотрудника через API")
@allure.feature("Employee API")
@allure.severity(allure.severity_level.CRITICAL)
def test_patch_employee(headers, setup_test_data, db_session):
    employee_id = setup_test_data
    updated_employee = {
        "lastName": "Smith", 
        "isActive": False
    }
    with allure.step("Отправка запроса на обновление сотрудника"):
        patch_response = requests.patch(f"{EMPLOYEE_URL}/{employee_id}", json=updated_employee, headers=headers)
        print(f"Patch employee response: {patch_response.status_code}, {patch_response.text}")
        patch_response.raise_for_status()
        assert patch_response.status_code == 200

    with allure.step("Проверка, что данные обновлены"):
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