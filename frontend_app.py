import streamlit as st
import requests
from datetime import date, datetime
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()
BASE_URL = os.getenv("BASE_URL")

# Fallback if BASE_URL missing
if not BASE_URL:
    st.error("❌ BASE_URL not found in .env file.")
    st.stop()

# Page setup
st.set_page_config(page_title="MoodMapper", page_icon="🧠", layout="centered")
st.title("🧠 MoodMapper")
st.caption("Track your moods and uncover emotional trends.")

# Tabs for UI
tab1, tab2, tab3, tab4 = st.tabs(["👤 User", "📅 Log Mood", "📋 Mood Logs", "📊 Insights"])

# -----------------------------------
# 👤 TAB 1: Register / View Users
# -----------------------------------
with tab1:
    st.subheader("Register New User")
    with st.form("register_user"):
        name = st.text_input("Name")
        email = st.text_input("Email")
        submitted = st.form_submit_button("Register")
        if submitted:
            res = requests.post(f"{BASE_URL}/users", json={"name": name, "email": email})
            if res.status_code == 200:
                st.success(f"✅ User registered! ID: {res.json()['user_id']}")
            else:
                st.error(f"❌ Registration failed: {res.text}")

    st.divider()

    st.subheader("All Users")
    if st.button("Refresh Users"):
        res = requests.get(f"{BASE_URL}/users")
        if res.status_code == 200:
            st.dataframe(res.json(), use_container_width=True)
        else:
            st.error("❌ Failed to fetch users.")

# -----------------------------------
# 📅 TAB 2: Log Mood
# -----------------------------------
with tab2:
    st.subheader("Log Your Mood")
    with st.form("log_mood_form"):
        uid = st.number_input("User ID", min_value=1)
        mood = st.selectbox("How are you feeling?", ["happy", "sad", "angry", "anxious", "excited", "neutral"])
        trigger_note = st.text_input("What triggered this mood?")
        mood_date_str = st.text_input("Date (YYYY-MM-DD)", value=str(date.today()))
        submit_mood = st.form_submit_button("Submit Mood")

        if submit_mood:
            try:
                datetime.strptime(mood_date_str, "%Y-%m-%d")
            except ValueError:
                st.error("❌ Invalid date format. Please use YYYY-MM-DD.")
                st.stop()

            payload = {
                "mood": mood,
                "trigger_note": trigger_note,
                "date": mood_date_str,
                "user_id": int(uid)
            }
            res = requests.post(f"{BASE_URL}/moods", json=payload)
            if res.status_code == 200:
                st.success("✅ Mood logged successfully!")
            else:
                st.error(f"❌ Failed to log mood: {res.text}")

# -----------------------------------
# 📋 TAB 3: View / Update / Delete Moods
# -----------------------------------
with tab3:
    st.subheader("View Moods")
    view_uid = st.number_input("User ID", min_value=1, key="view_uid")
    if st.button("Show Moods"):
        res = requests.get(f"{BASE_URL}/moods/{view_uid}")
        if res.status_code == 200:
            data = res.json()
            if data:
                st.dataframe(data, use_container_width=True)
            else:
                st.info("ℹ️ No mood logs found.")
        else:
            st.error("❌ Could not fetch moods.")

    st.divider()

    st.subheader("✏️ Update Mood Entry")
    mood_id = st.number_input("Mood ID to Update", min_value=1, key="update_id")
    new_mood = st.selectbox("New Mood", ["happy", "sad", "angry", "anxious", "excited", "neutral"])
    new_trigger_note = st.text_input("New Trigger Note")
    if st.button("Update Mood"):
        res = requests.put(f"{BASE_URL}/moods/{mood_id}", json={"mood": new_mood, "trigger_note": new_trigger_note})
        if res.status_code == 200:
            st.success("✅ Mood updated!")
        else:
            st.error(f"❌ Update failed: {res.text}")

    st.divider()

    st.subheader("🗑️ Delete Mood Entry")
    delete_id = st.number_input("Mood ID to Delete", min_value=1, key="delete_id")
    if st.button("Delete Mood"):
        res = requests.delete(f"{BASE_URL}/moods/{delete_id}")
        if res.status_code == 200:
            st.success("✅ Mood deleted!")
        else:
            st.error(f"❌ Failed to delete mood: {res.text}")

# -----------------------------------
# 📊 TAB 4: Mood Summary + Recent
# -----------------------------------
with tab4:
    st.subheader("📊 Mood Summary and Recent Activity")
    uid = st.number_input("User ID for Insights", min_value=1, key="insights_uid")

    col1, col2 = st.columns(2)

    with col1:
        if st.button("Get Mood Summary"):
            res = requests.get(f"{BASE_URL}/moods/stats/summary/{uid}")
            if res.status_code == 200:
                summary = res.json()
                if summary:
                    st.bar_chart(summary)
                else:
                    st.info("ℹ️ No summary data.")
            else:
                st.error("❌ Failed to fetch summary.")

    with col2:
        if st.button("Get Recent Moods"):
            res = requests.get(f"{BASE_URL}/moods/recent/{uid}")
            if res.status_code == 200:
                recent = res.json()
                if recent:
                    st.dataframe(recent)
                else:
                    st.info("ℹ️ No recent moods.")
            else:
                st.error("❌ Failed to fetch recent moods.")
