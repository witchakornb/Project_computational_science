import connectDB
from flask import Flask, render_template, Response, make_response
import cv2
import schedule
from detection import generate, read_file

app = Flask(__name__)


# ลบไฟล์
def remove_file():
    f = open("count_FIle.txt", "w")
    f.close()


# กำหนดการทำงานทุก ๆ 1 นาที และ 10 วินาที
schedule.every(1).minutes.do(connectDB.insertDB)
schedule.every(10).seconds.do(remove_file)


# เพิ่มข้อมูลลงในไฟล์
def add_file(data):
    with open("count_FIle.txt", "a") as f:
        f.write(f"{data},\n")


# ทำการแปลภาพเป็น byte
def frame1():
    while True:
        schedule.run_pending()
        frame = generate()
        add_file(frame[1])
        frame = frame[0]
        _, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


# หน้าเริ่มต้นของเว็บ
@app.route('/')
def index():
    return make_response(render_template('index.html', name=str(int(read_file()))))


# หน้าต่างของ video
@app.route('/video')
def video():
    return Response(frame1(), mimetype='multipart/x-mixed-replace; boundary=frame', )


if __name__ == '__main__':
    app.run(debug=True)
