import joblib
from azureml.core.model import Model

def init():
    print("Helloooooo")

def run(data):
    try:
        print(data)
        return {'data' : data , 'message' : "Successfully classified Iris"}
    except Exception as e:
        error = str(e)
        return {'data' : error , 'message' : 'Failed to classify iris'}