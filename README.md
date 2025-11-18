# 🚀 WordSmith - AI Text Companion

> Transform your text instantly with AI-powered tools right in your browser

![Chrome Extension](https://img.shields.io/badge/Chrome-Extension-4285F4?style=for-the-badge&logo=googlechrome&logoColor=white)
![React](https://img.shields.io/badge/React-20232A?style=for-the-badge&logo=react&logoColor=61DAFB)
![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)
![AI Powered](https://img.shields.io/badge/AI-Powered-FF6B6B?style=for-the-badge)

WordSmith is a powerful Chrome extension that leverages AI to transform your text in seconds. Whether you're writing emails, social media posts, or documents, WordSmith helps you communicate better with intelligent text transformations.

## ✨ Features

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

### 📜 History & Saved Transformations
- **📋 History Tab** - View your last 7 days of transformations
- **⭐ Saved Tab** - Save favorite transformations permanently
- **🔄 Quick Reuse** - Easily reapply past transformations
- **🗑️ Bulk Delete** - Manage your transformation history

## 🎯 Why WordSmith?

- **🚀 Instant Results** - Transform text in seconds, no waiting
- **🎨 Multiple Styles** - 8 different transformation options
- **📜 Smart History** - Track and reuse your transformations
- **⭐ Save Favorites** - Keep important transformations forever
- **🔒 Privacy First** - Your data is stored locally and securely
- **⚡ Lightning Fast** - Powered by Claude AI for best results
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
- **Anthropic Claude** - Advanced AI for text transformations
- **SQLite** - Lightweight database for history storage

## 📦 Installation

### For Users (Chrome Extension)

#### Method 1: From GitHub Releases (Recommended)
1. 📥 [Download the latest release](../../releases/latest)
2. 📁 Extract the `wordsmith-extension.zip` file
3. 🌐 Open Chrome and navigate to `chrome://extensions/`
4. 🔧 Enable **"Developer mode"** (toggle in top-right)
5. 📂 Click **"Load unpacked"** and select the extracted folder
6. ✅ WordSmith will appear in your extensions toolbar!

#### Method 2: Build from Source
```bash
# Clone the repository
git clone https://github.com/yourusername/wordsmith.git
cd wordsmith

# Build the extension
cd frontend
npm install
npm run build

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
- Anthropic API Key ([Get one here](https://console.anthropic.com/))

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
# Edit .env and add your ANTHROPIC_API_KEY

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
npm run build
```

For extension development:
1. Run `npm run build` to create the `dist` folder
2. Load the `dist` folder in Chrome as an unpacked extension
3. Make changes to the code
4. Run `npm run build` again
5. Click the refresh icon in `chrome://extensions/` to see changes

## 🔧 Configuration

### Backend Environment Variables

Create a `.env` file in the `backend` directory:

```env
# Required: Anthropic API Key
ANTHROPIC_API_KEY=your_anthropic_api_key_here

# Optional: Server configuration
PORT=8000
HOST=0.0.0.0
DEBUG=True

# Optional: Database (SQLite by default)
DATABASE_URL=sqlite:///./wordsmith.db
```

### Getting Your Anthropic API Key
1. Visit [console.anthropic.com](https://console.anthropic.com/)
2. Sign up for an account
3. Navigate to API Keys
4. Generate a new API key
5. Add it to your `.env` file

### Frontend Configuration

Update the API URL in `frontend/src/utils/api.js`:

```javascript
// For local development
export const API_BASE_URL = 'http://127.0.0.1:8000';

// For production deployment
export const API_BASE_URL = 'https://your-backend-url.com';
```

## 📚 API Documentation

When the backend is running, visit:
- **Interactive API Docs**: `http://localhost:8000/docs`
- **Alternative Docs**: `http://localhost:8000/redoc`

### Main Endpoints

- `POST /api/v1/transform` - Transform text with AI
- `GET /api/v1/history` - Get transformation history
- `POST /api/v1/history/save` - Save a transformation
- `DELETE /api/v1/history` - Delete history items
- `GET /api/v1/health` - Health check

## 🎮 Usage

1. **Click the WordSmith extension icon** in your Chrome toolbar
2. **Paste or type your text** in the input area
3. **Select a transformation type** (Grammar Fix, Formal, etc.)
4. **Click "Transform"** and watch the magic happen!
5. **Copy the result** or click **⭐ Save** to keep it forever
6. **View History** to see your recent transformations
7. **Check Saved** tab for your favorite transformations

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
wordsmith/
├── frontend/               # Chrome extension & React app
│   ├── src/
│   │   ├── components/    # React components
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

- 🐞 **Bug Reports**: [Open an issue](../../issues/new?template=bug_report.md)
- 💡 **Feature Requests**: [Request a feature](../../issues/new?template=feature_request.md)
- 💬 **Questions**: [Start a discussion](../../discussions)

## 🌟 Roadmap

- [x] **History Feature** - Track your transformations ✅
- [x] **Save Favorites** - Keep important transformations ✅
- [ ] **Multi-Select Transformations** - Apply multiple transforms at once
- [ ] **Custom Prompts** - Create your own transformation types
- [ ] **Firefox Extension** - Expand to Firefox Add-ons
- [ ] **Export/Import** - Backup your saved transformations
- [ ] **Dark Mode** - Eye-friendly dark theme
- [ ] **Keyboard Shortcuts** - Quick access to features
- [ ] **Cloud Sync** - Sync history across devices

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 📊 Stats

![GitHub stars](https://img.shields.io/github/stars/yourusername/wordsmith?style=social)
![GitHub forks](https://img.shields.io/github/forks/yourusername/wordsmith?style=social)
![GitHub issues](https://img.shields.io/github/issues/yourusername/wordsmith)
![GitHub last commit](https://img.shields.io/github/last-commit/yourusername/wordsmith)

## 🙏 Acknowledgments

- Anthropic Claude for powerful AI transformations
- FastAPI for the amazing Python framework
- React team for the excellent frontend library
- Chrome Extensions team for the platform

---

<div align="center">

**Made with ❤️ by [Your Name]**

[⭐ Star this repo](../../stargazers) • [🐛 Report Bug](../../issues) • [💡 Request Feature](../../issues)

</div>
