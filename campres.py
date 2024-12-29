import cv2
from utils import *
import os
import cv2
from cvzone.HandTrackingModule import HandDetector 
import mediapipe as mp

# Presentation and camera dimensions
pres_dims = (1080, 1080)
cam_dims = (300, 300)

# Convert PowerPoint slides to images
ppt_path="HandGesturespptassistant.pptx"
slides_list = Convert_ppt2Img(ppt_path, pres_dims)

# Variables 
slide_num = 0
change_slide = False
drawings_log=[]
show_landmarks=True

pointer_color=(0,0,255)
annotation_color=(0,0,255)
mpad_color=(128,128,128)
allow_gestures=False

# Dictionary to map finger gestures to actions
gestures_dict = {"pointer": [0, 1, 0, 0, 0], "draw": [0, 1, 1, 0, 0], "erase": [0, 0, 0, 0, 0], 
                 "next": [0, 0, 0, 0, 1], "prev": [1, 0, 0, 0, 0]}

# Initialize the hand  and face detectors
detector = HandDetector(detectionCon=0.7, maxHands=2)
face_detector=mp.solutions.face_detection

# Open camera
cap = cv2.VideoCapture(0)
assert cap.isOpened(), "Can't access Camera device"

while True:
    ret, cam = cap.read()
    if not ret or cv2.waitKey(10) == ord("q"):
        cv2.destroyAllWindows()
        cap.release()
        break
    
    slide = slides_list[slide_num]
    
    # Resize and flip camera image
    cam = cv2.resize(cam, cam_dims)
    cam = cv2.flip(cam, 1)
    
    # hands and face detection
    hands, cam = detector.findHands(cam, flipType=True,draw=show_landmarks)
    
    
    # Create a copy of the original slide for displaying
    display = slide.copy()
    
    if hands:
        
        face_bbox = detect_face(face_detector, cam, Isbgr=True)#Detecting face in cam's frame
        if face_bbox:
            top_left, ___ , bottom_left,___ = face_bbox

            upper=top_left[1]
            lower=bottom_left[1]
            face_centerY=int((upper+lower)//2)# get the face's centerline
           
            if show_landmarks:#displaying  face's centerline ( testing and debugging  only)
                cv2.line(cam,(0,face_centerY),(cam_dims[0],face_centerY),(0,255,0),1)


        
        
        
        
        #Two hands Gestures:
        
        if len(hands)==2:
            gesture1=detector.fingersUp(hands[0])
            gesture2=detector.fingersUp(hands[1])
            
            if gesture1==[1,1,1,0,0] and gesture2==[1,1,1,0,0]:#Zooming gesture
                
                landmarks1 = hands[0]['lmList']
                pt1=landmarks1[5][:2]# get the coordinates of the base of the index finger in the first hand
                landmarks2=hands[1]['lmList']
                pt2=landmarks2[5][:2]# get the coordinates of the base of the index finger in the second hand
                
                cv2.line(cam,pt1,pt2,(0,255,0),2)
                mid_pt=(int((pt1[0]+pt2[0])/2),int((pt1[1]+pt2[1])/2))
                
                mapped_pt=(int((mid_pt[0])*(pres_dims[0]/cam_dims[0])),int((mid_pt[1])*(pres_dims[1]/cam_dims[1])))
                cv2.circle(display,mapped_pt,5,(0,255,0),2)
                
                
                dist = np.linalg.norm(np.array(pt1) - np.array(pt2))# compute euclidean distance between the two pts
                zoom_factor = min(max(dist/100,1),2)  # compute the scale factor (between x1 and x2)
                
                zoom_width = int(pres_dims[0] / zoom_factor)
                zoom_height = int(pres_dims[1] / zoom_factor)
                
                #coordinates of the upper left corner of the zoomed region
                x1 = max(mapped_pt[0] - zoom_width // 2, 0)
                y1 = max(mapped_pt[1] - zoom_height // 2, 0)
                
                #coordinates of the bottom right corner of the  region
                x2 = min(mapped_pt[0] + zoom_width // 2, pres_dims[0])
                y2 = min(mapped_pt[1] + zoom_height // 2, pres_dims[1])
                
                zoomed_region = display[y1:y2, x1:x2]#extract the zoomed region from the slide
                
                
                zoomed_slide = cv2.resize(zoomed_region, pres_dims)#fit the zoomed region to the slide preview window
                
                
                display = zoomed_slide#overwrite the zoomed region in the slide preview win

                txt=str(zoom_factor)
                
                cv2.putText(cam,"x"+txt,mid_pt, cv2.FONT_HERSHEY_PLAIN, 1, (50, 50, 50), 2)
                

                


            
        
        
        # Single hand Gestures:
        
        # Get the center and landmarks of the hand
        _, cy = hands[0]['center']
        landmarks = hands[0]['lmList']
        
        if cy<face_centerY:#check whether hand is above the center of the face

            allow_gestures=True
        else:
            allow_gestures=False
        
        
        gesture = detector.fingersUp(hands[0])
        for action, val in gestures_dict.items():
            
            if gesture == val:
                
                if action == "next" and not change_slide and slide_num < len(slides_list) - 1 and allow_gestures:
                    slide_num += 1
                    change_slide = True
                    
                
                elif action == "prev" and not change_slide and slide_num > 0 and allow_gestures:
                
                    slide_num -= 1
                    change_slide = True
                
                elif action == "pointer":
                
                    change_slide = False
                    
                    index_tip = landmarks[8][:2]  # Get the index finger tip coordinates
                    
                    p1,p2=display_mouse_pad(cam,"   Mouse Pad",0.6,mpad_color)
                    
                    mouse_pad_width=p2[0]-p1[0]
                    mouse_pad_height=p2[1]-p1[1]
                    
                    


                    # Mapping the index tip coordinates to the slide coordinates
                    
                    if index_tip[0] > p1[0] and index_tip[0] < p2[0] and index_tip[1] > p1[1] and index_tip[1] < p2[1]:#ensures that the tip is within the mouse pad region
                        
                        index_tip_on_slide=map_pointer_to_slide(index_tip,p1,(p2[0]-p1[0]),(p2[1]-p1[1]),pres_dims)


                        cv2.circle(cam,index_tip,4,(255,255,255),2)#highlight index finger on cam

                        cv2.circle(display, index_tip_on_slide, 5, pointer_color, -1)  # display the pointer on the slide
                        
                                
                    #pointer_last_loc=index_tip_on_slide
                
                
                
                
                elif action == "draw":
                    
                    change_slide = False
                    index_tip = landmarks[8][:2]                    
                    p1,p2=display_mouse_pad(cam,"   annotation",0.6,(255,255,255))
                    
                    if index_tip[0] > p1[0] and index_tip[0] < p2[0] and index_tip[1] > p1[1] and index_tip[1] < p2[1]:#ensures that the tip is within the mouse pad region

                        index_tip_on_slide=map_pointer_to_slide(index_tip,p1,(p2[0]-p1[0]),(p2[1]-p1[1]),pres_dims)
                    
                        cv2.circle(cam,index_tip,4,annotation_color,2)#highlight index finger on cam

                        drawings_log.append(index_tip_on_slide)#store the index's tip movement history
                    

                elif action == "erase" and allow_gestures:
                    change_slide = False 
                    drawings_log.clear()

    draw_on_display(display,drawings_log,annotation_color)#annotate points on display
    
    display[0:cam_dims[1], 0:cam_dims[0], :] = cam # combine cam and slide into a single frame

    cv2.imshow("Cam/Pres Preview", display)    # show the combined display (camera + slide)

