
import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker
from datetime import datetime

DATABASE_URL = "postgresql+psycopg2://x_clients_db_3fmx_user:mzoTw2Vp4Ox4NQH0XKN3KumdyAYE31uq@dpg-cour99g21fec73bsgvug-a.oregon-postgres.render.com/x_clients_db_3fmx"
engine = sa.create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
metadata = sa.MetaData()

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

company = sa.Table(
    'company', metadata,
    sa.Column('id', sa.Integer, primary_key=True),
    sa.Column('name', sa.String(256), nullable=False),
    sa.Column('description', sa.String(1024)),
    sa.Column('is_active', sa.Boolean, nullable=False, default=True)
)

class EmployeeDB:
    def __init__(self):
        self.session = Session()

    def insert_employee(self, employee_data):
        insert_stmt = employee.insert().values(**employee_data)
        result = self.session.execute(insert_stmt)
        self.session.commit() 
        return result.inserted_primary_key[0]

    def select_employee(self, employee_id: int) -> dict:
        select_stmt = sa.select(employee).where(employee.c.id == employee_id)
        result = self.session.execute(select_stmt).mappings().fetchone()
        if result:
            return dict(result)
        else:
            print(f"Employee with id {employee_id} not found.")
            return None

    def update_employee(self, employee_id: int, update_data: dict):
        update_stmt = employee.update().where(employee.c.id == employee_id).values(**update_data)
        self.session.execute(update_stmt)
        self.session.commit()

    def delete_employee(self, employee_id):
        delete_stmt = employee.delete().where(employee.c.id == employee_id)
        self.session.execute(delete_stmt)
        self.session.commit()
 
    def insert_company(self, company_data):
        insert_stmt = company.insert().values(**company_data)
        result = self.session.execute(insert_stmt)
        self.session.commit()
        return result.inserted_primary_key[0]

    def delete_company(self, company_id):
        delete_stmt = company.delete().where(company.c.id == company_id)
        self.session.execute(delete_stmt)
        self.session.commit()

    def delete_employees_by_company_id(self, company_id):
        delete_stmt = employee.delete().where(employee.c.company_id == company_id)
        self.session.execute(delete_stmt)
        self.session.commit()

    def close(self):
        self.session.close()
