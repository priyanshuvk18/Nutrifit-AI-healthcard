# Quick Start Guide

## Prerequisites
- Python 3.8+
- MongoDB (local or MongoDB Atlas)
- Tesseract OCR installed
- OpenAI API key

## Installation

### 1. Clone the Repository
```bash
git clone <repository-url>
cd AI-Powered-Personal-Diet
```

### 2. Install Dependencies

**Backend:**
```bash
pip install -r requirements.txt
```

**Key packages:**
- fastapi
- uvicorn
- motor (MongoDB async driver)
- openai
- pytesseract
- pdf2image
- pdfplumber
- tensorflow
- scikit-learn
- sentence-transformers
- faiss-cpu
- reportlab
- pillow

### 3. Set Up Environment Variables

Create a `.env` file in the root directory:

```env
# MongoDB
MONGODB_URL=mongodb://localhost:27017
DATABASE_NAME=nutrifit_db

# OpenAI API
OPENAI_API_KEY=your_openai_api_key_here

# Tesseract (Windows example)
TESSERACT_CMD=C:/Program Files/Tesseract-OCR/tesseract.exe

# JWT Secret
SECRET_KEY=your_secret_key_here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# App Settings
APP_NAME=NutriFit AI
DEBUG=True
```

### 4. Install Tesseract OCR

**Windows:**
- Download from: https://github.com/UB-Mannheim/tesseract/wiki
- Install and note the installation path
- Update `TESSERACT_CMD` in `.env`

**Linux:**
```bash
sudo apt-get install tesseract-ocr
sudo apt-get install poppler-utils
```

**macOS:**
```bash
brew install tesseract
brew install poppler
```

### 5. Start MongoDB

**Local MongoDB:**
```bash
mongod
```

**Or use MongoDB Atlas:**
- Create account at mongodb.com
- Create cluster
- Get connection string
- Update `MONGODB_URL` in `.env`

### 6. Run the Application

**Start Backend Server:**
```bash
# Run from the root directory (AI-Powered Personal Diet)
uvicorn backend.main:app --reload --host 0.0.0.0 --port 8001
```

The API will be available at: `http://localhost:8001`
API Documentation: `http://localhost:8001/docs`


**Serve Frontend:**
Option 1 - Python HTTP Server:
```bash
cd frontend
python -m http.server 3000
```

Option 2 - Live Server (VS Code extension):
- Install "Live Server" extension
- Right-click `index.html` → "Open with Live Server"

Frontend will be available at: `http://localhost:5500`

### 7. Run Tests
```bash
# Run from the root directory
pytest
```


### 7. Create Admin User

First, register a normal user through the UI, then update in MongoDB:

```javascript
// In MongoDB shell or Compass
use nutrifit_db
db.users.updateOne(
  { email: "your-email@example.com" },
  { $set: { is_admin: true } }
)
```

---

## 📱 Usage Guide

### For Regular Users:

1. **Register/Login**: Create an account at `/index.html`

2. **Upload Medical Report**:
   - Navigate to "Upload Report"
   - Upload PDF or image of blood test/medical report
   - Wait for OCR extraction (10-30 seconds)
   - View extracted metrics and risk assessment

3. **Explore Calculators**:
   - Go to "Calculators"
   - Use BMI, BMR, TDEE, Macros, or Water calculators
   - Results auto-populate between calculators

4. **Track Food**:
   - Navigate to "Food Tracker"
   - Upload food image OR search manually
   - Log meals by type (Breakfast/Lunch/Dinner/Snack)
   - View daily nutrition summary

5. **Chat with AI**:
   - Go to "AI Assistant"
   - Type or use 🎤 voice input
   - Ask health/nutrition questions
   - Get personalized, grounded responses

6. **View Rewards**:
   - Check "Rewards" page
   - See your points, level, badges
   - Track achievements and progress
   - Compete on leaderboard

7. **Manage Profile**:
   - Update personal info
   - Set health goals
   - View calculated metrics

### For Admins:

1. **Access Admin Panel**:
   - Click "Admin Dashboard" in nav (only visible to admins)

2. **Monitor System**:
   - View total users, reports, plans
   - Check risk distribution
   - Analyze top foods logged

3. **Manage Users**:
   - View all users with pagination
   - Toggle admin status
   - Delete users (with all their data)

4. **Review Reports**:
   - Filter reports by risk level
   - View extracted metrics
   - Monitor upload trends

---

## 🔑 Key API Endpoints

### Authentication
- `POST /auth/register` - Register new user
- `POST /auth/login` - Login
- `GET /auth/me` - Get current user profile

### Health Reports
- `POST /health/upload` - Upload medical report
- `GET /health/reports` - Get user's reports
- `GET /health/reports/{id}` - Get specific report
- `DELETE /health/reports/{id}` - Delete report

### Plans
- `POST /health/generate-plans` - Generate diet + workout plans
- `GET /plans` - Get user's plans

### Food Tracking
- `POST /food/recognize` - Upload food image
- `POST /food/search` - Search food database
- `POST /food/log` - Log food entry
- `GET /food/logs` - Get user's food logs

### Chatbot
- `POST /food/chat` - Send message to AI assistant

### Calculators (NEW)
- `POST /calculators/bmi` - Calculate BMI
- `POST /calculators/bmr` - Calculate BMR
- `POST /calculators/tdee` - Calculate TDEE
- `POST /calculators/macros` - Calculate macros
- `POST /calculators/water-intake` - Calculate water needs

