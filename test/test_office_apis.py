import pytest
import requests
from requests import Response
from datetime import datetime

BASE_URL = "http://localhost:8080/office"


@pytest.fixture()
def add_and_delete_office():
    new_office = {
        "name": 'Test_Office',
        "location": 'Bangalore',
        "totalRooms": 25,

    }
    new_office_response = requests.post(BASE_URL, json=new_office)
    assert new_office_response.status_code == 201
    print("office created")
    office = new_office_response.json()

    yield office["officeId"]
    response = requests.delete(BASE_URL + f"/{office['officeId']}")
    assert response.status_code == 200
    print("office deleted")


def test_get_all_offices():
    response = requests.get(BASE_URL)
    assert response.status_code == 200
    offices = response.json()
    assert isinstance(offices, list)
    assert len(offices) >= 0


def test_get_office_by_id(add_and_delete_office):
    officeId = add_and_delete_office
    response = requests.get(f"{BASE_URL}/{officeId}")
    assert response.status_code == 200
    office = response.json()
    assert isinstance(office, dict)
    assert "officeId" in office
    assert "name" in office
    assert "location" in office
    assert "totalRooms" in office
    assert officeId == office["officeId"]


def test_add_office():
    new_office = {
        "name": 'Test_Office',
        "location": 'Bangalore',
        "totalRooms": 25
    }
    response = requests.post(BASE_URL, json=new_office)
    assert response.status_code == 201
    office = response.json()
    assert isinstance(office, dict)
    assert "officeId" in office
    assert office["name"] == new_office["name"]
    assert office["location"] == new_office["location"]
    assert office["totalRooms"] == new_office["totalRooms"]


def test_remove_office():
    new_office_response = add_office()
    assert new_office_response.status_code == 201
    office = new_office_response.json()
    office_id = office["officeId"]
    response = requests.delete(BASE_URL + f"/{office_id}")
    assert response.status_code == 200
    assert response.text == "Office Deleted"

    response = get_office_by_id(office_id)
    assert response.status_code == 404


def test_update_office_details(add_and_delete_office):
    office_id = add_and_delete_office

    updated_office = {
        "name": 'Updated_Office',
        "location": 'Bangalore',
        "totalRooms": 20
    }
    response = requests.put(BASE_URL + f"/{office_id}", json=updated_office)
    assert response.status_code == 200
    updated_office_data = response.json()
    assert updated_office_data["officeId"] == office_id
    assert updated_office_data["name"] == updated_office["name"]
    assert updated_office_data["location"] == updated_office["location"]
    assert updated_office_data["totalRooms"] == updated_office["totalRooms"]


def add_office() -> Response:
    new_office = {
        "name": 'Test_Office',
        "location": 'Bangalore',
        "totalRooms": 25,

    }
    return requests.post(BASE_URL, json=new_office)


def delete_office(id) -> Response:
    return requests.delete(f"{BASE_URL}/{id}")


def get_office_by_id(id) -> Response:
    return requests.get(f"{BASE_URL}/{id}")
