import boto3
import cv2
import os
import mediapipe as mp
import time
from tkinter import *
from PIL import Image, ImageTk
import cv2
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
access_key_id = 'ASIA5FOTSP45MY7C27XK'
secret_access_key = 'aZ5EFtmXAcFklRWKOmgf/UVNDleOWQjrNGrJB0ga'
session_token = 'FwoGZXIvYXdzENL//////////wEaDGJcgpfb3CKryrBxQCLPAT9rf7AAIM36sWFtjSszYOwBPezn2EePYfTALI43H903n80eilFD1P5r9Ga9yHQXMqlEolUmt0pDBJkvwgHUXQ3sGSG/aldvVOmspQxEMFV6/0TQ/zTCGnmuzpVDpI9a686WzngBdNwOFv6JblCQfcAq+Iy4Z3OQLnWcLD05toW4kPrrDwBsRwRgABjp5U7zqsZDKHzuiv7LsXKCJ6LnkAEq3tArBPxfuh5qxOJY4PpJEjgEFFot56PuwHqCWDP8pxSsutRkYbBsphisiNFOmSiR1rqNBjItqKbOINPUKTU4fbA8QMXocmNmgSrzmzvuvBhdp7WBmFC9uHId5PLkx4M0Psff'
region = 'us-east-1'
client = boto3.client('rekognition',
                      region_name=region,
                      aws_access_key_id=access_key_id,
                      aws_secret_access_key=secret_access_key,
                      aws_session_token=session_token)
photo = 'SonTung.jpg'
photo2 = 'frame69.jpg'
s3 = boto3.resource(
    service_name='s3',
    region_name=region,
    aws_access_key_id=access_key_id,
    aws_secret_access_key=secret_access_key,
    aws_session_token=session_token
)

currentframe = 0;


def Chuyendoi(anh):
    with open(anh, 'rb') as source_image:
        source_bytes = source_image.read()
        return source_bytes


def Checkmang(arr, index):
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
        i += 1


def Sosanh(source_bytes):
    gioihan = Kiemtrasoluong(source_bytes)
    index = 0
    dem = 0
    cohieu = False
    ketqua = []
    while dem < gioihan:
        while index < 9:
            anh = './celebs' + str(index) + '.jpg'
            with open(anh, 'rb') as source_image:
                source_bytes2 = source_image.read()
            response = client.compare_faces(SourceImage={'Bytes': source_bytes2}, TargetImage={'Bytes': source_bytes})
            print(response)
            print('-------------')
            if response['FaceMatches'] != []:
                if response['FaceMatches'][0]['Similarity'] > 50:
                    if not Checkmang(ketqua, index):
                        ketqua.append(index)
                        cohieu = True
                        index = 0
                        break
            index += 1
        dem += 1
        if not cohieu:
            ketqua.append(-1)
        cohieu = False
    return ketqua


def kiemTraNgheSi(index):
    switcher = {
        0: 'Châu Bùi',
        1: 'Sơn Tùng M-TP',
        2: 'Elon Musk',
        3: 'Quang Lê',
        4: 'Đông Nhi',
        5: 'Ông Cao Thắng',
        6: 'Erik',
        7: 'Bích Phương',
        8: 'Trường Giang',
    }
    return switcher.get(index, "Không nhận dạng được")


win = Tk()
win.geometry("600x600+200+30")
win.resizable(False, False)
win.configure(bg='#1b407a')
w = 400
h = 300

color = "#581845"
frame_1 = Frame(win, width=600, height=320, bg=color).place(x=0, y=0)
frame_2 = Frame(win, width=600, height=320, bg=color).place(x=0, y=350)

v = Label(frame_1, width=w, height=h)
v.place(x=10, y=10)
cap = cv2.VideoCapture("Test.mp4")


def take_copy(im):
    la = Label(frame_2, width=w - 100, height=h - 100)
    la.place(x=10, y=370)
    copy = im.copy()
    copy = cv2.resize(copy, (w - 100, h - 100))
    rgb = cv2.cvtColor(copy, cv2.COLOR_BGR2RGB)
    image = Image.fromarray(copy)
    imgtk = ImageTk.PhotoImage(image)
    la.configure(image=imgtk)
    la.image = imgtk
    name = './data/frame' + str(currentframe) + '.jpg'
    cv2.imwrite(name, rgb)
    vitri = Sosanh(Chuyendoi(name))
    for i in range(0, len(vitri)):
        ketqua = kiemTraNgheSi(vitri[i])
        save = Label(win, text=ketqua)
        save.place(x=450, y=500 + i * 25)
    # ketqua=kiemTraNgheSi(vitri)
    # print(ketqua)
    # save = Label(win,text = ketqua)
    # save.place(x=450,y=500)


def select_img():
    global rgb
    _, img = cap.read()
    if img is not None:
        img = cv2.resize(img, (w, h))
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
