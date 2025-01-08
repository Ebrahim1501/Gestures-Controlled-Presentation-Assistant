
# Hand Gesture-Controlled PowerPoint Presentation
This project allows you to control a PowerPoint presentation using hand gestures, leveraging computer vision and MediaPipe's Hand Tracking Module. The goal is to provide a seamless and intuitive way to interact with power point presentations using simple single-and two-hand gestures for actions like navigating between slides, drawing annotations, zooming in/out, and controlling pointer movements.

## Features supported:
- **Face Detection**: Detect and track the face’s position for gesture restrictions, based on the face's orientation, ensuring gestures are only recognized when the user is facing the camera.
- **Next/Previous Slide Control**: Navigate between slides using  a single hand gestures.
- **Pointer Mode**: Enable mouse pointer movement.
- **Drawing Mode**: Draw annotations directly onto the presentation slides.
- **Erase Annotations**: Clear back all annotations from the presentation.
- **Zoom Control**: Zoom in and out of slides using both hands.

## Key Note!!

- **Face-Centered Gesture Restriction**:
  Gestures such as navigation and annotation drawing are **only** recognized when the user's hands are above the **centerline of the face** (extracted through face tracking module). <u> This feature is important to prevents unintentional activations for gestures while normally presenting with hands</u>.
![FaceCenterLineThreshold ](https://github.com/user-attachments/assets/6cb2f861-67b4-41fd-9ed0-1b15fb42a417)

##  Default Gestures:

- **Next Slide**: Raise only The Pinky finger up to navigate to the next slide.
- **Previous Slide**: Thumb finger up while the rest of the fingers are down.


![Navigate](https://github.com/user-attachments/assets/94117782-96e6-4d1a-a9e3-8ccc0ab654ab)






- **Move Cursor**: Raise the index finger up while keeping all other fingers down.

![mouse-cursor](https://github.com/user-attachments/assets/d1f993fd-52c1-42fb-a791-aac44430a21a)



- **Zooming In/Out**: Raise the thumb, index, and middle finger of both hands and move both hands closer or farther apart to zoom in or out accordingly.

![zooming-in-out](https://github.com/user-attachments/assets/17e5372b-7b5c-4196-a19e-c590bfda7b36)



- **Annotation**: Raise both the middle and index fingers while keeping the rest of the fingers down.
- **Erase**: Open and close all five fingers to erase all annotations.

![draw-erase](https://github.com/user-attachments/assets/e37987fd-4b10-4c9c-a501-2f7cd9713d51)





