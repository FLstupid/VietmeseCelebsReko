import boto3
from tkinter import *
from PIL import Image,ImageTk, ImageDraw
import cv2
import numpy as np
import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
from tkinter import filedialog


# def xuly(event):
#     global root
#     root.filename = filedialog.askopenfilename(initialdir="", title="Select A File",
#                                                filetypes=(("mp4 files", "*.mp4"), ("all files", "*.*")))
#     print(root.filename)
# root = Tk()
# root.title("Nhận diện khuôn mặt")
# root.geometry('400x300')
# bt=tk.Button(root,text='OPEN',fg='black')
# bt.pack(side=TOP,fill=BOTH)
# bt.bind('<Button-1>',xuly)
# root.mainloop()
access_key_id = 'ASIA4AO7KQFMOKIV6LFU'
secret_access_key = 'h+uJShh5pHfW/XbsivEY5CiuLhj2/PHQ+z+EiFqK'
session_token = 'FwoGZXIvYXdzEDgaDEXG+mXsb/dkz6UN4SLPAXHOV3fEwgbFjFXyQsNujyWW8qtV4IUoj5e/YuhmB5AndpZxmFoMcXDDxymaWivLHaSR39SoaMMKqoj/uSS0oToEC8ReDp7sJ4DVVSTaFitUAXCnQOyhEIuewyp8jR8nFQNeyHd3r0Jgu+n6T9IhbW8o+12AjrzKKngklMj6YZFQzopF9fLHZpEnfAkmdT2i57EPcPj1Yu3qHMVjT/5f7prJpcUB+u8H9/cWVbPz9f5fwZIP6lai1Gzb+ht+Ip4E5HghgjmLutYPm75pZJz7/yjR+piNBjItzGrB/jVmHwovEd9cXn2o6PnyxmOtZCrEDEuRbQhc92P+Fjm5p3Qv26xyCdLj'
region = 'us-east-1'
client=boto3.client('rekognition',
                    region_name=region,
                    aws_access_key_id=access_key_id,
                    aws_secret_access_key=secret_access_key,
                    aws_session_token=session_token)
s3 = boto3.resource(
    service_name='s3',
    region_name=region,
    aws_access_key_id=access_key_id,
    aws_secret_access_key=secret_access_key,
    aws_session_token=session_token
)

currentframe=0;
def Chuyendoi(anh):
    with open(anh, 'rb') as source_image:
        source_bytes = source_image.read()
        return source_bytes
def Checkmang(arr,index):
    for i in range(0, len(arr)):
        if arr[i] == index:
            return True
    return False
def Kiemtrasoluong(source_bytes):
    response = client.detect_labels(Image={'Bytes': source_bytes})
    i = 0
    while i < len(response['Labels']):
        if response['Labels'][i]['Name'] == 'Person':
            return len(response['Labels'][i]['Instances'])
            break
        i += 1
def Sosanh(source_bytes):
    gioihan=Kiemtrasoluong(source_bytes)
    index = 0
    dem=0
    cohieu=False
    ketqua=[]
    while dem<gioihan:
        while (index<51):
            anh = './celebs' + str(index) + '.jpg'
            with open(anh, 'rb') as source_image:
                source_bytes2 = source_image.read()
            response = client.compare_faces(SourceImage={'Bytes': source_bytes2}, TargetImage={'Bytes': source_bytes})
            if(response['FaceMatches']!=[]):
                if(response['FaceMatches'][0]['Similarity']>70):
                    if Checkmang(ketqua,index)==False:
                        ketqua.append(index)
                        cohieu=True
                        index=0
                        break;
            index += 1
        dem+=1
        if cohieu==False:
            ketqua.append(-1)
        cohieu=False
    return ketqua
