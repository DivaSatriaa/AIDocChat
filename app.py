import re

import numpy as np
import streamlit as st

from src.pdf_loader import load_pdf
from src.chunker import chunk_text
from src.embedder import create_embeddings
from src.vector_db import (
    store_chunks,
    search_documents
)
from src.llm import ask_llm

from src.document_manager import (
    get_documents,
    add_document,
    delete_document
)

from src.room_manager import (
    get_rooms,
    create_room,
    get_room,
    update_room,
    delete_room,
    add_message,
    set_room_documents,
    remove_document_from_rooms
)


# =========================================================
# Page configuration
# =========================================================

st.set_page_config(
    page_title="AIDocChat",
    page_icon="🤖",
    layout="wide"
)


# =========================================================
# Helper: semantic source snippet
# =========================================================

def get_relevant_snippet(
    text,
    question,
    max_sentences=2
):

    sentences = re.split(
        r"(?<=[.!?])\s+",
        text.strip()
    )

    sentences = [
        sentence.strip()
        for sentence in sentences
        if sentence.strip()
    ]

    if not sentences:
        return text

    question_embedding = create_embeddings(
        [question]
    )[0]

    sentence_embeddings = create_embeddings(
        sentences
    )

    question_norm = np.linalg.norm(
        question_embedding
    )

    sentence_norms = np.linalg.norm(
        sentence_embeddings,
        axis=1
    )

    similarities = (
        sentence_embeddings @ question_embedding
    ) / (
        sentence_norms
        * question_norm
        + 1e-8
    )

    best_index = int(
        np.argmax(similarities)
    )

    start = max(
        0,
        best_index - 1
    )

    end = min(
        len(sentences),
        best_index + max_sentences
    )

    snippet = " ".join(
        sentences[start:end]
    )

    if start > 0:
        snippet = "... " + snippet

    if end < len(sentences):
        snippet += " ..."

    return snippet


# =========================================================
# Session state
# =========================================================

if "current_room_id" not in st.session_state:

    rooms = get_rooms()

    if rooms:
        st.session_state.current_room_id = rooms[0]["id"]

    else:
        room = create_room(
            "New Chat"
        )

        st.session_state.current_room_id = (
            room["id"]
        )


# =========================================================
# Load current room
# =========================================================

current_room = get_room(
    st.session_state.current_room_id
)

if current_room is None:

    room = create_room(
        "New Chat"
    )

    st.session_state.current_room_id = (
        room["id"]
    )

    current_room = room


# =========================================================
# Sidebar
# =========================================================

with st.sidebar:

    st.title("🤖 AIDocChat")

    st.caption(
        "AI Document Assistant"
    )

    # =====================================================
    # Chat Rooms
    # =====================================================

    st.subheader("💬 Chat Rooms")

    rooms = get_rooms()

    if st.button(
        "＋ New Chat",
        use_container_width=True
    ):

        room = create_room(
            "New Chat"
        )

        st.session_state.current_room_id = (
            room["id"]
        )

        st.rerun()

    for room in rooms:

        is_current = (
            room["id"]
            == st.session_state.current_room_id
        )

        label = (
            "● "
            if is_current
            else "○ "
        )

        label += room["name"]

        if st.button(
            label,
            key=f"room_{room['id']}",
            use_container_width=True
        ):

            st.session_state.current_room_id = (
                room["id"]
            )

            st.rerun()

    # =====================================================
    # Room management
    # =====================================================

