import pytest
import requests
from socketio import Client

BASE_URL = "http://localhost:8000"

@pytest.fixture
def client():
    return Client(transports=["websocket"])

def test_get_history():
    response = requests.get(f"{BASE_URL}/history")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    print("test_get_history passed!")

def test_clear_board():
    response = requests.post(f"{BASE_URL}/clear")
    assert response.status_code == 200
    assert response.json()["status"] == "cleared"
    print("test_get_history passed!")

def test_draw_line():
    """Test the /draw_line endpoint."""
    response = requests.post(
        f"{BASE_URL}/draw_line",
        params={
            "x": 10,
            "y": 20,
            "width": 100,
            "height": 50,
            "color": "#FF0000"
        }
    )
    assert response.status_code == 200
    assert response.json() == {"status": "line drawn"}
    print("test_draw_line passed!")

def test_draw_ellipse():
    """Test the /draw_ellipse endpoint."""
    response = requests.post(
        f"{BASE_URL}/draw_ellipse",
        params={
            "x": 50,
            "y": 50,
            "rx": 30,
            "ry": 20,
            "color": "#00FF00"
        }
    )
    assert response.status_code == 200
    assert response.json() == {"status": "ellipse drawn"}
    print("test_draw_ellipse passed!")

def test_draw_rect():
    """Test the /draw_rect endpoint."""
    response = requests.post(
        f"{BASE_URL}/draw_rect",
        params={
            "x": 100,
            "y": 100,
            "width": 200,
            "height": 150,
            "color": "#0000FF"
        }
    )
    assert response.status_code == 200
    assert response.json() == {"status": "rectangle drawn"}
    print("test_draw_rect passed!")
    
if __name__ == "__main__":
    test_draw_line()
    test_draw_ellipse()
    test_draw_rect()
    test_get_history()
    test_clear_board()