# 🧠 MoodMapper – A RESTful Mood Tracking API with Insights and UI

MoodMapper is a mood journaling platform that helps users log daily emotions and understand their emotional patterns over time. It features a custom-built REST API using Flask and MySQL, with an optional modern frontend powered by Streamlit.

---

## 🚀 Features

- 🧾 REST API with 8 endpoints
- 👤 User registration and listing
- 📅 Mood logging with trigger notes
- ✏️ Edit and delete mood logs
- 📊 View mood summary and recent activity
- 💻 Frontend using Streamlit
- 🔐 Secrets and URLs stored in `.env`
- ✅ API tested using Postman

---

## 📦 Tech Stack

| Layer        | Technology                    |
|--------------|-------------------------------|
| Backend      | Python + Flask (REST API)     |
| Database     | MySQL (`mysql-connector-python`) |
| Frontend     | Streamlit (optional UI)       |
| Config       | `.env` file for secure secrets |
| API Testing  | Postman                       |

---

## 🔌 API Endpoints

### 👤 User APIs

| Method | Endpoint     | Description        |
|--------|--------------|--------------------|
| POST   | `/users`     | Register a new user |
| GET    | `/users`     | List all users     |

### 📅 Mood APIs

| Method | Endpoint                | Description                     |
|--------|-------------------------|---------------------------------|
| POST   | `/moods`                | Log a new mood                  |
| GET    | `/moods/<int:user_id>`  | View all moods for a user       |
| PUT    | `/moods/<int:id>`       | Update a specific mood entry    |
| DELETE | `/moods/<int:id>`       | Delete a specific mood entry    |

### 📊 Insights APIs

| Method | Endpoint                                  | Description               |
|--------|-------------------------------------------|---------------------------|
| GET    | `/moods/stats/summary/<int:user_id>`      | Mood counts by type       |
| GET    | `/moods/recent/<int:user_id>`             | 5 most recent mood entries|

---

## 🗃️ Database Schema

You can either use the SQL below or run the provided `mysql.sql` script.

```sql
CREATE DATABASE IF NOT EXISTS moodmapper;
USE moodmapper;

CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE
);

CREATE TABLE IF NOT EXISTS moods (
    id INT AUTO_INCREMENT PRIMARY KEY,
    mood VARCHAR(50) NOT NULL,
    trigger_note TEXT,
    date DATE NOT NULL,
    user_id INT,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

```
## ⚙️ Environment Setup (`.env`)

Create a `.env` file in your project root directory with the following content:

```env
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=your_mysql_password
DB_NAME=moodmapper
BASE_URL=http://127.0.0.1:5000
```
✅ The frontend uses BASE_URL to point to the backend — helpful for future deployment flexibility.

##🧑‍💻 How to Run the Project
1. Clone & Install
```
git clone https://github.com/your-username/moodmapper.git
cd moodmapper

# Create virtual environment
 python -m venv moodmapper_venv
 moodmapper_venv\Scripts\activate   # Windows
 source moodmapper_venv/bin/activate  # macOS/Linux

# Install dependencies
 pip install -r requirements.txt

```
2. Set Up Database
You can either:
- Run mysql.sql in SQLYog or MySQL CLI, or
- Paste the SQL schema (shown above)
- Make sure the database name is moodmapper.


3. Run Flask Backend (Terminal 1)
```
    python app.py
```

4. Run Streamlit Frontend (Terminal 2)
```
streamlit run frontend_app.py
```

 Keep both Flask and Streamlit running in separate terminals for full functionality.

 ## 📮 Testing the API with Postman
 All 8 API endpoints were tested using Postman to ensure:
- Correct request/response formats
- Expected HTTP status codes
- Error handling and validations

You can import a Postman collection or test manually using POST, GET, PUT, DELETE methods with the base URL:
http://127.0.0.1:5000/

## 📊 Sample API Request

### POST /moods
```
{
  "mood": "happy",
  "trigger_note": "Completed the project",
  "date": "2025-06-19",
  "user_id": 1
}

```
Response:
```
{
  "message": "Mood logged successfully"
}

```





