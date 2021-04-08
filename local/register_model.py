from azureml.core import Workspace
from azureml.core.model import Model

def main():
    print('Cargando configuracion workspace...')
    ws = Workspace.from_config()

    print('Registrando modelo...')
    model = Model.register(
        workspace = ws,
        model_path ="weights/yolov3.tf.data-00000-of-00001",
        model_name = "yolov3-tf",
        tags = {"version": "1"},
        description = "Model yolov3 with tensorflow"
    )

if __name__ == '__main__':
    main()