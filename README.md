# Student Self-Service Chatbot: Proof of Concept

This repository presents a **Proof of Concept (PoC)** for a chatbot designed to reduce the workload of Student Success Advisors by answering frequent student queries using **NLP**, **semantic search**, and **predictive classification**.

## Project Structure

Student Self-Service Chatbot/

├── data/  
│   ├── raw/                   # Original input data (PDFs, CSV)  
│   └── processed/             # Cleaned CSVs and vector pickles  
├── models/                   # Trained classifier, Label Encoder  
├── notebooks/                # Jupyter notebooks for building the chatbot backend  
│   ├── 01_scrapping.ipynb  
│   ├── 02_extract_FAQs_Resources.ipynb  
│   ├── 03_build_embeddings.ipynb  
│   └── 04_train_classifier.ipynb  
├── resources/                # Architecture diagrams and reference files  
├── src/                      # All backend source code  
│   ├── api.py                # FastAPI app for query prediction  
│   ├── chatbot_interface.py  # Streamlit frontend  
│   ├── retriever.py          # Embedding search, classification, LLM fallback  
│   ├── query_classifier.py   # PyTorch classifier for query type  
│   ├── embedding_hf.py       # SentenceTransformer encoder  
│   ├── models.py             # Classifier architecture (torch.nn)  
│   ├── openai_utils.py       # Support for OpenAI Chat API fallback  
│   └── test.py               # Unit testing logic  
├── docs/                     # GitHub Pages static site  
│   └── index.html            # HTML report for project presentation  
├── requirements.txt          # Python dependencies  
└── README.md                 # Project overview  

## 🧠 NLP Pipeline

- Text normalization: `ftfy`, `unicodedata`, `re` (used only for Word2Vec and GloVe)
- Lemmatization & tokenization: `spaCy` (only for Word2Vec and GloVe)
- Vectorization:
  - Word2Vec: Trained on local FAQs and resources
  - GloVe: Pre-trained (100d) from Stanford
  - HuggingFace Sentence Transformers (`all-MiniLM-L6-v2`): used as final model due to superior semantic understanding
- Query classification: `faq`, `resource`, `chitchat`, `offramp` (PyTorch classifier)

## 📚 Corpus Construction

- Extracted FAQs from Winter 2024 PDF documents
- Scraped student resources from Conestoga’s [Student Success Portal](https://successportal.conestogac.on.ca/)
- Combined into a unified semantic index using embeddings

## 🧠 Retrieval Logic (Retriever)

**This is the brain of the chatbot system, implemented in `src/retriever.py`:**

- Receives a student query and classifies it (`faq`, `resource`, `chitchat`, or `offramp`)
- Converts the query into an embedding vector using the selected model
- Compares it with all stored document vectors using cosine similarity
- If similarity is high (> 0.8), returns a matched result (even for `chitchat`)
- If similarity is low or the query is `offramp`, it falls back to a generative response using OpenAI


### 🔁 Why OpenAI?

Originally, the fallback LLM was implemented using `distilgpt2` from Hugging Face. However, due to random or less coherent completions, the fallback was replaced with the **OpenAI Chat API**, which provides more reliable and context-aware responses.

✅ This requires setting your OpenAI API key as an environment variable:

```bash
export OPENAI_API_KEY=your-key-here
```
(Use set on Windows or configure in .env if preferred.)


##  Demo Features
Ask natural language questions like:
"Hi my name is Paula"
"How can I pay my fees?"
"I need help creating my CV"
"My student status will expire"
"I need a human advisor, I am tired!" 

### Answers are returned with:
💬 Relevant info (answer or link)
📄 Source (FAQ or resource)
📈 Similarity score
🔁 Escalation fallback via LLM (if needed)

## Models Used
- Word2Vec: Trained on internal FAQs + resources
- GloVe: Pre-trained 100d vectors from Stanford NLP
- HuggingFace: all-MiniLM-L6-v2 for contextual sentence embeddings
- DistilGPT2: Used as LLM fallback for chitchat and low similarity (replaced by OpenAI)
- OpenAI Chat API: Used as fallback LLM for low-confidence or chitchat queries



## To Do
- Override chitchat classification if semantic similarity is very high
- Add user feedback option to flag incorrect answers
- Deploy to Streamlit Cloud or Render
- Add multilingual support
- Implement memory (context) for follow-up questions

## Authors
- Paula Ramirez 

##  **How to Run the Application**

### 1. Activate your virtual environment (PowerShell):
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process
.\venv\Scripts\activate
```
### 2. Run the FastAPI backend:
```powershell
streamlit run src/chatbot_interface.py --server.port 8501
```
### 3. Launch the Streamlit chatbot interface:
```powershell
streamlit run src/chatbot_interface.py --server.port 8501
```

