import joblib
from azureml.core.model import Model

from azureml.contrib.services.aml_request import AMLRequest, rawhttp
from azureml.contrib.services.aml_response import AMLResponse
from PIL import Image
import json
from yolov3_tf2.models import YoloV3

def init():
    global model
    model_path = Model.get_model_path("yolov3-tf")
    print("Model Path is  ", model_path)
    #model = joblib.load(model_path)

    num_classes = 80
    yolo = YoloV3(classes=num_classes)
    yolo.load_weights(model_path).expect_partial()
    print('weights loaded')
    
@rawhttp
def run(request):
    print("This is run()")
    
    if request.method == 'GET':
        # For this example, just return the URL for GETs.
        respBody = str.encode(request.full_path)
        return AMLResponse(respBody, 200)
    elif request.method == 'POST':
        file_bytes = request.files["image"]
        image = Image.open(file_bytes).convert('RGB')
        # For a real-world solution, you would load the data from reqBody
        # and send it to the model. Then return the response.

        # For demonstration purposes, this example just returns the size of the image as the response..
        return AMLResponse(json.dumps(image.size), 200)
    else:
        return AMLResponse("bad request", 500)