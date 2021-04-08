from azureml.core import Workspace
from azureml.core.webservice import AciWebservice
from azureml.core.webservice import Webservice
from azureml.core.model import InferenceConfig
from azureml.core.environment import Environment
from azureml.core import Workspace
from azureml.core.model import Model
from azureml.core.conda_dependencies import CondaDependencies

def main():
    print('Cargando configuracion workspace...')
    ws = Workspace.from_config()

    #print('Registrando modelo...')
    #model = Model.register(workspace = ws,
    #          model_path ="weights/yolov3.tf.data-00000-of-00001",
    #          model_name = "yolov3-tf",
    #          tags = {"version": "1"},
    #          description = "Model yolov3 with tensorflow")

    print('Obteniendo modelo...')
    model = Model(ws, 'yolov3-tf')

    print("Configurando Objects...")
    aciconfig = AciWebservice.deploy_configuration(
        cpu_cores=2,
        memory_gb=2,
        tags={"data":"solo yolov3 tensorflow"},
        description='yolov3 y tensorflow'
    )

    inference_config = InferenceConfig(
        entry_script="score.py",
        source_directory="./lib",
        conda_file='conda-cpu.yml',
        runtime='python'
    )
    
    print("Desplegando...")
    service = Model.deploy(
        workspace=ws,
        name='yolov3-tf-deploy',
        models=[model],
        inference_config=inference_config,
        deployment_config=aciconfig, 
        overwrite = True
    )
    
    service.wait_for_deployment(show_output=True)
    url = service.scoring_uri
    print(url)

if __name__ == '__main__':
    main()