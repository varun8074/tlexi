import os
from langchain_community.document_loaders import PyPDFLoader, Docx2txtLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import FAISS
from transformers import pipeline


# 📄 Load and chunk PDF + DOCX files
def load_documents(folder_path):
    documents = []
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        if filename.endswith(".pdf"):
            loader = PyPDFLoader(file_path)
        elif filename.endswith(".docx"):
            loader = Docx2txtLoader(file_path)
        else:
            continue

        try:
            file_docs = loader.load()
            for i, doc in enumerate(file_docs):
                doc.metadata["filename"] = filename
                doc.metadata["chunk_id"] = i
            documents.extend(file_docs)
        except Exception as e:
            print(f"❌ Failed to load {filename}: {e}")

    return documents

def split_documents(documents):
    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100)
    return splitter.split_documents(documents)

# 🧠 Create and save FAISS vectorstore
def create_faiss_vectorstore(docs):
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    vectorstore = FAISS.from_documents(docs, embeddings)
    vectorstore.save_local("faiss_index")
    print("✅ FAISS index created and saved.")
    return vectorstore

# 📦 Load FAISS index if it exists
def load_vectorstore():
    index_path = "faiss_index/index.faiss"
    if not os.path.exists(index_path):
        raise FileNotFoundError("❌ FAISS index not found. Run the index creation first.")
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    return FAISS.load_local("faiss_index", embeddings, allow_dangerous_deserialization=True)


# 🏁 Entry point
import os
from transformers import pipeline

def downloader():
    pdf_folder = "src/pdfs"

    if not os.path.exists(pdf_folder) or len(os.listdir(pdf_folder)) == 0:
        return "❌ Please add at least one PDF file in the 'pdfs/' folder."

    try:
        if not os.path.exists(os.path.join("faiss_index")) or \
           not os.path.exists(os.path.join("faiss_index", "index.faiss")):

            print("📂 FAISS index not found. Creating one from PDFs...")
            raw_docs = load_documents(pdf_folder)
            docs = split_documents(raw_docs)
            vectorstore = create_faiss_vectorstore(docs)

        else:
            print("📦 Loading existing FAISS index...")
            vectorstore = load_vectorstore()

        print("🔁 Using local Hugging Face model (flan-t5-base)...")
        qa_pipeline = pipeline("text2text-generation", model="google/flan-t5-base")

        retriever = vectorstore.as_retriever()

        return retriever, qa_pipeline

    except Exception as e:
        return f"⚠️ Error occurred: {str(e)}"


    
