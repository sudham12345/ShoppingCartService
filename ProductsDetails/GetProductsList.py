import psycopg2
import json
import os

def get_records(event,context):

    parameters = event['queryStringParameters']

    conn = psycopg2.connect(
            host=os.environ['POSTGRES_HOST'],
            port=os.environ['POSTGRES_PORT'],
            dbname=os.environ['POSTGRES_DB'],
            user=os.environ['POSTGRES_USER'],
            password=os.environ['POSTGRES_PASSWORD']
        )
    
    cursor = conn.cursor()

    query = "SELECT * FROM shoppingcart.products WHERE LOWER(prod_category)=LOWER(%s)"
    cursor.execute(query,(parameters['category'],))
    
    records = cursor.fetchall()

    cursor.close()
    conn.close()

    if records == []:
       return{
        "body": json.dumps ("No product list found with Category: "+str(parameters['category']),default=str)
       }
    else:
       return {
        "statusCode":200,
        "body": json.dumps(records,default=str)
       }
      
    
    
    

    