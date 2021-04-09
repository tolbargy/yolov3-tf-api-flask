from azureml.core import Workspace
from azureml.core.webservice import AciWebservice
from azureml.core.model import InferenceConfig
from azureml.core.model import Model

def main():
    print('Cargando configuracion workspace...')
    ws = Workspace.from_config()

    print('Obteniendo modelo...')
    model = Model(ws, 'yolov3-tf')

    print("Configurando Objects...")
    aciconfig = AciWebservice.deploy_configuration(
        cpu_cores=2,
        memory_gb=2,
        tags={"data":"solo yolov3 tensorflow"},
        description='yolov3 y tensorflow',
        dns_name_label='ceibatest'
    )

    inference_config = InferenceConfig(
        entry_script="score.py",
        source_directory="../azure",
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