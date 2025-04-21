mode = "torch"

from networktables import NetworkTables
import time
import cv2

if mode == "torch":
    from ultralytics import YOLO

elif mode == "tf":
    from tensorflow.lite.python.interpreter import Interpreter
    import numpy as np

roboRIOIP = "localhost"

# Network Tables Inicialização
NetworkTables.initialize(roboRIOIP)
NetworkTables.waitForConnectionListenerQueue(1)
table = NetworkTables.getTable("/RaspberryPI")
fpsEntry = table.getEntry("FPS")
statusEntry = table.getEntry("Status")
modeEntry = table.getEntry("Modo")

modeEntry.setString(mode)
statusEntry.setString("INICIALIZANDO...")

# Abre câmera
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 320)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 320)
statusEntry.setString("Capturando")

if mode == "tf":
    # Carrega modelo
    interpreter = Interpreter(model_path="yolov8n_float16.tflite")
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

        # Aqui você trataria os outputs conforme o seu modelo
        # Exemplo: detections = interpreter.get_tensor(output_details[0]['index'])

        end = time.time()
        fps = 1 / (end - start)
        fps = f"{fps:.2f}"
        print(f"FPS: {fps}")
        fpsEntry.setString(fps)
        cv2.putText(frame, fps, (105, 65), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 3)
        cv2.imshow("camera", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

elif mode == "torch":
    model = YOLO("yolov8n.pt")

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
