import json
import os
import uuid
from datetime import datetime


ROOMS_FILE = "data/rooms.json"


def _ensure_storage():
    os.makedirs("data", exist_ok=True)

    if not os.path.exists(ROOMS_FILE):
        with open(
            ROOMS_FILE,
            "w",
            encoding="utf-8"
        ) as file:
            json.dump([], file, indent=4)


def get_rooms():
    _ensure_storage()

    with open(
        ROOMS_FILE,
        "r",
        encoding="utf-8"
    ) as file:
        return json.load(file)


def save_rooms(rooms):
    _ensure_storage()

    with open(
        ROOMS_FILE,
        "w",
        encoding="utf-8"
    ) as file:
        json.dump(
            rooms,
            file,
            indent=4,
            ensure_ascii=False
        )


def create_room(name="New Chat"):
    rooms = get_rooms()

    room = {
        "id": uuid.uuid4().hex[:8],
        "name": name,
        "document_ids": [],
        "messages": [],
        "created_at": datetime.now().isoformat()
    }

    rooms.append(room)

    save_rooms(rooms)

    return room


def get_room(room_id):
    rooms = get_rooms()

    for room in rooms:
        if room["id"] == room_id:
            return room

    return None


def update_room(room_id, **updates):
    rooms = get_rooms()

    for room in rooms:

        if room["id"] == room_id:

            room.update(updates)

            save_rooms(rooms)

            return room

    return None


def delete_room(room_id):
    rooms = get_rooms()

    new_rooms = [
        room
        for room in rooms
        if room["id"] != room_id
    ]

    if len(new_rooms) == len(rooms):
        return False

    save_rooms(new_rooms)

    return True


def add_message(
    room_id,
    role,
    content
):
    rooms = get_rooms()

    for room in rooms:

        if room["id"] == room_id:

            room["messages"].append({
                "role": role,
                "content": content
            })

            save_rooms(rooms)

            return True

    return False


def set_room_documents(
    room_id,
    document_ids
):
    return update_room(
        room_id,
        document_ids=document_ids
    )


def remove_document_from_rooms(
    document_id
):
    rooms = get_rooms()

    changed = False

    for room in rooms:

        if document_id in room["document_ids"]:

            room["document_ids"] = [
                doc_id
                for doc_id in room["document_ids"]
                if doc_id != document_id
            ]

            changed = True

    if changed:
        save_rooms(rooms)

    return changed