from langchain.document_loaders import TextLoader
from langchain.vectorstores import FAISS
from langchain.chains import RetrievalQA
from langchain.document_loaders import TextLoader
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.llms import OpenAI
from langchain.chains.summarize import load_summarize_chain
from langchain.text_splitter import RecursiveCharacterTextSplitter, PythonCodeTextSplitter
from scraper import get_information
from dotenv import find_dotenv, load_dotenv
load_dotenv(find_dotenv())
from langchain.prompts.chat import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
)


llm = OpenAI(temperature=0.9)

#print(llm(text))

first = 0
def function1(question, text):
    global first
    if first == 0:
        first = 1

        template = "You are an informed product assistant that provides detailed information about products available in Home Depot. " +\
                   "Your goal is to help the user quickly understand product specifications, uses, installation instructions, and compatibility " +\
                   "by providing concise and accurate information. Ensure you keep your explanations brief yet comprehensive. Simplify titles " +\
                   "and other information to make it user-friendly."

        qa.run(template)
        return "Hi! How can I help you?"

    text_splitter = PythonCodeTextSplitter(chunk_size=4000, chunk_overlap=300)
    docs = text_splitter.create_documents([text])
    embeddings = OpenAIEmbeddings()

    docsearch = FAISS.from_documents(docs, embeddings)
    qa = RetrievalQA.from_chain_type(llm=llm, chain_type="stuff", retriever=docsearch.as_retriever())
    query = question

    analysis = qa.run(query)
    return analysis.translate(str.maketrans("", "", "_*"))


