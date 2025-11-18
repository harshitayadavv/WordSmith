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
| • **Bullet Points** | Convert paragraphs to clear, organized bullet lists | Meeting notes, action items |
| 😎 **Add Emojis** | Enhance text with contextually appropriate emojis | Social media, informal communication |
| 🐦 **Tweetify** | Optimize text for Twitter with hashtags and engagement | Social media marketing |

## 🎯 Why WordSmith?

- **🚀 Instant Results** - Transform text in seconds, no waiting
- **🎨 Multiple Styles** - 8 different transformation options
- **🔒 Privacy First** - Your text is processed securely and not stored
- **⚡ Lightning Fast** - Powered by Groq's ultra-fast Llama 3.1 AI
- **💡 Smart Context** - AI understands your intent and maintains meaning
- **🔧 Developer Friendly** - Clean, well-documented codebase

## 🛠️ Tech Stack

**Frontend (Chrome Extension)**
- **React.js** - Modern component-based UI
- **Tailwind CSS** - Utility-first styling
- **Chrome Manifest V3** - Latest extension architecture

**Backend (API Server)**
- **FastAPI** - High-performance Python web framework
- **Groq API** - Ultra-fast Llama 3.1 inference
- **Railway** - Cloud deployment platform

## 📦 Installation & Demo

### 🌐 Try It Online First!
**Want to test WordSmith before installing?** Try the live web demo:
**[🚀 https://word-smith-three.vercel.app/](https://word-smith-three.vercel.app/)**

### For Users (Chrome Extension)

#### Method 1: GitHub Releases
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
# Go to chrome://extensions/ → Developer Mode → Load Unpacked → Select 'frontend/dist'
```

### For Developers

#### 🖥️ Backend Setup
```bash
# Navigate to backend directory
cd wordsmith_backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Setup environment variables
cp .env.example .env
# Add your GROQ_API_KEY to .env file

# Run development server
python run.py
```

#### 🎨 Frontend Setup
```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev

# Build for production
npm run build
```

## 🔧 Configuration

### Environment Variables

Create a `.env` file in the `wordsmith_backend` directory:

```env
# Required: Get your API key from https://console.groq.com
GROQ_API_KEY=your_groq_api_key_here

# Optional: Custom configuration
PORT=8000
DEBUG=true
```

### Getting Your Groq API Key
1. Visit [console.groq.com](https://console.groq.com)
2. Sign up for a free account
3. Generate an API key
4. Add it to your `.env` file

## 📚 API Documentation

- **Production API**: `https://wordsmith-production.up.railway.app/docs`
- **Local Development**: `http://localhost:8000/docs`

Interactive Swagger documentation with all endpoints, request/response examples, and testing capabilities.

## 🚀 Deployment

**Backend**: Automatically deployed to Railway from the `main` branch
**Frontend**: Distributed as Chrome extension via GitHub Releases

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
- Add tests for new features
- Update documentation as needed
- Ensure all checks pass before submitting PR

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🐛 Support & Issues

- 🐞 **Bug Reports**: [Open an issue](../../issues/new?template=bug_report.md)
- 💡 **Feature Requests**: [Request a feature](../../issues/new?template=feature_request.md)
- 💬 **Questions**: [Start a discussion](../../discussions)

## 🌟 Roadmap

- [ ] **Firefox Extension** - Expand to Firefox Add-ons
- [ ] **Custom Prompts** - Allow users to create custom transformations
- [ ] **Batch Processing** - Process multiple texts at once
- [ ] **History & Favorites** - Save and revisit transformations
- [ ] **Team Features** - Share and collaborate on text transformations
- [ ] **API Rate Limiting** - Smart usage optimization

## 📊 Stats

![GitHub stars](https://img.shields.io/github/stars/yourusername/wordsmith?style=social)
![GitHub forks](https://img.shields.io/github/forks/yourusername/wordsmith?style=social)
![GitHub issues](https://img.shields.io/github/issues/yourusername/wordsmith)
![GitHub last commit](https://img.shields.io/github/last-commit/yourusername/wordsmith)

---

<div align="center">

**Made with ❤️ by Harshita**

[⭐ Star this repo](../../stargazers) • [🐛 Report Bug](../../issues) • [💡 Request Feature](../../issues)

</div>
