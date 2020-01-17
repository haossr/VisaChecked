import json
from joblib import load

# import requests

MODEL_PATH = "resource/m.joblib"

def lambda_handler(event, context):
    """Sample pure Lambda function

    Parameters
    ----------
    event: dict, required
        API Gateway Lambda Proxy Input Format

        Event doc: https://docs.aws.amazon.com/apigateway/latest/developerguide/set-up-lambda-proxy-integrations.html#api-gateway-simple-proxy-for-lambda-input-format

    context: object, required
        Lambda Context runtime methods and attributes

        Context doc: https://docs.aws.amazon.com/lambda/latest/dg/python-context-object.html

    Returns
    ------
    API Gateway Lambda Proxy Output Format: dict

        Return doc: https://docs.aws.amazon.com/apigateway/latest/developerguide/set-up-lambda-proxy-integrations.html
    """
    data = event['queryStringParameters']
    print(event)
    probs = predict(data['visa_type'],
                           data['degree'],
                           data['expertise'],
                           data['nationality'],
                           data['start_week_day'])
    return {
        'statusCode': 200,
        'body': json.dumps({
                'message': "success",
                'probs': probs})
        }
        
def predict(visa_type, degree, expertise, nationality, start_week_day):
    # load the model
    m = load(MODEL_PATH)
    
    # preprocessing
    if expertise != 'Electrical Engineering' and expertise != 'Computer and Information Science':
        expertise = "other"
    if nationality != "chinese" and nationality != "PreferNotToANswer":
        nationality = "other"
    key = "_".join([visa_type, degree, expertise, nationality, start_week_day]) 
    
    _classes = ['1-5', '6-20', '21-30', '31-40', '41-50', '51-60', '60+']
    _probs = [0.032015065913371, 0.1111111111111111, 0.1318267419962335, 0.19962335216572505, 0.3229755178907721, 0.12900188323917136, 0.07344632768361582] 
    if key in m:
        _probs = m[key]

    return list(zip(_classes, _probs))    
