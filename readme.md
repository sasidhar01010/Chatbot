# 🧠 Self-Reflective RAG with LangGraph & Streamlit

An intelligent **Question-Answering system with self-correction**.  
Unlike standard RAG (Retrieval-Augmented Generation) pipelines, this system **evaluates its own retrievals and answers**. If the retrieved documents are irrelevant or the generated answer is a hallucination, the system **automatically rewrites the query and retries**.

Built using **LangChain**, **LangGraph**, **ChromaDB**, and **Streamlit**.

---

# 🚀 Key Features

- 🔁 **Self-Reflection Loop**  
  Detects hallucinations or irrelevant context and retries automatically.

- ✍️ **Query Transformation**  
  Rewrites user queries to improve document retrieval quality.

- 📊 **Relevance Grading**  
  Uses an LLM to judge whether retrieved documents are relevant to the query.

- 🧪 **Hallucination Detection**  
  Verifies that the generated answer is grounded in retrieved documents.

- 🖥️ **Interactive Streamlit UI**  
  Displays answers along with the system’s internal reasoning flow.

---

## 🛠️ Architecture

The system follows a **cyclic graph workflow** implemented using **LangGraph**:

```mermaid
graph TD
    A[Start] --> B[Retrieve Documents]
    B --> C{Grade Documents}
    C -- Relevant --> D[Generate Answer]
    C -- Irrelevant --> E[Transform Query]
    E --> B
    D --> F{Check Hallucination}
    F -- Grounded & Useful --> G[End / Show Answer]
    F -- Hallucinated / Not Useful --> E
````

### Workflow Steps

1. **Retrieve** – Fetches documents using vector search
2. **Grade** – Checks if documents are relevant
3. **Transform** – Rewrites the query if retrieval is poor
4. **Generate** – Produces an answer using grounded context
5. **Verify** – Confirms the answer is factual and useful

---

## 📋 Prerequisites

* Python **3.9+**
* An **OpenAI API Key**

---

## 📦 Installation

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/yourusername/self-reflective-rag.git
cd self-reflective-rag
```

### 2️⃣ Create a Virtual Environment (Recommended)

```bash
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
```

### 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

---

## ⚙️ Configuration

### 🔑 Environment Variables

Create a `.env` file in the root directory:

```env
OPENAI_API_KEY=sk-your-openai-api-key
```

### 📄 Add Your Data

* Place the PDF you want to chat with in the root directory
* Rename it to **`input.pdf`**
* The system will automatically ingest and index it on first run

---

## 🏃‍♂️ Usage

Run the Streamlit app:

```bash
streamlit run app.py
```

Access the UI at:

```
http://localhost:8501
```

---

## 📂 Project Structure

```text
├── app.py                 # Streamlit UI entry point
├── main_app.py            # Workflow initialization & orchestration
├── workflow_manager.py    # LangGraph workflow definition
├── workflow_nodes.py      # Core logic (Retrieve, Generate, Grade)
├── prompt_templates.py    # LLM prompts for grading & rewriting
├── pdf_handler.py         # PDF text extraction
├── text_processing.py     # Chunking & preprocessing logic
├── vector_store.py        # ChromaDB setup and retrieval
├── .env                   # API keys (not committed)
├── input.pdf              # Source document
└── requirements.txt       # Dependencies
```

---

## 🔧 Customization

* **Model Selection**
  Change the model (e.g., GPT-4) in `prompt_templates.py`

* **Chunk Size**
  Modify `chunk_size` in `text_processing.py` (default: 250)

* **Retry Limit**
  Adjust `recursion_limit` in `app.py` (default: 15)

