import cv2

def get_first_external_camera():
    camera = cv2.VideoCapture(1)  # Index 1 usually refers to the first external webcam
    success, _ = camera.read()
    if success:
        return camera
    camera.release()
    return None

camera = get_first_external_camera()

if camera is None:
    print("No accessible external camera found!")
    exit()

def generate_frames():
    while True:
        success, frame = camera.read()
        if not success:
            print("Failed to read frame from the camera.")
            break
        else:
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

# Call the function to check
next(generate_frames())