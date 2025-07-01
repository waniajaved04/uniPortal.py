from models.user import User

class Admin(User):
    def __init__(self, name, email, password):
        super().__init__(name, email, password, role="admin")

    def add_course(self, course_list, course):
        course_list.append(course)

    def post_notice(self, notice_board, message):
        notice_board.add_notice(message)