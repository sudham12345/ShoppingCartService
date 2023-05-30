#import requests
import psycopg2
import json
import os
import EventValidate
#import cognitojwt
from decimal import Decimal
from datetime import date

"""
def add_product(event,context):

    parameters = event['queryStringParameters']
    productId=parameters['productId']
    print('post man input', parameters['productId'])
    print("http://127.0.0.1:3000/product"+ f"?productId={productId}")
    response = requests.get("http://127.0.0.1:3000/product" + f"?productId={productId}")
    #print(response.json())
    return {
        "statusCode":200,
     #   "body": json.dumps("http://127.0.0.1:3000/Product?productId="+str(parameters['productId']),default=str)
        "body": json.dumps(response,default=str)
       }


#get_product_from_external_service(1001)

"""

def add_product(event,context):
    
    try:
        parameters = json.loads(event['body'])
    except Exception as e:
        return  {
            "statusCode": 500,
            "body": json.dumps({
                "message": f"Required params : uuId (string), productId (int), productQty (int) {e}"
            })
        }
        
    response = EventValidate.validate_parameters(parameters) 

    if response==True:
        if parameters['productQty']<=0:
            return {
                "statusCode": 500,                  
                "body": json.dumps(
                {"status" : "FAIL",
                "message": "Cannot add a product with quantity "+str(parameters['productQty'])
                },default=str)
            }
    else:
        return response      


    """
        response = requests.get("http://127.0.0.1:3000/Product?productId="+parameters['productId'])
        prodDetails = response.json()

        prodName = prodDetails['productName']       
        prodPrice = prodQty * proddetails['productPrice']
    """
    
    try:
        conn = psycopg2.connect(
                host=os.environ['POSTGRES_HOST'],
                port=os.environ['POSTGRES_PORT'],
                dbname=os.environ['POSTGRES_DB'],
                user=os.environ['POSTGRES_USER'],
                password=os.environ['POSTGRES_PASSWORD']
            )
           
        """
        userName = None

        jwtToken = event["headers"].get("Authorization")

        if jwtToken:        
            try:
                verifiedUser = cognitojwt.decode(
                jwt_token, os.environ['AWS_REGION'], os.environ['USERPOOL_ID'])
                
            except (cognitojwt.CognitoJWTException, ValueError):
                verifiedUser = {}

            userName = verifiedUser.get("sub")
        """

        cursor = conn.cursor()

        query = "select prod_name, prod_price from shoppingcart.products where prod_id =%s"
        cursor.execute(query,(parameters['productId'],))
    
        prodDetails = cursor.fetchall()
      
        if prodDetails == []:
            cursor.close()
            conn.close()
            return {
                "statusCode": 200,
                "body": json.dumps(
                    {"status" : "FAIL",
                     "message": "No product found with product Id : "+str(parameters['productId'])
                    },default=str)
                }
        else:
            """  
            if userName:
                query = "select user_id from shoppingcart.user where TRIM(user_name)=TRIM(%s)"
                cursor.execute(query,(userName,))
                userId = cursor.fetchall()       
                userId = userId[0][0]
            
            """
            cookieuuId = parameters['uuId']                
            prodId = parameters['productId']
            prodName = prodDetails[0][0]
            prodQty = parameters['productQty']
            prodPrice = prodQty * prodDetails[0][1]
            prodcreateDate = date.today()
            produpdateDate = date.today()

            query = "SELECT MAX(cart_id)+1 from shoppingcart.cart"
            cursor.execute(query)
            cartId = cursor.fetchall()          

            if cartId[0][0] is None:
                cartId =1
            else:
                cartId = cartId[0][0]

            """
            if user_sub:
                query = "INSERT INTO shoppingcart.user_cart values(%s,%s,%s,%s,%s,%s,%s,%s)"
                cursor.execute(query,(cartId,
                                  userId,
                                  prodId,
                                  prodName,
                                  prodQty,
                                  prodPrice,
                                  prodcreateDate,
                                  produpdateDate))
            else:
            """
            query = "INSERT INTO shoppingcart.cart values(%s,%s,%s,%s,%s,%s,%s,%s)"
            cursor.execute(query,(cartId,
                                  cookieuuId,
                                  prodId,
                                  prodName,
                                  prodQty,
                                  prodPrice,
                                  prodcreateDate,
                                  produpdateDate))
            conn.commit()     

            return {
                "statusCode": 200,
                "body": json.dumps(
                   { "status" : "SUCCESS",
                     "message": "product successfully added to cart with cart ID:"+str(cartId),
                     "cartId"         : cartId,
                     "cookieUudi"     : cookieuuId,
                     "productId"      : prodId, 
                     "prodName"       : prodName,
                     "prodQty"        : prodQty,
                     "prodPrice"      : Decimal(prodPrice),
                     "prodcreateDate" : prodcreateDate,
                     "produpdateDate" : produpdateDate
                    },default=str)
                }
    
    except Exception as e:
        conn.rollback()
        return  {
            "statusCode": 500,
            "body": json.dumps({
                "status" : "FAIL",
                "message": f"Failed to add product: {e}"
            })
        }
    
    finally:
        cursor.close()
        conn.close()


    

