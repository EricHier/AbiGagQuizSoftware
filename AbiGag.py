import pygame
import time
import socket
import random
from threading import Thread

##Werte
width = 1920
height = 1080

white = (255, 255, 255)
black = (0,0,0)
red = (255, 80, 80)
blue = (0, 153, 255)


##Pygame Setup
pygame.init()

display = pygame.display.set_mode((width,height), pygame.FULLSCREEN)
pygame.display.set_caption("Abi Gag 2019")

##UDPReciever Setup
UDP_IP = socket.gethostbyname(socket.gethostname())
UDP_PORT = 5005
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((UDP_IP, UDP_PORT))

print("IP: " + UDP_IP)


##Import Bilder
antwortBildR = ["", "", "", ""]
for i in range(4):
    antwortBildR[i] = pygame.image.load("Tokens/RotAntwort" + str(i) + ".png")

antwortBildB = ["", "", "", ""]
for i in range(4):
    antwortBildB[i] = pygame.image.load("Tokens/BlauAntwort" + str(i) + ".png")


##Import sound
sound = pygame.mixer.Sound('Tokens/buzzer.wav')


##Variablen
aktuelleFrage = 0
zustand = "vorschau"

spiel = 0
antworten = []

buzzer = False

global vorschaubild
vorschaubild = 0

global punkteRot
punkteRot = 0
global punkteBlau
punkteBlau = 0

loginRot = -1
loginBlau = -1

def addText(text, color, size, pos):
    ##Fügt einen Text ein
    surf = pygame.font.Font("freesansbold.ttf", size).render(text, True, color)
    rect = surf.get_rect()
    rect.center = pos
    display.blit(surf, rect)

def onLogin(playerID, answerID):
    global zustand
    if zustand == "frage":
        global loginRot
        global loginBlau
        if int(playerID) == 0:
            loginRot = int(answerID)
        if int(playerID) == 1:
            loginBlau = int(answerID)


def empfang():
    while True:
        ##Empfängt die Daten
        data, addr = sock.recvfrom(1024) # buffer size is 1024 bytes
        content = data.decode("utf-8")
        print(content)
        onLogin(content[1], content[4])
    

def vor():
    global zustand
    global aktuelleFrage
    global loginBlau
    global loginRot
    global punkteBlau
    global punkteRot
    global buzzer
    if zustand == "einloggung":
        zustand = "loesung"
        if loginRot == antworten[aktuelleFrage] and not buzzer:
            punkteRot += 1
        if loginBlau == antworten[aktuelleFrage] and not buzzer:
            punkteBlau += 1
    elif zustand == "loesung":
        if aktuelleFrage < len(antworten) - 1:
            loginRot = -1
            loginBlau = -1
            zustand = "frage"
            aktuelleFrage += 1
    elif zustand == "vorschau":
        zustand = "frage"
        aktuelleFrage = 0

def zurueck():
    global zustand
    global aktuelleFrage
    if zustand == "loesung":
        zustand = "einloggung" if not buzzer else "frage"
    elif zustand == "einloggung":
        zustand = "frage"
        global loginRot
        global loginBlau
        loginRot = -1
        loginBlau = -1
    elif zustand == "frage" and not aktuelleFrage == 0:
        zustand = "loesung"
        aktuelleFrage -= 1
    loginRot = -1
    loginBlau = -1


def neuesSpiel(nr):
    global spiel
    spiel = nr

    global punkteRot
    global punkteBlau
    punkteRot = 0
    punkteBlau = 0

    global loginRot
    global loginBlau

    loginRot = -1
    loginBlau = -1

    global antworten
    global buzzer
    if nr == 1:
        antworten = [3, 3]
        buzzer = False
    elif nr == 2:
        antworten = [3, 2]
        buzzer = True

    global bilder
    bilder = []
    for i in range(1, len(antworten)+1):  
        titelFrage = "Spiel" + str(nr) + "Frage/" + str(i) + ".png"
        titelAntwort = "Spiel" + str(nr) + "Antwort/" + str(i) + ".png"
        bilder.append((pygame.image.load(titelFrage), pygame.image.load(titelAntwort), antworten[i-1]))

    global zustand
    zustand = "vorschau"
    global vorschaubild
    vorschaubild = pygame.image.load("Spiel" + str(nr) + "Frage/Vorschau.png")

