import  cv2
from sympy.utilities.iterables import connected_components
from util import get_parking_spots_bboxes, empty_or_not

mask = r'C:\Users\Rakesh\OneDrive\Desktop\Codes\Python\Yolov8 models\02__Car Parking Detection\Media\mask_1920_1080.png'
video_path = r'C:\Users\Rakesh\OneDrive\Desktop\Codes\Python\Yolov8 models\02__Car Parking Detection\Media\parking_1920_1080_loop.mp4'


mask = cv2.imread(mask, 0)
cap = cv2.VideoCapture(video_path)

connected_components = cv2.connectedComponentsWithStats(mask, 4, cv2.CV_32S)

spots = get_parking_spots_bboxes(connected_components)

spots_status = [None for j in spots]

# print(spots[0])

frame_nmr = 0
ret = True
step = 30
while ret:
    ret, frame = cap.read()

    if frame_nmr % step ==0:
         for spot_index, spot in enumerate(spots):
             x1, y1, w, h = spot

             spot_crop = frame[y1:y1 + h, x1:x1 + w, :]

             spot_status = empty_or_not(spot_crop)
             spots_status[spot_index] = spot_status

    for spot_index, spot in enumerate(spots):
        spot_status = spots_status[spot_index]
        x1, y1, w, h = spots[spot_index]
        if spot_status:
            frame = cv2.rectangle(frame, (x1, y1), (x1 + w, y1 + h), (0, 255, 0), 2)
        else:
            frame = cv2.rectangle(frame, (x1, y1), (x1 + w, y1 + h), (0, 0, 255), 2)
    cv2.imshow('frame', frame)
    if cv2.waitKey(25) & 0xFF == ord('q'):
        break

    frame_nmr += 1


cap.release()
cv2.destroyAllWindows()