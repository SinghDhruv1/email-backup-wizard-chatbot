import streamlit as st
import json
import time
from datetime import datetime

# Page configuration
st.set_page_config(
    page_title="Email Backup Wizard Support",
    page_icon="📧",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #2196F3, #1976D2);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
    }
    .chat-message {
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
        max-width: 80%;
    }
    .user-message {
        background-color: #e3f2fd;
        margin-left: auto;
        text-align: right;
    }
    .bot-message {
        background-color: #f5f5f5;
        border-left: 4px solid #2196F3;
    }
    .stTextInput > div > div > input {
        border-radius: 20px;
    }
    .stButton > button {
        border-radius: 20px;
        background-color: #2196F3;
        color: white;
        border: none;
    }
</style>
""", unsafe_allow_html=True)

# Knowledge base - same as n8n workflow
KNOWLEDGE_BASE = {
    "office365": {
        "user_login": "To log in to Office 365 as a user: Select Office 365 from left panel, enter email address, uncheck 'I am admin', click Login. Enter credentials on Microsoft login page and grant permissions.",
        "admin_login": "To log in as Office 365 admin: Select Office 365, enter admin email, check 'I am admin', click Login. Enter credentials, grant permissions, then select desired users from the list.",
        "admin_feature": "The 'I am Admin' checkbox allows delegated authentication via Microsoft Graph, avoiding need for individual user credentials."
    },
    "google_workspace": {
        "single_user": "Select Google Workspace from left panel, enter email, uncheck 'I am admin', click Login. Grant permissions on Google login page.",
        "admin_setup": "Requires Service Account ID and P12 certificate file. Must enable APIs: Admin SDK, Gmail, Calendar, People APIs.",
        "calendar_limitation": "Calendar data is currently not supported for Google Workspace migration."
    },
    "imap": {
        "requirements": "Need: Email ID, Password/App Password, IMAP Host, IMAP Port, stable internet connection.",
        "batch_mode": "Enable 'Use Batch Mode', prepare CSV file with email,password format for multiple users.",
        "login_issues": "Some services require App Password instead of regular password for third-party tools."
    },
    "issues": {
        "slow_migration": "Speed depends on system performance, internet speed, and server bandwidth. Test showed 1GB in 30 minutes on i5 with 10Mbps.",
        "connection_lost": "Can occur due to unstable internet, server downtime, or bandwidth limits. Try again later.",
        "gmail_imap": "Google disabled IMAP setting. Use OAuth login method instead of IMAP."
    },
    "features": {
        "incremental_backup": "Enabled by default under Filter tab. Allows resuming from where migration left off.",
        "folder_structure": "Original folder structure is preserved during backup/migration.",
        "concurrent_migration": "Up to 3-5 users can be migrated simultaneously.",
        "split_pst": "Recommended for large data. Can split PST into 2GB, 5GB, 10GB, 20GB, 25GB, or 30GB parts."
    },
    "providers": {
        "aol": "Requires App Password generation from Account Security settings.",
        "yandex": "Requires App Password from Security settings with two-step verification enabled.",
        "zoho": "Generate App Password from Security > Application-specific passwords.",
        "proton": "Requires Proton Bridge credentials, not App Password.",
        "att": "Generate App Password from My Account > Sign-in info > Manage secure mail key.",
        "comcast": "Enable Third Party Access Security in Settings > Security.",
        "icloud": "Generate App-Specific Password from Apple ID security settings."
    }
}

# Keywords for matching
KEYWORDS = {
    "office365": ['office 365', 'o365', 'microsoft', 'admin login', 'user login', 'graph api', 'delegated'],
    "google_workspace": ['google workspace', 'gmail oauth', 'google admin', 'service account', 'p12', 'certificate'],
    "imap": ['imap', 'batch mode', 'csv file', 'multiple users', 'host', 'port'],
    "issues": ['slow', 'speed', 'connection lost', 'error', 'failed', 'timeout', 'bandwidth'],
    "features": ['incremental', 'backup', 'folder structure', 'concurrent', 'split pst', 'filter'],
    "providers": ['aol', 'yandex', 'zoho', 'proton', 'att', 'comcast', 'icloud', 'app password', 'bridge']
}

def search_knowledge(user_message):
    """Search knowledge base for relevant information"""
    user_message_lower = user_message.lower()

    best_match = None
    max_score = 0
    matched_content = ""

    # Find best matching category
    for category, words in KEYWORDS.items():
        score = sum(1 for word in words if word in user_message_lower)
        if score > max_score:
            max_score = score
            best_match = category

    # Get relevant content
    if best_match and best_match in KNOWLEDGE_BASE:
        matched_content = " ".join(KNOWLEDGE_BASE[best_match].values())

    return {
        "category": best_match,
        "confidence": max_score,
        "content": matched_content,
        "is_relevant": max_score > 0
    }

def generate_response(user_message, search_result):
    """Generate response based on search results"""
    if not search_result["is_relevant"]:
        return """I'm sorry, but your question seems to be outside my area of expertise with Email Backup Wizard software. 

