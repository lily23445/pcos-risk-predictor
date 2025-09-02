# pages/exercises.py
import time, webbrowser
import streamlit as st
import utils.nav as nav

# ──────────────────────────────────────────────────────────────
# Page setup & auth gate
# ──────────────────────────────────────────────────────────────
st.set_page_config(page_title="PCOS Tracker | Exercises",
                   page_icon="💪", layout="wide")
nav.render_menu()

if not getattr(st.user, "is_logged_in", False):
    st.switch_page("../Login.py")

# Defaults
st.session_state.setdefault("workout_log", [])
st.session_state.setdefault("weekly_progress", 0)

# ──────────────────────────────────────────────────────────────
# Static exercise library  (add / edit anytime)
# ──────────────────────────────────────────────────────────────
EXERCISES = [
    {
        "title": "HIIT Strength Circuit",
        "icon": "🔥",
        "difficulty": "Intermediate",
        "duration": "20-30 min",
        "type": "HIIT",
        "focus": "Insulin Resistance",
        "description": "High-intensity intervals combining body-weight moves to spike glucose utilisation and boost metabolism.",
        "benefits": ["Improves insulin sensitivity≈40%", "24-h post-burn", "Builds lean muscle"],
        "routine": ["Burpees (30s)", "Mountain Climbers (30s)", "Jump Squats (30s)", "Rest (30s)"],
        "video": "https://youtu.be/ml6cT4AZdqI",
    },
    {
        "title": "Resistance Training Basics",
        "icon": "💪",
        "difficulty": "Beginner",
        "duration": "20-30 min",
        "type": "Strength",
        "focus": "Weight Loss",
        "description": "Foundational lifts with body-weight & light dumbbells to raise basal metabolic rate.",
        "benefits": ["Builds muscle", "Increases metabolism", "Strengthens bones"],
        "routine": ["Squats (12)", "Push-ups (10)", "Lunges (10/leg)", "Plank (30s)"],
        "video": "https://youtu.be/U0bhE67HuDY",
    },
    {
        "title": "Gentle Yoga Flow",
        "icon": "🧘‍♀️",
        "difficulty": "Beginner",
        "duration": "15-20 min",
        "type": "Yoga",
        "focus": "Stress Relief",
        "description": "Calming poses that lower cortisol and improve flexibility.",
        "benefits": ["Reduces stress hormones", "Enhances sleep", "Improves mobility"],
        "routine": ["Cat-Cow (1 min)", "Child's Pose (2 min)", "Warrior II (1 min/side)", "Savasana (5 min)"],
        "video": "https://youtu.be/v7AYKMP6rOE",
    },
    {
        "title": "Power Walking Plan",
        "icon": "🚶‍♀️",
        "difficulty": "Beginner",
        "duration": "30+ min",
        "type": "Cardio",
        "focus": "Energy",
        "description": "Low-impact cardio that improves insulin sensitivity without spiking cortisol.",
        "benefits": ["Cardio health", "Joint-friendly", "Mood booster"],
        "routine": ["Warm-up (5 min)", "Brisk Walk (20 min)", "Incline Intervals (3×2 min)", "Cool-down (5 min)"],
        "video": "https://youtu.be/YPll-0b9lA4",
    },
    {
        "title": "Core & Stability",
        "icon": "🎯",
        "difficulty": "Intermediate",
        "duration": "15-20 min",
        "type": "Strength",
        "focus": "Weight Loss",
        "description": "Targets deep core to support posture & lower-back health common in PCOS.",
        "benefits": ["Strengthens core", "Improves balance", "Burns abdominal fat"],
        "routine": ["Dead Bug (10/side)", "Bird-Dog (10/side)", "Forearm Plank (30s)", "Glute Bridge (15)"],
        "video": "https://youtu.be/qWYRI-e8DAr",
    },
    {
        "title": "Advanced HIIT Challenge",
        "icon": "⚡",
        "difficulty": "Advanced",
        "duration": "30+ min",
        "type": "HIIT",
        "focus": "Insulin Resistance",
        "description": "Met-con session for seasoned athletes—maximises glycogen clearance.",
        "benefits": ["Peak insulin sensitivity", "Highest calorie burn", "Cardio endurance"],
        "routine": ["Burpee Box Jumps (45s)", "Kettlebell Swings (45s)", "Battle Ropes (45s)", "Rest (15s)"],
        "video": "https://youtu.be/2-b-qPz-tX8",
    },
]

