# Personal Blog Q&A Bot 🤖

A semantic search-powered Q&A system that answers questions about blog content using RAG (Retrieval Augmented Generation). Built with Flask, LangChain, and Claude 3.7 Sonnet.

![Demo](https://img.shields.io/badge/Demo-Local-brightgreen) ![Python](https://img.shields.io/badge/Python-3.9-blue) ![License](https://img.shields.io/badge/License-MIT-yellow)

## ✨ Features

- 🔍 **Semantic Search**: Uses FAISS vector database for intelligent content retrieval
- 🤖 **AI-Powered Responses**: Powered by Claude 3.7 Sonnet via Anthropic API
- 💬 **Chat Interface**: Beautiful, responsive web interface with real-time responses
- 📝 **Personalized Answers**: Responds in the author's voice and style
- 🆓 **Free Embeddings**: Uses HuggingFace sentence transformers (runs locally)
- 📱 **Mobile Responsive**: Works seamlessly on desktop and mobile devices
- 💻 **Local Development**: Optimized for local hosting and development

## 🏠 Local Demo

This project is designed for **local development and demonstration**. The web interface runs on your machine, providing a secure and cost-effective way to showcase your personal AI assistant.

**Access your bot at**: `http://localhost:8000`

> **Why Local?** 
> - 💰 **Cost-effective**: Saves on API credits and hosting costs
> - 🔒 **Secure**: Your API key stays on your machine
> - ⚡ **Fast**: No cold starts or network latency
> - 🛠️ **Customizable**: Easy to modify and experiment with

## 🛠️ Tech Stack

- **Backend**: Flask, Python 3.9
- **AI/ML**: LangChain, Anthropic Claude 3.7 Sonnet, HuggingFace Transformers
- **Vector Database**: FAISS
- **Frontend**: HTML5, CSS3, Vanilla JavaScript
- **Deployment**: Railway
- **Dependencies**: See `requirements.txt`

## 📋 Prerequisites

- Python 3.9 or higher
- Anthropic API key ([get one here](https://console.anthropic.com/))
- Git installed on your machine

## 🔧 Local Development Setup

### 1. Clone the Repository
```bash
git clone https://github.com/SatvikP/satvik-qa-bot-webapp.git
cd satvik-qa-bot-webapp
```

### 2. Create Virtual Environment
```bash
# Create virtual environment
python -m venv venv

# Activate it
# On macOS/Linux:
source venv/bin/activate
# On Windows:
venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Set Environment Variables
```bash
# Set your Anthropic API key
export ANTHROPIC_API_KEY="your-api-key-here"

# On Windows:
set ANTHROPIC_API_KEY=your-api-key-here
```

### 5. Add Your Content
Place your blog posts and content as `.txt` files in the `content/` directory:
```
content/
├── about-me.txt
├── blog-post-1.txt
├── blog-post-2.txt
└── ...
```

### 6. Run the Application
```bash
python app.py
```

**🎉 Access your bot at**: `http://localhost:8000`

**Note**: The first startup takes 1-2 minutes as it processes your content and creates the vector database.

## 📝 Usage

1. **Open your browser** and navigate to `http://localhost:8000`
2. **Type questions** about your content in the chat interface
3. **Get personalized responses** based on your blog content
4. **Enjoy the conversation!** The bot responds in your voice and style

### Example Questions
- "What programming languages do you recommend?"
- "Tell me about your experience with AI"
- "What are your thoughts on web development?"
- "What projects have you worked on?"

## 🚀 Deployment (Optional)

While this project is optimized for local use, you can deploy it to cloud platforms if needed:

### Requirements for Cloud Deployment
- **Memory**: 2GB+ (ML libraries are memory-intensive)
- **Storage**: 1GB+ for dependencies
- **Budget**: ~$5-10/month for reliable hosting

### Recommended Platforms
- **DigitalOcean App Platform** ($5/month) - Best balance of features and cost
- **Railway Pro** ($5/month) - Great developer experience
- **Heroku** ($7/month) - Popular and reliable
- **AWS/Google Cloud** (Pay-as-you-go) - Enterprise-grade

### Why Local is Better
- ✅ **No hosting costs** - runs on your machine
- ✅ **Instant startup** - no cold starts
- ✅ **API savings** - only use credits when testing
- ✅ **Easy debugging** - full control and logs
- ✅ **Perfect for demos** - showcase during interviews or presentations

*Note: Free hosting platforms (Render, Railway free, Replit) have resource limitations that make it challenging to run ML-heavy applications.*

## 📁 Project Structure

```
satvik-qa-bot-webapp/
├── app.py                 # Main Flask application
├── main.py               # CLI version (for testing)
├── templates/
│   └── index.html        # Web interface
├── content/              # Your blog content (.txt files)
│   ├── about-me.txt
│   ├── blog-post-1.txt
│   └── ...
├── venv/                 # Virtual environment (local only)
├── vector_db/           # Generated vector database (created on first run)
├── requirements.txt     # Python dependencies
├── .gitignore          # Git ignore file
└── README.md           # This file
```

## 🎯 Usage

1. **Visit your deployed app** or run locally
2. **Type questions** about the content in the chat interface
3. **Get personalized responses** based on the blog content

### Example Questions
- "What programming languages do you recommend?"
- "Tell me about your experience with AI"
- "What are your thoughts on web development?"
- "What projects have you worked on?"

## ⚙️ Configuration

### Customizing Responses
Edit the prompt in `app.py` around line 80 to change how the bot responds:

```python
prompt = f"""Based on the following content about the blog author, answer this question as if you are the blog author.
Use the same tone and perspective as shown in the content.
[Your custom instructions here]

Content:
{context}

Question: {question}

Answer:"""
```

### Adding More Content
Simply add more `.txt` files to the `content/` directory and restart the app. The system will automatically:
- Process new content
- Create embeddings
- Make it searchable

### Changing the Model
To use a different Claude model, update the model name in `app.py`:
```python
self.llm = ChatAnthropic(
    model="claude-3-haiku-20240307",  # Faster, cheaper option
    # model="claude-3-opus-20240229",  # More powerful option
    anthropic_api_key=self.anthropic_api_key
)
```

### Port Configuration
To run on a different port, modify the last line in `app.py`:
```python
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 9000))  # Change from 8000 to 9000
    app.run(debug=True, host='0.0.0.0', port=port)
```

## 🐛 Troubleshooting

### Common Issues

**"Bot not initialized" error**:
- Check that your `ANTHROPIC_API_KEY` is set correctly: `echo $ANTHROPIC_API_KEY`
- Ensure you have `.txt` files in the `content/` directory
- Check terminal logs for detailed error messages

**Port already in use**:
- On Mac, port 8000 might be used by other services
- Change the port in `app.py` or kill the conflicting process:
```bash
lsof -i :8000  # Find what's using the port
kill -9 PID   # Kill the process (replace PID with actual process ID)
```

**Slow first startup**:
- The first run takes 1-2 minutes to process content and create embeddings
- Subsequent starts are much faster as the vector database is cached

**API quota/rate limiting**:
- Check your Anthropic API usage at [console.anthropic.com](https://console.anthropic.com)
- Consider using Claude Haiku for cheaper requests during development

**Virtual environment issues**:
```bash
# If packages aren't found, make sure venv is activated
source venv/bin/activate  # Mac/Linux
venv\Scripts\activate     # Windows

# Reinstall dependencies if needed
pip install -r requirements.txt
```

### Viewing Logs
All logs appear in your terminal when running `python app.py`. Look for:
- ✅ Success messages (setup complete, files loaded)
- ❌ Error messages (API issues, missing files)
- 🔄 Processing updates (creating embeddings, etc.)

### Performance Tips
- **Smaller content files** = faster processing
- **More specific questions** = better answers
- **Claude Haiku** = faster, cheaper responses
- **Restart app** after adding new content files

## 🔒 Security

- **API Keys**: Never commit API keys to version control
- **Environment Variables**: Always use environment variables for sensitive data
- **Content**: Ensure your content doesn't contain sensitive information

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [Anthropic](https://www.anthropic.com/) for Claude API
- [LangChain](https://python.langchain.com/) for RAG framework
- [HuggingFace](https://huggingface.co/) for free embeddings
- [Railway](https://railway.app/) for hosting platform

## 📞 Support

If you have questions or need help:

1. **Check the logs** in your terminal when running `python app.py`
2. **Review this README** for common solutions in the Troubleshooting section
3. **Verify your setup** - API key, content files, virtual environment
4. **Open an issue** on GitHub for bugs or feature requests

## 🎯 Perfect For

- 📊 **Portfolio Projects** - Showcase your AI/ML skills
- 🎤 **Technical Interviews** - Live demo of RAG implementation
- 🏠 **Personal Use** - Query your own blog/content easily
- 📚 **Learning** - Understand how RAG systems work
- 💼 **Client Demos** - Show potential of AI-powered content systems

---

**Built with ❤️ using Claude, LangChain, and Flask**

*Local-first approach for maximum flexibility and cost savings*