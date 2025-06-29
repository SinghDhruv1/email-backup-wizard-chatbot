import streamlit as st
import json
import time
import random
from datetime import datetime

# Page configuration
st.set_page_config(
    page_title="Email Backup Wizard Support",
    page_icon="📧",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Enhanced CSS for better styling
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 15px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 8px 32px rgba(0,0,0,0.1);
    }
    .chat-message {
        padding: 1.5rem;
        border-radius: 15px;
        margin: 1rem 0;
        max-width: 85%;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
    }
    .user-message {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        margin-left: auto;
        text-align: right;
    }
    .bot-message {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        color: white;
        border-left: 5px solid #ff6b6b;
    }
    .info-box {
        background: #e3f2fd;
        border-left: 4px solid #2196f3;
        padding: 1rem;
        margin: 1rem 0;
        border-radius: 5px;
    }
    .warning-box {
        background: #fff3cd;
        border-left: 4px solid #ffc107;
        padding: 1rem;
        margin: 1rem 0;
        border-radius: 5px;
    }
    .success-box {
        background: #d4edda;
        border-left: 4px solid #28a745;
        padding: 1rem;
        margin: 1rem 0;
        border-radius: 5px;
    }
</style>
""", unsafe_allow_html=True)

@st.cache_data
def load_knowledge_base():
    """Load knowledge base from JSON file"""
    try:
        with open('knowledge_base.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        st.error("Knowledge base file not found. Please ensure knowledge_base.json is in the same directory.")
        return {}
    except json.JSONDecodeError:
        st.error("Error reading knowledge base file. Please check the JSON format.")
        return {}

def search_knowledge_base(user_message, knowledge_base):
    """Search knowledge base for relevant information"""
    user_message_lower = user_message.lower()
    best_match = None
    max_score = 0
    matched_content = {}

    # Search through all categories and items
    for category, items in knowledge_base.items():
        for item_key, item_data in items.items():
            if isinstance(item_data, dict) and 'keywords' in item_data:
                # Calculate relevance score based on keyword matches
                score = sum(2 for keyword in item_data['keywords'] if keyword.lower() in user_message_lower)

                # Boost score for exact matches
                if any(keyword.lower() == user_message_lower.strip() for keyword in item_data['keywords']):
                    score += 5

                if score > max_score:
                    max_score = score
                    best_match = f"{category}.{item_key}"
                    matched_content = item_data

    return {
        "category": best_match,
        "confidence": max_score,
        "content": matched_content,
        "is_relevant": max_score > 0
    }

def format_response(content):
    """Format response content into readable markdown"""
    if not content:
        return "I couldn't find specific information about that."

    response = ""

    # Add title
    if 'title' in content:
        response += f"## {content['title']}\n\n"

    # Add overview/note
    if 'overview' in content:
        response += f"{content['overview']}\n\n"
    if 'note' in content:
        response += f"💡 **{content['note']}**\n\n"

    # Add recommended method
    if 'recommended_method' in content:
        response += f"### 🎯 Recommended Method: {content['recommended_method']}\n\n"

    # Add settings
    if 'settings' in content:
        response += "### ⚙️ Settings:\n"
        for key, value in content['settings'].items():
            response += f"- **{key}**: `{value}`\n"
        response += "\n"

    # Add steps
    if 'steps' in content:
        response += "### 📋 Step-by-Step Instructions:\n"
        for step in content['steps']:
            response += f"{step}\n\n"

    # Add OAuth steps
    if 'oauth_steps' in content:
        response += "### 🔐 OAuth Login Steps:\n"
        for step in content['oauth_steps']:
            response += f"{step}\n\n"

    # Add benefits
    if 'benefits' in content:
        response += "### ✨ Benefits:\n"
        for benefit in content['benefits']:
            response += f"- {benefit}\n"
        response += "\n"

    # Add OAuth benefits
    if 'oauth_benefits' in content:
        response += "### ✨ OAuth Benefits:\n"
        for benefit in content['oauth_benefits']:
            response += f"- {benefit}\n"
        response += "\n"

    # Add tips
    if 'tips' in content:
        response += "### 💡 Pro Tips:\n"
        for tip in content['tips']:
            response += f"- {tip}\n"
        response += "\n"

    # Add troubleshooting
    if 'troubleshooting' in content:
        response += "### 🔧 Troubleshooting:\n"
        for issue in content['troubleshooting']:
            response += f"- {issue}\n"
        response += "\n"

    # Add common causes
    if 'common_causes' in content:
        response += "### 🔍 Common Causes:\n"
        for cause in content['common_causes']:
            response += f"- {cause}\n"
        response += "\n"

    # Add speed improvements
    if 'speed_improvements' in content:
        response += "### ⚡ Speed Improvements:\n"
        for improvement in content['speed_improvements']:
            response += f"- {improvement}\n"
        response += "\n"

    # Add immediate fixes
    if 'immediate_fixes' in content:
        response += "### 🚨 Immediate Fixes:\n"
        for fix in content['immediate_fixes']:
            response += f"- {fix}\n"
        response += "\n"

    # Add advanced solutions
    if 'advanced_solutions' in content:
        response += "### 🔧 Advanced Solutions:\n"
        for solution in content['advanced_solutions']:
            response += f"- {solution}\n"
        response += "\n"

    # Add common solutions
    if 'common_solutions' in content:
        response += "### 💡 Common Solutions:\n"
        for solution in content['common_solutions']:
            response += f"- {solution}\n"
        response += "\n"

    # Add provider specific info
    if 'provider_specific' in content:
        response += "### 📧 Provider-Specific Solutions:\n"
        for provider, solution in content['provider_specific'].items():
            response += f"- **{provider}**: {solution}\n"
        response += "\n"

    # Add what it does
    if 'what_it_does' in content:
        response += "### 🎯 What It Does:\n"
        for item in content['what_it_does']:
            response += f"- {item}\n"
        response += "\n"

    # Add how to enable
    if 'how_to_enable' in content:
        response += "### 🔧 How to Enable:\n"
        for step in content['how_to_enable']:
            response += f"{step}\n\n"

    # Add use cases
    if 'use_cases' in content:
        response += "### 📈 Use Cases:\n"
        for case in content['use_cases']:
            response += f"- {case}\n"
        response += "\n"

    # Add why split
    if 'why_split' in content:
        response += "### 🤔 Why Split PST Files?\n"
        for reason in content['why_split']:
            response += f"- {reason}\n"
        response += "\n"

    # Add size options
    if 'size_options' in content:
        response += "### 📦 Size Options:\n"
        for option in content['size_options']:
            response += f"- {option}\n"
        response += "\n"

    # Add recommendation
    if 'recommendation' in content:
        response += f"### 🎯 Recommendation:\n{content['recommendation']}\n\n"

    # Add benchmark
    if 'benchmark' in content:
        response += f"### 📊 Performance Benchmark:\n{content['benchmark']}\n\n"

    # Add patience note
    if 'patience_note' in content:
        response += f"### ⏰ Important Note:\n{content['patience_note']}\n\n"

    # Add IMAP note
    if 'imap_note' in content:
        response += f"### ⚠️ Important:\n{content['imap_note']}\n\n"

    # Add limitation
    if 'limitation' in content:
        response += f"### ⚠️ Limitation:\n{content['limitation']}\n\n"

    # Add alternative
    if 'alternative' in content:
        response += f"### 🔄 Alternative:\n{content['alternative']}\n\n"

    # Add requirements
    if 'requirements' in content:
        response += "### 📋 Requirements:\n"
        for req in content['requirements']:
            response += f"- {req}\n"
        response += "\n"

    # Add supported providers
    if 'supported_providers' in content:
        response += "### 📧 Supported Providers:\n"
        for provider in content['supported_providers']:
            response += f"- {provider}\n"
        response += "\n"

    # Add basic steps
    if 'basic_steps' in content:
        response += "### 🚀 Basic Steps:\n"
        for step in content['basic_steps']:
            response += f"{step}\n\n"

    return response

def generate_response(user_message, search_result, knowledge_base):
    """Generate response based on search results"""
    if not search_result["is_relevant"]:
        return f"""🤔 I understand you're asking about "{user_message}", but I don't have specific information about that topic in my knowledge base.

