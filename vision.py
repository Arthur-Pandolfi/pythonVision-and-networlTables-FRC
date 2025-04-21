AI_FRAMEWORK = "tf"
AI_MODEL = "yolov8n_float16.tflite"

from networktables import NetworkTables
import time
import cv2

if AI_FRAMEWORK == "torch":
    from ultralytics import YOLO
    import torch
    device = torch.device("cuda:0" if torch.cuda.is_available else "cpu")
    print("Yolo Device:", device)
    model = YOLO(AI_MODEL)
    model.to(device=device)

elif AI_FRAMEWORK == "tf":
    from tensorflow.lite.python.interpreter import Interpreter
    import numpy as np

roboRIOIP = "localhost"

# Network Tables Inicialização
NetworkTables.initialize(roboRIOIP)
NetworkTables.waitForConnectionListenerQueue(1)
table = NetworkTables.getTable("/RaspberryPI")
fpsEntry = table.getEntry("FPS")
statusEntry = table.getEntry("Status")
AIFrameworkEntry = table.getEntry("Framework de IA")

AIFrameworkEntry.setString(AI_FRAMEWORK)
statusEntry.setString("INICIALIZANDO...")

# Abre câmera
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 320)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 320)
statusEntry.setString("Capturando")

if AI_FRAMEWORK == "tf":
    # Carrega modelo
    interpreter = Interpreter(model_path=AI_MODEL)
    interpreter.allocate_tensors()

    input_details = interpreter.get_input_details()
    output_details = interpreter.get_output_details()
    

    while True:
        start = time.time()
        ret, frame = cap.read()
        if not ret:
            break

        input_data = cv2.resize(frame, (input_details[0]['shape'][2], input_details[0]['shape'][1]))
        input_data = np.expand_dims(input_data, axis=0).astype(np.float32)

        interpreter.set_tensor(input_details[0]['index'], input_data)
        interpreter.invoke()

        end = time.time()
        fps = 1 / (end - start)
        fps = f"{fps:.2f}"
        print(f"FPS: {fps}")
        fpsEntry.setString(fps)
        cv2.putText(frame, fps, (105, 65), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 3)
        cv2.imshow("camera", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

elif AI_FRAMEWORK == "torch":
    while True:
        start = time.time()
        ret, frame = cap.read()
        if not ret:
            break
        
        model.predict(source=frame)
        end = time.time()
        fps = 1 / (end - start)
        fps = f"{fps:.2f}"
        print(f"FPS: {fps}")
        fpsEntry.setString(fps)
        cv2.putText(frame, fps, (105, 65), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 3)
        cv2.imshow("camera", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

statusEntry.setString("CÓDIGO ENCERRADO")
NetworkTables.shutdown()
cap.release()
cv2.destroyAllWindows()
