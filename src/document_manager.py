import json
import os
import uuid
from datetime import datetime

from src.vector_db import delete_document_collection


DOCUMENTS_FILE = "data/documents.json"
UPLOAD_DIR = "data/uploads"


def _ensure_storage():
    os.makedirs("data", exist_ok=True)
    os.makedirs(UPLOAD_DIR, exist_ok=True)

    if not os.path.exists(DOCUMENTS_FILE):
        with open(DOCUMENTS_FILE, "w", encoding="utf-8") as file:
            json.dump([], file, indent=4)


def get_documents():
    _ensure_storage()

    with open(
        DOCUMENTS_FILE,
        "r",
        encoding="utf-8"
    ) as file:
        return json.load(file)


def save_documents(documents):
    _ensure_storage()

    with open(
        DOCUMENTS_FILE,
        "w",
        encoding="utf-8"
    ) as file:
        json.dump(
            documents,
            file,
            indent=4,
            ensure_ascii=False
        )


def add_document(
    filename,
    file_bytes
):
    documents = get_documents()

    document_id = uuid.uuid4().hex[:8]

    safe_filename = filename

    file_path = os.path.join(
        UPLOAD_DIR,
        f"{document_id}_{safe_filename}"
    )

    with open(file_path, "wb") as file:
        file.write(file_bytes)

    document = {
        "id": document_id,
        "name": filename,
        "path": file_path,
        "created_at": datetime.now().isoformat()
    }

    documents.append(document)

    save_documents(documents)

    return document


def get_document(document_id):
    documents = get_documents()

    for document in documents:
        if document["id"] == document_id:
            return document

    return None


def delete_document(document_id):
    documents = get_documents()

    document = None

    for item in documents:
        if item["id"] == document_id:
            document = item
            break

    if document is None:
        return False

    # Delete physical PDF
    file_path = document.get("path")

    if file_path and os.path.exists(file_path):
        os.remove(file_path)

    # Delete Chroma collection
    delete_document_collection(
        document_id
    )

    # Remove metadata
    documents = [
        item
        for item in documents
        if item["id"] != document_id
    ]

    save_documents(documents)

    return True