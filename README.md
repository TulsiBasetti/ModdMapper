# 🧠 MoodMapper – Track Your Moods with Meaning

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

