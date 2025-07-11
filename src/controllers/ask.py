# 💬 Ask questions to the LLM


def format_response(result, docs):
    sources = []
    for doc in docs[:3]:
        sources.append(
            {
                "text": doc.page_content[:300] + "...",
                "source": doc.metadata.get("filename", "Unknown"),
            }
        )

    return {"answer": result, "citations": sources}


def ask_question(query, retriever, qa_pipeline):

    # Retrieve relevant documents
    docs = retriever.get_relevant_documents(query)
    context = "\n\n".join([doc.page_content for doc in docs[:3]])

    # Build prompt for the local model
    prompt = f"Answer the question based on the context:\n\nContext: {context}\n\nQuestion: {query}"

    # Run the QA pipeline (e.g., HuggingFace Transformers model)
    result = qa_pipeline(prompt, max_new_tokens=200)[0]["generated_text"]

    # Format and return the response
    return format_response(result, docs)
