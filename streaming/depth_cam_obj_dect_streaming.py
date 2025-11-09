import cv2
import subprocess
from ultralytics import YOLO
import os

# ---------------- Global flags ----------------
enable_detection = True   # Always run YOLO detection

# ---------------- MediaMTX RTSP URL ----------------
username = os.environ.get("RTSP_USERNAME")
password = os.environ.get("RTSP_PASSWORD")
host = os.environ.get("RTSP_HOST", "0.tcp.ap.ngrok.io")
port = os.environ.get("RTSP_PORT", "8554")
input_path = os.environ.get("RTSP_DEPTH_PATH", "drsys/test/test")
output_path = os.environ.get("RTSP_DEPTH_OUTPUT_PATH", "drsys/test/test/obj")

# Input RTSP URL
if username and password:
    input_rtsp_url = f"rtsp://{username}:{password}@{host}:{port}/{input_path}"
else:
    input_rtsp_url = f"rtsp://{host}:{port}/{input_path}"

# Output RTSP URL
if username and password:
    output_rtsp_url = f"rtsp://{username}:{password}@{host}:{port}/{output_path}"
else:
    output_rtsp_url = f"rtsp://{host}:{port}/{output_path}"

print(f"Reading from RTSP: {input_rtsp_url}")
print(f"Streaming to RTSP: {output_rtsp_url}")

# ---------------- YOLO setup ----------------
onnx_model = YOLO("yolo11n.onnx")

# ---------------- OpenCV RTSP capture ----------------
cap = cv2.VideoCapture(input_rtsp_url)
if not cap.isOpened():
    print("❌ Failed to open RTSP input stream")
    exit(0)

width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
fps = int(cap.get(cv2.CAP_PROP_FPS)) or 30

# ---------------- FFmpeg setup ----------------
ffmpeg_cmd = [
    'ffmpeg', '-y', '-f', 'rawvideo', '-pix_fmt', 'bgr24', '-s', f'{width}x{height}', '-r', str(fps), '-i', '-',
    '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-preset', 'veryfast', '-tune', 'zerolatency',
    '-rtsp_transport', 'tcp', '-f', 'rtsp', output_rtsp_url
]

process = subprocess.Popen(ffmpeg_cmd, stdin=subprocess.PIPE)
print("🔴 Streaming started. Press CTRL+C to stop.")

# ---------------- Streaming loop ----------------
try:
    while True:
        ret, frame = cap.read()
        if not ret:
            print("❌ Failed to read frame from RTSP input")
            break

        # Apply YOLO detection
        if enable_detection:
            results = onnx_model.track(
                frame, persist=True, verbose=False,
                tracker="bytetrack.yaml", conf=0.7, iou=0.7, classes=[0]
            )
            annotated_frame = results[0].plot()
            output_frame = annotated_frame
        else:
            output_frame = frame

        # Send frame to FFmpeg
        try:
            process.stdin.write(output_frame.tobytes())
        except BrokenPipeError:
            print("❌ FFmpeg pipe broken. Restarting FFmpeg...")
            process.stdin.close()
            process.wait()
            process = subprocess.Popen(ffmpeg_cmd, stdin=subprocess.PIPE)

except KeyboardInterrupt:
    print("\n🛑 Streaming stopped by user.")
finally:
    cap.release()
    process.stdin.close()
    process.wait()
    print("✅ Clean shutdown complete.")
