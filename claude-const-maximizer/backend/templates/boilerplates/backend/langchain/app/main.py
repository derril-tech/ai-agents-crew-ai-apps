from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
import os
from dotenv import load_dotenv

# LangChain imports
from langchain.chat_models import ChatOpenAI
from langchain.llms import OpenAI
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Pinecone
from langchain.chains import LLMChain, ConversationalRetrievalChain
from langchain.prompts import PromptTemplate
from langchain.memory import ConversationBufferMemory
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.document_loaders import PyPDFLoader, TextLoader
import pinecone

load_dotenv()

app = FastAPI(title="LangChain AI API", version="1.0.0")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize LangChain components
llm = ChatOpenAI(
    temperature=0.7,
    model_name="gpt-4",
    openai_api_key=os.getenv("OPENAI_API_KEY")
)

embeddings = OpenAIEmbeddings(
    openai_api_key=os.getenv("OPENAI_API_KEY")
)

# Initialize Pinecone
pinecone.init(
    api_key=os.getenv("PINECONE_API_KEY"),
    environment=os.getenv("PINECONE_ENVIRONMENT")
)

# Pydantic models
class ChatRequest(BaseModel):
    message: str
    conversation_id: Optional[str] = None
    context: Optional[str] = None

class ChatResponse(BaseModel):
    response: str
    conversation_id: str
    sources: Optional[List[str]] = None

class DocumentUpload(BaseModel):
    content: str
    metadata: Optional[Dict[str, Any]] = None

class RAGRequest(BaseModel):
    question: str
    top_k: int = 5

# Memory storage for conversations
conversation_memories: Dict[str, ConversationBufferMemory] = {}

@app.get("/")
async def root():
    return {"message": "LangChain AI API is running"}

@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """Simple chat endpoint with conversation memory"""
    try:
        # Get or create conversation memory
        if request.conversation_id not in conversation_memories:
            conversation_memories[request.conversation_id] = ConversationBufferMemory(
                memory_key="chat_history",
                return_messages=True
            )
        
        memory = conversation_memories[request.conversation_id]
        
        # Create conversation chain
        conversation_chain = ConversationalRetrievalChain.from_llm(
            llm=llm,
            memory=memory,
            return_source_documents=True
        )
        
        # Generate response
        result = conversation_chain({"question": request.message})
        
        return ChatResponse(
            response=result["answer"],
            conversation_id=request.conversation_id,
            sources=[doc.metadata.get("source", "") for doc in result.get("source_documents", [])]
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/rag/query", response_model=ChatResponse)
async def rag_query(request: RAGRequest):
    """RAG query endpoint using vector database"""
    try:
        # Get vector store
        index_name = os.getenv("PINECONE_INDEX_NAME", "default-index")
        vectorstore = Pinecone.from_existing_index(
            index_name=index_name,
            embedding=embeddings
        )
        
        # Create retrieval chain
        qa_chain = ConversationalRetrievalChain.from_llm(
            llm=llm,
            retriever=vectorstore.as_retriever(search_kwargs={"k": request.top_k}),
            return_source_documents=True
        )
        
        # Query
        result = qa_chain({"question": request.question})
        
        return ChatResponse(
            response=result["answer"],
            conversation_id="rag_session",
            sources=[doc.metadata.get("source", "") for doc in result.get("source_documents", [])]
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/rag/upload")
async def upload_document(document: DocumentUpload):
    """Upload document to vector database"""
    try:
        # Text splitter
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200
        )
        
        # Split text
        texts = text_splitter.split_text(document.content)
        
        # Create embeddings and store in Pinecone
        index_name = os.getenv("PINECONE_INDEX_NAME", "default-index")
        vectorstore = Pinecone.from_texts(
            texts=texts,
            embedding=embeddings,
            index_name=index_name,
            metadatas=[document.metadata or {}] * len(texts)
        )
        
        return {"message": f"Uploaded {len(texts)} chunks to vector database"}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/generate")
async def generate_text(prompt: str, max_tokens: int = 1000):
    """Generate text using LLM"""
    try:
        # Create LLM chain
        template = PromptTemplate(
            input_variables=["prompt"],
            template="{prompt}"
        )
        
        chain = LLMChain(llm=llm, prompt=template)
        result = chain.run(prompt=prompt)
        
        return {"generated_text": result}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "openai_key": "configured" if os.getenv("OPENAI_API_KEY") else "missing",
        "pinecone_key": "configured" if os.getenv("PINECONE_API_KEY") else "missing"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
