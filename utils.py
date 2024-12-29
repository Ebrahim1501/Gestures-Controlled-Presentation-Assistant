import cv2
#used for power point ppts handling
from spire.presentation.common import * 
from spire.presentation import *
import os

import numpy as np
import mediapipe as mp



def Convert_ppt2Img(ppt_path,dims=None):#"D:\\PyProjects\\HandGesturespptassistant.pptx"
    
    slides_list=[]
    
    
    
    presentation = Presentation()

    # Load a PowerPoint presentation
    presentation.LoadFromFile(ppt_path)


    #output_dir = "Output"
    #if not os.path.exists(output_dir):
    #   os.makedirs(output_dir)





    # Loop through the slides in the presentation
    for i, slide in enumerate(presentation.Slides):
        
        
        # Save each slide as a PNG image
        image = slide.SaveAsImage()
        
        #print(type(image))--------------------> returns object of type:<class 'spire.presentation.common.Stream.Stream'>
        image_bytes = image.ToArray()  # Get bytes from stream object 
            
            
        
        image_np = np.frombuffer(image_bytes, dtype=np.uint8)# Convert byte array to numpy array
            
        image_np = cv2.imdecode(image_np, cv2.IMREAD_COLOR)# Decode  using OpenCV
        
        if dims:
            image_np=cv2.resize(image_np,dims)#if dimensions are provided....
            

        
        #print(image_np.shape)
        #if i==0:
            #print (dir(image))

        #image.Save(fileName)
        slides_list.append(image_np)
        image.Dispose()

    # Dispose the presentation object
    presentation.Dispose()
    return slides_list



def map_cam_to_slide(point,cam_dims,pres_dims):
    
    mapped_pt=(         int(point[0] * (pres_dims[0] / cam_dims[0])),int(point[1] * (pres_dims[1] / cam_dims[1]))    )      
    return mapped_pt
                        






def map_pointer_to_slide(point,mpad_upperleft,mpad_width,mpad_height,pres_dims):
    
                        mapped_pt = (
                        int((point[0]-mpad_upperleft[0] ) * (pres_dims[0] / mpad_width)),
                        int((point[1]) * (pres_dims[1] / mpad_height))  
                                         )
                        return mapped_pt
                        
                        
                    
def display_mouse_pad(cam,header_text,transparency_factor=0.8,mpad_color=(128, 128, 128)):
    overlay = cam.copy()
                    
    #coordinates of the upper left corner of the rectangle
    x = int(cam.shape[0] * 1 / 2)  
    y = 0  
    width = cam.shape[0] // 2
    height= cam.shape[1] // 2            

    cv2.rectangle(cam, (x, y), (cam.shape[0],cam.shape[1] // 2),mpad_color, -1)  # Draw the rectangle
                    
   

    cv2.addWeighted(overlay, transparency_factor, cam, 1 - transparency_factor, 0, cam)  # make the rectangle transparent
    
    cv2.putText(cam,header_text, (x, y+12  ), cv2.FONT_HERSHEY_PLAIN, 1, (50, 50, 50), 2)
    
    return((x,y),(x+width,y+height))

                    


def draw_on_display(display,drawings_log,color):
    
    for drawing in drawings_log:
        cv2.circle(display, drawing, 5,color, -1)











def detect_face(mp_model,img,Isbgr=False):
    
     height, width, _ = img.shape

     if Isbgr==True:
         img=cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
        
     #mp_face_detection = mp.solutions.face_detection
     face_detection = mp_model.FaceDetection(min_detection_confidence=0.7)

     
     results=face_detection.process(img)
     if results.detections:
        bbox = results.detections[0].location_data.relative_bounding_box

        
        x_org=int(bbox.xmin*width)
        y_org=int(bbox.ymin*height)
        bbox_width=int(bbox.width*width)
        bbox_height=int(bbox.height*height)
        
        top_left=(x_org,y_org)
        top_right=(x_org+bbox_width,y_org)
        bottom_left=(x_org,y_org+bbox_height)
        bottom_right=(x_org+bbox_width,y_org+bbox_height)
        
        return[top_left,top_right,bottom_left,bottom_right]
     else :
         return None    
         

     
         
'''

mp_face_detection = mp.solutions.face_detection

# Initialize webcam
cap = cv2.VideoCapture(0)
assert cap.isOpened(), "Can't access Camera device"

# Loop to capture video frames and detect faces
while True:
    ret, frame = cap.read()
    if not ret or cv2.waitKey(10) == ord('q'):
        break
    frame=cv2.flip(frame,1)

    # Call the detect_face function
    face_bbox = detect_face(mp_face_detection, frame, Isbgr=True)

    if face_bbox:
        # Draw the bounding box on the frame
        top_left, top_right, bottom_left, bottom_right = face_bbox
        
        # Draw rectangle based on the top-left and bottom-right coordinates
        cv2.rectangle(frame, top_left, bottom_right, (0, 255, 0), 2)
        
        # Optionally, draw the corners of the box
#        cv2.circle(frame, top_left, 5, (0, 255, 0), -1)
 #       cv2.circle(frame, top_right, 5, (0, 255, 0), -1)
  #      cv2.circle(frame, bottom_left, 5, (0, 255, 0), -1)
   #     cv2.circle(frame, bottom_right, 5, (0, 255, 0), -1)

    # Display the frame with the face bounding box
    upper=top_left[1]
    lower=bottom_left[1]
    center=(upper+lower)//2
    x=frame.shape[1]
    cv2.line(frame,(0,center),(x,center),(0,255,0))
    
    
    cv2.imshow("Face Detection", frame)

# Release the webcam and close all OpenCV windows
cap.release()
cv2.destroyAllWindows()



'''


