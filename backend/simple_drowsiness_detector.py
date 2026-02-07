import cv2
import numpy as np
import threading
import time
import pygame
import os
from datetime import datetime
import mediapipe as mp

class SimpleDrowsinessDetector:
    def __init__(self):
        # Eye Aspect Ratio threshold
        self.EYE_AR_THRESH = 0.25
        self.EYE_AR_CONSEC_FRAMES = 30
        
        # Initialize counters and flags
        self.COUNTER = 0
        self.ALARM_ON = False
        self.is_running = False
        
        # Initialize MediaPipe Face Mesh
        self.mp_face_mesh = mp.solutions.face_mesh
        self.face_mesh = self.mp_face_mesh.FaceMesh(
            static_image_mode=False,
            max_num_faces=1,
            refine_landmarks=True,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5
        )
        
        # Eye landmark indices for MediaPipe
        self.LEFT_EYE = [362, 382, 381, 380, 374, 373, 390, 249, 263, 466, 388, 387, 386, 385, 384, 398]
        self.RIGHT_EYE = [33, 7, 163, 144, 145, 153, 154, 155, 133, 173, 157, 158, 159, 160, 161, 246]
        
        # Initialize pygame for sound
        try:
            pygame.mixer.init()
            self.alarm_sound = None
            self.create_alarm_sound()
        except:
            print("Warning: Could not initialize sound system")
            
        # Statistics
        self.total_blinks = 0
        self.sleep_alerts = 0
        self.session_start = datetime.now()
        
    def create_alarm_sound(self):
        """Create a simple alarm tone"""
        try:
            # Generate a simple alarm beep
            sample_rate = 22050
            duration = 1.0
            frequency = 800
            
            frames = int(duration * sample_rate)
            arr = np.zeros((frames, 2))
            
            for i in range(frames):
                wave = np.sin(2 * np.pi * frequency * i / sample_rate)
                arr[i] = [wave * 0.3, wave * 0.3]
            
            # Convert to 16-bit integers
            arr = (arr * 32767).astype(np.int16)
            
            # Save as temporary file
            import wave
            with wave.open("temp_alarm.wav", "w") as f:
                f.setnchannels(2)
                f.setsampwidth(2)
                f.setframerate(sample_rate)
                f.writeframes(arr.tobytes())
                
            self.alarm_sound = "temp_alarm.wav"
        except Exception as e:
            print(f"Could not create alarm sound: {e}")
    
    def calculate_ear(self, landmarks, eye_indices):
        """Calculate Eye Aspect Ratio using MediaPipe landmarks"""
        try:
            # Get eye landmarks
            eye_points = []
            for idx in eye_indices:
                if idx < len(landmarks):
                    x = landmarks[idx].x
                    y = landmarks[idx].y
                    eye_points.append([x, y])
            
            if len(eye_points) < 6:
                return 0
            
            # Convert to numpy array
            eye_points = np.array(eye_points)
            
            # Calculate distances
            # Vertical distances
            v1 = np.linalg.norm(eye_points[1] - eye_points[5])
            v2 = np.linalg.norm(eye_points[2] - eye_points[4])
            
            # Horizontal distance
            h = np.linalg.norm(eye_points[0] - eye_points[3])
            
            # Calculate EAR
            if h > 0:
                ear = (v1 + v2) / (2.0 * h)
            else:
                ear = 0
                
            return ear
        except:
            return 0
    
    def play_alarm(self):
        """Play alarm sound"""
        try:
            if self.alarm_sound and os.path.exists(self.alarm_sound):
                pygame.mixer.music.load(self.alarm_sound)
                pygame.mixer.music.play(-1)  # Loop indefinitely
        except Exception as e:
            print(f"Could not play alarm: {e}")
    
    def stop_alarm(self):
        """Stop alarm sound"""
        try:
            pygame.mixer.music.stop()
        except:
            pass
    
    def detect_drowsiness(self, frame):
        """Main drowsiness detection function using MediaPipe"""
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.face_mesh.process(rgb_frame)
        
        drowsiness_detected = False
        status = "Alert"
        ear = 0
        
        if results.multi_face_landmarks:
            for face_landmarks in results.multi_face_landmarks:
                # Calculate EAR for both eyes
                left_ear = self.calculate_ear(face_landmarks.landmark, self.LEFT_EYE[:6])
                right_ear = self.calculate_ear(face_landmarks.landmark, self.RIGHT_EYE[:6])
                
                # Average EAR
                ear = (left_ear + right_ear) / 2.0
                
                # Draw eye landmarks
                h, w, _ = frame.shape
                for idx in self.LEFT_EYE[:6] + self.RIGHT_EYE[:6]:
                    if idx < len(face_landmarks.landmark):
                        x = int(face_landmarks.landmark[idx].x * w)
                        y = int(face_landmarks.landmark[idx].y * h)
                        cv2.circle(frame, (x, y), 2, (0, 255, 0), -1)
                
                # Check for drowsiness
                if ear < self.EYE_AR_THRESH:
                    self.COUNTER += 1
                    
                    if self.COUNTER >= self.EYE_AR_CONSEC_FRAMES:
                        if not self.ALARM_ON:
                            self.ALARM_ON = True
                            self.sleep_alerts += 1
                            self.play_alarm()
                        
                        drowsiness_detected = True
                        status = "DROWSINESS ALERT!"
                        cv2.putText(frame, "DROWSINESS ALERT!", (10, 30),
                                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
                        cv2.putText(frame, "WAKE UP!", (10, 70),
                                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
                else:
                    self.COUNTER = 0
                    if self.ALARM_ON:
                        self.ALARM_ON = False
                        self.stop_alarm()
                        self.total_blinks += 1
        else:
            status = "No face detected"
        
        # Display information
        cv2.putText(frame, f"EAR: {ear:.2f}", (300, 30), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
        cv2.putText(frame, f"Blinks: {self.total_blinks}", (10, 100),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
        cv2.putText(frame, f"Alerts: {self.sleep_alerts}", (10, 130),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
        cv2.putText(frame, f"Status: {status}", (10, 160),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
        
        return frame, drowsiness_detected, status
    
    def start_detection(self, camera_index=0):
        """Start the drowsiness detection"""
        self.is_running = True
        cap = cv2.VideoCapture(camera_index)
        
        if not cap.isOpened():
            print("Error: Could not open camera")
            return
        
        print("Drowsiness Detection Started (MediaPipe). Press 'q' to quit.")
        
        while self.is_running:
            ret, frame = cap.read()
            if not ret:
                break
            
            # Flip frame horizontally for mirror effect
            frame = cv2.flip(frame, 1)
            
            # Detect drowsiness
            frame, drowsy, status = self.detect_drowsiness(frame)
            
            # Display frame
            cv2.imshow("Drowsiness Detection - Smart Grocery Planner", frame)
            
            # Break on 'q' key press
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        
        # Cleanup
        cap.release()
        cv2.destroyAllWindows()
        self.stop_alarm()
    
    def stop_detection(self):
        """Stop the drowsiness detection"""
        self.is_running = False
    
    def get_statistics(self):
        """Get detection statistics"""
        session_duration = datetime.now() - self.session_start
        return {
            "session_duration": str(session_duration),
            "total_blinks": self.total_blinks,
            "sleep_alerts": self.sleep_alerts,
            "current_status": "Running" if self.is_running else "Stopped",
            "detection_method": "MediaPipe Face Mesh"
        }

# Web interface integration
class DrowsinessWebInterface:
    def __init__(self):
        self.detector = SimpleDrowsinessDetector()
        self.detection_thread = None
        
    def start_web_detection(self):
        """Start detection in a separate thread for web interface"""
        if self.detection_thread is None or not self.detection_thread.is_alive():
            self.detection_thread = threading.Thread(target=self.detector.start_detection)
            self.detection_thread.daemon = True
            self.detection_thread.start()
            return {"status": "started", "message": "Drowsiness detection started using MediaPipe"}
        else:
            return {"status": "already_running", "message": "Detection already running"}
    
    def stop_web_detection(self):
        """Stop detection"""
        self.detector.stop_detection()
        return {"status": "stopped", "message": "Drowsiness detection stopped"}
    
    def get_web_statistics(self):
        """Get statistics for web interface"""
        return self.detector.get_statistics()

if __name__ == "__main__":
    # Test the drowsiness detector
    detector = SimpleDrowsinessDetector()
    detector.start_detection()
