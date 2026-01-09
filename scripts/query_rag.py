from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings, HuggingFacePipeline
from langchain_core.prompts import ChatPromptTemplate
from transformers import pipeline
import textwrap

EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
LLM_MODEL = "google/flan-t5-base"

def load_vector_store():
    embeddings = HuggingFaceEmbeddings(
        model_name=EMBEDDING_MODEL,
        encode_kwargs={"normalize_embeddings": True},
    )

    return Chroma(
        collection_name="python_faq",
        embedding_function=embeddings,
        persist_directory="./chroma_db",
    )


def load_llm():
    pipe = pipeline(
        "text2text-generation",
        model=LLM_MODEL,
        max_new_tokens=200,
        truncation=True,
    )
    return HuggingFacePipeline(pipeline=pipe)

def truncate_text(text, max_chars=1800):
    if len(text) > max_chars:
        return text[:max_chars] + "\n[context truncated]"
    return text


PROMPT = ChatPromptTemplate.from_template(
    """You are a Python expert.
Answer the question using only the context below.
If the answer is not present, say that the information is not available.

Context:
{context}

Question:
{question}

Answer:"""
)


def ask_question(question, k=3):
    vector_store = load_vector_store()
    llm = load_llm()

    docs = vector_store.similarity_search(question, k=k)
    context = truncate_text(context)

    context = "\n\n".join(
        f"Question: {d.metadata.get('question')}\nAnswer: {d.page_content}"
        for d in docs
    )
    
    context = truncate_text(context)

    prompt = PROMPT.format(question=question, context=context)
    response = llm.invoke(prompt)

    if hasattr(response, "content"):
        return response.content.strip()

    return str(response).strip()


def format_output(text, width=80):
    return "\n".join(textwrap.wrap(text, width))


if __name__ == "__main__":
    print("Python FAQ RAG system")
    print("=" * 60)

    while True:
        try:
            q = input("Question (or 'exit'): ").strip()
            if q.lower() in {"exit", "quit"}:
                break

            answer = ask_question(q)
            print("\nAnswer:")
            print(format_output(answer))
            print("-" * 60)

        except KeyboardInterrupt:
            break
