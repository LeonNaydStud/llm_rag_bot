from langchain_core.prompts import ChatPromptTemplate
from app.services.vectorstore import get_vector_store
from app.services.llm import get_llm
from app.utils.text import truncate_text
from app.core.config import settings

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


def answer_question(question: str, top_k: int) -> str:
    vector_store = get_vector_store()
    llm = get_llm()

    docs = vector_store.similarity_search(question, k=top_k)

    context = "\n\n".join(
        f"Question: {d.metadata.get('question')}\nAnswer: {d.page_content}"
        for d in docs
    )

    context = truncate_text(context, settings.max_context_chars)

    prompt = PROMPT.format(question=question, context=context)
    response = llm.invoke(prompt)

    if hasattr(response, "content"):
        return response.content.strip()

    return str(response).strip()
