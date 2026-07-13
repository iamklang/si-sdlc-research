# T003–T007 — contract/integration/unit tests (ครอบ acceptance scenario ทั้ง 5 + FR-008/009)
# หมายเหตุ TDD: ไฟล์นี้ถูกเขียน "ก่อน" โค้ดใน src/ ตาม constitution II
from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)


def test_create_defaults_to_pending():          # scenario #1 · FR-002
    r = client.post("/tasks", json={"title": "ซื้อของ"})
    assert r.status_code == 201
    body = r.json()
    assert body["status"] == "pending"
    assert body["completed_at"] is None


def test_list_returns_all():                     # scenario #2 · FR-003
    for t in ["a", "b", "c"]:
        client.post("/tasks", json={"title": t})
    r = client.get("/tasks")
    assert r.status_code == 200
    assert len(r.json()) >= 3


def test_complete_is_idempotent():               # scenario #3 · FR-006 · edge case
    tid = client.post("/tasks", json={"title": "x"}).json()["id"]
    first = client.post(f"/tasks/{tid}/complete").json()
    assert first["status"] == "done" and first["completed_at"]
    second = client.post(f"/tasks/{tid}/complete").json()
    assert second["completed_at"] == first["completed_at"]   # ทำซ้ำแล้วไม่เปลี่ยน


def test_filter_by_status_done():                # scenario #4 · FR-003
    r = client.get("/tasks", params={"status": "done"})
    assert r.status_code == 200
    assert all(t["status"] == "done" for t in r.json())


def test_delete_then_404():                      # scenario #5 · FR-007
    tid = client.post("/tasks", json={"title": "y"}).json()["id"]
    assert client.delete(f"/tasks/{tid}").status_code == 204
    assert client.get(f"/tasks/{tid}").status_code == 404


def test_title_too_long_returns_422():           # FR-008/009 · T007
    r = client.post("/tasks", json={"title": "a" * 201})
    assert r.status_code == 422
    assert r.json()["error"]["code"] == "validation_error"
