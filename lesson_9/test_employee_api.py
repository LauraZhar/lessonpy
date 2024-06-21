import pytest
import requests
import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker
from datetime import datetime

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
COMPANY_ID = 10157  # Замените на реальный ID компании, если требуется

# Логин и пароль для авторизации
AUTH_CREDENTIALСЛS = {
    "username": "raphael",
    "password": "cool-but-crude"
}

@pytest.fixture(scope="module")
def auth_token():
    response = requests.post(AUTH_URL, json=AUTH_CREDENTIALСЛS)
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
    insert_stmt = employee.insert().values(new_employee).returning(employee.c.id)
    result = db_session.execute(insert_stmt)
    db_session.commit()
    test_employee_id = result.scalar()
    yield test_employee_id
    db_session.execute(employee.delete().where(employee.c.id == test_employee_id))
    db_session.commit()

def test_get_employees(headers, setup_test_data):
    response = requests.get(EMPLOYEE_URL, headers=headers, params={"company": COMPANY_ID})
    print(f"Get employees response: {response.status_code}, {response.text}")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

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
    db_session.execute(employee.delete().where(employee.c.id == employee_id))
    db_session.commit()

def test_get_employee_by_id(headers, setup_test_data):
    employee_id = setup_test_data
    response = requests.get(f"{EMPLOYEE_URL}/{employee_id}", headers=headers)
    print(f"Get employee by ID response: {response.status_code}, {response.text}")
    assert response.status_code == 200
    employee_data = response.json()
    assert employee_data["id"] == employee_id
    assert employee_data["firstName"] == "TestFirst"
    assert employee_data["lastName"] == "TestLast"
    assert employee_data["phone"] == "1234567890"
    assert employee_data["email"] == "test@example.com"

def test_patch_employee(headers, setup_test_data, db_session):
    employee_id = setup_test_data
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
