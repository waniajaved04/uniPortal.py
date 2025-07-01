class Course:
    def __init__(self, course_code, title, credit_hours, instructor):
        self.course_code = course_code
        self.title = title
        self.credit_hours = credit_hours
        self.instructor = instructor

    def get_info(self):
        return {
            "Code": self.course_code,
            "Title": self.title,
            "Credits": self.credit_hours,
            "Instructor": self.instructor
        }