import json

from django.test import Client, TestCase

from .models import Note


class NotesApiTests(TestCase):
    def setUp(self) -> None:
        self.client = Client()

    def test_health_endpoint(self) -> None:
        response = self.client.get("/api/health/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["status"], "ok")

    def test_create_and_list_notes(self) -> None:
        payload = {"title": "Write docs", "body": "Update API docs", "status": "todo"}
        create_response = self.client.post(
            "/api/notes/",
            data=json.dumps(payload),
            content_type="application/json",
        )
        self.assertEqual(create_response.status_code, 201)
        self.assertEqual(Note.objects.count(), 1)

        list_response = self.client.get("/api/notes/")
        self.assertEqual(list_response.status_code, 200)
        self.assertEqual(len(list_response.json()["data"]), 1)

    def test_update_and_delete_note(self) -> None:
        note = Note.objects.create(title="Initial", body="body", status="todo")

        update_response = self.client.put(
            f"/api/notes/{note.id}/",
            data=json.dumps({"title": "Updated", "status": "done"}),
            content_type="application/json",
        )
        self.assertEqual(update_response.status_code, 200)
        note.refresh_from_db()
        self.assertEqual(note.title, "Updated")
        self.assertEqual(note.status, "done")

        delete_response = self.client.delete(f"/api/notes/{note.id}/")
        self.assertEqual(delete_response.status_code, 204)
        self.assertEqual(Note.objects.count(), 0)
