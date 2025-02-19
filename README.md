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

