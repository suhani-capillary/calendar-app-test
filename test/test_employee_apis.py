import pytest
import requests
from requests import Response
from datetime import datetime

BASE_URL = "http://localhost:8080/employee"

@pytest.fixture()
def add_and_delete_employee():
    new_employee = {
        "name": 'Test_User',
        "email": 'TestUser' + str(datetime.now()) + '@gmail.com',
        "officeId": 101,
        "dob": '2001-10-20'
    }
    new_employee_response = requests.post(BASE_URL, json=new_employee)
    assert new_employee_response.status_code == 201
    print("employee added")
    employee = new_employee_response.json()

    yield employee
    response = requests.delete(BASE_URL + f"/{employee['empId']}")
    assert response.status_code == 200
    print("employee removed")

def test_get_all_employees():
    response = requests.get(BASE_URL)
    assert response.status_code == 200
    employees = response.json()
    assert isinstance(employees, list)
    assert len(employees) >= 0


def test_get_employee_by_email(add_and_delete_employee):

    email = add_and_delete_employee['email']
    response = requests.get(BASE_URL + "/email/" + email)
    assert response.status_code == 200
    employee = response.json()
    assert isinstance(employee, dict)
    assert "empId" in employee
    assert "name" in employee
    assert "email" in employee
    assert email == employee["email"]


def test_add_employee():
    new_employee = {
        "name": 'Test_User',
        "email": 'TestUser' + str(datetime.now()) + '@gmail.com',
        "officeId": 101,
        "dob": '2001-10-20'
    }
    response = requests.post(BASE_URL, json=new_employee)
    assert response.status_code == 201
    employee = response.json()
    assert isinstance(employee, dict)
    assert "empId" in employee
    assert employee["name"] == new_employee["name"]
    assert employee["email"] == new_employee["email"]


def test_remove_employee():
    new_employee_response = add_employee()
    assert new_employee_response.status_code == 201
    employee = new_employee_response.json()
    emp_id = employee["empId"]

    response = requests.delete(BASE_URL + f"/{emp_id}")
    assert response.status_code == 200
    assert response.text == "Employee Deleted"

    response = get_employee_by_id(emp_id)
    assert response.status_code == 404


def test_update_employee_details(add_and_delete_employee):

    employee = add_and_delete_employee
    emp_id = employee["empId"]

    updated_employee = {
        "name": "Update_user",
        "email": 'TestUser' + str(datetime.now()) + '@gmail.com',
        "officeId": 101,
        "dob": '2001-10-25'
    }
    response = requests.put(BASE_URL + f"/{emp_id}", json=updated_employee)
    assert response.status_code == 200
    updated_employee_data = response.json()
    assert updated_employee_data["empId"] == emp_id
    assert updated_employee_data["name"] == updated_employee["name"]
    assert updated_employee_data["email"] == updated_employee["email"]


def add_employee() -> Response:
    new_employee = {
        "name": 'Test_User',
        "email": 'TestUser' + str(datetime.now()) + '@gmail.com',
        "officeId": 101,
        "dob": '2001-10-20'
    }
    return requests.post(BASE_URL, json=new_employee)


def delete_employee(id: str) -> Response:
    return requests.delete(f"{BASE_URL}/{id}")


def get_employee_by_id(id: str) -> Response:
    return requests.get(f"{BASE_URL}/{id}")
