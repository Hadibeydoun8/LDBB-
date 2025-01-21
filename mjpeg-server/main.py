import cv2
from flask import Flask, Response

app = Flask(__name__)

# Initialize the camera
cap = cv2.VideoCapture(0)

def generate_frames():
    while True:
        # Read frame by frame
        ret, frame = cap.read()
        if not ret:
            break
        # Encode the frame in MJPEG format
        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/cam.mjpeg')
def video_feed():
    return Response(generate_frames(), 
                    mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)