def render():
    ##Zeigt an
    global loginBlau
    global loginRot
    global zustand
    if not buzzer:
        if zustand == "frage":
            display.blit(bilder[aktuelleFrage][0], (0, 0))
            if not loginRot == -1:
                pygame.draw.rect(display, red, [0, 200, 100, 100])
            if not loginBlau == -1:
                pygame.draw.rect(display, blue, [1820, 200, 100, 100])
            addText(str(punkteRot), red, 100, (50, 50))
            addText(str(punkteBlau), blue, 100, (1720, 50))
            
            
        elif zustand == "einloggung":
            display.blit(bilder[aktuelleFrage][0], (0, 0))
            display.blit(antwortBildR[int(loginRot)], (0, 0))
            display.blit(antwortBildB[int(loginBlau)], (0, 0))
            addText(str(punkteRot), red, 100, (50, 50))
            addText(str(punkteBlau), blue, 100, (1720, 50))

            
            
        elif zustand == "loesung":
            display.blit(bilder[aktuelleFrage][1], (0, 0))
            display.blit(antwortBildR[int(loginRot)], (0, 0))
            display.blit(antwortBildB[int(loginBlau)], (0, 0))
            addText(str(punkteRot), red, 100, (50, 50))
            addText(str(punkteBlau), blue, 100, (1720, 50))

        elif zustand == "vorschau":
            display.blit(vorschaubild, (0, 0))

        

    else:
        if loginBlau == 0 and zustand == "frage":
            display.fill(blue)
            display.blit(bilder[aktuelleFrage][0], (0, 0))
            addText(str(punkteRot), white, 100, (50, 50))
            addText(str(punkteBlau), white, 100, (1720, 50))
            pygame.display.update()
            sound.play()
            time.sleep(5)
            zustand = "loesung"
            loginBlau = -1
            loginRot = -1
        elif loginRot == 0 and zustand == "frage":
            display.fill(red)
            display.blit(bilder[aktuelleFrage][0], (0, 0))
            addText(str(punkteRot), white, 100, (50, 50))
            addText(str(punkteBlau), white, 100, (1720, 50))
            pygame.display.update()
            sound.play()
            time.sleep(5)
            zustand = "loesung"
            loginRot = -1
            loginBlau = -1
        else:
            display.fill(black)

        if zustand == "frage":
            display.blit(bilder[aktuelleFrage][0], (0, 0))
        elif zustand == "loesung":
            display.blit(bilder[aktuelleFrage][1], (0, 0))
        elif zustand == "vorschau":
            display.blit(vorschaubild, (0, 0))

        addText(str(punkteRot), red, 100, (50, 50))
        addText(str(punkteBlau), blue, 100, (1720, 50))
    
    pygame.display.update()


def update():
    ##Die Haupschleife
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                vor()
            elif event.key == pygame.K_LEFT:
                zurueck()
            elif event.key == pygame.K_o:
                global punkteBlau
                punkteBlau += 1
            elif event.key == pygame.K_l:
                punkteBlau -= 1
            elif event.key == pygame.K_w:
                global punkteRot
                punkteRot += 1
            elif event.key == pygame.K_s:
                punkteRot -= 1
            elif event.key == pygame.K_1:
                neuesSpiel(1)
            elif event.key == pygame.K_2:
                neuesSpiel(2)
            elif event.key == pygame.K_3:
                neuesSpiel(3)
            elif event.key == pygame.K_4:
                neuesSpiel(4)
            


    global zustand
    if not loginRot == -1 and not loginBlau == -1 and zustand == "frage" and not buzzer:
        pygame.draw.rect(display, red, [0, 200, 100, 100])
        pygame.draw.rect(display, blue, [1820, 200, 100, 100])
        pygame.display.update()
        time.sleep(1)
        zustand = "einloggung"


t = Thread(target=empfang, args=())
t.start()

neuesSpiel(1)

while True:
    update()
    render()
    
    
    
