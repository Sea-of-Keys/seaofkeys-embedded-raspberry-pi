# This example is a hello world example
# for using a keypad with the Raspberry Pi
import threading, time, os
import RPi.GPIO as GPIO
import time
import requests
from api import setup, login, refresh

session = requests.Session()
roomID = "1"

buzzer = 4

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(buzzer,GPIO.OUT)

L1 = 5
L2 = 6
L3 = 13
L4 = 19

C1 = 12
C2 = 16
C3 = 20
C4 = 21

total = 0

userInput = []
correct = False

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(18,GPIO.OUT)
GPIO.setup(15,GPIO.OUT)

GPIO.setup(L1, GPIO.OUT)
GPIO.setup(L2, GPIO.OUT)
GPIO.setup(L3, GPIO.OUT)
GPIO.setup(L4, GPIO.OUT)

GPIO.setup(C1, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(C2, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(C3, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(C4, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

def autoRefresh(session):
    while True:
        refresh(session)
        time.sleep(3600)



def lamp(sleepTime, color):       
    
    if color == "green":            
        GPIO.output(15,GPIO.HIGH)
        time.sleep(sleepTime)        
            
        GPIO.output(buzzer,GPIO.HIGH)   
        time.sleep(0.2)
        GPIO.output(buzzer,GPIO.LOW)
        
        GPIO.output(15,GPIO.LOW)
        
    elif color == "red":    
        GPIO.output(18,GPIO.HIGH)
        time.sleep(sleepTime)    
        GPIO.output(18,GPIO.LOW) 


def ConvertInput(userInput):
    
    result = ""
    
    for item in userInput:
        
        result += item
        
    return result       

def UserHasAccess(code):
    
    obj = {"code": code,"room_id": roomID}
    x = requests.post(url,json=obj)      
    access = x.json()["data"]   
    
    return access
        
 
def keyPressed(keyPressed):    
    global total    
    total+=1 
    GPIO.output(buzzer,GPIO.HIGH)   
    
    lamp(0.2, "green")
    GPIO.output(buzzer,GPIO.LOW)
    userInput.append(keyPressed)


def reset():
    global total
    global userInput
    total = 0
    userInput = []
    print("Program has been reset")    
    
def readLine(line, characters):
    
    GPIO.output(line, GPIO.HIGH)    

    if(GPIO.input(C1) == 1):
        keyPressed(characters[0])         
        
    if(GPIO.input(C2) == 1):
        keyPressed(characters[1])    
        
    if(GPIO.input(C3) == 1):
        keyPressed(characters[2])    
        
    if(GPIO.input(C4) == 1):
        keyPressed(characters[3])            
    
    GPIO.output(line, GPIO.LOW)
    
def main();

    if os.environ.get("ROOMID") == None or os.environ.get("SECERT") == None or os.environ.get("EMBEDDEDID") == None or os.environ.get("URL") == None:
        return
    setup(session)

    threading.Thread(target=autoRefresh, args=(session,)).start()
    while not correct:
        readLine(L1, ["1","2","3","A"])
        readLine(L2, ["4","5","6","B"])
        readLine(L3, ["7","8","9","C"])
        readLine(L4, ["*","0","#","D"])
        time.sleep(0.2)

        for item in userInput:
            if(item == "*"):
                reset()

        if total >= 6:    

            if login(session, ConvertInput(userInput)): 
                print("Password is correct")
                lamp(5,"green")            
                reset()

            else:            
                print("Password is incorrect")
                lamp(5,"red")
                reset()

if __name__ == "__main__":
    main()
