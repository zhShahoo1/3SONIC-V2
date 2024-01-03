import cv2

def find_external_camera(start_index=0, max_index=3):
    for i in range(start_index, max_index):
        camera = cv2.VideoCapture(i)
        if camera is not None and camera.isOpened():
            success, _ = camera.read()
            if success:
                print(f"External camera found at index {i}")
                return camera
            camera.release()
    return None

camera = find_external_camera()

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
