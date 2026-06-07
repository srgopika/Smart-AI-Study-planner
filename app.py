import streamlit as st
from datetime import datetime, timedelta
import random
def generate_study_plan(subjects, priorities, days_left, daily_hours):
    plan = {}
    current_date = datetime.today().date()
    day_names = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
   #priority based algorithm
    weights = {sub: 3 if priorities.get(sub) == "High" else 2 if priorities.get(sub) == "Medium" else 1 for sub in subjects}
    total_weight = sum(weights.values())
    base_hours = {sub: max(1, round((weights[sub] / total_weight) * daily_hours * 0.9)) for sub in subjects}
    for i in range(min(14, days_left)):
        day_name = day_names[i % 7]
        date_str = (current_date + timedelta(days=i)).strftime("%b %d")
        full_day = f"{day_name} ({date_str})"
        tasks = []
        remaining_hours = daily_hours
        sorted_subjects = sorted(subjects, key=lambda x: weights[x], reverse=True)
        random.shuffle(sorted_subjects)
        for sub in sorted_subjects:
            if remaining_hours <= 0: break
            hours = min(base_hours[sub], remaining_hours)
            if weights[sub] == 3 and remaining_hours >= 2:
                hours = min(hours + 1, remaining_hours)
            if hours >= 1:
                tasks.append(f"{sub} ({hours}h)")
                remaining_hours -= hours
        if remaining_hours >= 1:
            if random.random() > 0.5:
                tasks.append(f"Revision / Previous Topics ({remaining_hours}h)")
            else:
                high_pri = [s for s in subjects if weights[s] == 3]
                if high_pri and remaining_hours >= 1:
                    sub = random.choice(high_pri)
                    tasks.append(f"{sub} (Extra {remaining_hours}h)")
                else:
                    tasks.append(f"Revision ({remaining_hours}h)")
        plan[full_day] = tasks
    return plan
def get_study_tips(subjects, daily_hours):
    tips = ["Use Pomodoro Technique: 25 min study + 5 min break","Study your toughest subject first when energy is high","Revise what you studied yesterday before new topics","Take short breaks between subjects","Stay consistent — even small daily progress compounds"]
    if daily_hours >= 5:
        tips.append("Split long study sessions into 2 parts with a break")
    return tips
st.set_page_config(page_title="Smart AI Study Planner", layout="centered")
st.title("Smart AI Study Planner")
st.markdown("Intelligent Study Schedule Generator")
st.sidebar.header("Plan Your Study")
subjects_input = st.sidebar.text_area("Subjects (one per line)","Maths\nPhysics\nChemistry\nEnglish\nComputer Science\nPsychology\nHome Science\nSpanish",height=160)
subjects_list = [s.strip() for s in subjects_input.split("\n") if s.strip()]
exam_date = st.sidebar.date_input("Exam Date",value=datetime.today() + timedelta(days=25))
daily_hours = st.sidebar.slider("Available Study Hours Per Day", 1, 10, 4)
st.sidebar.markdown("Subject Priority")
priorities = {}
for sub in subjects_list:
    priorities[sub] = st.sidebar.selectbox(f"{sub}", ["High", "Medium", "Low"], index=1, key=sub)
if st.sidebar.button("Generate Smart Study Plan", type="primary"):
    if not subjects_list:
        st.error("Please enter at least one subject")
    else:
        today = datetime.today().date()
        days_left = (exam_date - today).days
        if days_left <= 0:
            st.error("Exam date must be in the future!")
        else:
            with st.spinner("Creating your personalized study plan..."):
                plan = generate_study_plan(subjects_list, priorities, days_left, daily_hours)
                st.success(f"Plan Generated for next {days_left} days")
                st.subheader("Your Study Schedule")
                for day, tasks in plan.items():
                    st.markdown(f"{day}")
                    for task in tasks:
                        st.markdown(f"• {task}")
                    st.markdown("---")
                st.subheader("Summary")
                total_hrs = sum(sum(int(t.split('(')[1].split('h')[0]) for t in tasks) for tasks in plan.values())
                st.info(f"Total Study Hours in Plan:{total_hrs} hours")
                st.subheader("AI Study Tips")
                for tip in get_study_tips(subjects_list, daily_hours):
                    st.markdown(f"• {tip}")
st.caption("Smart AI Study Planner")