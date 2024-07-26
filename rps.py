import random
import time
import cv2
import cvzone
from cvzone.HandTrackingModule import HandDetector

cap = cv2.VideoCapture(0)
cap.set(3, 640)
cap.set(4, 480)

detector = HandDetector(maxHands=1)

timer = 0
stateResult = False
startGame = False
cheatMode = False
scores = [0, 0]  # AI and then player
randomNumber = 0

while True:
    imgBG = cv2.imread("resources/BG.png")
    success, img = cap.read()

    imgScaled = cv2.resize(img, (0, 0), None, 0.8, 0.8)
    imgScaled = imgScaled[:, 50:510]
    imgScaled = cv2.flip(imgScaled, 1)

    # detecting hands in the scaled image
    hands, img = detector.findHands(imgScaled)

    if startGame:

        if stateResult is False:
            timer = time.time() - initialTime
            cv2.putText(imgBG, str(int(timer)), (610, 435), cv2.FONT_HERSHEY_PLAIN, 6, (255, 0, 255), 4)

            if timer > 3:
                stateResult = True
                timer = 0

                # rock = 1
                # paper = 2
                # scissors = 3

                if hands:
                    hand = hands[0]
                    fingers = detector.fingersUp(hand)
                    if fingers == [0, 0, 0, 0, 0]:
                        playerMove = 1
                    elif fingers == [1, 1, 1, 1, 1]:
                        playerMove = 2
                    elif fingers == [0, 1, 1, 0, 0]:
                        playerMove = 3
                    else:
                        playerMove = "invalid"

                    if cheatMode:
                        # waiting a few milliseconds to always pick the winning move
                        time.sleep(0.1)
                        if playerMove == 1:
                            randomNumber = 2
                        elif playerMove == 2:
                            randomNumber = 3
                        elif playerMove == 3:
                            randomNumber = 1
                    else:
                        randomNumber = random.randint(1, 3)

                    imgAI = cv2.imread(f'resources/{randomNumber}.png', cv2.IMREAD_UNCHANGED)
                    imgBG = cvzone.overlayPNG(imgBG, imgAI, (160, 380))

                    # Player Wins
                    if playerMove == 1 and randomNumber == 3 or \
                            playerMove == 2 and randomNumber == 1 or \
                            playerMove == 3 and randomNumber == 2:
                        scores[1] += 1

                    # AI Wins
                    if playerMove == 3 and randomNumber == 1 or \
                            playerMove == 1 and randomNumber == 2 or \
                            playerMove == 2 and randomNumber == 3:
                        scores[0] += 1

                    print(fingers)
                    print(playerMove)

    imgBG[282:666, 800:1260] = imgScaled

    if stateResult:
        imgBG = cvzone.overlayPNG(imgBG, imgAI, (160, 380))

    cv2.putText(imgBG, str(scores[0]), (390, 250), cv2.FONT_HERSHEY_PLAIN, 6, (255, 255, 255), 6)
    cv2.putText(imgBG, str(scores[1]), (1160, 250), cv2.FONT_HERSHEY_PLAIN, 6, (255, 255, 255), 6)

    # cv2.imshow("Camera Feed", img)
    # cv2.imshow("Scaled Feed", imgScaled)
    cv2.imshow("BG", imgBG)

    key = cv2.waitKey(1)

    if key == ord('s'):
        startGame = True
        initialTime = time.time()
        stateResult = False

    elif key == ord('d'):
        cheatMode = not cheatMode
        print(f'O' if cheatMode else 'F')
