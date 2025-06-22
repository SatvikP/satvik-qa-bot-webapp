# app.py - Updated for Railway deployment
import os
import glob
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
os.environ["TOKENIZERS_PARALLELISM"] = "false"

from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_anthropic import ChatAnthropic

app = Flask(__name__)
CORS(app)

class BlogQABot:
    def __init__(self, content_dir="content", anthropic_api_key=None):
        self.content_dir = content_dir
        self.anthropic_api_key = anthropic_api_key
        self.vectorstore = None
        self.llm = None
        self.setup_components()
    
    def setup_components(self):
        print("🔄 Loading content...")
        documents = []
        
        # Load all .txt files in content directory
        content_files = glob.glob(os.path.join(self.content_dir, "*.txt"))
        for file_path in content_files:
            try:
                loader = TextLoader(file_path, encoding='utf-8')
                docs = loader.load()
                documents.extend(docs)
                print(f"✅ Loaded: {file_path}")
            except Exception as e:
                print(f"❌ Error loading {file_path}: {e}")
        
        if not documents:
            raise ValueError(f"No documents found in {self.content_dir}")
        
        print(f"📚 Total documents loaded: {len(documents)}")
        
        # Split into chunks
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200
        )
        texts = text_splitter.split_documents(documents)
        print(f"📄 Split into {len(texts)} chunks")
        
        # Create embeddings
        print("🔄 Creating embeddings...")
        embeddings = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2"
        )
        
        # Create vector database
        print("🔄 Creating vector database...")
        self.vectorstore = FAISS.from_documents(texts, embeddings)
        
        # Setup Claude
        print("🔄 Setting up Claude...")
        self.llm = ChatAnthropic(
            model="claude-3-7-sonnet-20250219",
            anthropic_api_key=self.anthropic_api_key
        )
        
        print("✅ Setup complete! Ready to answer questions.")
    
    def ask_question(self, question):
        try:
            # Get relevant documents
            docs = self.vectorstore.similarity_search(question, k=3)
            
            # Create context from documents
            context = "\n\n".join([doc.page_content for doc in docs])
            
            # Custom prompt
            prompt = f"""Based on the following content about the blog author - Satvik, answer this question as if you are the blog author.
Use the same tone and perspective as shown in the content.
If the content doesn't contain enough information, say so honestly.
Keep your response conversational and helpful. And Keep it short and concise.

Content:
{context}

Question: {question}

Answer:"""
            
            # Get response from Claude
            response = self.llm.invoke(prompt)
            return {
                "success": True,
                "answer": response.content,
                "sources": len(docs)
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }

# Initialize the bot when the app starts
print("🚀 Initializing Blog Q&A Bot...")
api_key = os.getenv("ANTHROPIC_API_KEY")
if not api_key:
    print("❌ Please set ANTHROPIC_API_KEY environment variable")
    # Don't exit in production, let Railway show the error
    bot = None
else:
    try:
        bot = BlogQABot(anthropic_api_key=api_key)
    except Exception as e:
        print(f"❌ Failed to initialize bot: {e}")
        bot = None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/ask', methods=['POST'])
def ask_question():
    if bot is None:
        return jsonify({"success": False, "error": "Bot not initialized. Please check API key and content files."})
    
    data = request.get_json()
    question = data.get('question', '').strip()
    
    if not question:
        return jsonify({"success": False, "error": "Please provide a question"})
    
    result = bot.ask_question(question)
    return jsonify(result)

@app.route('/health')
def health():
    if bot is None:
        return jsonify({"status": "error", "message": "Bot not initialized"}), 500
    return jsonify({"status": "healthy", "message": "Bot is ready to answer questions!"})

if __name__ == '__main__':
    # Railway provides PORT environment variable
    port = int(os.environ.get('PORT', 8000))
    app.run(debug=False, host='0.0.0.0', port=port)