import socket
import yaml
import json
import time
import math

cfg = None
with open('config.yml') as file:
    try:
        cfg = yaml.safe_load(file)
    except yaml.YAMLError as exc:
        print(exc)

SERVER_IP = cfg["server"]["address"]
SERVER_PORT = cfg["server"]["port"]
MOTOR_STOP = cfg["servoMotor"]["stop"]
MOTOR_SPEED = cfg["servoMotor"]["speed"]
HEAD_STOP = cfg["headMotor"]["stop"]
HEAD_SPEED = cfg["headMotor"]["speed"]

sock = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_DGRAM) # UDP

def sendMovement(x = 0, y = 0, head = 0):
    leftDrive, rightDrive, headDrive = getDrives(x, y, head)
    print(leftDrive, rightDrive, headDrive)

    command = {
        "commands": {
            "servoMotor": {
                "leftDrive": leftDrive,
                "rightDrive": rightDrive
            }
        },
        "forward": {
            "head":  {
                "commands": {
                    "servoMotor": {
                        "mainDrive": headDrive
                    }
                }
            }
        }
    }

    sendCommand(command)
    return True

def getDrives(x, y, head):
    r, theta = cartesianToPolar(x, y)

    if theta <= 90:
        leftDrive = 1
        rightDrive = remap(theta, 0, 90, -1, 1)
    elif theta <= 180:
        leftDrive = remap(theta, 90, 180, 1, -1)
        rightDrive = 1
    elif theta <= 270:
        leftDrive = -1 
        rightDrive = remap(theta, 180, 270, 1, -1)
    elif theta <= 360:
        leftDrive = remap(theta, 270, 360, -1, 1)
        rightDrive = -1
    else:
        leftDrive = 0
        rightDrive = 0

    r = min(r, 1)
    leftDrive = leftDrive * r * MOTOR_SPEED + MOTOR_STOP
    rightDrive = rightDrive * r * MOTOR_SPEED + MOTOR_STOP

    #exponential for finer control
    headDrive = head * head * HEAD_SPEED + HEAD_STOP

    return (leftDrive, rightDrive, headDrive)

def cartesianToPolar(x, y):
    theta = math.degrees(math.atan2(-y, x))
    r = math.sqrt(x * x + y * y)
    if theta < 0:
        theta += 360
    return (r, theta)

def remap(x, inMin, inMax, outMin, outMax):
    return outMin + (x - inMin) * (outMax - outMin) / (inMax - inMin);

SOUNDS = ["dog", "beginning", "emerge", "exterminate", "prepare", "surviveinme", "hohohoho", "happyHolidays"]
MIN_SOUND_TIME = 5 #seconds
lastSoundTime = 0
def sendSound(index):
    global lastSoundTime

    currentTime = time.time()
    if currentTime - lastSoundTime < MIN_SOUND_TIME:
        return
    lastSoundTime = currentTime

    soundName = SOUNDS[min(index, len(SOUNDS) - 1)]
    command = {
        "commands": {
            "playsound": soundName
        }
    }

    sendCommand(command)
    return True

def sendCommand(command):
    sock.sendto(json.dumps(command).encode(), (SERVER_IP, SERVER_PORT))
