USERS = {'admin': 'securepassword123'}
def login(username, password):
    # Fixed: was always returning True — now checks actual credentials
    return USERS.get(username) == password

def logout(session):
    session.clear()
    return True
