import cv2
import mediapipe as mp
import numpy as np
import json
from tqdm import tqdm

mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands

#추출하고 손의 랜드마크 id를 수정해야 함 
# 현재에는 2,5,9,13,17의 각도를 구한 것
finger_landmarks = {'Thumb': [0, 2, 3], 'Index Finger': [0, 5, 6], 'Middle Finger': [0, 9, 10], 'Ring Finger': [0, 13, 14], 'Pinky': [0, 17, 18]}

#손가락의 각도 구하는 함수
def calculate_angle(a, b, c):
    a = np.array(a)
    b = np.array(b)
    c = np.array(c)

    ba = a - b
    bc = c - b

    cosine_angle = np.dot(ba, bc) / (np.linalg.norm(ba) * np.linalg.norm(bc))
    angle = np.arccos(cosine_angle)

    return np.degrees(angle)

both_hands_detected_frames = 0

# 비디오 파일 경로 설정 (실제 파일 경로로 교체)
video_path = "C:/Users/Desktop/video/drive-download-20240124T011103Z-00.mp4"
cap = cv2.VideoCapture(video_path)

# 비디오 파일 여는데 실패한 경우 에러 출력 후 종료
if not cap.isOpened():
    print("비디오 파일을 열 수 없습니다.")
    exit()

# 비디오 속성 가져오기
fps = int(cap.get(cv2.CAP_PROP_FPS))
frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

# mediapipe Hands 모델 초기화
with mp_hands.Hands(min_detection_confidence=0.8, min_tracking_confidence=0.5) as hands:
    frame_number = 0

    # 각 손가락별로 JSON 파일을 열기 위한 딕셔너리 초기화 경로 설정 수정 
    json_files_left = {finger: open(f'C:/Users/Desktop/curve/landmarks_curve_left_{finger}.json', 'w') for finger in finger_landmarks}
    json_files_right = {finger: open(f'C:/Users/Desktop/curve/landmarks_curve_right_{finger}.json', 'w') for finger in finger_landmarks}

    for _ in tqdm(range(frame_count)):
        ret, frame = cap.read()

        if not ret:
            break  # 비디오가 끝나면 루프 종료

        frame_number += 1

        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image.flags.writeable = False
        results = hands.process(image)
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        landmarks_data_left = {}
        landmarks_data_right = {}

        if results.multi_hand_landmarks:
            hands_count = len(results.multi_hand_landmarks)
            if hands_count == 2:
                # 왼손, 오른손 분류
                if results.multi_hand_landmarks[0].landmark[0].x > results.multi_hand_landmarks[1].landmark[0].x:
                    left_hand = results.multi_hand_landmarks[0]
                    right_hand = results.multi_hand_landmarks[1]
                else:
                    left_hand = results.multi_hand_landmarks[1]
                    right_hand = results.multi_hand_landmarks[0]
                both_hands_detected_frames += 1

            elif hands_count == 1:
                # 한 손만 감지된 경우
                if results.multi_hand_landmarks[0].landmark[4].x < results.multi_hand_landmarks[0].landmark[20].x:
                    left_hand = results.multi_hand_landmarks[0]
                    right_hand = None
                else:
                    left_hand = None
                    right_hand = results.multi_hand_landmarks[0]
            else:
                left_hand = None
                right_hand = None
        else:
            left_hand = None
            right_hand = None

        for finger, points in finger_landmarks.items():
            if left_hand is not None:
                angle_left = calculate_angle(
                    [left_hand.landmark[points[0]].x, left_hand.landmark[points[0]].y],
                    [left_hand.landmark[points[1]].x, left_hand.landmark[points[1]].y],
                    [left_hand.landmark[points[2]].x, left_hand.landmark[points[2]].y])
                landmarks_data_left[finger] = angle_left
            else:
                landmarks_data_left[finger] = None

            if right_hand is not None:
                angle_right = calculate_angle(
                    [right_hand.landmark[points[0]].x, right_hand.landmark[points[0]].y],
                    [right_hand.landmark[points[1]].x, right_hand.landmark[points[1]].y],
                    [right_hand.landmark[points[2]].x, right_hand.landmark[points[2]].y])
                landmarks_data_right[finger] = angle_right
            else:
                landmarks_data_right[finger] = None

        # 왼손 각도 데이터를 파일에 저장
        for finger, angle in landmarks_data_left.items():
            json.dump(angle, json_files_left[finger])
            json_files_left[finger].write('\n')

        # 오른손 각도 데이터를 파일에 저장
        for finger, angle in landmarks_data_right.items():
            json.dump(angle, json_files_right[finger])
            json_files_right[finger].write('\n')

# 파일 닫기
for file in json_files_left.values():
    file.close()

for file in json_files_right.values():
    file.close()

cap.release()  # 비디오 캡처 객체 해제
print(f"양손이 모두 감지된 프레임 수: {both_hands_detected_frames}")
