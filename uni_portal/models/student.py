from models.user import User

class Student(User):
    def __init__(self, name, email, password, roll_number):
        super().__init__(name, email, password, role="student")
        self.roll_number = roll_number
        self.enrolled_courses = []
        self.grades = {}
        self.fee_status = "Unpaid"

    def enroll_course(self, course_code):
        if course_code not in self.enrolled_courses:
            self.enrolled_courses.append(course_code)

    def view_grades(self):
        return self.grades

    def check_fee_status(self):
        return self.fee_status