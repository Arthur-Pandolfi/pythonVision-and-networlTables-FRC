print("importando... demora mesmo")
from ultralytics import YOLO
import os
print("cabou de importar")

os.mkdir("./models/")
os.chdir("./models")

def export_to_tensorflow_base_model(wantedModel: str, path_to_save: str):
    print("Exportando YOLO para TensorFlow SavedModel...")
    model = YOLO(wantedModel)    
    model.export(format="saved_model") 
    if not os.path.exists(path_to_save):
        raise FileNotFoundError(f"Exportação para SavedModel falhou: {path_to_save} não encontrado.")
    print(f"SavedModel salvo em: {path_to_save}\n")

if __name__ == "__main__":
    try:
        export_to_tensorflow_base_model("yolov8n.pt", ".yolov8n_saved_model")
        os.rename("./yolov8n_saved_model/yolov8n_float16.tflite", "../yolov8n_float16.tflite")
        print("Modelo exportando com sucesso!")
    except Exception as e:
        print(f"\033[0mAlgum erro:\033[0m {e}")

        