# 🤖 AIDocChat

A local AI-powered document assistant that allows users to upload PDF documents, ask questions about their contents, and receive answers using Retrieval-Augmented Generation (RAG).

AIDocChat runs locally using **Ollama** for the language model and **ChromaDB** for vector storage.

---

## 📸 Screenshot

<img width="1920" height="1080" alt="image" src="https://github.com/user-attachments/assets/15be34b3-1dc2-4dfa-b809-024e76c35ca7" />

---

## ✨ Features

* 📄 Upload and process PDF documents directly from the UI
* 🧠 Automatic text chunking and embedding
* 🔎 Semantic document retrieval using ChromaDB
* 💬 Chat with documents using a local LLM
* 🤖 Powered by Ollama
* 📚 Multiple PDF documents
* 💬 Multiple persistent chat rooms
* 🔗 Use multiple documents within a single chat room
* 🗑️ Delete documents and their associated vector data
* 💾 Persistent documents and chat history
* 🌍 Multilingual embedding support
* 📖 Source references with page numbers
* 🔍 Relevant source snippets for retrieved context
* 🔒 Fully local processing with no external LLM API required

---

## 🧠 How It Works

AIDocChat uses a Retrieval-Augmented Generation (RAG) pipeline.

```text
                    ┌──────────────┐
                    │  PDF Upload  │
                    └──────┬───────┘
                           │
                           ▼
                    ┌──────────────┐
                    │ PDF Loader   │
                    └──────┬───────┘
                           │
                           ▼
                    ┌──────────────┐
                    │  Chunking    │
                    └──────┬───────┘
                           │
                           ▼
                  ┌──────────────────┐
                  │ Sentence         │
                  │ Transformer      │
                  │ Embeddings       │
                  └────────┬─────────┘
                           │
                           ▼
                    ┌──────────────┐
                    │  ChromaDB     │
                    └──────┬───────┘
                           │
                           │
                    User Question
                           │
                           ▼
                  ┌──────────────────┐
                  │ Question         │
                  │ Embedding        │
                  └────────┬─────────┘
                           │
                           ▼
                    ┌──────────────┐
                    │  Retrieval   │
                    └──────┬───────┘
                           │
                    Relevant Chunks
                           │
                           ▼
                  ┌──────────────────┐
                  │     Ollama       │
                  │  Qwen3 4B       │
                  └────────┬─────────┘
                           │
                           ▼
                    ┌──────────────┐
                    │ AI Response  │
                    └──────────────┘
```

---

## 🏗️ Architecture

AIDocChat separates documents from chat rooms.

```text
Document
│
├── PDF file
└── Embeddings
      │
      ├──────────────┐
      ▼              ▼
   Chat Room A    Chat Room B
      │              │
   Messages       Messages
```

This allows the same document to be reused across multiple chat rooms without embedding the document again.

### Document Storage

Documents are stored persistently in:

```text
data/
├── uploads/
└── documents.json
```

### Chat Room Storage

Chat rooms and their message history are stored in:

```text
data/rooms.json
```

### Vector Storage

Each document has its own ChromaDB collection:

```text
database/chroma/
├── doc_<document_id>
├── doc_<document_id>
└── ...
```

Deleting a document also removes its associated ChromaDB collection.

---

## 🛠️ Tech Stack

| Technology            | Purpose             |
| --------------------- | ------------------- |
| Python                | Core application    |
| Streamlit             | Web UI              |
| Sentence Transformers | Text embeddings     |
| ChromaDB              | Vector database     |
| Ollama                | Local LLM inference |
| Qwen3 4B Instruct     | Language model      |
| PyPDF / PDF loader    | PDF text extraction |

### Embedding Model

```text
paraphrase-multilingual-MiniLM-L12-v2
```

The multilingual embedding model allows the retrieval pipeline to work across multiple languages.

### LLM

```text
qwen3:4b-instruct
```

The LLM runs locally through Ollama.

---