# =====================================================
# Room management
# =====================================================

    st.divider()

    st.subheader("⚙️ Current Chat")

    current_room = get_room(
        st.session_state.current_room_id
    )

    new_room_name = st.text_input(
        "Chat name",
        value=current_room["name"],
        key=f"room_name_input_{current_room['id']}"
    )

    if st.button(
        "💾 Save Name",
        use_container_width=True
    ):

        new_room_name = new_room_name.strip()

        if new_room_name:

            update_room(
                current_room["id"],
                name=new_room_name
            )

            st.rerun()

        else:

            st.warning(
                "Chat name cannot be empty."
            )


    if st.button(
        "🗑 Delete Chat",
        use_container_width=True
    ):

        delete_room(
            current_room["id"]
        )

        rooms = get_rooms()

        if rooms:

            st.session_state.current_room_id = (
                rooms[0]["id"]
            )

        else:

            room = create_room(
                "New Chat"
            )

            st.session_state.current_room_id = (
                room["id"]
            )

        st.rerun()
    # =====================================================
    # Documents
    # =====================================================

    st.divider()

    st.subheader("📚 Documents")

    documents = get_documents()

    if not documents:

        st.caption(
            "No documents yet."
        )

    for document in documents:

        col1, col2 = st.columns(
            [5, 1]
        )

        with col1:

            st.write(
                f"📄 {document['name']}"
            )

        with col2:

            if st.button(
                "🗑",
                key=f"delete_{document['id']}"
            ):

                delete_document(
                    document["id"]
                )

                remove_document_from_rooms(
                    document["id"]
                )

                st.rerun()

    # =====================================================
    # Upload document
    # =====================================================

    st.divider()

    st.subheader(
        "📤 Upload Document"
    )

    uploaded_file = st.file_uploader(
        "Choose PDF",
        type=["pdf"],
        key="document_uploader"
    )

    if uploaded_file is not None:

        if st.button(
            "Process Document",
            use_container_width=True
        ):

            try:

                with st.status(
                    "Processing document...",
                    expanded=True
                ):

                    # =====================================
                    # Save document
                    # =====================================

                    st.write(
                        "💾 Saving document..."
                    )

                    document = add_document(
                        uploaded_file.name,
                        uploaded_file.getbuffer()
                    )

                    # =====================================
                    # Load PDF
                    # =====================================

                    st.write(
                        "📖 Reading PDF..."
                    )

                    pages = load_pdf(
                        document["path"]
                    )

                    # =====================================
                    # Chunking
                    # =====================================

                    st.write(
                        "✂️ Creating chunks..."
                    )

                    all_chunks = []

                    for page in pages:

                        chunks = chunk_text(
                            page["text"]
                        )

                        for chunk in chunks:

                            all_chunks.append({
                                "page": page["page"],
                                "text": chunk
                            })

                    st.write(
                        f"{len(pages)} pages → "
                        f"{len(all_chunks)} chunks"
                    )

                    # =====================================
                    # Embedding
                    # =====================================

                    st.write(
                        "🧠 Creating embeddings..."
                    )

                    texts = [
                        chunk["text"]
                        for chunk in all_chunks
                    ]

                    embeddings = create_embeddings(
                        texts
                    )

                    st.write(
                        f"Embedding shape: "
                        f"{embeddings.shape}"
                    )

                    # =====================================
                    # Store
                    # =====================================

                    st.write(
                        "💾 Storing vectors..."
                    )

                    store_chunks(
                        document["id"],
                        all_chunks,
                        embeddings
                    )

                    # =====================================
                    # Add to current room
                    # =====================================

                    current_room = get_room(
                        st.session_state.current_room_id
                    )

                    document_ids = (
                        current_room["document_ids"]
                    )

                    if document["id"] not in document_ids:

                        document_ids.append(
                            document["id"]
                        )

                    set_room_documents(
                        current_room["id"],
                        document_ids
                    )

                    st.write(
                        "✅ Document ready!"
                    )

                st.success(
                    f"{uploaded_file.name} "
                    "is ready."
                )

                st.rerun()

            except Exception as error:

                st.error(
                    f"Failed to process document: "
                    f"{error}"
                )


# =========================================================
# Main UI
# =========================================================

current_room = get_room(
    st.session_state.current_room_id
)

st.title(
    f"💬 {current_room['name']}"
)