For personalized assistance with your specific issue, please contact our live support team at: **https://emailbackupwizard.com/support.html**

Our support team can help you with:
• Technical troubleshooting
• Account-specific issues  
• Custom migration scenarios
• Billing and licensing questions"""

    category = search_result["category"]
    content = search_result["content"]

    response_templates = {
        "office365": f"**Office 365 Setup:**\n{content}\n\n💡 Need more specific help? Contact our support team at: https://emailbackupwizard.com/support.html",
        "google_workspace": f"**Google Workspace Configuration:**\n{content}\n\n💡 For detailed setup instructions, visit our support page: https://emailbackupwizard.com/support.html",
        "imap": f"**IMAP Configuration:**\n{content}\n\n💡 Still having issues? Our support team can help: https://emailbackupwizard.com/support.html",
        "issues": f"**Troubleshooting:**\n{content}\n\n💡 If the problem persists, please contact support: https://emailbackupwizard.com/support.html",
        "features": f"**Feature Information:**\n{content}\n\n💡 For advanced configuration help: https://emailbackupwizard.com/support.html",
        "providers": f"**Email Provider Setup:**\n{content}\n\n💡 Need step-by-step guidance? Contact us: https://emailbackupwizard.com/support.html"
    }

    return response_templates.get(category, f"Based on your question: \"{user_message}\"\n\n{content}\n\n💡 For more detailed assistance: https://emailbackupwizard.com/support.html")

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant", 
            "content": "👋 Hi! I'm here to help you with Email Backup Wizard. You can ask me about:\n\n• Office 365 & Google Workspace setup\n• IMAP configuration\n• Migration issues & troubleshooting\n• Software features\n\nWhat would you like to know?",
            "timestamp": datetime.now()
        }
    ]

# Header
st.markdown("""
<div class="main-header">
    <h1>📧 Email Backup Wizard Support</h1>
    <p>Ask me anything about email backup and migration!</p>
</div>
""", unsafe_allow_html=True)

# Chat interface
chat_container = st.container()

with chat_container:
    # Display chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

# Chat input
if prompt := st.chat_input("Ask about email backup, Office 365 login, IMAP setup..."):
    # Add user message
    st.session_state.messages.append({
        "role": "user", 
        "content": prompt,
        "timestamp": datetime.now()
    })

    # Display user message
    with st.chat_message("user"):
        st.markdown(prompt)

    # Generate and display assistant response
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            # Simulate processing time
            time.sleep(1)

            # Search knowledge base
            search_result = search_knowledge(prompt)

            # Generate response
            response = generate_response(prompt, search_result)

            # Display response
            st.markdown(response)

    # Add assistant message to session state
    st.session_state.messages.append({
        "role": "assistant", 
        "content": response,
        "timestamp": datetime.now()
    })

# Sidebar with information
with st.sidebar:
    st.markdown("### 📊 Chat Statistics")
    st.metric("Total Messages", len(st.session_state.messages))
    st.metric("User Questions", len([m for m in st.session_state.messages if m["role"] == "user"]))

    st.markdown("### 🔗 Quick Links")
    st.markdown("- [Live Support](https://emailbackupwizard.com/support.html)")
    st.markdown("- [Documentation](https://emailbackupwizard.com)")

    st.markdown("### 💡 Sample Questions")
    sample_questions = [
        "How do I login to Office 365?",
        "What are IMAP requirements?", 
        "Why is migration slow?",
        "How to setup Google Workspace?",
        "What is incremental backup?"
    ]

    for question in sample_questions:
        if st.button(question, key=f"sample_{hash(question)}"):
            st.session_state.messages.append({
                "role": "user", 
                "content": question,
                "timestamp": datetime.now()
            })
            st.rerun()

    if st.button("🗑️ Clear Chat"):
        st.session_state.messages = [st.session_state.messages[0]]  # Keep welcome message
        st.rerun()

# Footer
st.markdown("---")
st.markdown("*Powered by Streamlit • Email Backup Wizard Support Bot*")