## 📁 Project Structure

```text
AIDocChat/
│
├── app.py
│
├── data/
│   ├── uploads/
│   ├── documents.json
│   └── rooms.json
│
├── database/
│   └── chroma/
│
├── src/
│   ├── chat.py
│   ├── chunker.py
│   ├── document_manager.py
│   ├── embedder.py
│   ├── llm.py
│   ├── pdf_loader.py
│   ├── query_rewriter.py
│   ├── retriever.py
│   ├── room_manager.py
│   └── vector_db.py
│
├── requirements.txt
└── README.md
```

---

## 🚀 Getting Started

### 1. Clone the repository

```bash
git clone <YOUR_REPOSITORY_URL>
cd AIDocChat
```

### 2. Create a virtual environment

Linux / WSL:

```bash
python3 -m venv venv
source venv/bin/activate
```

Windows:

```powershell
python -m venv venv
venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Install Ollama

Install Ollama and make sure the required model is available:

```bash
ollama pull qwen3:4b-instruct
```

Verify that Ollama is running:

```bash
ollama list
```

### 5. Run the application

```bash
streamlit run app.py
```

The application will be available at:

```text
http://localhost:8501
```

---

## 💬 Usage

### Upload a document

1. Open AIDocChat.
2. Go to **Upload Document** in the sidebar.
3. Select a PDF.
4. Click **Process Document**.
5. Wait until the document has been embedded and stored.

### Create a chat

Click:

```text
＋ New Chat
```

A chat room can contain one or multiple documents.

### Ask questions

Type a question in the chat input.

AIDocChat will:

1. Convert the question into an embedding.
2. Search the selected documents.
3. Retrieve the most relevant chunks.
4. Send the retrieved context to the local LLM.
5. Generate an answer based on the retrieved document context.
6. Display the relevant source pages.

---

## 📚 Source References

Retrieved sources are displayed below the generated answer.

Each source includes:

```text
Source
Document
Page
Relevant snippet
```

The full retrieved chunk can also be expanded when needed.

This provides transparency into which parts of the document were used to generate the answer.

---

## 💾 Persistence

AIDocChat uses persistent local storage.

Restarting Streamlit does **not** delete:

* Uploaded PDFs
* Document metadata
* ChromaDB embeddings
* Chat rooms
* Chat history

The stored data remains available the next time the application is started.

---

## 🔐 Privacy

AIDocChat is designed to run locally.

Documents are processed locally and the LLM runs through Ollama.

No external LLM API is required for the core RAG pipeline.

> Users are responsible for securing the local machine and any documents stored by the application.

---

## ⚠️ Current Limitations

* PDF text extraction quality depends on the source PDF.
* Scanned/image-only PDFs may require OCR support.
* Retrieval quality depends on chunking and embedding quality.
* Very large document collections may require additional retrieval optimization.
* Chat history is currently stored locally as JSON.
* The application is currently designed as a local/single-user application.

---

## 🗺️ Roadmap

Potential future improvements:

* [ ] OCR support for scanned PDFs
* [ ] Streaming LLM responses
* [ ] Better semantic reranking
* [ ] Citation highlighting inside document text
* [ ] PDF preview
* [ ] Drag-and-drop document management
* [ ] Export conversations
* [ ] Authentication and multi-user support
* [ ] Improved document metadata
* [ ] Retrieval evaluation and benchmarking

---

## 📌 Project Status

**Status: MVP Complete**

The current version demonstrates a complete local RAG workflow:

```text
PDF
 ↓
Text Extraction
 ↓
Chunking
 ↓
Multilingual Embeddings
 ↓
ChromaDB
 ↓
Semantic Retrieval
 ↓
Ollama / Qwen3
 ↓
Answer + Sources
```

---

## 👨‍💻 Author

**Diva**
[https://github.com/DivaSatriaa]

Developed as a personal AI/RAG project to explore local document
question-answering systems, vector databases, embeddings, and LLM integration.
