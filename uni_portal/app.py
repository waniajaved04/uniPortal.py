import streamlit as st
from utils.session import load_json, save_json
from models.user import User
from models.student import Student
from models.admin import Admin

# Initialize session state variable for user
if "user" not in st.session_state:
    st.session_state.user = None

st.set_page_config(page_title="University Portal", page_icon="🎓")

def login():
    st.title("🎓 Sir Syed University of Engineering and Technology")

    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        users = load_json("data/users.json")
        user_data = next((u for u in users if u["email"] == email and u["password"] == password), None)

        if user_data:
            # Filter keys based on role class __init__ parameters
            if user_data["role"] == "student":
                allowed_keys = ["name", "email", "password", "roll_number"]  # adjust as per your Student __init__
                filtered_data = {k: user_data[k] for k in allowed_keys if k in user_data}
                user = Student(**filtered_data)
            elif user_data["role"] == "admin":
                allowed_keys = ["name", "email", "password"]  # adjust per Admin __init__
                filtered_data = {k: user_data[k] for k in allowed_keys if k in user_data}
                user = Admin(**filtered_data)
            else:
                user = User(user_data["name"], user_data["email"], user_data["password"])

            st.session_state.user = user
            st.success(f"Logged in as {user.name}")
            st.rerun()
        else:
            st.error("Invalid email or password")


def logout():
    st.session_state.user = None
    st.rerun()

from utils.session import load_json, save_json

def student_dashboard(student):
    st.subheader(f"🎓 Welcome, {student.name} ({student.roll_number})")

    # Profile
    with st.expander("👤 View Profile"):
        st.json(student.view_profile())

    # Enrolled Courses
    with st.expander("📚 My Courses"):
        if student.enrolled_courses:
            st.write(student.enrolled_courses)
        else:
            st.info("You are not enrolled in any courses.")

    # Enroll in New Course
    with st.expander("➕ Enroll in a Course"):
        courses = load_json("data/courses.json")
        course_codes = [c["course_code"] for c in courses]
        options = list(set(course_codes) - set(student.enrolled_courses))
        
        if options:
            selected = st.selectbox("Select a course to enroll:", options)
            if st.button("Enroll"):
                student.enroll_course(selected)
                st.success(f"Enrolled in {selected} ✅")
        else:
            st.info("No new courses available to enroll.")

    # View Grades
    with st.expander("📝 My Grades"):
        grades = load_json("data/grades.json")
        student_grades = grades.get(student.roll_number, {})
        if student_grades:
            st.write(student_grades)
        else:
            st.info("No grades available yet.")

    # Fee Status
    with st.expander("💰 Fee Status"):
        st.write(f"Your current fee status is: **{student.check_fee_status()}**")

    # Notice Board
    with st.expander("📢 University Notices"):
        notices = load_json("data/notices.json")
        for note in notices:
            st.markdown(f"- {note}")

from models.course import Course

def admin_dashboard(admin):
    st.subheader(f"🛠️ Admin Panel – {admin.name}")

    # 1. Add New Course
    with st.expander("➕ Add New Course"):
        code = st.text_input("Course Code")
        title = st.text_input("Course Title")
        credits = st.number_input("Credit Hours", min_value=1, max_value=6, step=1)
        instructor = st.text_input("Instructor Name")

        if st.button("Add Course"):
            if code and title and instructor:
                new_course = {
                    "course_code": code,
                    "title": title,
                    "credit_hours": credits,
                    "instructor": instructor
                }
                course_data = load_json("data/courses.json")
                course_data.append(new_course)
                save_json("data/courses.json", course_data)
                st.success(f"Course '{title}' added successfully!")
            else:
                st.warning("Please fill all course fields.")

    # 2. Post a Notice
    with st.expander("📢 Post New Notice"):
        new_notice = st.text_area("Write your notice here:")
        if st.button("Post Notice"):
            if new_notice.strip():
                notices = load_json("data/notices.json")
                notices.append(new_notice.strip())
                save_json("data/notices.json", notices)
                st.success("Notice posted successfully!")
            else:
                st.warning("Notice cannot be empty.")

    # 3. View All Students (Optional)
    with st.expander("👥 View Registered Students"):
        users = load_json("data/users.json")
        students = [u for u in users if u["role"] == "student"]
        if students:
            for s in students:
                st.markdown(f"- **{s['name']}** ({s['roll_number']}) – {s['email']}")
        else:
            st.info("No students registered yet.")


def main():
    st.sidebar.title("📚 University Portal")
    
    if st.session_state.user:
        st.sidebar.markdown(f"**Logged in as:** {st.session_state.user.name}")
        if st.sidebar.button("🚪 Logout"):
            logout()

        # Routing based on role
        if st.session_state.user.role == "student":
            student_dashboard(st.session_state.user)
        elif st.session_state.user.role == "admin":
            admin_dashboard(st.session_state.user)
        else:
            st.info("Unknown user role.")
    else:
        login()

if __name__ == "__main__":
    main()