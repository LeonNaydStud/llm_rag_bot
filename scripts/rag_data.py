import os
import requests
from bs4 import BeautifulSoup
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings

os.environ["USER_AGENT"] = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/120.0 Safari/537.36"
)

FAQ_URLS = [
    "https://docs.python.org/3/faq/general.html",
    "https://docs.python.org/3/faq/programming.html",
]

def load_faq_pages(urls):
    documents = []

    for url in urls:
        response = requests.get(url, timeout=15)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")
        content = soup.find("div", {"role": "main"})
        if content is None:
            continue

        current_question = None
        current_answer_parts = []

        for tag in content.find_all(["h2", "h3", "p", "ul", "ol"]):
            if tag.name in ["h2", "h3"]:
                if current_question and current_answer_parts:
                    answer_text = "\n".join(current_answer_parts).strip()
                    if len(answer_text) > 200:
                        documents.append(
                            Document(
                                page_content=answer_text,
                                metadata={
                                    "question": current_question,
                                    "source": url,
                                },
                            )
                        )
                current_question = tag.get_text(strip=True)
                current_answer_parts = []

            else:
                text = tag.get_text(" ", strip=True)
                if text:
                    current_answer_parts.append(text)

        if current_question and current_answer_parts:
            answer_text = "\n".join(current_answer_parts).strip()
            if len(answer_text) > 200:
                documents.append(
                    Document(
                        page_content=answer_text,
                        metadata={
                            "question": current_question,
                            "source": url,
                        },
                    )
                )

    return documents


def main():
    print("Loading Python FAQ pages...")
    docs = load_faq_pages(FAQ_URLS)
    print(f"Extracted FAQ entries: {len(docs)}")

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=100,
        separators=["\n\n", "\n", " ", ""],
    )

    chunks = splitter.split_documents(docs)
    print(f"Chunks after splitting: {len(chunks)}")

    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2",
        encode_kwargs={"normalize_embeddings": True},
    )

    Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        collection_name="python_faq",
        persist_directory="./chroma_db",
    )

    print("Vector store successfully created")


if __name__ == "__main__":
    main()