# ──────────────────────────────────────────────────────────────
# Filters UI
# ──────────────────────────────────────────────────────────────
st.markdown("### 🎛️ Find Your Workout")
fc1, fc2, fc3, fc4 = st.columns(4)
f_diff   = fc1.selectbox("Difficulty", ["All","Beginner","Intermediate","Advanced"])
f_dur    = fc2.selectbox("Duration",  ["All","15-20 min","20-30 min","30+ min"])
f_type   = fc3.selectbox("Type",      ["All","Cardio","Strength","HIIT","Yoga"])
f_focus  = fc4.selectbox("Focus",     ["All","Insulin Resistance","Weight Loss","Stress Relief","Energy"])

def match(ex):
    return ((f_diff=="All"  or ex["difficulty"]==f_diff)
         and (f_dur=="All"  or ex["duration"]==f_dur)
         and (f_type=="All" or ex["type"]==f_type)
         and (f_focus=="All"or ex["focus"]==f_focus))

filtered = [ex for ex in EXERCISES if match(ex)]
st.caption(f"{len(filtered)} workout(s) match your filters")

# ──────────────────────────────────────────────────────────────
# Exercise cards
# ──────────────────────────────────────────────────────────────
for ex in filtered:
    diff_class = ex["difficulty"].lower()
    st.markdown(
        f"""
<div style="background:rgba(255,255,255,.9);border-radius:16px;padding:1.5rem;margin:1rem 0;
            box-shadow:0 4px 20px rgba(0,0,0,.08);">
  <div style="display:flex;align-items:center;gap:1rem;">
    <span style="font-size:2rem;">{ex['icon']}</span>
    <h3 style="margin:0;">{ex['title']}</h3>
  </div>
  <div style="display:flex;gap:.5rem;flex-wrap:wrap;margin:.5rem 0 1rem 0;">
    <span class="tag">{ex['difficulty']}</span>
    <span class="tag">{ex['duration']}</span>
    <span class="tag">{ex['type']}</span>
    <span class="tag">{ex['focus']}</span>
  </div>
  <p>{ex['description']}</p>
  <details>
    <summary>Show routine</summary>
    {" → ".join(ex['routine'])}
  </details>
  <p style="margin-top:.5rem;"><em>Benefits: {', '.join(ex['benefits'])}</em></p>
  <div style="margin-top:1rem;">
    <a href="{ex['video']}" target="_blank">▶️ Watch demo</a>
  </div>
</div>
""",
        unsafe_allow_html=True,
    )

    c1, c2 = st.columns(2)
    with c1:
        if st.button(f"Start '{ex['title']}'", key=f"start_{ex['title']}"):
            st.session_state.workout_log.append(
                {"exercise": ex["title"], "date": time.strftime("%Y-%m-%d")}
            )
            st.session_state.weekly_progress += 1
            st.success("Logged! Great job 👏")
    with c2:
        if st.button("Add to weekly plan", key=f"plan_{ex['title']}"):
            st.session_state.setdefault("custom_plan", []).append(ex["title"])
            st.info("Added to plan ✅")

# ──────────────────────────────────────────────────────────────
# Weekly plan (auto-fills from chosen filters or custom additions)
# ──────────────────────────────────────────────────────────────
st.markdown("## 📅 Your Weekly PCOS Plan")
days = ["Mon","Tue","Wed","Thu","Fri","Sat","Sun"]
plan = st.session_state.get("custom_plan") or [ex["title"] for ex in filtered[:7]] or ["Rest"]*7

cols = st.columns(7)
for d, col, workout in zip(days, cols, plan):
    col.markdown(f"**{d}**<br/>{workout}", unsafe_allow_html=True)

# ──────────────────────────────────────────────────────────────
# Progress tracker
# ──────────────────────────────────────────────────────────────
st.markdown("## 📈 Progress This Week")
m1, m2, m3 = st.columns(3)
m1.metric("Workouts logged", st.session_state.weekly_progress)
m2.metric("Last workout",
          st.session_state.workout_log[-1]["exercise"] if st.session_state.workout_log else "–")
goal = 4
pct  = min(100, st.session_state.weekly_progress/goal*100)
m3.metric("Goal completion", f"{pct:.0f}%")

# ──────────────────────────────────────────────────────────────
# Lightweight style tags
# ──────────────────────────────────────────────────────────────
st.markdown("""
<style>
/* Tags on cards */
.tag{
    background:#667eea;
    color:#ffffff;              /* white text on indigo background */
    border-radius:12px;
    padding:2px 8px;
    font-size:.75rem;
}

/* Darker body text for readability */
body, .exercise-description, .benefit-item, .page-subtitle,
.benefits-title, p, li, details, summary, .stCaption{
    color:#334155;              /* slate-700 */
}

/* Meta badges (“Intermediate”, “20-30 min”…) */
.tag, .meta-badge, .nav a{color:#ffffff;}

/* Ensure subtitle isn’t washed out on white cards */
.page-subtitle{font-size:1.1rem;font-weight:500;}
</style>
""", unsafe_allow_html=True)
