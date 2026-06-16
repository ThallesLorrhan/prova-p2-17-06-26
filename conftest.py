import os
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

os.environ["DATABASE_URL"] = "postgresql://postgres:postgres@localhost:5433/produtos_test"

from main import app, Base, get_db

engine = create_engine(os.environ["DATABASE_URL"])
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture
def client():
    Base.metadata.create_all(bind=engine)

    def override_get_db():
        db = TestingSessionLocal()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app) as c:
        yield c

    Base.metadata.drop_all(bind=engine)
    app.dependency_overrides.clear()

@pytest.fixture
def produto_existente(client):
    response = client.post("/produtos", json={
        "nome": "Notebook",
        "preco": 3500,
        "estoque": 10,
        "ativo": True
    })
    return response.json()
