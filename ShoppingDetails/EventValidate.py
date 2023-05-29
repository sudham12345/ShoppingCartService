import json

def validate_parameters(parameters):

    if not parameters.get("uuId"):
        return  {
            "statusCode": 500,
            "body": json.dumps({
                "status" : "FAIL",
                "message": "Missing uuId: Required uuId (string in body)"
            },default=str
            )
        }
       
    elif not parameters.get("productId"):
        return  {
            "statusCode": 500,
            "body": json.dumps({
                "status" : "FAIL",
                "message": "Missing uuId: Required productId (int in body)"
            },default=str
            )
        }
    
    elif not parameters.get("productQty"):
        return  {
            "statusCode": 500,
            "body": json.dumps({
                "status" : "FAIL",
                "message": "Missing uuId: Required productQty (int in body)"
            },default=str
            )
        }
         
    elif not isinstance(parameters['productId'],int):
        return {
            "statusCode": 200,
            "body": json.dumps(
            {"status" : "FAIL",
             "message": "Expecting a numeric input, Invalid productId received : " + str(parameters['productId'])
            },default=str)
        }
      
    elif  not isinstance(parameters['productQty'],int):
        return {
            "statusCode": 200,
            "body": json.dumps(
            {"status" : "FAIL",
             "message": "Expecting a numeric input, Invalid productQty received : " + str(parameters['productQty'])
            },default=str)
        }
    
    else:
        return True

