# Import necessary packages for hand gesture recognition project
import cv2
import numpy as np
import mediapipe as mp
import tensorflow as tf
from tensorflow.keras.models import load_model
import tkinter as tk
from PIL import Image, ImageTk

# Initialize models

# this module will perform the hand recognition algorithm
# create the object of module and store it in mpHands
mpHands = mp.solutions.hands 

hands = mpHands.Hands(
    max_num_hands = 1, # Max number of hands detected in single frame
    min_detection_confidence=0.7, 
)
mpDraw = mp.solutions.drawing_utils # Draws in key points in hands

# Load gesture recognizer model
model = load_model('models/mp_hand_gesture')

# Load class names
f = open('models/gesture.names', 'r')
classNames = f.read().split('\n')
f.close()
print(classNames)

# Initialize the webcam - camera ID of system
camera = cv2.VideoCapture(1)

# Create the main GUI window
root = tk.Tk()
root.title("Hand Gesture Recognition App")

# Create a label to display the camera feed
label = tk.Label(root)
label.pack()

# Create a label to display the class name
class_label = tk.Label(root, text="Class: ")
class_label.pack()

def update_frame():
    # read each frame from webcam
    _, frame = camera.read()
    x,y,c = frame.shape

    # Flip frame vertically
    frame = cv2.flip(frame, 1) #flip the webcam frame

    # Convert to color
    framergb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    # Get hand landmark prediction
    result = hands.process(framergb)

    className = ''

    # post-processing result
    if result.multi_hand_landmarks:
        landmarks = []
        for handslms in result.multi_hand_landmarks:
            for lm in handslms.landmark:
                # Return normalized result..
                lmx = int(lm.x * x)
                lmy = int(lm.y * y)
                landmarks.append([lmx, lmy])
            
        # Drawing landmarks on frames
        mpDraw.draw_landmarks(frame, handslms, mpHands.HAND_CONNECTIONS)
        
        # Predict gesture
        prediction = model.predict([landmarks])
        # Return max value
        classID = np.argmax(prediction)
        className = classNames[classID]

    #show prediction on frame
    cv2.putText(
        frame, 
        className, 
        (10, 50), 
        cv2.FONT_HERSHEY_SIMPLEX,
        1, (0,0,255), 2, 
        cv2.LINE_AA
    )

    # Convert the OpenCV frame to a format suitable for Tkinter
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    img = Image.fromarray(frame_rgb)
    img_tk = ImageTk.PhotoImage(image=img)
    label.img_tk = img_tk
    label.config(image=img_tk)

    # Display the class name on a separate label
    class_label.config(text=f"Class:  + {className}")
    print(className)
    root.after(1, update_frame)

# Start capturing and updating frames
update_frame()

# Start the Tkinter main loop
root.mainloop()

# Release the webcam
camera.release()
cv2.destroyAllWindows()