# =========================================================
# Current room documents
# =========================================================

documents = get_documents()

document_map = {
    document["id"]: document
    for document in documents
}

selected_documents = [
    document_map[doc_id]
    for doc_id in current_room["document_ids"]
    if doc_id in document_map
]

if selected_documents:

    st.caption(
        "📚 Using: "
        + ", ".join(
            document["name"]
            for document in selected_documents
        )
    )

else:

    st.warning(
        "No documents selected for this chat. "
        "Upload a document from the sidebar."
    )


# =========================================================
# Document selector
# =========================================================

if documents:

    with st.expander(
        "📚 Manage documents for this chat"
    ):

        selected_ids = st.multiselect(
            "Documents used by this chat",
            options=[
                document["id"]
                for document in documents
            ],
            default=[
                document["id"]
                for document in selected_documents
            ],
            format_func=lambda document_id:
                document_map[document_id]["name"]
        )

        if set(selected_ids) != set(
            current_room["document_ids"]
        ):

            set_room_documents(
                current_room["id"],
                selected_ids
            )

            st.rerun()


# =========================================================
# Display chat history
# =========================================================

for message in current_room["messages"]:

    with st.chat_message(
        message["role"]
    ):

        st.markdown(
            message["content"]
        )


# =========================================================
# Chat input
# =========================================================

question = st.chat_input(
    "Ask something about your documents..."
)


if question:

    # =====================================================
    # User message
    # =====================================================

    add_message(
        current_room["id"],
        "user",
        question
    )

    with st.chat_message("user"):

        st.markdown(
            question
        )

    # =====================================================
    # Check documents
    # =====================================================

    current_room = get_room(
        st.session_state.current_room_id
    )

    if not current_room["document_ids"]:

        answer = (
            "Please select at least one document "
            "for this chat."
        )

        with st.chat_message(
            "assistant"
        ):

            st.markdown(
                answer
            )

        add_message(
            current_room["id"],
            "assistant",
            answer
        )

    else:

        with st.chat_message(
            "assistant"
        ):

            # =============================================
            # Retrieval
            # =============================================

            with st.spinner(
                "Searching documents..."
            ):

                question_embedding = (
                    create_embeddings(
                        [question]
                    )[0]
                )

                retrieved_chunks = (
                    search_documents(
                        current_room["document_ids"],
                        question_embedding,
                        n_results=5
                    )
                )

            # =============================================
            # Context
            # =============================================

            context = "\n\n".join(
                chunk["text"]
                for chunk in retrieved_chunks
            )

            # =============================================
            # Conversation history
            # =============================================

            history = (
                current_room["messages"]
            )

            # =============================================
            # LLM
            # =============================================

            with st.spinner(
                "Thinking..."
            ):

                answer = ask_llm(
                    question,
                    context,
                    history
                )

            st.markdown(
                answer
            )

            # =============================================
            # Sources
            # =============================================

            if retrieved_chunks:

                st.divider()

                st.markdown(
                    "### 📚 Sources"
                )

                for i, chunk in enumerate(
                    retrieved_chunks,
                    start=1
                ):

                    document = document_map.get(
                        chunk["document_id"]
                    )

                    document_name = (
                        document["name"]
                        if document
                        else "Unknown document"
                    )

                    st.markdown(
                        f"**Source {i} · "
                        f"{document_name} · "
                        f"Page {chunk['page']}**"
                    )

                    snippet = (
                        get_relevant_snippet(
                            chunk["text"],
                            question
                        )
                    )

                    st.write(
                        snippet
                    )

                    with st.expander(
                        "Show full source"
                    ):

                        st.write(
                            chunk["text"]
                        )

                    st.divider()

            # =============================================
            # Save answer
            # =============================================

            add_message(
                current_room["id"],
                "assistant",
                answer
            )

            # Rerun so persistent chat state is reflected
            st.rerun()