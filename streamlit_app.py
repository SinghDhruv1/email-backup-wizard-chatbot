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
    .feature-card {
        background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
        padding: 1rem;
        border-radius: 10px;
        margin: 0.5rem 0;
        color: white;
        text-align: center;
    }
    .step-card {
        background: #f8f9fa;
        border-left: 4px solid #28a745;
        padding: 1rem;
        margin: 0.5rem 0;
        border-radius: 5px;
    }
    .warning-card {
        background: #fff3cd;
        border-left: 4px solid #ffc107;
        padding: 1rem;
        margin: 0.5rem 0;
        border-radius: 5px;
    }
    .success-card {
        background: #d4edda;
        border-left: 4px solid #28a745;
        padding: 1rem;
        margin: 0.5rem 0;
        border-radius: 5px;
    }
</style>
""", unsafe_allow_html=True)

# Enhanced Knowledge Base with detailed, engaging responses
ENHANCED_KNOWLEDGE_BASE = {
    "office365": {
        "user_login": {
            "title": "🔐 Office 365 User Login - Step by Step",
            "steps": [
                "1️⃣ **Select Office 365** from the left panel in Email Backup Wizard",
                "2️⃣ **Enter your email address** (e.g., john@company.com)",
                "3️⃣ **Uncheck 'I am admin'** checkbox (this is for regular users)",
                "4️⃣ **Click the Login button** - this opens Microsoft's secure login page",
                "5️⃣ **Enter your credentials** on the Microsoft page (same as Outlook login)",
                "6️⃣ **Grant permissions** when prompted - this allows the backup tool to access your emails"
            ],
            "tips": [
                "💡 Use the same credentials you use for Outlook.com or office.com",
                "🔒 Your password is never stored - Microsoft handles authentication",
                "⚡ The process takes 30-60 seconds depending on your connection"
            ],
            "troubleshooting": [
                "❌ **Login Failed?** Check if 2FA is enabled - you might need an app password",
                "❌ **Permission Denied?** Contact your IT admin - they may need to enable third-party apps",
                "❌ **Timeout Error?** Try again - sometimes Microsoft servers are busy"
            ]
        },
        "admin_login": {
            "title": "👑 Office 365 Admin Login - Bulk User Access",
            "steps": [
                "1️⃣ **Select Office 365** from the left panel",
                "2️⃣ **Enter your ADMIN email** (must have admin privileges)",
                "3️⃣ **Check 'I am admin'** checkbox ✅",
                "4️⃣ **Click Login** - opens Microsoft admin consent page",
                "5️⃣ **Enter admin credentials** and approve permissions",
                "6️⃣ **Select users** from the list that appears",
                "7️⃣ **Start backup** for multiple users simultaneously"
            ],
            "benefits": [
                "🚀 **Bulk Processing**: Backup multiple users without individual passwords",
                "🔐 **Secure**: Uses Microsoft Graph API - no password storage needed",
                "⚡ **Efficient**: Process 3-5 users simultaneously",
                "📊 **Centralized**: Perfect for IT administrators"
            ]
        }
    },
    "google_workspace": {
        "oauth_login": {
            "title": "🔍 Google Workspace OAuth Login",
            "steps": [
                "1️⃣ **Select Google Workspace** from left panel",
                "2️⃣ **Enter your Gmail/Workspace email**",
                "3️⃣ **Uncheck 'I am admin'** for single user",
                "4️⃣ **Click Login** - opens Google's secure page",
                "5️⃣ **Grant permissions** for Gmail, Calendar, Contacts access"
            ],
            "note": "🎯 **Pro Tip**: This method works for both personal Gmail and Google Workspace accounts!"
        },
        "admin_setup": {
            "title": "⚙️ Google Workspace Admin Setup (Advanced)",
            "requirements": [
                "📋 **Service Account ID** from Google Cloud Console",
                "🔑 **P12 Certificate File** (private key)",
                "🔧 **Enabled APIs**: Admin SDK, Gmail API, Calendar API, People API"
            ],
            "steps": [
                "1️⃣ Create Service Account in Google Cloud Console",
                "2️⃣ Download P12 certificate file",
                "3️⃣ Enable required APIs in Google Cloud",
                "4️⃣ Configure domain-wide delegation",
                "5️⃣ Enter details in Email Backup Wizard"
            ],
            "limitation": "⚠️ **Note**: Calendar data migration is currently not supported for Google Workspace"
        }
    },
    "email_providers": {
        "yahoo": {
            "title": "📮 Yahoo Mail Setup Guide",
            "method": "IMAP Configuration",
            "settings": {
                "IMAP Host": "imap.mail.yahoo.com",
                "IMAP Port": "993",
                "Security": "SSL/TLS",
                "Authentication": "App Password Required"
            },
            "app_password_steps": [
                "1️⃣ Go to Yahoo Account Security settings",
                "2️⃣ Turn on 2-step verification (if not already enabled)",
                "3️⃣ Generate App Password for 'Mail'",
                "4️⃣ Use this App Password instead of your regular password",
                "5️⃣ Enter in Email Backup Wizard IMAP settings"
            ],
            "tips": [
                "🔐 **Never use your regular Yahoo password** - always use App Password",
                "📱 **Keep App Password safe** - treat it like a regular password",
                "🔄 **App Password expires** - generate new one if login fails"
            ]
        },
        "gmail": {
            "title": "📧 Gmail Setup - OAuth vs IMAP",
            "recommended": "OAuth Login (Easier & Secure)",
            "oauth_benefits": [
                "✅ **No App Password needed**",
                "✅ **More secure** - Google handles authentication",
                "✅ **Faster setup** - just click and authorize",
                "✅ **Works with 2FA** automatically"
            ],
            "imap_alternative": {
                "note": "⚠️ **IMAP Method**: Google has disabled less secure app access",
                "solution": "Use OAuth login method instead - it's easier and more secure!"
            }
        },
        "aol": {
            "title": "📬 AOL Mail Configuration",
            "settings": {
                "IMAP Host": "imap.aol.com",
                "IMAP Port": "993",
                "Security": "SSL/TLS"
            },
            "app_password_steps": [
                "1️⃣ Sign in to your AOL Account Security page",
                "2️⃣ Click 'Generate app password'",
                "3️⃣ Select 'Other app' and enter 'Email Backup'",
                "4️⃣ Copy the generated password",
                "5️⃣ Use this in Email Backup Wizard (not your regular password)"
            ]
        },
        "outlook_hotmail": {
            "title": "🔷 Outlook.com / Hotmail Setup",
            "method": "OAuth Login (Recommended)",
            "steps": [
                "1️⃣ **Select Office 365** (works for Outlook.com too)",
                "2️⃣ **Enter your @outlook.com or @hotmail.com email**",
                "3️⃣ **Uncheck 'I am admin'**",
                "4️⃣ **Click Login** and authorize"
            ],
            "alternative": "Can also use IMAP with App Password if needed"
        }
    },
    "troubleshooting": {
        "slow_migration": {
            "title": "🐌 Migration Running Slow? Here's Why & How to Fix",
            "common_causes": [
                "🌐 **Internet Speed**: Slow upload/download affects transfer speed",
                "💻 **System Performance**: Old computer = slower processing",
                "📊 **Data Size**: Large mailboxes (10GB+) take longer",
                "🔄 **Server Load**: Email provider's server might be busy",
                "🔌 **Background Apps**: Other software using internet bandwidth"
            ],
            "speed_improvements": [
                "⚡ **Close other apps** using internet (YouTube, Netflix, etc.)",
                "🔄 **Restart your router** - fresh connection often helps",
                "💾 **Free up disk space** - at least 20% free space needed",
                "🕐 **Run during off-peak hours** (late night/early morning)",
                "📊 **Use Split PST** feature for large mailboxes"
            ],
            "benchmark": "📈 **Real Test**: 1GB mailbox = ~30 minutes on i5 processor with 10Mbps internet",
            "patience_note": "⏰ **Be Patient**: Large migrations can take several hours - that's normal!"
        },
        "connection_issues": {
            "title": "🔌 Connection Lost? Quick Fixes",
            "immediate_fixes": [
                "🔄 **Check internet connection** - try opening a website",
                "⏸️ **Pause and resume** the migration",
                "🔌 **Restart your router/modem**",
                "💻 **Close and reopen** Email Backup Wizard",
                "🕐 **Wait 5-10 minutes** then try again"
            ],
            "advanced_solutions": [
                "🔧 **Change DNS servers** to 8.8.8.8 and 8.8.4.4",
                "🛡️ **Temporarily disable antivirus** (re-enable after backup)",
                "🔥 **Check firewall settings** - allow Email Backup Wizard",
                "📡 **Try different network** (mobile hotspot as test)"
            ]
        }
    },
    "features": {
        "incremental_backup": {
            "title": "🔄 Incremental Backup - Never Lose Progress!",
            "what_it_does": [
                "💾 **Remembers where it stopped** if interrupted",
                "⚡ **Skips already backed up emails** on restart",
                "🎯 **Only processes new/changed emails** in subsequent runs",
                "📊 **Saves time and bandwidth** on large mailboxes"
            ],
            "how_to_enable": [
                "1️⃣ Go to **Filter** tab in Email Backup Wizard",
                "2️⃣ **Incremental Backup is ON by default** ✅",
                "3️⃣ **No additional setup needed** - it just works!"
            ],
            "use_cases": [
                "🏢 **Daily backups** - only new emails get processed",
                "🔄 **Resume interrupted backups** - continue where you left off",
                "📈 **Regular maintenance** - keep backups up-to-date efficiently"
            ]
        },
        "split_pst": {
            "title": "✂️ Split PST Files - Handle Large Mailboxes",
            "why_split": [
                "📁 **Outlook PST limit**: 50GB maximum file size",
                "💾 **Easier management**: Smaller files are easier to handle",
                "🔄 **Better performance**: Outlook opens smaller PST files faster",
                "💿 **Storage flexibility**: Fit on different storage devices"
            ],
            "size_options": [
                "📦 **2GB** - For older Outlook versions",
                "📦 **5GB** - Good balance of size and manageability", 
                "📦 **10GB** - Standard recommendation",
                "📦 **20GB** - For modern systems",
                "📦 **25GB** - Large but manageable",
                "📦 **30GB** - Maximum recommended size"
            ],
            "recommendation": "🎯 **Best Practice**: Use 10GB splits for most scenarios"
        }
    }
}

# Enhanced keyword matching with more comprehensive coverage
ENHANCED_KEYWORDS = {
    "office365": ['office 365', 'o365', 'microsoft', 'outlook.com', 'hotmail', 'admin login', 'user login', 'graph api', 'delegated', 'microsoft login'],
    "google_workspace": ['google workspace', 'gmail', 'google admin', 'service account', 'p12', 'certificate', 'oauth', 'google login'],
    "yahoo": ['yahoo', 'yahoo mail', 'ymail', 'rocketmail'],
    "aol": ['aol', 'aol mail', 'aim mail'],
    "email_providers": ['imap', 'smtp', 'app password', 'email provider', 'mail server', 'email settings'],
    "troubleshooting": ['slow', 'speed', 'connection lost', 'error', 'failed', 'timeout', 'bandwidth', 'not working', 'problem', 'issue'],
    "features": ['incremental', 'backup', 'folder structure', 'concurrent', 'split pst', 'filter', 'resume', 'pause']
}

def enhanced_search_knowledge(user_message):
    """Enhanced search with better matching and scoring"""
    user_message_lower = user_message.lower()

    # Direct provider matching
    if any(word in user_message_lower for word in ['yahoo', 'ymail']):
        return {
            "category": "yahoo",
            "confidence": 10,
            "content": ENHANCED_KNOWLEDGE_BASE["email_providers"]["yahoo"],
            "is_relevant": True
        }

    if any(word in user_message_lower for word in ['aol', 'aim']):
        return {
            "category": "aol", 
            "confidence": 10,
            "content": ENHANCED_KNOWLEDGE_BASE["email_providers"]["aol"],
            "is_relevant": True
        }

    if any(word in user_message_lower for word in ['gmail', 'google mail']):
        return {
            "category": "gmail",
            "confidence": 10, 
            "content": ENHANCED_KNOWLEDGE_BASE["email_providers"]["gmail"],
            "is_relevant": True
        }

    # Enhanced keyword matching
    best_match = None
    max_score = 0
    matched_content = {}

    for category, words in ENHANCED_KEYWORDS.items():
        score = sum(2 if word in user_message_lower else 0 for word in words)
        if score > max_score:
            max_score = score
            best_match = category

    # Get relevant content based on category
    if best_match and max_score > 0:
        if best_match == "office365":
            if "admin" in user_message_lower:
                matched_content = ENHANCED_KNOWLEDGE_BASE["office365"]["admin_login"]
            else:
                matched_content = ENHANCED_KNOWLEDGE_BASE["office365"]["user_login"]
        elif best_match == "google_workspace":
            matched_content = ENHANCED_KNOWLEDGE_BASE["google_workspace"]["oauth_login"]
        elif best_match == "troubleshooting":
            if "slow" in user_message_lower:
                matched_content = ENHANCED_KNOWLEDGE_BASE["troubleshooting"]["slow_migration"]
            else:
                matched_content = ENHANCED_KNOWLEDGE_BASE["troubleshooting"]["connection_issues"]
        elif best_match == "features":
            if "split" in user_message_lower or "pst" in user_message_lower:
                matched_content = ENHANCED_KNOWLEDGE_BASE["features"]["split_pst"]
            else:
                matched_content = ENHANCED_KNOWLEDGE_BASE["features"]["incremental_backup"]

    return {
        "category": best_match,
        "confidence": max_score,
        "content": matched_content,
        "is_relevant": max_score > 0
    }

def format_enhanced_response(content, category):
    """Format response with rich content"""
    if not content:
        return "I couldn't find specific information about that. Let me connect you with our support team!"

    response = f"## {content.get('title', 'Information')}

"

    # Add steps if available
    if 'steps' in content:
        response += "### 📋 Step-by-Step Instructions:
"
        for step in content['steps']:
            response += f"{step}

"

    # Add settings if available  
    if 'settings' in content:
        response += "### ⚙️ Settings:
"
        for key, value in content['settings'].items():
            response += f"**{key}**: `{value}`

"

    # Add tips if available
    if 'tips' in content:
        response += "### 💡 Pro Tips:
"
        for tip in content['tips']:
            response += f"{tip}

"

    # Add troubleshooting if available
    if 'troubleshooting' in content:
        response += "### 🔧 Troubleshooting:
"
        for issue in content['troubleshooting']:
            response += f"{issue}

"

    # Add benefits if available
    if 'benefits' in content:
        response += "### ✨ Benefits:
"
        for benefit in content['benefits']:
            response += f"{benefit}

"

    # Add common causes if available
    if 'common_causes' in content:
        response += "### 🔍 Common Causes:
"
        for cause in content['common_causes']:
            response += f"{cause}

"

    # Add speed improvements if available
    if 'speed_improvements' in content:
        response += "### ⚡ Speed Improvements:
"
        for improvement in content['speed_improvements']:
            response += f"{improvement}

"

    # Add app password steps if available
    if 'app_password_steps' in content:
        response += "### 🔑 App Password Setup:
"
        for step in content['app_password_steps']:
            response += f"{step}

"

    response += "
---
💬 **Need more help?** Contact our live support: [https://emailbackupwizard.com/support.html](https://emailbackupwizard.com/support.html)"

    return response

def generate_enhanced_response(user_message, search_result):
    """Generate enhanced, engaging responses"""
    if not search_result["is_relevant"]:
        return f"""🤔 Hmm, that's an interesting question! While I'd love to help with "{user_message}", it seems to be outside my expertise with Email Backup Wizard software.

