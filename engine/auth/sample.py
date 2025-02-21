import cv2
import os

# Define paths
haar_cascade_path = "engine//auth//haarcascade_frontalface_default.xml"
save_folder = "engine//auth//samples"

# Ensure Haarcascade file exists
if not os.path.exists(haar_cascade_path):
    print(f"Error: Haarcascade file not found at {haar_cascade_path}")
    exit()

# Ensure save directory exists
os.makedirs(save_folder, exist_ok=True)

# Start webcam
cap = cv2.VideoCapture(0)  # 0 for default webcam

# Check if camera opened successfully
if not cap.isOpened():
    print("Error: Could not open webcam.")
    exit()

cap.set(3, 640)  # Set video frame width
cap.set(4, 480)  # Set video frame height

# Load face detector
detector = cv2.CascadeClassifier(haar_cascade_path)

# Get user input
face_id = input("Enter a Numeric user ID here: ")
print(f"📸 Capturing 100 face images for ID {face_id}...")

count = 1  # Image counter
total_images = 100  # Number of images to capture

while count <= total_images:
    ret, img = cap.read()  # Capture frame
    if not ret:
        print("Error: Failed to capture image.")
        break

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  # Convert to grayscale
    faces = detector.detectMultiScale(gray, 1.3, 5)

    for (x, y, w, h) in faces:
        cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)  # Draw rectangle
        count += 1

        # Save face image
        image_path = os.path.join(save_folder, f"face.{face_id}.{count}.jpg")
        cv2.imwrite(image_path, gray[y:y+h, x:x+w])
        print(f"✅ Image {count}/{total_images} saved at {image_path}")

        cv2.imshow("Capturing Faces...", img)  # Display the frame

    # Stop after 100 images or if ESC is pressed
    if cv2.waitKey(1) & 0xFF == 27 or count >= total_images:
        break

# Cleanup
print("Captured 100 images.")
cap.release()
cv2.destroyAllWindows()
