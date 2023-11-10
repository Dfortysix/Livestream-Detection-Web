import cv2 as cv



def detectRealTime():
    weightsPath = "frozen_inference_graph.pb"
    configPath = "ssd_mobilenet_v3_large_coco_2020_01_14.pbtxt"
    thres = 0.6 # Threshold to detect object


    cap = cv.VideoCapture(0)
    classNames= ['person', 'bicycle', 'car', 'motorcycle', 'airplane', 'bus', 'train', 'truck', 'boat', 'traffic light', 'fire hydrant', 'street sign', 'stop sign', 'parking meter', 'bench', 'bird', 'cat', 'dog', 'horse', 'sheep', 'cow', 'elephant', 'bear', 'zebra', 'giraffe', 'hat', 'backpack', 'umbrella', 'shoe', 'eye glasses', 'handbag', 'tie', 'suitcase', 'frisbee', 'skis', 'snowboard', 'sports ball', 'kite', 'baseball bat', 'baseball glove', 'skateboard', 'surfboard', 'tennis racket', 'bottle', 'plate', 'wine glass', 'cup', 'fork', 'knife', 'spoon', 'bowl', 'banana', 'apple', 'sandwich', 'orange', 'broccoli', 'carrot', 'hot dog', 'pizza', 'donut', 'cake', 'chair', 'couch', 'potted plant', 'bed', 'mirror', 'dining table', 'window', 'desk', 'toilet', 'door', 'tv', 'laptop', 'mouse', 'remote', 'keyboard', 'cell phone', 'microwave', 'oven', 'toaster', 'sink', 'refrigerator', 'blender', 'book', 'clock', 'vase', 'scissors', 'teddy bear', 'hair drier', 'toothbrush', 'hair brush']

    net = cv.dnn_DetectionModel(weightsPath,configPath)
    net.setInputSize(320,320)
    net.setInputScale(1.0/ 127.5)
    net.setInputMean((127.5, 127.5, 127.5))
    net.setInputSwapRB(True)

    while True:
        success,img = cap.read()
        img = cv.flip(img,1)
        img = cv.resize(img,(720,500),cv.INTER_AREA)
        classIds, confs, bbox = net.detect(img,confThreshold=thres)


        if len(classIds) != 0:
            for classId, confidence,box in zip(classIds.flatten(),confs.flatten(),bbox):
                cv.rectangle(img,box,color=(0,255,0),thickness=2)
                cv.putText(img,classNames[classId-1].upper(),(box[0]+10,box[1]+30),
                cv.FONT_HERSHEY_COMPLEX,1,(0,255,0),2)
                cv.putText(img,str(round(confidence*100,2)),(box[0]+200,box[1]+30),
                cv.FONT_HERSHEY_COMPLEX,1,(255,255,255),2)

        ret, buffer = cv.imencode('.jpg', img)  # Chuyển đổi khung hình thành định dạng JPEG

        img = buffer.tobytes()

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + img + b'\r\n')  # Trả về
        if cv.waitKey(20) & 0xFF == ord("x"):
            break

    cap.release()
    cv.destroyAllWindows()
