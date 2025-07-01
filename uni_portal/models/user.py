class User:
    def __init__(self, name, email, password, role):
        self.name = name
        self.email = email
        self.password = password
        self.role = role

    def view_profile(self):
        return {
            "Name": self.name,
            "Email": self.email,
            "Role": self.role
        }