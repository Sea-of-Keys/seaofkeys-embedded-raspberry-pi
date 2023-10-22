import os


url = os.environ.get("URL")
def setup(session):
    secert = os.environ.get("SECERT")
    embedded_id = os.environ.get("EMBEDDEDID")

    data = {
        'ssshhh': secert,
        'embedded_id': int(embedded_id)
    }
    response = session.post(url + "em/setup", json=data)

    if response.status_code == 200:
        print("Setup successful")
        return True

def login(session, code):
    room_id = os.environ.get("ROOMID")

    data = {
       'code': code,
        'room_id': int(room_id)
    }

    response = session.post(url + "em/login", json=data)

    if response.status_code == 200:
        print("Login successful")
        return True
    else:
        return False



def refresh(session):
    response = session.get(url + "em/refresh")