### 🎯 **What I Can Help With:**
- 📧 **Email Provider Setup** (Yahoo, Gmail, AOL, Outlook)
- 🔐 **Office 365 & Google Workspace** configuration  
- ⚙️ **IMAP Settings** and troubleshooting
- 🐌 **Performance Issues** and speed optimization
- ✨ **Advanced Features** like incremental backup & PST splitting

### 🆘 **Need Immediate Help?**
Our support team specializes in unique situations: **[Live Support](https://emailbackupwizard.com/support.html)**

### 💡 **Try asking me:**
- *"How to login to Yahoo mail?"*
- *"Office 365 admin setup"*
- *"Why is migration slow?"*
- *"Gmail OAuth setup"*

What else can I help you with? 😊"""

    content = search_result["content"]
    formatted_response = format_response(content)

    # Add footer with support link
    formatted_response += "\n---\n💬 **Need more help?** Contact our live support: [https://emailbackupwizard.com/support.html](https://emailbackupwizard.com/support.html)"

    return formatted_response

# Load knowledge base
knowledge_base = load_knowledge_base()

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant", 
            "content": """🎉 **Welcome to Email Backup Wizard Support!** 

I'm your AI assistant, ready to help you with all things email backup and migration! 

### 🚀 **What I Can Help You With:**
• 📧 **Email Provider Setup** (Yahoo, Gmail, AOL, Outlook, etc.)
• 🔐 **Office 365 & Google Workspace** configuration  
• ⚙️ **IMAP Settings** and troubleshooting
• 🐌 **Performance Issues** and speed optimization
• ✨ **Advanced Features** like incremental backup & PST splitting

### 💡 **Try asking me:**
• *"How can I login to Yahoo mail?"*
• *"Office 365 admin setup steps"*
• *"Why is my migration running slow?"*
• *"What are Gmail OAuth benefits?"*

**What would you like to know?** 😊""",
            "timestamp": datetime.now()
        }
    ]

# Header
st.markdown("""
<div class="main-header">
    <h1>🚀 Email Backup Wizard Support</h1>
    <p>Your AI-powered migration assistant - Making email backup simple & fast!</p>
</div>
""", unsafe_allow_html=True)

# Main chat interface
if knowledge_base:  # Only show chat if knowledge base loaded successfully
    # Display chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Chat input
    if prompt := st.chat_input("Ask me about Yahoo login, Office 365 setup, slow migration, Gmail OAuth, or any email backup question..."):
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
            with st.spinner("🤔 Analyzing your question..."):
                # Simulate processing time
                time.sleep(random.uniform(1.0, 2.0))

                # Search knowledge base
                search_result = search_knowledge_base(prompt, knowledge_base)

                # Generate response
                response = generate_response(prompt, search_result, knowledge_base)

                # Display response
                st.markdown(response)

        # Add assistant message to session state
        st.session_state.messages.append({
            "role": "assistant", 
            "content": response,
            "timestamp": datetime.now()
        })

# Sidebar
with st.sidebar:
    st.markdown("### 📊 Chat Analytics")
    total_messages = len(st.session_state.messages)
    user_questions = len([m for m in st.session_state.messages if m["role"] == "user"])

    col1, col2 = st.columns(2)
    with col1:
        st.metric("💬 Messages", total_messages)
    with col2:
        st.metric("❓ Questions", user_questions)

    if user_questions > 0:
        st.metric("🤖 Response Rate", "100%")

    st.markdown("---")

    st.markdown("### 🔗 Quick Access")
    st.markdown("🆘 [Live Support](https://emailbackupwizard.com/support.html)")
    st.markdown("📚 [Documentation](https://emailbackupwizard.com)")
    st.markdown("💾 [Download Software](https://emailbackupwizard.com)")

    st.markdown("---")

    st.markdown("### 🎯 Popular Questions")
    popular_questions = [
        "How can I login to Yahoo mail?",
        "Office 365 admin setup guide", 
        "Why is my backup running slow?",
        "Gmail OAuth vs IMAP setup",
        "AOL app password creation",
        "What is incremental backup?",
        "How to split large PST files?",
        "Login failed solutions"
    ]

    for i, question in enumerate(popular_questions):
        if st.button(f"💡 {question}", key=f"popular_{i}"):
            st.session_state.messages.append({
                "role": "user", 
                "content": question,
                "timestamp": datetime.now()
            })
            st.rerun()

    st.markdown("---")

    if st.button("🗑️ Clear Chat History", type="secondary"):
        st.session_state.messages = [st.session_state.messages[0]]  # Keep welcome message
        st.rerun()

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666; padding: 20px;'>
    <p><strong>🚀 Powered by Streamlit • Email Backup Wizard AI Support</strong></p>
    <p>💡 <em>Making email migration simple, one question at a time!</em></p>
</div>
""", unsafe_allow_html=True)
