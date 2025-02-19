from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import SentenceTransformerEmbeddings
from langchain.vectorstores import Chroma
from langchain_community.llms import LlamaCpp
from langchain.chains import RetrievalQA
from langchain.schema.runnable import RunnablePassthrough
from langchain.schema.output_parser import StrOutputParser
from langchain.prompts import ChatPromptTemplate
import gradio as gr
import os

# Set Hugging Face API token (if needed)
os.environ['HUGGINGFACEHUB_API_TOKEN'] = "yourkey"

# Load documents from a directory
loader = PyPDFDirectoryLoader("/content/drive/MyDrive/HealthCareData/")
docs = loader.load()

# Split documents into chunks
text_splitter = RecursiveCharacterTextSplitter(chunk_size=300, chunk_overlap=50)
chunks = text_splitter.split_documents(docs)

# Create embeddings and vector store
embeddings = SentenceTransformerEmbeddings(model_name="NeuML/pubmedbert-base-embeddings")
vectorstore = Chroma.from_documents(chunks, embeddings)

# Create a retriever
retriever = vectorstore.as_retriever(search_kwargs={'k': 5})

# Load the LLM (LlamaCpp)
llm = LlamaCpp(
    model_path='/content/drive/MyDrive/HealthCareData/mistral-7b-instruct-v0.1.Q6_K.gguf',
    temperature=0.2,
    max_tokens=2048,
    top_p=1
)

# Define the prompt template
template = """
You are a Medical Assistant that follows the instructions and generates accurate responses based on the query and the context provided. Please be truthful and give direct answers.

{query}
"""

prompt = ChatPromptTemplate.from_template(template)

# Create the retrieval chain
retrieval_chain = (
    {"context": retriever, "query": RunnablePassthrough()}
    | prompt
    | llm
    | StrOutputParser()
)

# Define the chat function for Gradio
def chat(user_input):
    if user_input.lower() == 'exit':
        return "Exiting..."
    if not user_input.strip():
        return "Please enter a valid query."
    result = retrieval_chain.invoke(user_input)
    return result

# Create Gradio interface with improved design
iface = gr.Interface(
    fn=chat,
    inputs=gr.Textbox(label="Your Query", placeholder="Type your question here...", lines=2),
    outputs=gr.Textbox(label="Response"),
    title="🩺 BioMistral Medical Chatbot",
    description="🤖 Ask me any healthcare or biology-related queries!",
    theme="soft",
    live=True,
    css="""
        body {
            background-color: #f0f4f8;
            color: #333;
        }
        .gradio-container {
            border-radius: 12px;
            box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.1);
            background: #ffffff;
            padding: 20px;
        }
        input, textarea {
            border-radius: 8px;
            border: 1px solid #ddd;
            padding: 10px;
        }
        button {
            background-color: #007bff;
            color: white;
            border-radius: 8px;
            padding: 10px 15px;
            border: none;
            transition: 0.3s;
        }
        button:hover {
            background-color: #0056b3;
        }
    """
)

# Launch the Gradio app
iface.launch()
