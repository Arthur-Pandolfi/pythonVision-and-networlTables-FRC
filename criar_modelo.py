AI_MODEL = "yolov8n.pt"
AI_MODEL_WITHOUT_ARCHIVE_EXTENSION = "yolov8n"

print("importando... demora mesmo")
from ultralytics import YOLO
import os
print("cabou de importar")

os.mkdir("./models")
os.chdir("./models")

def export_to_tensorflow_base_model(wantedModel: str, path_to_save: str):
    print("Exportando YOLO para TensorFlow SavedModel...")
    model = YOLO(wantedModel)    
    model.export(format="saved_model") 
    print(f"SavedModel salvo em: {path_to_save}\n")

if __name__ == "__main__":
    try:
        export_to_tensorflow_base_model(AI_MODEL, f"./{AI_MODEL}_saved_model")
        os.rename(f"./{AI_MODEL_WITHOUT_ARCHIVE_EXTENSION}_saved_model/{AI_MODEL_WITHOUT_ARCHIVE_EXTENSION}_float16.tflite", f"../{AI_MODEL}_float16.tflite")
        os.rename(f"./{AI_MODEL}", f"../{AI_MODEL}")
        print("Modelo exportando com sucesso!")
    except Exception as e:
        print(f"\033[0mAlgum erro:\033[0m {e}")
