# Import necessary modules and libraries
from langchain.embeddings.openai import OpenAIEmbeddings  # Import the OpenAI embeddings
from langchain.vectorstores import FAISS  # Import the FAISS vector store for storing and retrieving vectors efficiently
from langchain.chat_models import ChatOpenAI  # Import the ChatOpenAI model for generating responses
from langchain.chains import LLMChain  # Import the LLMChain to manage the processing flow
from dotenv import find_dotenv, load_dotenv  # Import dotenv for managing environment variables
# Import classes for handling prompts and messages
from langchain.prompts.chat import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
)
from langchain.text_splitter import RecursiveCharacterTextSplitter, PythonCodeTextSplitter
import textwrap  # Import textwrap for formatting the text output

# Load environment variables from the .env file
load_dotenv(find_dotenv())
# Initialize the OpenAI embeddings
embeddings = OpenAIEmbeddings()

# Function to create the vector database using text
def database(text):
    # Instantiate a PythonCodeTextSplitter with specific chunk size and overlap
    text_splitter = PythonCodeTextSplitter(chunk_size=1000, chunk_overlap=100)
    # Split the text into 'documents' or chunks
    docs = text_splitter.create_documents(text)
    # Generate the FAISS database from these documents using the OpenAI embeddings
    db = FAISS.from_documents(docs, embeddings)
    return db  # Return the database

# Function to get response from a query using a vector database
def get_response_from_query(db, query, k=4):
    # Search for similar documents in the database
    docs = db.similarity_search(query, k=k)
    # Collect the content of the documents
    docs_page_content = " ".join([d.page_content for d in docs])

    # Initialize a ChatOpenAI instance with a specific model and temperature
    chat = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0.2)

    # Define the system message prompt template
    template = """
        You are a helpful assistant that that can answer questions about Products on Home Depot 
        based on the production information: {docs}
        
        Only use the factual information from the transcript to answer the question.
        
        If you feel like you don't have enough information to answer the question, say "I don't know".
        """
    # Create a system message prompt from the template
    system_message_prompt = SystemMessagePromptTemplate.from_template(template)

    # Define the human question prompt template
    human_template = "Answer the following question: {question}"
    # Create a human message prompt from the template
    human_message_prompt = HumanMessagePromptTemplate.from_template(human_template)

    # Create a chat prompt template from the system and human message prompts
    chat_prompt = ChatPromptTemplate.from_messages(
        [system_message_prompt, human_message_prompt]
    )

    # Initialize the LLMChain with the chat model and the chat prompt
    chain = LLMChain(llm=chat, prompt=chat_prompt)

    # Run the chain to get a response to the query
    response = chain.run(question=query, docs=docs_page_content)
    # Clean up the response by replacing line breaks
    response = response.replace("\n", "")
    return response, docs  # Return the response and the documents

# Function to generate an answer to a query using a text database
def answer(text, query):
    # Create the database from the text
    db = database(text)
    response, docs = get_response_from_query(db, query)
    return (textwrap.fill(response))


