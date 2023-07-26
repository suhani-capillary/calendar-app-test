import pytest
import requests
from requests import Response
from datetime import datetime

BASE_URL = "http://localhost:8080/meeting-room"


def test_get_all_meeting_rooms():
    response = requests.get(BASE_URL)
    assert response.status_code == 200
    meeting_rooms = response.json()
    assert isinstance(meeting_rooms, list)
    assert len(meeting_rooms) >= 0


def test_get_meeting_room_by_id():
    new_meeting_room_response = add_meeting_room()
    assert new_meeting_room_response.status_code == 201
    roomId = new_meeting_room_response.json()['roomId']
    response = requests.get(f"{BASE_URL}/{roomId}")
    assert response.status_code == 200
    meeting_room = response.json()
    assert isinstance(meeting_room, dict)
    assert "roomId" in meeting_room
    assert "name" in meeting_room
    assert "capacity" in meeting_room
    assert "officeLocation" in meeting_room
    assert roomId == meeting_room["roomId"]


def test_add_meeting_room():
    new_meeting_room = {
        "name": 'Test_Meeting_Room',
        "capacity": 15,
        "officeId": 101
    }
    response = requests.post(BASE_URL, json=new_meeting_room)
    assert response.status_code == 201
    meeting_room = response.json()
    assert isinstance(meeting_room, dict)
    assert "roomId" in meeting_room
    assert meeting_room["name"] == new_meeting_room["name"]
    assert meeting_room["capacity"] == new_meeting_room["capacity"]


def test_remove_meeting_room():
    new_meeting_room_response = add_meeting_room()
    assert new_meeting_room_response.status_code == 201
    meeting_room = new_meeting_room_response.json()
    roomId= meeting_room["roomId"]

    response = requests.delete(BASE_URL + f"/{roomId}")
    assert response.status_code == 200
    assert response.text == "Meeting Room deleted successfully!"

    response = get_meeting_room_by_id(roomId)
    assert response.status_code == 404


def test_update_meeting_room_details():
    new_meeting_room_response = add_meeting_room()
    assert new_meeting_room_response.status_code == 201
    meeting_room = new_meeting_room_response.json()
    roomId = meeting_room["roomId"]

    updated_meeting_room = {
        "name": 'Updated_Meeting_Room',
        "capacity": 15,
        "officeId": 101
    }
    response = requests.put(BASE_URL + f"/{roomId}", json=updated_meeting_room)
    assert response.status_code == 200
    updated_meeting_room_data = response.json()
    assert updated_meeting_room_data["roomId"] == roomId
    assert updated_meeting_room_data["name"] == updated_meeting_room["name"]
    assert updated_meeting_room_data["capacity"] == updated_meeting_room["capacity"]


def add_meeting_room() -> Response:
    new_meeting_room = {
        "name": 'Test_Meeting_Room',
        "capacity": 10,
        "officeId": 101,

    }
    return requests.post(BASE_URL, json=new_meeting_room)


def delete_meeting_room(id: str) -> Response:
    return requests.delete(f"{BASE_URL}/{id}")


def get_meeting_room_by_id(id: str) -> Response:
    return requests.get(f"{BASE_URL}/{id}")
