import pytest
from fastapi.testclient import TestClient
from src.main import app

def test_app_starts():
    """Test that the app starts without errors"""
    client = TestClient(app)
    response = client.get("/")
    assert response.status_code == 200
    assert "message" in response.json()

def test_chat_endpoint_exists():
    """Test that the chat endpoint is available (will return 422 for missing body or 401 for missing auth)"""
    client = TestClient(app)
    # Use hardcoded API prefix since settings might not be accessible in test context
    response = client.post("/api/chat", json={})
    # Should return either 422 (validation error) or 401/403 (auth error) - both mean endpoint exists
    assert response.status_code in [401, 403, 422, 405]  # 405 if it's a GET-only endpoint

def test_conversations_endpoint_exists():
    """Test that the conversations endpoint is available"""
    client = TestClient(app)
    # Use hardcoded API prefix since settings might not be accessible in test context
    response = client.get("/api/conversations")
    # Should return 401/403 (auth error) - means endpoint exists
    assert response.status_code in [401, 403]

if __name__ == "__main__":
    # Run basic tests
    try:
        test_app_starts()
        print("✓ App starts successfully")
    except Exception as e:
        print(f"✗ App start test failed: {e}")

    try:
        test_chat_endpoint_exists()
        print("✓ Chat endpoint exists")
    except Exception as e:
        print(f"✗ Chat endpoint test failed: {e}")

    try:
        test_conversations_endpoint_exists()
        print("✓ Conversations endpoint exists")
    except Exception as e:
        print(f"✗ Conversations endpoint test failed: {e}")

    print("Basic tests completed")