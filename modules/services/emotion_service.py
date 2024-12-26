from deepface import DeepFace
import cv2
import numpy as np

def detect_emotion(image_file, detector_backend="retinaface"):
    """
    Detect emotion in an image using DeepFace with different detector backends.
    
    Args:
        image_file: The uploaded image file
        detector_backend: The face detection backend to use 
                        ('retinaface', 'mtcnn', 'opencv', 'ssd', or 'dlib')
    Returns:
        dict: Contains emotion, confidence score, and any error messages
    """
    try:
        # Convert image file to numpy array
        file_bytes = np.frombuffer(image_file.read(), np.uint8)
        image = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
        
        # Analyze the image with specified backend
        result = DeepFace.analyze(
            img_path=image,
            actions=["emotion"],
            enforce_detection=False,
            detector_backend=detector_backend
        )
        
        # Handle output as a list
        if isinstance(result, list):
            result = result[0]
            
        # Get the emotion scores
        emotions = result.get("emotion", {})
        dominant_emotion = result.get("dominant_emotion", "Unknown")
        confidence = emotions.get(dominant_emotion, 0)
            
        return {
            "mood": dominant_emotion,
            "confidence": round(confidence, 2),
            "all_emotions": {k: round(v, 2) for k, v in emotions.items()}
        }
        
    except Exception as e:
        print(f"Error in emotion detection: {e}")
        return {
            "mood": f"Error detecting emotion: {str(e)}",
            "confidence": 0,
            "all_emotions": {}
        }