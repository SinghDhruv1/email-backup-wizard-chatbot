# Email Backup Wizard Chatbot - Streamlit

## 🚀 Quick Deploy to Streamlit Cloud (FREE)

### Method 1: Streamlit Cloud (Recommended - 100% Free)

1. **Create GitHub Repository:**
   - Upload these files to a new GitHub repo
   - Make sure the repo is public

2. **Deploy to Streamlit Cloud:**
   - Go to [share.streamlit.io](https://share.streamlit.io)
   - Sign in with GitHub
   - Click "New app"
   - Select your repository
   - Set main file: `streamlit_app.py`
   - Click "Deploy"

3. **Your app will be live at:**
   `https://your-username-your-repo-name.streamlit.app`

### Method 2: Local Development

```bash
# Install dependencies
pip install streamlit

# Run the app
streamlit run streamlit_app.py
```

### Method 3: Other Free Hosting Options

#### Hugging Face Spaces (Alternative)
1. Create account at [huggingface.co](https://huggingface.co)
2. Create new Space with Streamlit
3. Upload files
4. Auto-deploys

#### Render (Alternative)
1. Connect GitHub repo to [render.com](https://render.com)
2. Select "Web Service"
3. Build command: `pip install -r requirements.txt`
4. Start command: `streamlit run streamlit_app.py --server.port $PORT --server.address 0.0.0.0`

## 📁 File Structure
```
├── streamlit_app.py          # Main application
├── requirements.txt          # Dependencies
├── .streamlit/
│   └── config.toml          # Streamlit configuration
├── .streamlit/
│   └── secrets.toml         # Secrets (optional)
└── README.md                # This file
```

## 🎯 Features
- ✅ Real-time chat interface
- ✅ Knowledge base search
- ✅ Contextual responses
- ✅ Sample questions
- ✅ Chat statistics
- ✅ Mobile responsive
- ✅ No external API dependencies
- ✅ 100% free hosting

## 🔧 Customization
- Edit knowledge base in `KNOWLEDGE_BASE` dictionary
- Modify keywords in `KEYWORDS` dictionary
- Update styling in the CSS section
- Add more sample questions

## 📊 Usage Analytics
The app tracks:
- Total messages
- User questions
- Chat history (session-based)

## 🌐 Live Demo
After deployment, share your Streamlit app URL with customers for instant support!
