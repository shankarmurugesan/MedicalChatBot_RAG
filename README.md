# BioMistral Medical Chatbot

This project is a medical chatbot built using LangChain, Mistral-7B, and Gradio. It allows users to ask healthcare or biology-related queries and get accurate responses.

## Workflow

```mermaid
graph TD;
    A[Start] --> B[Load PDF Documents];
    B --> C[Split Documents into Chunks];
    C --> D[Generate Embeddings];
    D --> E[Create Vector Store];
    E --> F[Initialize LLM];
    F --> G[Create Retrieval Chain];
    G --> H[Define Gradio Interface];
    H --> I[Deploy to Hugging Face Spaces];
    I --> J[End];

### Explanation of the Diagram

1. **Start**: The process begins.
2. **Load PDF Documents**: Use `PyPDFDirectoryLoader` to load PDF files from a directory.
3. **Split Documents into Chunks**: Use `RecursiveCharacterTextSplitter` to split documents into smaller chunks.
4. **Generate Embeddings**: Use `SentenceTransformerEmbeddings` to generate embeddings for the text chunks.
5. **Create Vector Store**: Use `Chroma` to create a vector store from the embeddings.
6. **Initialize LLM (LlamaCpp)**: Load the Mistral-7B model using `LlamaCpp`.
7. **Create Retrieval Chain**: Combine the retriever, prompt template, LLM, and output parser into a retrieval chain.
8. **Define Gradio Interface**: Create a Gradio interface for user interaction.
9. **Deploy to Hugging Face Spaces**: Push the code to Hugging Face Spaces for deployment.
10. **End**: The process completes.
