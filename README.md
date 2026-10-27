# AlumniConnect - Centralized Alumni Data Management & Engagement Platform

**SIH Problem Statement Code:** `SIH25017`  
**Subtitle:** Centralized Alumni Data Management & Engagement Platform  

---

## 📌 Project Overview

**AlumniConnect** is a centralized college-specific Alumni Management and Engagement Platform built for Smart India Hackathon (**SIH25017**). It bridges the gap between students, alumni, and college administration by solving the core problems of:
1. **Fragmented Alumni Records** scattered across social networks and spreadsheets.
2. **Difficulty Finding Suitable Mentors** matching a student's specific career trajectory.
3. **Manual Event Management** for reunions, webinars, and technical talks.
4. **Poor Communication** regarding job/internship referrals and college updates.
5. **Lack of Analytics** to track alumni achievements and engagement.

---

## 🛠️ Technology Stack

- **Frontend:** HTML5, Jinja2 Templates, Vanilla JavaScript, Tailwind CSS.
- **Backend Framework:** Python Flask (Modular Architecture with Blueprints).
- **Database:** SQLite with Flask-SQLAlchemy ORM & Flask-Login authentication.
- **Machine Learning & NLP:** Scikit-learn (`TfidfVectorizer`, `cosine_similarity`), NLTK (Tokenization, stop-words cleaning).
- **Data Analysis & Analytics:** Pandas, NumPy.
- **Interactive Visualizations:** Plotly (Embedded interactive charts in Jinja2 templates).

---

## 🚀 Key Features

### A. Student Portal
- **Dashboard:** Key metrics, top AI mentor matches, upcoming events, and bulletins.
- **Profile Management:** Academic details, skills, interests, career goals, preferred industry, location.
- **AI Mentor Matching Engine:** TF-IDF & Cosine Similarity vector matching with match percentages and explainable match reasons.
- **Alumni Directory:** Backend search and multi-select filtering by department, graduation year, industry, location, and skills.
- **Mentorship Requests:** Send guidance notes and monitor request statuses (Pending, Accepted, Rejected, Completed).
- **Opportunities Board:** Search full-time jobs and AI-scored internship recommendations.
- **Event Registrations:** Single-click RSVP for college webinars, reunions, and workshops.
- **Notifications & Bulletins:** Activity notification bell and college announcements.

### B. Alumni Portal
- **Dashboard:** Pending mentorship requests, active mentees, posted jobs, and engagement metrics.
- **Professional Profile:** Current company, job title, industry sector, location, experience, skills, bio, LinkedIn URL, and mentorship availability toggle.
- **Mentorship Management:** Accept, reject, or mark mentorship requests as completed.
- **Opportunities Posting:** Post full-time jobs and internships directly for college juniors.
- **Achievements Showcase:** Publish career milestones, IEEE papers, and industry awards.
- **Event RSVPs & Bulletins:** Register for alumni meets and view administrative notices.

### C. Administration Console
- **Dashboard:** Real-time KPI summary cards (Total Students, Total Alumni, Verified Alumni, Active Mentors, Jobs, Internships, Events, Requests).
- **User Management:** Search, view, delete, and toggle profile verification status for alumni.
- **Opportunity Moderation:** Manage and delete full-time jobs and internships.
- **Event Organization:** Create, schedule, and broadcast webinars, reunions, and technical talks.
- **Announcement Broadcasting:** Publish official notices with instant notification delivery to all users.
- **Plotly Analytics Dashboard:** 10 interactive Plotly charts powered by Pandas data aggregations.

---

## 🧠 Machine Learning Pipeline (`ml/recommendation_engine.py`)

```
Student Profile Text (Skills + Goals + Department + Industry)
                        ↓
             NLTK Text Preprocessing
         (Lowercasing, Tokenization, Stopwords)
                        ↓
            TF-IDF Vector Extraction
                        ↓
         Cosine Similarity Matrix Calculation
                        ↓
        Multi-Factor Weighted Final Scoring
(TF-IDF 40% + Skill Match 30% + Dept 15% + Industry/Goal 15%)
                        ↓
     Explainable Output (Match % + Reasons List)
```

### Explainability Example
- **Match:** 92% (Excellent Match)
- **Reasons:**
  - Same Department (*Artificial Intelligence & Data Science*)
  - Matching Skills: *Python, Machine Learning*
  - Aligned Career Goal (*Senior AI Research Engineer*)

---

## 📊 Plotly Analytics Dashboard (10 Interactive Charts)

1. **Alumni Distribution by Department** (Donut Chart)
2. **Alumni Distribution by Graduation Year** (Bar Chart)
3. **Alumni Top Industry Sectors** (Horizontal Bar Chart)
4. **Alumni Geographic Location** (Bar Chart)
5. **Monthly User Registrations Trend** (Line Chart)
6. **Mentorship Request Status Breakdown** (Donut Chart)
7. **Jobs vs Internships Posted** (Grouped Bar Chart)
8. **Event Registration & Participation** (Bar Chart)
9. **Top In-Demand Alumni Skills** (Horizontal Bar Chart)
10. **Platform Engagement Growth Index** (Area Chart)

---

## 🔐 Default Demo Accounts

The project includes pre-seeded accounts for evaluators:

| Role | Email | Password |
| :--- | :--- | :--- |
| **Admin** | `admin@alumniconnect.com` | `admin123` |
| **Student** | `student@alumniconnect.com` | `student123` |
| **Alumni** | `alumni@alumniconnect.com` | `alumni123` |

---

## ⚡ Installation & Execution Guide

### 1. Prerequisites
Ensure **Python 3.10+** and `pip` are installed on your system.

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Seed Database (Generates 20+ Students, 30+ Alumni, Jobs, Internships, Events)
```bash
python seed.py
```

### 4. Run Application
```bash
python app.py
```

Open your browser and navigate to: **`http://localhost:5000`**

---

## 🧪 SIH Demonstration Workflow

1. **Admin Login:** Log in as `admin@alumniconnect.com`. Inspect KPIs, toggle alumni profile verification status, and view the **10 Plotly Analytics Charts**.
2. **Student Login:** Log in as `student@alumniconnect.com`. Go to **AI Match Mentors**. Inspect match scores and explainable match reasons.
3. **Send Request:** Click **Request Mentorship** to send a request to alumni Priya Kumar (`alumni@alumniconnect.com`).
4. **Alumni Login:** Log in as `alumni@alumniconnect.com`. Accept the mentorship request.
5. **Post Opportunity:** As alumni, post a new internship position (*e.g., Data Science Intern*).
6. **Student Verification:** Log in back as student. View recommended internships with match percentage, apply, and register for an upcoming Alumni Meet event.
7. **Real-time Analytics Update:** Return to Admin dashboard to confirm updated event registrations and request counters.
