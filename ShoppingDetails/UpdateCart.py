import requests
import psycopg2
import json
import os
import EventValidate
from decimal import Decimal
from datetime import date

"""
def get_product(event,context):

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

def update_product(event,context):

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
        if parameters['productQty']==0:
            return {
                "statusCode": 200,                  
                "body": json.dumps(
                {"status" : "FAIL",
                "message": "Cannot add or update a product with quantity "+str(parameters['productQty'])
                },default=str)
            } 
    else:
        return response      
    
    try:
        conn = psycopg2.connect(
            host=os.environ['POSTGRES_HOST'],
            port=os.environ['POSTGRES_PORT'],
            dbname=os.environ['POSTGRES_DB'],
            user=os.environ['POSTGRES_USER'],
            password=os.environ['POSTGRES_PASSWORD']
        )
    
        """
        response = requests.get("http://127.0.0.1:3000/Product?productId="+parameters['productId'])
        prodDetails = response.json()

        prodName = prodDetails['productName']       
        prodPrice = prodQty * proddetails['productPrice']
        """
  
        cursor = conn.cursor()

        query = "select prod_name, prod_price from shoppingcart.products where prod_id =%s"
      
        cursor.execute(query,(parameters['productId'],))
    
        prodDetails = cursor.fetchall()
       
        if prodDetails == []:
            return {
                "statusCode": 200,
                "body": json.dumps(
                    {"status" : "FAIL",
                     "message": "No product found with product Id : "+str(parameters['productId'])
                    },default=str)
                }
        else:
            
            prodQty = parameters['productQty']
            cookieuuId = parameters['uuId']
            prodId = parameters['productId']
            prodName = prodDetails[0][0]            
            prodPrice = Decimal(prodDetails[0][1])
            prodcreateDate = date.today()
            produpdateDate = date.today()

            query = "select prod_qty from shoppingcart.cart where prod_id=%s and cookie_uuid=%s"
            cursor.execute(query,(prodId,cookieuuId))
            updateQty = cursor.fetchall()

            if len(updateQty) > 0:
                updateQty = updateQty[0][0]
                updateQty += parameters['productQty']

                if updateQty <=0:
                    query = "DELETE from shoppingcart.cart where prod_id=%s and cookie_uuid=%s"
                    cursor.execute(query,(prodId,cookieuuId))
                    conn.commit()
                    return {
                    "statusCode": 200,
                    "body": json.dumps(
                       {"status" : "FAIL",
                        "message": "product Qty is less than 0, deleting the item from cart with Product ID:"+str(prodId)
                       },default=str)
                    }
                
                updatePrice = updateQty * prodPrice

                query="UPDATE shoppingcart.cart SET prod_qty=%s, prod_price=%s,update_date=%s where prod_id=%s and cookie_uuid=%s"
                cursor.execute(query,(updateQty,updatePrice,produpdateDate,prodId,cookieuuId))
                conn.commit() 

                return {
                    "statusCode": 200,
                    "body": json.dumps(
                       {"status" : "SUCCESS",
                         "message": "product successfully updated in cart with product ID:"+str(prodId),
                         "productId"      : prodId, 
                         "prodName"       : prodName,
                         "prodQty"        : updateQty,
                         "prodPrice"      : Decimal(updatePrice),
                         "produpdateDate" : produpdateDate
                        },default=str)
                    }
            else:
                #cursor = conn.cursor()
                query = "SELECT MAX(cart_id)+1 from shoppingcart.cart"
                cursor.execute(query)
                cartId = cursor.fetchall() 
                cartId = cartId[0][0]
                prodPrice = prodPrice * prodQty

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
                       {"message": "product successfully added to cart with cart ID:"+str(cartId),
                         "cookieUuid"     : cookieuuId,
                         "productId"      : prodId, 
                         "prodName"       : prodName,
                         "prodQty"        : prodQty,
                         "prodPrice"      : Decimal(prodPrice),
                         "prodcreateDate" : prodcreateDate,
                         "produpdateDate" : produpdateDate
                        },default=str)
                    }
    
    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps(
                {"status" : "FAIL",
                "message": f"Failed to add or update the product: {e}"
                })
        }
    
    finally:
        cursor.close()
        conn.close()
      

    