### Gamification (NEW)
- `GET /gamification/points` - Get user points and level
- `POST /gamification/award-points` - Award points
- `GET /gamification/badges` - Get badges status
- `GET /gamification/achievements` - Get achievements
- `POST /gamification/unlock-achievement` - Unlock achievement
- `GET /gamification/leaderboard` - Get leaderboard

### PDF Export (NEW)
- `POST /pdf/export-diet-plan/{id}` - Export diet plan PDF
- `POST /pdf/export-workout-plan/{id}` - Export workout plan PDF
- `POST /pdf/export-health-summary` - Export health summary PDF

### Admin
- `GET /admin/stats` - System statistics
- `GET /admin/users` - All users (paginated)
- `PUT /admin/users/{id}/toggle-admin` - Toggle admin status
- `DELETE /admin/users/{id}` - Delete user
- `GET /admin/reports` - All reports (with filters)
- `GET /admin/analytics` - Health analytics

---

## 🎯 Hackathon Demo Script

### 5-Minute Demo Flow:

**1. Introduction (30s)**
- Problem: Fragmented health data, generic advice
- Solution: NutriFit AI - personalized health with gamification

**2. Core Features (2min)**
- Upload medical report → OCR extraction → Risk assessment
- Generate AI-powered diet + workout plans
- Food tracker with image recognition

**3. Hackathon Features (1.5min)**
- **Calculators**: Run through BMI → BMR → TDEE → Macros
- **Gamification**: Show badges, achievements, leaderboard
- **Voice Input**: Ask chatbot question with voice 🎤
- **PDF Export**: Download professional health summary

**4. Admin Dashboard (30s)**
- System-wide analytics
- User management capabilities
- Scalability demonstration

**5. Closing (30s)**
- 15+ features, production-ready
- $175B market opportunity
- Clear business model
- Thank you + Q&A

---

## 🐛 Troubleshooting

### Tesseract Not Found
```
Error: Tesseract not found
```
**Fix**: Install Tesseract and update `TESSERACT_CMD` path in `.env`

### MongoDB Connection Error
```
Error: Could not connect to MongoDB
```
**Fix**: 
- Ensure MongoDB is running: `mongod`
- Check `MONGODB_URL` in `.env`
- For Atlas: whitelist your IP

### OpenAI API Error
```
Error: Incorrect API key provided
```
**Fix**: Add valid OpenAI API key to `.env`

### Port Already in Use
```
Error: Address already in use
```
**Fix**: 
- Kill process: `netstat -ano | findstr :8000` (Windows)
- Or use different port: `uvicorn main:app --port 8001`

---

## 📊 Project Structure

```
AI-Powered-Personal-Diet/
├── backend/
│   ├── main.py                 # FastAPI app entry point
│   ├── routers/
│   │   ├── auth.py            # Authentication routes
│   │   ├── health.py          # Medical reports & plans
│   │   ├── food.py            # Food tracking & chatbot
│   │   ├── admin.py           # Admin panel routes
│   │   ├── calculators.py     # Health calculators (NEW)
│   │   ├── gamification.py    # Gamification system (NEW)
│   │   └── pdf_export.py      # PDF generation (NEW)
│   ├── ocr/
│   │   └── medical_ocr.py     # Tesseract OCR logic
│   ├── ml/
│   │   ├── food_recognition.py # CNN food classifier
│   │   └── chatbot_rag.py      # RAG chatbot
│   ├── utils/
│   │   └── pdf_generator.py   # ReportLab PDFs (NEW)
│   ├── schemas.py              # Pydantic models
│   ├── database.py             # MongoDB connection
│   ├── auth.py                 # JWT authentication
│   └── config.py               # Settings
├── frontend/
│   ├── pages/
│   │   ├── index.html          # Login/Register
│   │   ├── dashboard.html      # Main dashboard
│   │   ├── upload.html         # Report upload
│   │   ├── food-tracker.html   # Food logging
│   │   ├── calculators.html    # Health calculators (NEW)
│   │   ├── rewards.html        # Gamification (NEW)
│   │   ├── plans.html          # Diet/Workout plans
│   │   ├── chatbot.html        # AI assistant
│   │   ├── profile.html        # User profile
│   │   └── admin-*.html        # Admin pages
│   ├── css/
│   │   ├── style.css           # Main styles
│   │   └── animations.css      # Animation library (NEW)
│   └── js/
│       ├── config.js           # API config
│       ├── auth.js             # Auth logic
│       ├── dashboard.js
│       ├── calculators.js      # Calculator logic (NEW)
│       ├── toast.js            # Toast notifications (NEW)
│       └── *.js                # Page-specific scripts
├── .env.example                # Environment template
├── requirements.txt            # Python dependencies
├── README.md                   # This file
└── PITCH.md                    # Hackathon pitch doc (NEW)
```

---

## 👥 Contributing

This is a hackathon project. Contributions welcome!

1. Fork the repository
2. Create feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open Pull Request

---

## 📄 License

MIT License - feel free to use for your own projects!

---

## 🙏 Acknowledgments

- OpenAI for GPT-4 API
- Tesseract OCR team
- FastAPI and MongoDB communities
- All open-source contributors

---

## 📞 Contact

For questions or demo requests, please open an issue on GitHub.

---

**Built with ❤️ for [Hackathon Name] - NutriFit AI Team**
