# ResumeAI – AI-Powered Resume Analyzer

ResumeAI is a full-stack AI-powered resume analysis application that helps job seekers evaluate their resumes against job descriptions. It extracts information from PDF resumes, identifies matching and missing skills, calculates a keyword-based skill match percentage, and provides AI-powered recommendations using Google Gemini.

🌐 **Live Demo:** https://resume-ai-xi-two.vercel.app/

---

## 🚀 Features

- **PDF Resume Upload:** Upload resumes in PDF format.
- **Resume Text Extraction:** Extracts text from uploaded PDF files.
- **Skill Detection:** Identifies relevant skills from resumes and job descriptions.
- **Skill Matching:** Displays matched and missing skills.
- **Match Percentage:** Calculates a keyword-based skill match percentage.
- **AI Recommendations:** Uses Google Gemini to generate personalized resume improvement suggestions.
- **Visual Dashboard:** Displays analysis results through an interactive dashboard.
- **Analysis History:** Stores previous resume analyses in a database.

---

## 🛠️ Tech Stack

### Frontend
- React.js
- Vite
- JavaScript
- HTML5
- CSS3

### Backend
- Python
- FastAPI
- SQLAlchemy
- PyPDF
- Google Gemini API

### Database
- SQLite (local development)
- PostgreSQL (production deployment)

### Deployment
- Vercel (Frontend)
- Render (Backend and PostgreSQL)

---

## 📂 Project Structure

```text
ResumeAI/
│
├── frontend/
│   ├── public/
│   ├── src/
│   │   ├── assets/
│   │   ├── App.jsx
│   │   ├── App.css
│   │   ├── index.css
│   │   └── main.jsx
│   ├── package.json
│   └── vite.config.js
│
├── backend/
│   ├── main.py
│   ├── database.py
│   ├── models.py
│   ├── requirements.txt
│   ├── .env
│   └── resumeai.db
│
└── README.md
```

---

## ⚙️ Installation and Setup

### 1. Clone the Repository

```bash
git clone https://github.com/hritik4160-oss/ResumeAI.git
```

Navigate into the project:

```bash
cd ResumeAI
```

### 2. Backend Setup

Navigate to the backend directory:

```bash
cd backend
```

Create a virtual environment:

```bash
python -m venv venv
```

Activate it on Windows:

```bash
venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

### 3. Configure Environment Variables

Create a `.env` file inside the backend directory.

Add:

```env
GEMINI_API_KEY=your_gemini_api_key
```

For local development, the application uses SQLite by default.

For production, configure `DATABASE_URL` with your PostgreSQL connection string.

**Never commit your `.env` file or expose your API keys.**

### 4. Start the Backend

From the backend directory, run:

```bash
uvicorn main:app --reload --port 8000
```

Backend API:

```text
http://127.0.0.1:8000
```

FastAPI documentation:

```text
http://127.0.0.1:8000/docs
```

### 5. Frontend Setup

Open another terminal and navigate to the frontend directory:

```bash
cd frontend
```

Install dependencies:

```bash
npm install
```

Start the development server:

```bash
npm run dev
```

Open the local frontend URL displayed in your terminal.

---

## 🔑 API Configuration

ResumeAI uses the Google Gemini API to generate AI-powered resume recommendations.

To configure it:

1. Obtain a Gemini API key through Google AI Studio.
2. Add the key to the backend `.env` file.
3. Restart the backend server.

Keep your API key private.

---

## 🌍 Live Deployment

ResumeAI is deployed using:

| Component | Platform |
|---|---|
| Frontend | Vercel |
| Backend | Render |
| Database | PostgreSQL |
| AI Integration | Google Gemini |

**Live Application:**  
https://resume-ai-xi-two.vercel.app/

---

## 📊 How It Works

1. Upload a PDF resume.
2. Enter the target job description.
3. The backend extracts text from the resume.
4. Relevant skills are identified from both the resume and job description.
5. The application calculates the skill match percentage.
6. Matched and missing skills are displayed.
7. Google Gemini generates AI-powered recommendations.
8. Analysis results are stored in the database.

---

## ⚠️ Disclaimer

The displayed match percentage is based on keyword and skill matching. It is not an official ATS score and does not guarantee selection for a job.

AI-generated recommendations are intended as guidance and should be reviewed before making changes to a resume.

---

## 🔮 Future Improvements

- More advanced resume parsing.
- Support for additional document formats.
- Job-role-specific recommendations.
- Resume improvement suggestions.
- Enhanced analytics and reporting.
- User authentication and personalized dashboards.

---

## 👨‍💻 Author

**Hritik**

GitHub: https://github.com/hritik4160-oss

---

## ⭐ Support

If you find ResumeAI useful, consider giving this repository a star!

Built with React, FastAPI, Python, PostgreSQL, and Google Gemini.
