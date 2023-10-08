import cv2
import time
import imutils

cam=cv2.VideoCapture(0)

firstframe=None
secondframe=None
area=500
i=0
while True:
        _,img=cam.read()
        text1="NO MOVEMENT DETECTED"
        img=imutils.resize(img,width=500)
        gryimg=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
        gausimg=cv2.GaussianBlur(gryimg,(21,21),0)
        firstframe=gausimg
        time.sleep(0.11)
        _,img=cam.read()
        _,img=cam.read()
        img=imutils.resize(img,width=500)
        gryimg=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
        gausimg=cv2.GaussianBlur(gryimg,(21,21),0)
        secondframe=gausimg
        imgdiff=cv2.absdiff(firstframe,secondframe)
        thres=cv2.threshold(imgdiff,25,255,cv2.THRESH_BINARY)[1]
        thres=cv2.dilate(thres,None,iterations=4)
        # cv2.imshow("Thres",thres)
        cnts=cv2.findContours(thres.copy(),cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
        cnts=imutils.grab_contours(cnts)
        for c in cnts:
                if cv2.contourArea(c)<area:     continue
                (x,y,w,h)=cv2.boundingRect(c)
                cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,0),2)
                i+=1
                text1=f"MOVEMENT DETECTED FOR {i} TIMES" if i>1 else f"MOVEMENT DETECTED FOR {i} TIME"
        # print(text+str(i))
        text2 = "Press q to exit..."
        text3=f"TOTALS MOVEMENTS DETECTED ={i}"
        cv2.putText(img,text1,(10,20),cv2.FONT_HERSHEY_SIMPLEX,0.5,(255,255,0),2)
        cv2.putText(img,text3,(10,40),cv2.FONT_HERSHEY_SIMPLEX,0.5,(255,255,0),2)
        cv2.putText(img,text2,(10,60),cv2.FONT_HERSHEY_SIMPLEX,0.5,(255,255,0),2)

        cv2.imshow("Camfeed",img)
        key=cv2.waitKey(1) & 0xFF
        if key==ord("q") or key==ord("Q"):
                break

cam.release()
cv2.destroyAllWindows()