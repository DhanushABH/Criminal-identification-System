import os
import cv2
import numpy as np

size = 2
haar_cascade = cv2.CascadeClassifier('lbpcascade_frontalface.xml')


# Part 1: Create fisherRecognizer

def train_model():
    model = cv2.face.LBPHFaceRecognizer_create()
    fn_dir = 'face_samples'

    print('Training...')

    images = []
    labels = []
    names = {}
    id = 0

    for (subdirs, dirs, files) in os.walk(fn_dir):
        # Loop through each folder named after the subject in the photos
        for subdir in dirs:
            names[id] = subdir
            subjectpath = os.path.join(fn_dir, subdir)
            # Loop through each photo in the folder
            for filename in os.listdir(subjectpath):
                # Skip non-image formats
                f_name, f_extension = os.path.splitext(filename)
                if f_extension.lower() not in ['.png', '.jpg', '.jpeg', '.gif', '.pgm']:
                    print("Skipping " + filename + ", wrong file type")
                    continue
                path = os.path.join(subjectpath, filename)
                label = id

                # Load the image as grayscale
                image = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
                if image is None:
                    print("Unable to read image:", filename)
                    continue

                # Resize image to a fixed size
                image = cv2.resize(image, (112, 92))

                # Add image and label to lists
                images.append(image)
                labels.append(int(label))

            id += 1

    # Convert lists to NumPy arrays
    images = np.array(images)
    labels = np.array(labels)

    # Train the model
    model.train(images, labels)

    return model, names


# Part 2: Use fisherRecognizer on camera stream
def detect_faces(gray_frame):
    global size, haar_cascade

    # Resize to speed up detection (optional, change size above)
    mini_frame = cv2.resize(gray_frame, (int(gray_frame.shape[1] / size), int(gray_frame.shape[0] / size)))

    # Detect faces and loop through each one
    faces = haar_cascade.detectMultiScale(mini_frame)
    return faces


def recognize_face(model, frame, gray_frame, face_coords, names):
    (img_width, img_height) = (112, 92)
    recognized = []
    recog_names = []

    for i in range(len(face_coords)):
        face_i = face_coords[i]

        # Coordinates of face after scaling back by `size`
        (x, y, w, h) = [v * size for v in face_i]
        face = gray_frame[y:y + h, x:x + w]
        face_resize = cv2.resize(face, (img_width, img_height))

        # Try to recognize the face
        (prediction, confidence) = model.predict(face_resize)

        # print(prediction, confidence)
        if confidence < 95 and names[prediction] not in recog_names:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
            recog_names.append(names[prediction])
            recognized.append((names[prediction].capitalize(), confidence))
        elif confidence >= 95:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

    return frame, recognized


if __name__ == "__main__":
    # Call the train_model function
    model, names = train_model()
