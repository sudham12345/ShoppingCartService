import psycopg2
import json
import os

def delete_records(event,context):

    parameters = event['body']

    conn = psycopg2.connect(
            host=os.environ['POSTGRES_HOST'],
            port=os.environ['POSTGRES_PORT'],
            dbname=os.environ['POSTGRES_DB'],
            user=os.environ['POSTGRES_USER'],
            password=os.environ['POSTGRES_PASSWORD']
        )

    cursor = conn.cursor()

    for item in parameters:

        query = "DELETE FROM shoppingcart.cart WHERE cart_id=%s"   
        cursor.execute(query,(item['cartId'],))
       
    cursor.close()
    conn.close()
                   

    return {
        "statusCode":200,
        "body": json.dumps("Records deleted successfully",default=str)
    }