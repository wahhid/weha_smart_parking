import cv2

cap = cv2.VideoCapture(0)

while(True):
    ret, frame = cap.read()
    #gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    #cv2.imshow('frame',frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

#do some ops

cap.release()
cv2.imshow("output", output)
cv2.waitKey(0)
cv2.destroyAllWindows()