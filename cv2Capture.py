import facial_keypoints_detecter as fkd
import matplotlib.pyplot as plt
import cv2
import time
import os
import shutil
from pymsgbox import *
import threading
import tkinter
from tkinter import *
from PIL import Image, ImageTk
from time import sleep


global Graph
global cam
global Capture
global Msg
Msg = "Initialising System..."
Graph = None


cam = cv2.VideoCapture(0)


def TkinterWindow():
    global Capture
    global Msg
    global cam
    # Python program to open the
    # camera in Tkinter
    # Import the libraries,
    # tkinter, cv2, Image and ImageTk

    # Define a video capture object
    #vid = cv2.VideoCapture(3)

    # Declare the width and height in variables
    width, height = 800, 600

    # Set the width and height
    #vid.set(cv2.CAP_PROP_FRAME_WIDTH, width)
    #vid.set(cv2.CAP_PROP_FRAME_HEIGHT, height)

    # Create a GUI app
    app = Tk()
    app.title("Group 1's Additonal Maths Project 2023")

    # Bind the app with Escape keyboard to
    # quit app whenever pressed
    #app.bind('<Escape>', lambda e: app.quit())
    app.geometry("1067x800+1273+0")
    #app.attributes("-fullscreen", True)

    # Create a label and display it on app
    label_widget = Label(app)
    label_widget.pack()
    msg = Label(app)
    msg.config(font=('TkDefaultFont', 20))
    msg.pack()

    # Create a function to open camera and
    # display it in the label_widget on app


    def open_camera():
        global Capture
        global Msg
        global cam
        # Capture the video frame by frame
        Capture = cam.read()
        _, frame = Capture

        # Convert image from one color space to other
        try:
            opencv_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
        except:
            pass
            #app.destroy()
            #raise RuntimeError("Main Thread Closed")

        # Capture the latest frame and transform to image
        if Graph == None:
            captured_image = Image.fromarray(cv2.flip(opencv_image, 1))
        else:
            #app.attributes("-fullscreen", True)
            captured_image = Image.fromarray(cv2.cvtColor(cv2.imread(Graph), cv2.COLOR_BGR2RGBA))

        # Convert captured image to photoimage
        try:
            photo_image = ImageTk.PhotoImage(image=captured_image)
        except RuntimeError:
            pass #Waiting for Camera to start

        msg.configure(text=Msg)

        # Displaying photoimage in the label
        try:
            label_widget.photo_image = photo_image
        except:
            pass #Waiting for Camera to start

        # Configure image in the label
        try:
            label_widget.configure(image=photo_image)
        except:
            pass #Camera is starting

        # Repeat the same process after every 10 seconds
        label_widget.after(10, open_camera)


    '''# Create a button to open the camera in GUI app
    button1 = Button(app, text="Open Camera", command=open_camera)
    button1.pack()'''
    open_camera()

    # Create an infinite loop for displaying app on screen
    app.mainloop()

    


net = fkd.model.Net()
net.load_model('saved_model_facial_keypoints_detector.pt')


#cv2.namedWindow("FaceKeyPointReaderClient", cv2.WINDOW_NORMAL)
#cv2.moveWindow("FaceKeyPointReaderClient", 1280,0)
#cv2.setWindowProperty("FaceKeyPointReaderClient", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
cv2.namedWindow("FaceKeyPointReader", cv2.WINDOW_NORMAL)
cv2.moveWindow("FaceKeyPointReader", 0,0)

thread = threading.Thread(target=TkinterWindow, name="TkinterWindow")
thread.start()
sleep(5)
def getName():
    name = prompt(text='Enter User\'s name', title='Name')
    while True:
        if name == None or name == '':
            name = prompt(text='Enter User\'s name', title='Name')
        elif os.path.isdir('./cv2Capture/' + name):
            name = prompt(text='Name Already Exists. Enter User\'s name', title='Name')
        else:
            break
    return name
    
#alert(text='Position User in camera', title='Prepare')
name = getName()
while True:
    Msg = "Welcome "+name+"! Please position your face in the frame."
    #os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (0,0)
    #cv2.moveWindow("FaceKeyPointReaderClient", 1280,0)
    #cv2.moveWindow("FaceKeyPointReader", 0,0)
    ret, frame = Capture
    if not ret:
        print("failed to grab frame")
        break
    cv2.imshow("FaceKeyPointReader", frame)
    #cv2.imshow("FaceKeyPointReaderClient", frame)

    k = cv2.waitKey(1)
    if k%256 == 27:
        # ESC pressed
        #print("Escape hit, closing...")
        if confirm(title='Confirm exit',text='Are you sure you want to exit the software?') == 'Cancel':
            continue
        break
    elif k%256 == 32:
        # SPACE pressed
        ts = time.gmtime()
        #print(time.strftime("%Y-%m-%d-%H-%M-%S", ts))
        timestamp = name
        img_name = "cv2Capture/{}/Camera.png".format(timestamp)
        m_dir = './cv2Capture/{}'.format(timestamp)
        os.mkdir(m_dir)
        cv2.imwrite(img_name, frame)
        print("{} written!".format(img_name))
        #cv2.moveWindow("FaceKeyPointReaderClient", 1280,0)
        #cv2.moveWindow("FaceKeyPointReader", 0,0)
        try:
            keypoints, images = net.apps.detect_facial_keypoints(img_name, plot_enabled=True, saveFig="cv2Capture/{}/Graph.png".format(timestamp))
        except Exception as e:
            alert(text='No face detected! Please Retake.',title='Warning')
            print(e)
            shutil.rmtree(m_dir)
            continue
        if confirm(text='Scan Successful. Would you like to Save or Retake?', title='Scan Successful', buttons=['Retake','Save']) == 'Retake':
            shutil.rmtree(m_dir)
            continue
        #cv2.moveWindow("FaceKeyPointReaderClient", 1280,0)
        #cv2.moveWindow("FaceKeyPointReader", 0,0)
        Msg = "Thank you for Participating in this research. Have a Nice Day!"
        Graph = m_dir+"/Graph.png"
        #cv2.imshow("FaceKeyPointReaderClient",cv2.imread(m_dir+"/Graph.png"))
        #alert(text='Position User in camera', title='Prepare')
        name = getName()
        Graph = None
        

cam.release()

cv2.destroyAllWindows()
