import psycopg2
import json
import os
from decimal import Decimal

def list_records(event,context):

    try:
        parameters = json.loads(event['body'])
    except Exception as e:
        return  {
            "statusCode": 500,
            "body": json.dumps({
                "message": f"Required params : uuId (string) or userName(string) {e}"
            })
        }
   
    try:
        conn = psycopg2.connect(
                host=os.environ['POSTGRES_HOST'],
                port=os.environ['POSTGRES_PORT'],
                dbname=os.environ['POSTGRES_DB'],
                user=os.environ['POSTGRES_USER'],
                password=os.environ['POSTGRES_PASSWORD']
            )

        cursor = conn.cursor()

        if parameters.get("uuId"):
            query = "SELECT cart_id,prod_id,prod_name,prod_qty,prod_price FROM shoppingcart.cart WHERE cookie_uuid=%s"  
            cursor.execute(query,(parameters['uuId'],))
        """
        elif parameters.get("userName"):
            userName = parameters['userName']
            query = "select user_id from shoppingcart.user where TRIM(user_name)=TRIM(%s)"
            cursor.execute(query,(userName,))
            userId = cursor.fetchall()       
            userId = userId[0][0]
        
            query = "SELECT cart_id,prod_id,prod_name,prod_qty,prod_price FROM shoppingcart.user_cart WHERE user_id=%s"
            cursor.execute(query,(userId,))
      
        else:
            response = {
            "statusCode": 500,
            "body": json.dumps({
                "status" :"FAIL",
                "message": "Required params : uuId (string) or userName(string)"
            })
        }
        """ 
        records = cursor.fetchall()        
    
        listRecords=[]
    
        for row in records:
            listRecords.append(
            {"cartId"     : row[0],
            "productId"   : row[1],
            "prodName"    : row[2],
            "prodQty"     : row[3],
            "prodPrice"   : Decimal(row[4])
            })       

        if listRecords==[]:
            response = {
            "statusCode": 200,
            "body": json.dumps("No items to list in the cart", default=str)
            }
        else:
            response = {
                "statusCode":200,
                "body": json.dumps(listRecords,default=str)           
                }
        
    except Exception as e:
        response = {
            "statusCode": 500,
            "body": json.dumps({
                "status" :"FAIL",
                "message": f"Failed to list products: {e}"
            })
        }

    finally:
        cursor.close()
        conn.close()
        return response

  