# main.py - Fixed imports
import os
import glob
os.environ["TOKENIZERS_PARALLELISM"] = "false"
from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_anthropic import ChatAnthropic

class BlogQABot:
    def __init__(self, content_dir="content", anthropic_api_key=None):
        self.content_dir = content_dir
        self.anthropic_api_key = anthropic_api_key
        self.setup_components()
    
    def setup_components(self):
        # 1. Load your blog content (simpler approach)
        print("Loading content...")
        documents = []
        
        # Load all .txt files in content directory
        content_files = glob.glob(os.path.join(self.content_dir, "*.txt"))
        for file_path in content_files:
            try:
                loader = TextLoader(file_path, encoding='utf-8')
                docs = loader.load()
                documents.extend(docs)
                print(f"Loaded: {file_path}")
            except Exception as e:
                print(f"Error loading {file_path}: {e}")
        
        if not documents:
            raise ValueError(f"No documents found in {self.content_dir}. Make sure you have .txt files there.")
        
        print(f"Total documents loaded: {len(documents)}")
        
        # 2. Split into chunks
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200
        )
        texts = text_splitter.split_documents(documents)
        print(f"Split into {len(texts)} chunks")
        
        # 3. Create embeddings (free, runs locally)
        embeddings = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2"
        )
        
        # 4. Create vector database (using FAISS instead of Chroma)
        print("Creating vector database...")
        self.vectorstore = FAISS.from_documents(
            texts, 
            embeddings
        )
        
        # Save the database locally
        self.vectorstore.save_local("./vector_db")
        
        # 5. Setup Claude
        self.llm = ChatAnthropic(
            model="claude-3-7-sonnet-20250219",
            anthropic_api_key=self.anthropic_api_key
        )
        
        # 6. All setup complete
        print("Setup complete! Ready to answer questions.")
    
    def ask_question(self, question):
        # Get relevant documents
        docs = self.vectorstore.similarity_search(question, k=3)
        
        # Create context from documents
        context = "\n\n".join([doc.page_content for doc in docs])
        
        # Custom prompt to make it sound like you
        prompt = f"""Based on the following content about the blog author, answer this question as if you are the blog author.
Use the same tone and perspective as shown in the content.
If the content doesn't contain enough information, say so honestly.
Keep your response conversational and helpful. And Keep it short and concise.

Content:
{context}

Question: {question}

Answer:"""
        
        # Get response from Claude
        response = self.llm.invoke(prompt)
        return response.content, docs

# Usage
if __name__ == "__main__":
    # Get API key from environment variable for security
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        print("Please set ANTHROPIC_API_KEY environment variable")
        exit(1)
    
    # Initialize
    bot = BlogQABot(anthropic_api_key=api_key)
    
    # Ask questions
    while True:
        question = input("\nAsk me anything about my blog (or 'quit'): ")
        if question.lower() == 'quit':
            break
            
        answer, sources = bot.ask_question(question)
        print(f"\nAnswer: {answer}")
        print(f"\nBased on {len(sources)} source chunks from your content.")