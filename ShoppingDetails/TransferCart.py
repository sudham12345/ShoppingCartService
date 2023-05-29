import requests
import psycopg2
import json
import os
import EventValidate
from decimal import Decimal
from datetime import date

def transer_cart(event,context):
    
    try:
        parameters = json.loads(event['body'])         
    except Exception as e:
        return  {
            "statusCode": 500,
            "body": json.dumps({
                "status" : "FAIL",
                "message": f"Missing params, Required : uuId (string in body), userName (String in headers) {e}"
            })
        } 
    
    
    try:
     #   userName = event["headers"]["Authorization"]["sub"]
        userName = parameters.get("userName")
    except KeyError:
        return  {
            "statusCode": 400,
            "body": json.dumps({
                "status" : "FAIL",
                "message": "Invalid userName"
            },default=str)
        } 
    
    if not parameters.get("uuId"):
        return  {
            "statusCode": 500,
            "body": json.dumps({
                "status" : "FAIL",
                "message": "Missing uuId: Required uuId (string in body)"
            },default=str
            )
        }
    else:
        uuId = parameters['uuId']
   

    try:
        conn = psycopg2.connect(
                host=os.environ['POSTGRES_HOST'],
                port=os.environ['POSTGRES_PORT'],
                dbname=os.environ['POSTGRES_DB'],
                user=os.environ['POSTGRES_USER'],
                password=os.environ['POSTGRES_PASSWORD']
            )   
    
        cursor = conn.cursor()
        
        userName = parameters['userName']
        query = "select user_id from shoppingcart.user where TRIM(user_name)=TRIM(%s)"
        cursor.execute(query,(userName,))
        userId = cursor.fetchall()        
        
        if len(userId) > 0:
            userId = userId[0][0]
        else:
            raise KeyError("No User Id found")
        
        query = "select cart_id, prod_id, prod_name, prod_qty, prod_price, create_date, update_date\
                 from shoppingcart.cart where cookie_uuid=%s"
        cursor.execute(query,(uuId,))
        records=cursor.fetchall()

        for row in records:            
           
            query = "INSERT into shoppingcart.user_cart values(%s,%s,%s,%s,%s,%s,%s,%s)"
            cursor.execute(query,(row[0], userId, row[1], row[2], row[3], Decimal(row[4]), row[5], row[6]))
            conn.commit()

            #post to SQS Queue to delete from shoppingcart.cart
        
        response = {
                "statusCode": 200,                
                "body": json.dumps(
                   { "status" : "SUCCESS",
                     "message": "cart successfully transferred with User Id:"+str(userId),                  
                  },default=str)
                }

    except Exception as e:
        conn.rollback()
        response =  {
            "statusCode": 500,
            "body": json.dumps({
                "status" : "FAIL",
                "message": f"Failed to transfer cart: {e}"
            })
        }
    
    finally:
        cursor.close()
        conn.close()
        return response