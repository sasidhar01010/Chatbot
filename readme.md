# **RAG Workflow with Self-Reflection**  
*A Streamlit Application for Document-Based Question Answering*

This project leverages **Retrieval-Augmented Generation (RAG)** with **Self-Reflection** to provide precise answers to user queries based on document content. It combines the power of OpenAI's models with a streamlined workflow to retrieve relevant document chunks, generate insightful responses, and continually refine accuracy.

---

## **Getting Started**

### **Prerequisites**
- Python 3.7 or higher  
- An OpenAI API Key  

---

## **Installation Guide**

### **Step 1: Install Required Packages**  
Run the following command to install the dependencies:

```bash
pip install -r requirements.txt
```

### **Step 2: Configure API Key**  
Update the `.env` file with your OpenAI API key:

```plaintext
OPENAI_API_KEY = "your-openai-api-key"
```

---

## **How to Use**

1. **Launch the Application**  
   Start the Streamlit app by running:

   ```bash
   streamlit run app.py
   ```

2. **Access the Interface**  
   Open your browser and navigate to:  
   **[http://localhost:8501](http://localhost:8501)**

3. **Ask Your Questions**  
   - Upload a document.
   - Enter a query in the input field.
   - Click **"Get Answer"** to receive a response.

---

## **Project Overview**

### **Key Features**  
- **Document Upload**: Easily upload and process documents for analysis.  
- **Relevant Information Retrieval**: Extracts document chunks pertinent to your query.  
- **AI-Powered Responses**: Leverages OpenAI's API to generate high-quality, grounded answers.  
- **Self-Reflection**: Ensures accuracy and relevance in response generation.

---

## **File Structure**

| **File/Folder**         | **Description**                                              |
|--------------------------|--------------------------------------------------------------|
| `app.py`                | Main Streamlit application file.                             |
| `document_processing.py` | Functions for document parsing and processing.               |
| `main.py`               | Core workflow logic for RAG.                                 |
| `nodes.py`              | Definitions for processing nodes in the workflow.            |
| `pdf_utils.py`          | Utility functions for handling PDF files.                    |
| `prompts.py`            | Templates for generating query prompts in the RAG workflow.  |
| `vectorstore.py`        | Vector store management for document retrieval.              |
| `workflow.py`           | End-to-end RAG workflow implementation.                      |
| `.env`                  | Environment variables (includes OpenAI API key).             |
| `requirements.txt`      | List of all required Python packages.                        |
| `readme.md`             | Project documentation.                                       |

---

## **Usage Workflow**

1. **Document Chunking**  
   Breaks down documents into manageable pieces for vector-based search.

2. **Vector Retrieval**  
   Leverages vector stores to retrieve document sections relevant to user queries.

3. **Prompt Engineering**  
   Constructs prompts using retrieved chunks to maximize answer quality.

4. **Answer Generation**  
   Uses OpenAI's API to craft precise and contextually relevant answers.

5. **Self-Reflection**  
   Evaluates responses to refine accuracy and improve relevance.

---

## **Future Enhancements**
- Support for additional file types (e.g., Word, Excel).  
- Advanced analytics to provide insights into user queries.  
- Integration with alternative vector databases for improved scalability.  

Elevate your document-based question-answering experience with **RAG + Self-Reflection**. 🚀