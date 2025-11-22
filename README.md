# 🚀 WordSmith - AI Text Companion

> Transform your text instantly with AI-powered tools right in your browser

![Chrome Extension](https://img.shields.io/badge/Chrome-Extension-4285F4?style=for-the-badge&logo=googlechrome&logoColor=white)
![React](https://img.shields.io/badge/React-20232A?style=for-the-badge&logo=react&logoColor=61DAFB)
![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)
![AI Powered](https://img.shields.io/badge/AI-Powered-FF6B6B?style=for-the-badge)

WordSmith is a powerful Chrome extension that leverages AI to transform your text in seconds. Whether you're writing emails, social media posts, or documents, WordSmith helps you communicate better with intelligent text transformations.

## 🌐 Live Demo

**Try WordSmith now!**

| Platform | Link |
|----------|------|
| 🌐 **Web App** | [https://word-smith-sand.vercel.app](https://word-smith-sand.vercel.app) |
| 🔌 **Backend API** | [https://wordsmith-backend-iatg.onrender.com](https://wordsmith-backend-iatg.onrender.com) |
| 📚 **API Docs** | [https://wordsmith-backend-iatg.onrender.com/docs](https://wordsmith-backend-iatg.onrender.com/docs) |

## ✨ Features

### 🎯 Text Transformations
Transform any text with these AI-powered tools:

| Feature | Description | Perfect For |
|---------|-------------|-------------|
| ✏️ **Grammar Fix** | Fix grammar, spelling, and punctuation errors | Professional writing, emails |
| 💼 **Formal Tone** | Convert to professional, business-appropriate language | Work emails, reports, proposals |
| 😊 **Friendly Tone** | Make text warm, conversational, and approachable | Social media, casual emails |
| ✂️ **Shorten** | Make text more concise while keeping key points | Twitter, summaries, headlines |
| 📝 **Expand** | Add more details, context, and explanations | Blog posts, articles, presentations |
| 🔘 **Bullet Points** | Convert paragraphs to clear, organized bullet lists | Meeting notes, action items |
| 😎 **Add Emojis** | Enhance text with contextually appropriate emojis | Social media, informal communication |
| 🐦 **Tweetify** | Optimize text for Twitter with hashtags and engagement | Social media marketing |

### 🔥 Multi-Select Transformations
- **Combine Multiple Transformations** - Apply up to 8 transformations at once!
- **Smart Conflict Detection** - Prevents incompatible selections (e.g., Formal + Friendly)
- **Sequential Processing** - Transformations applied in the order you select them
- **Visual Order Indicator** - See exactly how your text will be transformed

**Compatible Combinations:**
- ✅ Grammar + Formal + Shorten
- ✅ Grammar + Bullet + Emoji
- ✅ Friendly + Expand + Emoji
- ❌ Formal + Friendly (tone conflict)
- ❌ Shorten + Expand (length conflict)

### 📜 History & Saved Transformations
- **📋 History Tab** - View your last 7 days of transformations
- **⭐ Saved Tab** - Save favorite transformations permanently
- **🔄 Quick Reuse** - Easily reapply past transformations
- **🗑️ Bulk Delete** - Manage your transformation history efficiently

## 🎯 Why WordSmith?

- **🚀 Instant Results** - Transform text in seconds, no waiting
- **🎨 Multiple Styles** - 8 different transformation options
- **🔗 Chain Transformations** - Combine multiple transforms for perfect results
- **📜 Smart History** - Track and reuse your transformations
- **⭐ Save Favorites** - Keep important transformations forever
- **🔒 Privacy First** - Your data is stored locally and securely
- **⚡ Lightning Fast** - Powered by Groq's ultra-fast Llama 3.1 AI
- **💡 Smart Context** - AI understands your intent and maintains meaning
- **🔧 Developer Friendly** - Clean, well-documented codebase

## 🛠️ Tech Stack

**Frontend (Chrome Extension)**
- **React.js** - Modern component-based UI
- **Vite** - Next-generation frontend tooling
- **Chrome Manifest V3** - Latest extension architecture

**Backend (API Server)**
- **FastAPI** - High-performance Python web framework
- **SQLAlchemy** - SQL database ORM
- **Groq API** - Ultra-fast Llama 3.1 AI inference
- **SQLite** - Lightweight database for history storage

**Deployment**
- **Frontend** - Vercel
- **Backend** - Render

## 📦 Installation

### For Users (Chrome Extension)

#### Method 1: From GitHub Releases (Recommended)
1. 📥 [Download the latest release](https://github.com/harshitayadavv/WordSmith/releases/latest)
2. 📁 Extract the `wordsmith-extension.zip` file
3. 🌐 Open Chrome and navigate to `chrome://extensions/`
4. 🔧 Enable **"Developer mode"** (toggle in top-right)
5. 📂 Click **"Load unpacked"** and select the extracted folder
6. ✅ WordSmith will appear in your extensions toolbar!

#### Method 2: Build from Source
```bash
# Clone the repository
git clone https://github.com/harshitayadavv/WordSmith.git
cd WordSmith

# Build the extension
cd frontend
npm install
npm run build:extension

# Install in Chrome
# 1. Go to chrome://extensions/
# 2. Enable "Developer Mode" (top-right toggle)
# 3. Click "Load unpacked"
# 4. Select the 'frontend/dist' folder
```

## 🚀 Development Setup

### Prerequisites
- Node.js 16+ and npm
- Python 3.9+
- Groq API Key ([Get one here](https://console.groq.com))

### 🖥️ Backend Setup

```bash
# Navigate to backend directory
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Setup environment variables
cp .env.example .env
# Edit .env and add your GROQ_API_KEY

# Initialize database
python -c "from app.core.database import init_db; init_db()"

# Run development server
python run.py
```

The backend will be available at `http://localhost:8000`

### 🎨 Frontend Setup

```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Start development server (for web testing)
npm run dev

# Build for Chrome extension
npm run build:extension

# Build for web deployment
npm run build
```

## 🔧 Configuration

### Backend Environment Variables

Create a `.env` file in the `backend` directory:

```env
# Required: Groq API Key
GROQ_API_KEY=your_groq_api_key_here

# Optional: Server configuration
PORT=8000
HOST=0.0.0.0
DEBUG=True

# Optional: Database (SQLite by default)
DATABASE_URL=sqlite:///./wordsmith.db
```

### Getting Your Groq API Key
1. Visit [console.groq.com](https://console.groq.com)
2. Sign up for a free account
3. Navigate to API Keys section
4. Create a new API key
5. Copy and add it to your `.env` file

**Note:** Groq offers a generous free tier with ultra-fast inference!

### Frontend Configuration

Update the API URL in `frontend/src/utils/api.js`:

```javascript
// For local development
export const API_BASE_URL = 'http://127.0.0.1:8000';

// For production (already configured)
export const API_BASE_URL = 'https://wordsmith-backend-iatg.onrender.com';
```

## 📚 API Documentation

- **Production API Docs**: [https://wordsmith-backend-iatg.onrender.com/docs](https://wordsmith-backend-iatg.onrender.com/docs)
- **Local Development**: `http://localhost:8000/docs`

### Main Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/api/v1/transform` | Transform text with AI |
| `GET` | `/api/v1/history` | Get transformation history |
| `POST` | `/api/v1/history/save` | Save a transformation |
| `DELETE` | `/api/v1/history` | Delete history items |
| `GET` | `/api/v1/health` | Health check |
| `GET` | `/api/v1/transformations` | List available transformations |

## 🎮 Usage

### Basic Transformation
1. **Click the WordSmith extension icon** in your Chrome toolbar
2. **Paste or type your text** in the input area
3. **Select a transformation type** (Grammar Fix, Formal, etc.)
4. **Click "Transform"** and watch the magic happen!
5. **Copy the result** or click **⭐ Save** to keep it forever

### Multi-Select Transformation (Advanced)
1. **Select multiple transformation buttons** - Click multiple options (e.g., Grammar + Formal + Shorten)
2. **See the order** - Transformations will be applied sequentially in the order selected
3. **Smart conflicts** - Incompatible options will be automatically disabled
4. **Clear all** - Click "Clear All" to reset your selections
5. **Transform** - Click transform to apply all selected transformations in sequence

**Example Multi-Transform Flow:**
```
Original: "i has big mistake in email"
  ↓ Grammar Fix
"I have a big mistake in the email"
  ↓ Formal Tone  
"I have made a significant error in the email correspondence"
  ↓ Shorten
"I made an error in the email"
```

### History & Saved
6. **View History** to see your recent transformations (last 7 days)
7. **Check Saved** tab for your favorite transformations (permanent)
8. **Reuse** past transformations with one click

## 🤝 Contributing

We welcome contributions! Here's how to get started:

1. 🍴 **Fork** the repository
2. 🌿 **Create** a feature branch (`git checkout -b feature/amazing-feature`)
3. ✨ **Make** your changes
4. ✅ **Test** thoroughly (run both frontend and backend)
5. 💫 **Commit** your changes (`git commit -m 'Add amazing feature'`)
6. 📤 **Push** to the branch (`git push origin feature/amazing-feature`)
7. 🎯 **Open** a Pull Request

### Development Guidelines
- Follow existing code style and conventions
- Test all features before submitting
- Update documentation as needed
- Ensure backend server runs without errors
- Test extension in Chrome before submitting PR

## 📝 Project Structure

```
WordSmith/
├── frontend/               # Chrome extension & React app
│   ├── src/
│   │   ├── components/    # React components
│   │   │   ├── TransformButtons.jsx  # Multi-select UI
│   │   │   ├── History.jsx
│   │   │   ├── SavedChats.jsx
│   │   │   └── ...
│   │   ├── utils/         # API utilities
│   │   └── App.jsx        # Main app component
│   ├── public/            # Static assets & manifest
│   └── dist/              # Built extension (after npm run build)
│
├── backend/               # FastAPI backend
│   ├── app/
│   │   ├── api/          # API routes
│   │   ├── core/         # Database & config
│   │   ├── models/       # Database models
│   │   ├── services/     # Business logic
│   │   └── main.py       # FastAPI app
│   └── requirements.txt   # Python dependencies
│
└── README.md
```

## 🐛 Support & Issues

- 🐞 **Bug Reports**: [Open an issue](https://github.com/harshitayadavv/WordSmith/issues/new)
- 💡 **Feature Requests**: [Request a feature](https://github.com/harshitayadavv/WordSmith/issues/new)
- 💬 **Questions**: [Start a discussion](https://github.com/harshitayadavv/WordSmith/discussions)

## 🌟 Roadmap

- [x] **History Feature** - Track your transformations ✅
- [x] **Save Favorites** - Keep important transformations ✅
- [x] **Multi-Select Transformations** - Apply multiple transforms at once ✅
- [x] **Web App Deployment** - Live on Vercel ✅
- [x] **Backend Deployment** - Live on Render ✅
- [ ] **Custom Prompts** - Create your own transformation types
- [ ] **Firefox Extension** - Expand to Firefox Add-ons
- [ ] **Export/Import** - Backup your saved transformations
- [ ] **Dark Mode** - Eye-friendly dark theme
- [ ] **Keyboard Shortcuts** - Quick access to features
- [ ] **Cloud Sync** - Sync history across devices
- [ ] **Browser Context Menu** - Right-click to transform selected text

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 📊 Stats

![GitHub stars](https://img.shields.io/github/stars/harshitayadavv/WordSmith?style=social)
![GitHub forks](https://img.shields.io/github/forks/harshitayadavv/WordSmith?style=social)
![GitHub issues](https://img.shields.io/github/issues/harshitayadavv/WordSmith)
![GitHub last commit](https://img.shields.io/github/last-commit/harshitayadavv/WordSmith)

## 🙏 Acknowledgments

- Groq for ultra-fast AI inference
- FastAPI for the amazing Python framework
- React team for the excellent frontend library
- Chrome Extensions team for the platform
- Vercel & Render for hosting

---

<div align="center">

**Made with ❤️ by [Harshita](https://github.com/harshitayadavv)**

[🌐 Try Live Demo](https://word-smith-sand.vercel.app) • [⭐ Star this repo](https://github.com/harshitayadavv/WordSmith/stargazers) • [🐛 Report Bug](https://github.com/harshitayadavv/WordSmith/issues) • [💡 Request Feature](https://github.com/harshitayadavv/WordSmith/issues)

</div>