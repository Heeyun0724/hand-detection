import json
import cv2
import mediapipe as mp

mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands

def onChange(pos):
    cap.set(cv2.CAP_PROP_POS_FRAMES, pos)

def detect_hands_in_video(cap):
    landmarks_data_left = [[] for _ in range(21)]  # 21개의 랜드마크를 가집니다.
    landmarks_data_right = [[] for _ in range(21)]  # 21개의 랜드마크를 가집니다.
    #fps = 5  # 초당 5프레임으로 설정
    #cap.set(cv2.CAP_PROP_FPS, fps)  # 초당 프레임 수 설정

    with mp_hands.Hands(min_detection_confidence=0.5, min_tracking_confidence=0.5, max_num_hands=2) as hands:
        while cap.isOpened():
            position = cv2.getTrackbarPos('Position', 'MediaPipe Hands')
            cap.set(cv2.CAP_PROP_POS_FRAMES, position)
            ret, frame = cap.read()
            if not ret:
                break

            # Convert the BGR image to RGB.
            image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            # Process the image and find the hand landmarks.
            results = hands.process(image)

            # Draw the hand landmarks on the image.
            if results.multi_hand_landmarks:
                hands_count = len(results.multi_hand_landmarks)
                for hand_landmarks in results.multi_hand_landmarks:
                    mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

                for id in range(21):  # For each landmark
                    if hands_count == 2:
                        if results.multi_hand_landmarks[0].landmark[0].x > results.multi_hand_landmarks[1].landmark[0].x:
                            left_hand = results.multi_hand_landmarks[0]
                            right_hand = results.multi_hand_landmarks[1]
                        else:
                            left_hand = results.multi_hand_landmarks[1]
                            right_hand = results.multi_hand_landmarks[0]
                            
                        coordinate_left = [left_hand.landmark[id].x, left_hand.landmark[id].y, left_hand.landmark[id].z]
                        coordinate_right = [right_hand.landmark[id].x, right_hand.landmark[id].y, right_hand.landmark[id].z]
                        landmarks_data_left[id].append(coordinate_left)
                        landmarks_data_right[id].append(coordinate_right)
                    elif hands_count == 1:  # If only one hand is detected
                        # Determine if the hand is left or right based on the position of the thumb and pinky
                        if results.multi_hand_landmarks[0].landmark[4].x < results.multi_hand_landmarks[0].landmark[20].x:
                            coordinate_right = [results.multi_hand_landmarks[0].landmark[id].x, results.multi_hand_landmarks[0].landmark[id].y, results.multi_hand_landmarks[0].landmark[id].z]
                            landmarks_data_right[id].append(coordinate_right)
                            landmarks_data_left[id].append([])
                        else:
                            coordinate_left = [results.multi_hand_landmarks[0].landmark[id].x, results.multi_hand_landmarks[0].landmark[id].y, results.multi_hand_landmarks[0].landmark[id].z]
                            landmarks_data_left[id].append(coordinate_left)
                            landmarks_data_right[id].append([])
                    else:  # If no hands are detected
                        landmarks_data_left[id].append([])
                        landmarks_data_right[id].append([])
            else:  # If no hands are detected
                for id in range(21):
                    landmarks_data_left[id].append([])
                    landmarks_data_right[id].append([])

            cv2.imshow('MediaPipe Hands', frame)
            cv2.setTrackbarPos('Position', 'MediaPipe Hands', int(cap.get(cv2.CAP_PROP_POS_FRAMES)))
            if cv2.waitKey(5) & 0xFF == 27:
                break


    for id, data in enumerate(landmarks_data_left):
        with open(f'C:/Users/Desktop/KIST/landmark/landmarks_data_left_{id}.json', 'w') as f:
            json.dump(data, f)  # 데이터를 JSON 형식으로 파일에 씁니다.

    for id, data in enumerate(landmarks_data_right):
        with open(f'C:/Users/Desktop/KIST/landmark/landmarks_data_right_{id}.json', 'w') as f:
            json.dump(data, f)  # 데이터를 JSON 형식으로 파일에 씁니다.


    cv2.destroyAllWindows()


cap = cv2.VideoCapture("C:/Users/Desktop/video/drive-download-20240124T011103Z-002/240123_13_SI008L0F_T2_output.mp4")
cv2.namedWindow('MediaPipe Hands')
total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
cv2.createTrackbar('Position', 'MediaPipe Hands', 0, total_frames, onChange)
detect_hands_in_video(cap)
cap.release()