import numpy as np
from ultralytics import YOLO
import cv2

# นำเข้าโมดูล numpy, ultralytics.YOLO และ cv2
# numpy ใช้สำหรับการคำนวณเชิงคณิตศาสตร์
# ultralytics.YOLO เป็นไลบรารีสำหรับ Object Detection ด้วยโมเดล YOLO
# cv2 ใช้สำหรับการประมวลผลภาพและวิดีโอ

model = YOLO("YOLO_data/yolov8s.pt")
# โหลดโมเดล YOLOv8 จากไฟล์ yolov8s.pt ในโฟลเดอร์ YOLO_data
# และเก็บเป็นตัวแปร model
cap = cv2.VideoCapture("Video/IMG_3809.MOV")
# กำหนดว่าจะใช้ไฟล์วิดีโอ IMG_3809.MOV ในโฟลเดอร์ Video เป็นแหล่งที่มาของวิดีโอ
# และเก็บเป็นตัวแปร cap
area = np.array([[0, 138], [535, 88], [1020, 125], [1020, 500]])
# กำหนดพื้นที่ที่ต้องการตรวจจับวัตถุ โดยใช้ numpy array ที่มีขนาด 4x2
# โดยแต่ละแถวแทนจุดเริ่มต้นและจุดสิ้นสุดของเส้นตรง
with open("YOLO_data/coco.txt", "r") as f:
    class_list = [line.strip() for line in f.readlines()]


# เปิดไฟล์ coco.txt ในโฟลเดอร์ YOLO_data เพื่อดึงรายชื่อคลาสจากไฟล์
# และเก็บไว้ในตัวแปร class_list

# ฟังก์ชันสำหรับสร้างผลลัพธ์
def generate():
    while True:
        lists = []
        ret, frame = cap.read()
        if not ret:
            break
        else:
            # ปรับขนาดเฟรมเพื่อให้เข้ากับโมเดล
            frame = cv2.resize(frame, (1020, 500))
            # ทำนายผลด้วยโมเดล
            results = model.predict(frame)
            data = results[0].boxes.boxes
            pdate = np.array(data).astype("float")

            # วนลูปตรวจสอบ object
            for row in pdate:
                x1, y1, x2, y2, conf, d = map(int, row)
                class_name = class_list[d]
                if d == 3:
                    center_x = (x1 + x2) // 2
                    center_y = (y1 + y2) // 2
                    results = cv2.pointPolygonTest(area, (center_x, center_y), False)
                    # ตรวจสอบว่า object อยู่ในพื้นที่ที่สนใจหรือไม่
                    if results >= 0:
                        # วาดสี่เหลี่ยมรอบ object และแสดงชื่อ class
                        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                        cv2.putText(frame, str(class_name), (x1, y1), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0))
                        lists.append(class_name)
            # แสดงจำนวน object ที่พบ
            cv2.putText(frame, "Count: " + str(int(read_file())), (10, 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
            # วาดพื้นที่ที่สนใจ
            cv2.polylines(frame, [area], True, (255, 0, 0), 2)
            return frame, len(lists)


def read_file():
    # สร้างตัวแปร data ในรูปแบบ numpy array และกำหนดค่าเริ่มต้นเป็น 0
    data = np.empty(0)
    # เปิดไฟล์ "count_File.txt" โดยใช้คำสั่ง with เพื่อรับประกันว่าไฟล์จะถูกปิดอัตโนมัติเมื่อเสร็จสิ้นการทำงาน
    with open("count_File.txt", "r") as f:
        try:
            # อ่านข้อมูลจากไฟล์โดยใช้ readline() และแยกข้อมูลด้วย "," จากนั้นเก็บข้อมูลลงในตัวแปร x
            x = f.readline().split(",")
            # เพิ่มค่าจำนวนที่ได้อ่านมาในตัวแปร data โดยแปลงค่าให้อยู่ในรูปแบบ integer ก่อน
            data = np.append(data, int(x[0]))
        except:
            # กรณีเกิดข้อผิดพลาดในการอ่านข้อมูลจากไฟล์ ให้เพิ่มค่า 0 เข้าไปในตัวแปร data
            data = np.append(data, int(0))
    # คำนวณค่าเฉลี่ยของข้อมูลทั้งหมดที่ได้อ่านมา และคืนค่าออกมาเป็นผลลัพธ์
    return np.mean(data)
