import json

from django.http import HttpRequest, HttpResponseNotAllowed, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from .models import Note


def _note_to_dict(note: Note) -> dict[str, str | int]:
    return {
        "id": note.id,
        "title": note.title,
        "body": note.body,
        "status": note.status,
        "created_at": note.created_at.isoformat(),
        "updated_at": note.updated_at.isoformat(),
    }


def _parse_json(request: HttpRequest) -> tuple[dict, JsonResponse | None]:
    try:
        data = json.loads(request.body or b"{}")
    except json.JSONDecodeError:
        return {}, JsonResponse({"error": "invalid json payload"}, status=400)
    return data, None


@require_http_methods(["GET"])
def health(_request: HttpRequest) -> JsonResponse:
    return JsonResponse({"status": "ok"})


@csrf_exempt
def note_collection(request: HttpRequest) -> JsonResponse | HttpResponseNotAllowed:
    if request.method == "GET":
        status_filter = request.GET.get("status")
        queryset = Note.objects.all()
        if status_filter:
            queryset = queryset.filter(status=status_filter)
        return JsonResponse({"data": [_note_to_dict(note) for note in queryset]})

    if request.method == "POST":
        payload, error = _parse_json(request)
        if error is not None:
            return error

        title = str(payload.get("title", "")).strip()
        if not title:
            return JsonResponse({"error": "title is required"}, status=400)

        status = str(payload.get("status", Note.STATUS_TODO)).strip()
        allowed_statuses = {choice[0] for choice in Note.STATUS_CHOICES}
        if status not in allowed_statuses:
            return JsonResponse({"error": "invalid status"}, status=400)

        note = Note.objects.create(
            title=title,
            body=str(payload.get("body", "")),
            status=status,
        )
        return JsonResponse({"data": _note_to_dict(note)}, status=201)

    return HttpResponseNotAllowed(["GET", "POST"])


@csrf_exempt
def note_detail(request: HttpRequest, note_id: int) -> JsonResponse | HttpResponseNotAllowed:
    try:
        note = Note.objects.get(id=note_id)
    except Note.DoesNotExist:
        return JsonResponse({"error": "note not found"}, status=404)

    if request.method == "GET":
        return JsonResponse({"data": _note_to_dict(note)})

    if request.method == "PUT":
        payload, error = _parse_json(request)
        if error is not None:
            return error

        title = str(payload.get("title", note.title)).strip()
        if not title:
            return JsonResponse({"error": "title is required"}, status=400)

        status = str(payload.get("status", note.status)).strip()
        allowed_statuses = {choice[0] for choice in Note.STATUS_CHOICES}
        if status not in allowed_statuses:
            return JsonResponse({"error": "invalid status"}, status=400)

        note.title = title
        note.body = str(payload.get("body", note.body))
        note.status = status
        note.save()
        return JsonResponse({"data": _note_to_dict(note)})

    if request.method == "DELETE":
        note.delete()
        return JsonResponse({}, status=204)

    return HttpResponseNotAllowed(["GET", "PUT", "DELETE"])