def kiemTraNgheSi(index):
    switcher={
        0: 'Châu Bùi',
        1: 'Sơn Tùng M-TP',
        2: 'Elon Musk',
        3: 'Chi Pu',
        4: 'Đông Nhi',
        5: 'Ông Cao Thắng',
        6: 'Karik',
        7: 'Mai Phương Thúy',
        8: 'Trường Giang',
        9: 'Nhã Phương',
        10: 'Trấn Thành',
        11: 'Hari Won',
        12: 'Erik',
        13: 'Đức Phúc',
        14: 'Hòa Minzy',
        15: 'Bích Phương',
        16: 'Đen Vâu',
        17: 'Hương Giang',
        18: 'Mỹ Tâm',
        19: 'Minh Hằng',
        20: 'Hồ Ngọc Hà',
        21: 'Bảo Anh',
        22: 'Hồ Quang Hiếu',
        23: 'Ngọc Trinh',
        24: 'Diệu Nhi',
        25: 'Binz',
        26: 'Khởi My',
        27: 'Kevil Khánh',
        28: 'siêu mẫu Thanh Hằng',
        29: 'Hoài Linh',
        30: 'Đỗ Thị Hà',
        31: 'Khánh Vân',
        32: 'Trần Tiểu Vy',
        33: 'Đỗ Mỹ Linh',
        34: "H'hen Nie",
        35: 'AMEE',
        36: 'Noo Phước Thịnh',
        37: 'Ninh Dương Lan Ngọc',
        38: 'Lý Hải',
        39: 'Mạc Văn Khoa',
        40: 'Đàm Vĩnh Hưng',
        41: 'Thủy Tiên',
        42: 'Lương Xuân Trường',
        43: 'Quế Ngọc Hải',
        44: 'Trần Đình Trọng',
        45: 'thủ môn Bùi Tiến Dũng',
        46: 'Phan Văn Đức',
        47: 'Duy Mạnh',
        48: 'Đoàn Văn Hậu',
        49: 'Hồ Chí Minh',
        50: 'Võ Nguyên Giáp',
    }
    return switcher.get(index,"Không nhận dạng được")
win = Tk()
win.geometry("600x600+200+30")
win.resizable(False, False)
win.configure(bg ='white')
r = 400
d = 300

color = "#00406e"
frame_1 = Frame(win,width = 600,height =320,bg = color).place(x=0,y=0)
frame_2 = Frame(win,width = 600,height =320,bg = color).place(x=0,y=350)

v = Label(frame_1, width=r, height=d)
v.place(x=10, y=10)
cap = cv2.VideoCapture("C:\\Users\\Admin\\PycharmProjects\\pythonProject\\QC.mp4")

frm = Label(frame_2,bg="black", width=43, height=13, borderwidth=1).place(x=10, y=370)
def take_copy(im):
    la = Label(frame_2, width=r-100, height=d-100)
    la.place(x=10, y=370)
    copy = im.copy()
    copy = cv2.resize(copy, (r-100, d-100))
    rgb = cv2.cvtColor(copy, cv2.COLOR_BGR2RGB)
    image = Image.fromarray(copy)
    imgtk = ImageTk.PhotoImage(image)
    la.configure(image=imgtk)
    la.image = imgtk
    name = './data/frame' + str(currentframe) + '.jpg'
    cv2.imwrite(name, rgb)
    vitri = Sosanh(Chuyendoi(name))
    for i in range(0, len(vitri)):
        ketqua=kiemTraNgheSi(vitri[i])
        save = Label(win, text=ketqua)
        save.place(x=350, y=400+i*25)
    # ketqua=kiemTraNgheSi(vitri)
    # print(ketqua)
    # save = Label(win,text = ketqua)
    # save.place(x=450,y=500)


def select_img():
    global rgb
    _, img = cap.read()
    img = cv2.resize(img, (r, d))
    rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    image = Image.fromarray(rgb)
    imgtk = ImageTk.PhotoImage(image)
    v.configure(image=imgtk)
    v.image = imgtk
    v.after(5, select_img)


select_img()
snap = Button(win, text="capture", command=lambda: take_copy(rgb))
snap.place(x=450, y=150, width=60, height=50)

win.mainloop()