🎯 **But don't worry!** Our amazing support team specializes in handling unique situations like yours.

### 🚀 Get Instant Help:
**Live Support**: [https://emailbackupwizard.com/support.html](https://emailbackupwizard.com/support.html)

### 👥 Our Support Team Rocks At:
• 🔧 **Technical troubleshooting** - They've seen it all!
• 🏢 **Account-specific issues** - Personalized solutions
• 🎨 **Custom migration scenarios** - Unique setups, no problem
• 💳 **Billing and licensing** - All your account questions

### 💡 **Quick Tip**: 
Try asking me about specific topics like:
• "How to login to Yahoo mail"
• "Office 365 admin setup"  
• "Why is my backup slow"
• "Gmail OAuth login"

I'm here to help! 😊"""

    category = search_result["category"]
    content = search_result["content"]

    # Handle special categories
    if category in ["yahoo", "aol", "gmail"]:
        return format_enhanced_response(content, category)

    # Handle general categories
    return format_enhanced_response(content, category)

# Initialize session state with a more engaging welcome message
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

# Enhanced header with animation
st.markdown("""
<div class="main-header">
    <h1>🚀 Email Backup Wizard Support</h1>
    <p>Your AI-powered migration assistant - Making email backup simple & fast!</p>
</div>
""", unsafe_allow_html=True)

# Chat interface
chat_container = st.container()

with chat_container:
    # Display chat messages with enhanced formatting
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

# Enhanced chat input with better prompts
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
            # Simulate more realistic processing time
            time.sleep(random.uniform(1.5, 2.5))

            # Search knowledge base
            search_result = enhanced_search_knowledge(prompt)

            # Generate response
            response = generate_enhanced_response(prompt, search_result)

            # Display response with typing effect simulation
            st.markdown(response)

    # Add assistant message to session state
    st.session_state.messages.append({
        "role": "assistant", 
        "content": response,
        "timestamp": datetime.now()
    })

# Enhanced sidebar with more features
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
        "Google Workspace configuration"
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

    st.markdown("---")
    st.markdown("### 🌟 Feedback")
    feedback = st.selectbox("How helpful was I?", ["Select...", "Very Helpful! 🌟", "Helpful 👍", "Okay 👌", "Needs Improvement 📝"])
    if feedback != "Select...":
        st.success(f"Thanks for your feedback: {feedback}")

# Enhanced footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666; padding: 20px;'>
    <p><strong>🚀 Powered by Streamlit • Email Backup Wizard AI Support</strong></p>
    <p>💡 <em>Making email migration simple, one question at a time!</em></p>
</div>
""", unsafe_allow_html=True)
