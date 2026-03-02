from langchain_huggingface import HuggingFaceEndpoint, ChatHuggingFace
from langchain_huggingface import HuggingFaceEmbeddings
from dotenv import load_dotenv

load_dotenv()

def load_chat_model():
    llm = HuggingFaceEndpoint(
        repo_id="HuggingFaceH4/zephyr-7b-beta",
        task="text-generation",
        temperature=0.7,
        max_new_tokens=100,
    )
    model = ChatHuggingFace(llm=llm)
    return model

# checking model working
# model = load_chat_model()
# print(model.invoke("what is the capital of india").content)

def load_embedding_model():
    embeddings = HuggingFaceEmbeddings(
        model_name="BAAI/bge-base-en-v1.5"
    )
    return embeddings

# testing...
# embeddings = load_embedding_model()
# print(len(embeddings.embed_query("hello World")))
