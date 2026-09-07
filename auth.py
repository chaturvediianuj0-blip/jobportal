def login(username, password):
    # Placeholder — real auth comes in Week 14 (Django)
    return username == 'admin' and password == 'password'

def logout(session):
    session.clear()
    return True
