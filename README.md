# WordSmith - AI Text Companion

A Chrome extension that transforms your text using AI-powered transformations including grammar fixes, tone changes, and more.

## Features

- ✏️ Grammar Fix - Fix grammar, spelling, and punctuation errors
- 💼 Formal - Convert to professional tone
- 😊 Friendly - Make text warm and conversational
- ✂️ Shorten - Make text more concise
- 📝 Expand - Add more details and explanations
- • Bullet Points - Convert to bullet point format
- 😎 Emoji - Add appropriate emojis
- 🐦 Tweetify - Convert to tweet format

## Tech Stack

**Frontend:**
- React.js
- Tailwind CSS
- Chrome Extension Manifest V3

**Backend:**
- FastAPI
- Groq API (Llama 3.1)
- Python 3.8+

## Installation

### For Users
1. Download the latest release from [Releases](link-to-releases)
2. Extract the zip file
3. Open Chrome and go to `chrome://extensions/`
4. Enable "Developer mode"
5. Click "Load unpacked" and select the extracted folder

### For Developers

#### Backend Setup
```bash
cd wordsmith_backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt

# Create .env file
cp .env.example .env
# Add your GROQ_API_KEY to .env

python run.py
```

#### Frontend Setup
```bash
cd frontend
npm install
npm run build
```

## Environment Variables

Create a `.env` file in the backend directory:
```
GROQ_API_KEY=your_groq_api_key_here
```

Get your Groq API key from [console.groq.com](https://console.groq.com)

## API Documentation

When running locally, visit http://localhost:8000/docs for interactive API documentation.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

MIT License - see LICENSE file for details

## Support

For support, please open an issue on GitHub or contact [your-email].
