import pytest

def test_lista_vazia(client):
    r = client.get("/produtos")
    assert r.status_code == 200
    assert r.json() == []

def test_criar_produto(client):
    r = client.post("/produtos", json={"nome":"Mouse","preco":100})
    assert r.status_code == 201
    assert r.json()["id"] > 0

def test_produto_aparece_na_listagem(client):
    client.post("/produtos", json={"nome":"Teclado","preco":200})
    r = client.get("/produtos")
    assert len(r.json()) == 1

def test_buscar_por_id(client, produto_existente):
    r = client.get(f"/produtos/{produto_existente['id']}")
    assert r.status_code == 200

def test_buscar_inexistente(client):
    r = client.get("/produtos/999")
    assert r.status_code == 404

def test_deletar_produto(client, produto_existente):
    r = client.delete(f"/produtos/{produto_existente['id']}")
    assert r.status_code == 204

def test_deletar_e_confirmar_remocao(client, produto_existente):
    client.delete(f"/produtos/{produto_existente['id']}")
    r = client.get(f"/produtos/{produto_existente['id']}")
    assert r.status_code == 404

def test_deletar_inexistente(client):
    r = client.delete("/produtos/999")
    assert r.status_code == 404

@pytest.mark.parametrize("payload",[
    {"nome":"","preco":100},
    {"nome":"Produto","preco":0},
    {"nome":"Produto","preco":-1},
])
def test_payload_invalido(client, payload):
    r = client.post("/produtos", json=payload)
    assert r.status_code == 422

def test_banco_isolado(client):
    r = client.get("/produtos")
    assert len(r.json()) == 0
