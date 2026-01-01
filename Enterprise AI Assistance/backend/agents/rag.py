import os
from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

class RAGAgent:
    def __init__(self):
        self.persist_directory = "./data/chroma_db"
        api_key = os.getenv("OPENAI_API_KEY")
        
        if api_key:
            self.embeddings = OpenAIEmbeddings()
            self.llm = ChatOpenAI(temperature=0, model="gpt-3.5-turbo")
            # Initialize vector store
            self.vector_store = Chroma(
                persist_directory=self.persist_directory, 
                embedding_function=self.embeddings
            )
        else:
            self.embeddings = None
            self.llm = None
            self.vector_store = None

    def ingest_document(self, file_path: str):
        if not self.embeddings:
            return "Error: OpenAI API Key not found."

        if file_path.endswith(".pdf"):
            loader = PyPDFLoader(file_path)
        else:
            loader = TextLoader(file_path)
            
        docs = loader.load()
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        splits = text_splitter.split_documents(docs)
        
        self.vector_store.add_documents(splits)
        return f"Ingested {len(splits)} chunks from {os.path.basename(file_path)}"

    def answer_query(self, query: str) -> str:
        if not self.llm:
            return "RAG Unavailable (No API Key)"
            
        retriever = self.vector_store.as_retriever(search_kwargs={"k": 3})
        
        template = """Answer the question based only on the following context:
        {context}

        Question: {question}
        """
        prompt = ChatPromptTemplate.from_template(template)
        
        def format_docs(docs):
            return "\n\n".join([d.page_content for d in docs])

        # LCEL Chain
        rag_chain = (
            {"context": retriever | format_docs, "question": RunnablePassthrough()}
            | prompt
            | self.llm
            | StrOutputParser()
        )
        
        try:
            # We also want sources. 
            # LCEL makes it slightly harder to get sources aside from just returning them.
            # For simplicity in this fix, we will just return the answer.
            # To get sources, we'd need a parallel chain or use invoke with full object.
            
            # Simple version:
            answer = rag_chain.invoke(query)
            
            # Retrieve docs manually for sources if needed
            relevant_docs = retriever.invoke(query)
            sources = list(set([doc.metadata.get("source", "Unknown") for doc in relevant_docs]))
            
            return f"{answer}\n\nSources: {', '.join(sources)}"
        except Exception as e:
            return f"Error providing answer: {str(e)}"
