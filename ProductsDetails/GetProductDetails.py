import psycopg2
import json
import os
from decimal import Decimal

def get_records(event,context):

    parameters = event['queryStringParameters']

    conn = psycopg2.connect(
            host=os.environ['POSTGRES_HOST'],
            port=os.environ['POSTGRES_PORT'],
            dbname=os.environ['POSTGRES_DB'],
            user=os.environ['POSTGRES_USER'],
            password=os.environ['POSTGRES_PASSWORD']
        )

    if not parameters['productId'].isnumeric() \
       or  parameters['productId'] is None:
        return{
         "body": json.dumps('Invalid product ID passed; ID should be integer and not NULL',default=str)
        }
    else:
        cursor = conn.cursor()
        query = "SELECT * FROM shoppingcart.products WHERE prod_id=%s"
    
        cursor.execute(query,(parameters['productId'],))
    
        records = cursor.fetchall()
        cursor.close()
        conn.close()    

    if records == [] :
        return{
            "body": json.dumps ("No product found with productId:"+str(parameters['productId']),default=str)
        }
    else: 
        return {
            "statusCode":200,
            "body": json.dumps(
                {
                 "prodName": records[0][2],
                 "prodPrice": Decimal(records[0][3])
                },default=str
            )         
        }
    
   