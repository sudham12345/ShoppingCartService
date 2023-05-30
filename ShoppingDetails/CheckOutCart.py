import requests
import psycopg2
import json
import os
from decimal import Decimal
from datetime import date

def checkout_cart(event,context):

    parameters = json.loads(event['body'])
     
    try:
       # userName = event["headers"]["Authorization"]["sub"]
        userName = parameters.get("userName")
    except KeyError:
        return  {
            "statusCode": 400,
            "body": json.dumps({
                "status" : "FAIL",
                "message": "Invalid userName"
            },default=str)
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
       
        query = "select user_id from shoppingcart.user where TRIM(user_name)=TRIM(%s)"
        cursor.execute(query,(userName,))
        userId = cursor.fetchall()        
        
        if len(userId) > 0:
            userId = userId[0][0]
        else:
            raise KeyError("No User Id found")
        

        query = "SELECT MAX(order_id)+1 from shoppingcart.orders"
        cursor.execute(query)
        orderId = cursor.fetchall()          

        if orderId[0][0] is None:
            orderId =1
        else:
            orderId = orderId[0][0]
        
        orderCreateDate = date.today()

        query = "INSERT into shoppingcart.orders values(%s,%s,%s)"
        cursor.execute(query,(orderId, userId, orderCreateDate))               

        query = "select cart_id,prod_id, prod_name, prod_qty, prod_price\
                 from shoppingcart.user_cart where user_id=%s"
        cursor.execute(query,(userId,))
        records=cursor.fetchall()

        for row in records:     

            query = "SELECT MAX(order_details_id)+1 from shoppingcart.order_details"
            cursor.execute(query)
            orderDetailsId = cursor.fetchall()          

            if orderDetailsId[0][0] is None:
                orderDetailsId =1
            else:
                orderDetailsId = orderDetailsId[0][0]       
            
            cartId = row[0]

            query = "INSERT into shoppingcart.order_details values(%s,%s,%s,%s,%s,%s)"
            cursor.execute(query,(orderDetailsId, orderId, row[1], row[2], row[3], Decimal(row[4])))
            
            query = "DELETE from shoppingcart.user_cart where cart_id=%s"
            cursor.execute(query,(cartId,))
        
        conn.commit()
        
        response = {
                "statusCode": 200,                
                "body": json.dumps(
                   { "status" : "SUCCESS",
                     "message": "cart successfully checked out with User Id:"+str(userId),                  
                  },default=str)
                }

    except Exception as e:
        conn.rollback()
        response =  {
            "statusCode": 500,
            "body": json.dumps({
                "status" : "FAIL",
                "message": f"Failed to checkout cart: {e}"
            })
        }
    
    finally:
        cursor.close()
        conn.close()
        return response