import mariadb
from detection import read_file


# import library mariadb และ module read_file จาก detection
def connectDB():
    # สร้างฟังก์ชัน connectDB() เพื่อเชื่อมต่อกับฐานข้อมูล
    try:
        conn = mariadb.connect(
            user="root",
            password="123456789",
            host="127.0.0.1",
            port=3306,
            database="user"
        )
        # ใช้ mariadb.connect() เพื่อเชื่อมต่อฐานข้อมูลด้วย username, password, host, port, database
    except mariadb.Error as ex:
        print(f"An error occurred while connecting to MariaDB: {ex}")
        # แสดงข้อผิดพลาด (error) กรณีไม่สามารถเชื่อมต่อกับฐานข้อมูลได้
    return conn
    # ส่งค่า conn กลับเพื่อให้ใช้ในการเรียกใช้ในฟังก์ชันอื่น


def insertDB():
    # สร้างฟังก์ชัน insertDB() เพื่อบันทึกข้อมูลลงในฐานข้อมูล
    con = connectDB()
    # เรียกใช้ฟังก์ชัน connectDB() เพื่อเชื่อมต่อกับฐานข้อมูลและรับค่า conn
    cur = con.cursor()
    # สร้าง cursor เพื่อใช้ส่งคำสั่ง SQL ไปยังฐานข้อมูล
    cur.execute("INSERT INTO data (count, location) VALUES (%d, %s)", (read_file(), 'อาคารวิทยวิภาส (SC09)'))
    # ส่งคำสั่ง SQL เพื่อเพิ่มข้อมูล count และ location ลงในตาราง data
    con.commit()
    # ยืนยันการเปลี่ยนแปลงข้อมูลในฐานข้อมูล
