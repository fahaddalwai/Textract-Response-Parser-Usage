import json
import boto3
from trp import Document
import pymysql
import sys
import os
from database_utils import insert_data_table2,select_all_from_table,insert_data_prompts, insert_data_table1, insert_data_vocab_based_lesson



s3 = boto3.client("s3")



user_name = "admin"
password = "alejandro"
rds_proxy_host = "proxy-1709461494239-mysqlforlambda.proxy-chgjhfwkta1o.us-east-2.rds.amazonaws.com"
db_name = "textractDB"

try:
        conn = pymysql.connect(host=rds_proxy_host, user=user_name, passwd=password, db=db_name, connect_timeout=5)
except pymysql.MySQLError as e:
    print("ERROR: Unexpected error: Could not connect to MySQL instance.")
    print(e)
    sys.exit(1)

print("SUCCESS: Connection to RDS for MySQL instance succeeded")



def getJobResults(jobId):
    """
    Get read pages based on jobId
    """
    pages = []
    textract = boto3.client("textract")
    response = textract.get_document_analysis(JobId=jobId)
    pages.append(response)

    nextToken = response.get("NextToken")  # Use get() method for safer access
    while nextToken:
        response = textract.get_document_analysis(JobId=jobId, NextToken=nextToken)
        pages.append(response)
        nextToken = response.get("NextToken")
    return pages




def lambda_handler(event, context):
    notificationMessage = json.loads(json.dumps(event))["Records"][0]["Sns"]["Message"]
    pdfTextExtractionStatus = json.loads(notificationMessage)["Status"]
    pdfTextExtractionJobTag = json.loads(notificationMessage)["JobTag"]
    pdfTextExtractionJobId = json.loads(notificationMessage)["JobId"]

    print(pdfTextExtractionJobTag + " : " + pdfTextExtractionStatus)
    
    
    if pdfTextExtractionStatus == "SUCCEEDED":
        response = getJobResults(pdfTextExtractionJobId)
        
        
        doc = Document(response)
        
        json_result = json.dumps(response)
        
        print(json_result)
        
        contains_aris = 'aris' in json_result
        
        if contains_aris:
            s3_bucket = "sheetstore"
            s3_key = "json/" + pdfTextExtractionJobTag+".json"
            s3.put_object(Body=json_result.encode('utf-8'), Bucket=s3_bucket, Key=s3_key)
    
            
            print(f"Raw response uploaded to S3: s3://{s3_bucket}/{s3_key}")
            
            document_data = {} #hasmap for storing. we convert this into json later
            
            
            for page_idx, page in enumerate(doc.pages):
                page_key = f"page_{page_idx}"
                document_data[page_key] = {
                    "tables": {},
                    "key_data": {},  # Key data for each page
                    "key_table_3_data": {},  # Key data for each page

                }
                
                
                
                for table_idx, table in enumerate(page.tables):
                    
                    table_key = f"table_{table_idx}"
                    document_data[page_key]["tables"][table_key] = []

                    for r, row in enumerate(table.rows):
                        row_data = []
                        for c, cell in enumerate(row.cells):
                            print(row_data)
                            row_data.append(cell.text)
                        document_data[page_key]["tables"][table_key].append(row_data)
                    

                    

        
        
                    #code to store in the sql
                    if table_idx==0:
                        # Loop through rows and cells to collect the data
                        for r, row in enumerate(table.rows):
                            row_data = []
                            for c, cell in enumerate(row.cells):
                                row_data.append(cell.text)
                            
                            # Insert each row into the MySQL table
                            print(row_data)
                            #insert_data_table1(conn, row_data)
                    
                        select_all_from_table(conn,'table1')
                        
                    elif table_idx == 1:  
                        # Loop through rows and cells to collect the data
                        for r, row in enumerate(table.rows):
                            row_data = []
                            for c, cell in enumerate(row.cells):
                                row_data.append(cell.text)
                        
                            # Insert each row into the MySQL table
                            #insert_data_table2(conn, row_data)
                    
                        select_all_from_table(conn,'table2')
                        
                    elif (table_idx == 2 or table_idx==3 or table_idx==4): 
                        # Loop through rows and cells to collect the data
                        for r, row in enumerate(table.rows):
                            row_data = []
                            for c, cell in enumerate(row.cells):
                                row_data.append(cell.text)
                        
                            # Insert each row into the MySQL table
                            #insert_data_prompts(conn, row_data)
                    
                        select_all_from_table(conn,'prompts')
                    

                
                keys = ["DATE", "LESSON TITLE", "LESSON NUMBER", "STUDENT'S NAME","Notes"]
                for key in keys:
                    field = page.form.getFieldByKey(key)
                    if field and field.value is not None:
                        print("Field: Key: {}, Value: {}".format(field.key, field.value))
                        document_data[page_key]["key_data"][key] = field.value.text   
                        
                        
                    
                # Search fields by key
                keys = ["Date:", "Time Started:", "Time Finished:", "Staff Initials:", "% Correct", "Notes:"]
                for key in keys:
                    fields = page.form.searchFieldsByKey(key)
            
                    # Ensure the 'key_table_3_data' key for the current key is present
                    if key not in document_data[page_key]["key_table_3_data"]:
                        document_data[page_key]["key_table_3_data"][key] = []
            
                    for field in fields:
                        if field.value is not None:
                            print("Key: {}, Field: Key: {}, Value: {}".format(key, field.key, field.value.text))
                            # Append the searched field value to the list
                            if field.value.text is not None:
                                document_data[page_key]["key_table_3_data"][key].append(field.value.text)
           
                    
                    
                    
                    
                    

                print(document_data)
                keys = ["DATE", "LESSON TITLE", "ESSON NUMBER", "STUDENT'S NAME"]
                row_data = []
                
                
                
                for key in keys:
                    field = page.form.getFieldByKey(key)
                    if field and field.value is not None:
                        row_data.append(field.value.text)
                    else:
                        row_data.append("")
                
                #insert_data_vocab_based_lesson(conn,row_data)
                select_all_from_table(conn,'vocab_based_lesson')
        # Convert the HashMap to JSON
            json_formatted_result = json.dumps(document_data, indent=2)
            s3_bucket = "sheetstore"
            s3_key = "formattedJSON/" + pdfTextExtractionJobTag+".json"
            s3.put_object(Body=json_formatted_result.encode('utf-8'), Bucket=s3_bucket, Key=s3_key)                
                        
                
        else:
            # Return an error if the field is not found
            print("Error: Field with keyword aris not found.")
            return {
                'statusCode': 400,
                'body': json.dumps('Wrong Document type entered')
            }
            
    