from app.core.security import (
    authenticate_user,
    create_access_token,
    get_password_hash,
    verify_password,
)


class TestPasswordHashing:
    def test_password_hash_and_verify(self):
        password = "securepassword123"
        hashed = get_password_hash(password)

        assert hashed != password
        assert verify_password(password, hashed) is True
        assert verify_password("wrongpassword", hashed) is False

    def test_different_passwords_different_hashes(self):
        password = "testpassword"
        hash1 = get_password_hash(password)
        hash2 = get_password_hash(password)

        assert hash1 != hash2


class TestAuthenticateUser:
    def test_authenticate_valid_user(self, test_db):
        db, _ = test_db
        authed_user = authenticate_user(db, "testuser", "testpassword123")

        assert authed_user is not None
        assert authed_user.username == "testuser"
        assert authed_user.email == "test@example.com"

    def test_authenticate_invalid_username(self, test_db):
        db, _ = test_db
        user = authenticate_user(db, "wronguser", "testpassword123")

        assert user is None

    def test_authenticate_invalid_password(self, test_db):
        db, _ = test_db
        user = authenticate_user(db, "testuser", "wrongpassword")

        assert user is None

    def test_authenticate_nonexistent_user(self, test_db):
        db, _ = test_db
        user = authenticate_user(db, "nonexistent", "password")

        assert user is None


class TestCreateAccessToken:
    def test_create_access_token(self):
        token = create_access_token(data={"sub": "testuser"})

        assert token is not None
        assert isinstance(token, str)
        assert len(token) > 0


class TestAuthEndpoints:
    def test_register_success(self, client):
        response = client.post(
            "/api/v1/auth/register",
            json={
                "username": "newuser",
                "email": "newuser@example.com",
                "password": "newpassword123",
            },
        )

        assert response.status_code == 201
        data = response.json()
        assert data["username"] == "newuser"
        assert data["email"] == "newuser@example.com"
        assert data["is_active"] is True
        assert "id" in data

    def test_register_duplicate_email(self, client):
        response = client.post(
            "/api/v1/auth/register",
            json={
                "username": "anotheruser",
                "email": "test@example.com",
                "password": "password123",
            },
        )

        assert response.status_code == 400
        assert "already registered" in response.json()["detail"].lower()

    def test_register_invalid_email(self, client):
        response = client.post(
            "/api/v1/auth/register",
            json={
                "username": "newuser",
                "email": "invalid-email",
                "password": "password123",
            },
        )

        assert response.status_code == 422

    def test_register_short_password(self, client):
        response = client.post(
            "/api/v1/auth/register",
            json={
                "username": "newuser",
                "email": "new@example.com",
                "password": "short",
            },
        )

        assert response.status_code == 422

    def test_login_success(self, client, test_db):
        response = client.post(
            "/api/v1/auth/login",
            data={"username": "testuser", "password": "testpassword123"},
        )

        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert data["token_type"] == "bearer"

    def test_login_wrong_password(self, client, test_db):
        response = client.post(
            "/api/v1/auth/login",
            data={"username": "testuser", "password": "wrongpassword"},
        )

        assert response.status_code == 401
        assert "incorrect" in response.json()["detail"].lower()

    def test_login_nonexistent_user(self, client):
        response = client.post(
            "/api/v1/auth/login",
            data={"username": "nonexistent", "password": "password123"},
        )

        assert response.status_code == 401

    def test_logout(self, client):
        response = client.post("/api/v1/auth/logout")

        assert response.status_code == 200
        assert "logged out" in response.json()["message"].lower()

    def test_get_me_unauthenticated(self, client):
        response = client.get("/api/v1/auth/me")

        assert response.status_code == 401

    def test_auth_status_unauthenticated(self, client):
        response = client.get("/api/v1/auth/status")

        assert response.status_code == 200
        assert response.json()["authenticated"] is False


class TestHealthEndpoints:
    def test_health_check(self, client):
        response = client.get("/api/v1/health")

        assert response.status_code == 200
        assert response.json()["status"] == "healthy"

    def test_readiness_check(self, client):
        response = client.get("/api/v1/health/ready")

        assert response.status_code == 200
        assert response.json()["status"] == "ready"
