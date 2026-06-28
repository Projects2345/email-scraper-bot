from flask_login import LoginManager, UserMixin

login_manager = LoginManager()
login_manager.login_view = "login"

class User(UserMixin):
    def __init__(self, id, name, email, password):
        self.id = id
        self.name = name
        self.email = email
        self.password = password

@login_manager.user_loader
def load_user(user_id):
    from storage import get_user_by_id
    user_data = get_user_by_id(int(user_id))
    if user_data:
        return User(user_data["id"], user_data["name"], user_data["email"], user_data["password"])
    return None
