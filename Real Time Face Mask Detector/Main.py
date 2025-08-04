import cv2
import numpy as np
from tensorflow.keras.models import load_model

def face_mask_detector():
    print("\nStarting Face Mask Detector...")

    # Load pre-trained model
    # Download a model (like "mask_detector_model.h5") and place it in your script directory.
    try:
        model = load_model('mask_detector_model.h5')
    except Exception as e:
        print("Model file not found. Please download a mask detection model as 'mask_detector_model.h5'.")
        print("You can find starter models at: https://github.com/prajnasb/observations/tree/master/experiements/data")
        return

    # Load OpenCV's Haar cascade for face detection
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

    cap = cv2.VideoCapture(0)  # 0 for webcam

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.1, 4)
        for (x, y, w, h) in faces:
            face_img = frame[y:y + h, x:x + w]
            resized = cv2.resize(face_img, (224, 224)) / 255.0
            reshaped = np.reshape(resized, (1, 224, 224, 3))
            result = model.predict(reshaped)
            label = "Mask" if result[0][0] > 0.5 else "No Mask"
            color = (0, 255, 0) if label == "Mask" else (0, 0, 255)
            cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)
            cv2.putText(frame, label, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, color, 2)

        cv2.imshow('Face Mask Detector', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    face_mask_detector()
