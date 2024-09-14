import cv2
import mediapipe as mp
import time
import random
from gtts import gTTS
import os
import threading
from playsound import playsound

class CameraCapture:
    def __init__(self, src=0):
        self.cap = cv2.VideoCapture(src)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 320)     # Lower resolution for performance
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 240)
        self.cap.set(cv2.CAP_PROP_FPS, 15)              # Reduce FPS to reduce load
        self.ret, self.frame = self.cap.read()
        self.lock = threading.Lock()
        self.running = True
        threading.Thread(target=self.update, args=()).start()

    def update(self):
        while self.running:
            ret, frame = self.cap.read()
            with self.lock:
                self.ret, self.frame = ret, frame

    def read(self):
        with self.lock:
            return self.ret, self.frame

    def release(self):
        self.running = False
        self.cap.release()

# Initialize MediaPipe for hand tracking
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils

def classify_hand_shape(hand_landmarks):
    thumb_tip = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP]
    index_finger_tip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
    middle_finger_tip = hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP]
    ring_finger_tip = hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_TIP]
    pinky_tip = hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_TIP]

    if (index_finger_tip.y < thumb_tip.y and
        middle_finger_tip.y < thumb_tip.y and
        ring_finger_tip.y < thumb_tip.y and
        pinky_tip.y < thumb_tip.y):
        return "Paper"
    elif (index_finger_tip.y < thumb_tip.y and
          middle_finger_tip.y < thumb_tip.y and
          ring_finger_tip.y > thumb_tip.y and
          pinky_tip.y > thumb_tip.y):
        return "Scissors"
    else:
        return "Rock"

def get_ai_move():
    return random.choice(["Rock", "Paper", "Scissors"])

def determine_winner(player_move, ai_move):
    if player_move == ai_move:
        return "It's a tie!"
    elif (player_move == "Rock" and ai_move == "Scissors") or \
         (player_move == "Paper" and ai_move == "Rock") or \
         (player_move == "Scissors" and ai_move == "Paper"):
        return "You win!"
    else:
        return "AI wins!"

def speak(text):
    tts = gTTS(text=text, lang='en')
    tts.save("response.mp3")
    playsound("response.mp3")

# Create and use the threaded camera capture                                                                                                                           
camera = CameraCapture()

frame_count = 0
ai_interval = 30          # AI processing every 30 frames to reduce overhead
game_delay = 5     # Delay in seconds between each game
hand_entry_buffer = 2.0    # Buffer time after hand enters frame (in seconds)

with mp_hands.Hands(min_detection_confidence=0.5, min_tracking_confidence=0.5) as hands:
    last_game_time = time.time()
    hand_entry_time = None    # To track when hand first enters frame

    while True:
        ret, frame = camera.read()
        if not ret:
            break

        frame_count += 1
        frame = cv2.flip(frame, 1)
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        result = hands.process(rgb_frame)

        if result.multi_hand_landmarks:
            if hand_entry_time is None:      # Detect when hand first enters frame
                hand_entry_time = time.time()
                print("Hand entered frame, starting buffer...")

            # Check if buffer time has passed
            if time.time() - hand_entry_time >= hand_entry_buffer:
                for hand_landmarks in result.multi_hand_landmarks:
                    mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

                    if frame_count % ai_interval == 0:    # Only process AI logic every 30 frames
                        current_time = time.time()
                        if current_time - last_game_time > game_delay:    # Check if enough time has passed
                            player_move = classify_hand_shape(hand_landmarks)
                            ai_move = get_ai_move()
                            winner = determine_winner(player_move, ai_move)
                            response = f"AI chose {ai_move}. You chose {player_move}. {winner}"
                            print(response)    # For debugging

                            speak(response)    # You can comment this out for testing without audio

                            last_game_time = current_time      # Reset the game timer
                            hand_entry_time = None             # Reset hand entry time after each game
        else:
            hand_entry_time = None        # Reset if hand leaves the frame

        cv2.imshow('Hand Tracking with AI - Hand Entry Buffer', frame)

        if cv2.waitKey(10) & 0xFF == ord('q'):
            print("Exiting the game...")
            break

camera.release()
cv2.destroyAllWindows()