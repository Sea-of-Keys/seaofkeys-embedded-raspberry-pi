import os


url = os.environ.get("URL")
def setup(session):
    secret = os.environ.get("SECRET")
    embedded_id = os.environ.get("EMBEDDEDID")

    data = {
        'ssshhh': secret,
        'embedded_id': int(embedded_id)
    }
    response = session.post(url + "/em/setup", json=data)

    if response.status_code == 200:
        print("Setup successful")
        return True

def login(session, code):
    room_id = os.environ.get("ROOMID")

    data = {
       'code': code,
        'room_id': int(room_id)
    }

    response = session.post(url + "/em/login", json=data)  
    print(response.status_code) 

    if response.status_code == 200:
        
        userHasAccess = response.json()["data"]        
        
        if userHasAccess:         
            print("Login successful")
            return True
    else:
        return False



def refresh(session):
    response = session.get(url + "/em/refresh")