from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from models import load_chat_model, load_embedding_model
from utils import get_transcript, format_docs

from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_core.runnables import (
    RunnablePassthrough,
    RunnableParallel,
    RunnableLambda
)
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # allow all origins (fine for development)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

#  Load models only once
chat_llm = load_chat_model()
embeddings = load_embedding_model()

#  Define PromptTemplate directly
template = PromptTemplate(
    template="""
        You are a helpful assistant.
        Answer ONLY from the provided transcript context.
        If the context is insufficient, just say you don't know.

        Context:
        {context}

        Question:
        {question}
        """,
    input_variables=["context", "question"]
)


class VideoRequest(BaseModel):
    video_id: str
    question: str


@app.post("/summarize")
def summarize_video(request: VideoRequest):

    transcript = get_transcript(request.video_id)

    chunks = RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=150
    ).create_documents([transcript])

    vector_store = FAISS.from_documents(chunks, embeddings)

    retriever = vector_store.as_retriever(
        search_type="similarity",
        search_kwargs={"k": 4}
    )

    parallel_chain = RunnableParallel({
        "context": retriever | RunnableLambda(format_docs),
        "question": RunnablePassthrough()
    })

    chain = parallel_chain | template | chat_llm | StrOutputParser()

    result = chain.invoke(request.question)

    return {"summary": result}