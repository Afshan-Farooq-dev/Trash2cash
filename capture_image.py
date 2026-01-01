import cv2

def capture_image_from_stream(stream_url, output_file="captured_image.jpg"):
    """
    Opens the camera stream, captures one frame, saves it, and closes the stream.
    """
    print(f"📡 Connecting to stream: {stream_url}")
    cap = cv2.VideoCapture(stream_url)

    if not cap.isOpened():
        print("❌ Error: Unable to open stream.")
        return False

    # Try to read a frame
    ret, frame = cap.read()
    if not ret:
        print("❌ Error: Failed to capture frame.")
        cap.release()
        return False

    # Save the frame as an image
    cv2.imwrite(output_file, frame)
    print(f"✅ Image captured and saved as '{output_file}'")

    # Release the stream
    cap.release()
    cv2.destroyAllWindows()
    return True


if __name__ == "__main__":
    # Example: replace with your ESP32-CAM stream URL
    stream_url = "http://192.168.10.23:4747/video"
    capture_image_from_stream(stream_url)
