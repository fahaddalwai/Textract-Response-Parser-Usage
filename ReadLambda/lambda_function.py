import os
import json
import boto3
import urllib.parse

import os
import json
import boto3
import urllib.parse
import fitz
import cv2
import numpy as np

s3 = boto3.client('s3', region_name='us-east-2')

def is_supported_file(key):
    # Check if the file extension is either 'pdf' or 'jpg'
    return key.lower().endswith(('.pdf', '.jpg','.jpeg'))

def convert_pdf_to_images(pdf_data):
    pdf_document = fitz.open(stream=pdf_data, filetype="pdf")
    images = []
    for page_num in range(pdf_document.page_count):
        page = pdf_document.load_page(page_num)
        image = page.get_pixmap()
        np_image = np.frombuffer(image.samples, dtype=np.uint8).reshape((image.height, image.width, 3))
        images.append(np_image)
    return images

def get_height_width(image):
    height, width = image.shape[:2]
    return height, width

def get_dpi(image):
    height, width = image.shape[:2]
    return (height / width) * 100

def skew_angle_hough_transform(image):
    # Apply Canny edge detection
    edges = cv2.Canny(image, 50, 200, apertureSize=3)

    # Perform Hough Line Transform
    lines = cv2.HoughLines(edges, rho=1, theta=np.pi / 180, threshold=200)

    if lines is not None and len(lines) > 1:
        # Extract angles from the lines
        angles = [line[0][1] for line in lines]
        most_common_angle = np.rad2deg(np.median(angles))
    else:
        most_common_angle = 0.0

    return most_common_angle

def lambda_handler(event, _):
    print("Triggered getTextFromS3PDF event: " + json.dumps(event, indent=2))

    bucket = event['Records'][0]['s3']['bucket']['name']
    key = urllib.parse.unquote_plus(event['Records'][0]['s3']['object']['key'])
    
    try:
        if key.lower().endswith('.jpeg'):
            new_key = os.path.splitext(key)[0] + '.jpg'
            s3.copy_object(Bucket=bucket, CopySource={'Bucket': bucket, 'Key': key}, Key=new_key)
            s3.delete_object(Bucket=bucket, Key=key)
            key = new_key
        
        if is_supported_file(key):
            textract = boto3.client("textract", region_name='us-east-2')
            
            # Retrieve the PDF data from S3
            response = s3.get_object(Bucket=bucket, Key=key)
            pdf_data = response['Body'].read()
            
            # Convert PDF to images
            images = convert_pdf_to_images(pdf_data)

            # Flag to determine if processing should continue
            process_image = True

            # Perform analysis on each image
            for image in images:
                height, width = get_height_width(image)
                dpi = get_dpi(image)
                skewness = skew_angle_hough_transform(image)
                
                print(f"Height={height}px, Width={width}px, DPI={dpi}, Skewness={skewness} degrees")

                # Your custom processing logic based on image properties
                if height <= 500:
                    # Image height does not meet criteria, set flag to False and break
                    process_image = False
                    error_message = f"Image {key} height ({height}px) does not meet the required minimum (500px)."
                    break
                elif width <= 500:
                    # Image width does not meet criteria, set flag to False and break
                    process_image = False
                    error_message = f"Image {key} width ({width}px) does not meet the required minimum (500px)."
                    break
                elif dpi <= 100:
                    # Image dpi does not meet criteria, set flag to False and break
                    process_image = False
                    error_message = f"Image {key} dpi ({dpi}) does not meet the required minimum (100)."
                    break
                elif abs(skewness) < 90 - 5 or abs(skewness) > 90 + 5:  # Adjust the skewness threshold as needed
                    # Image skewness does not meet criteria, set flag to False and break
                    process_image = False
                    error_message = f"Image {key} skewness ({skewness}) exceeds the allowed threshold (10 degrees)."
                    break

            if process_image:
                # Continue with text extraction processing
                textract.start_document_analysis(
                    DocumentLocation={"S3Object": {"Bucket": bucket, "Name": key}},
                    JobTag=key.replace("/", "#YOURWORD") + "_Job",
                    FeatureTypes=["FORMS", "TABLES"],
                    NotificationChannel={
                        "RoleArn": os.environ["SNSROLEARN"],
                        "SNSTopicArn": os.environ["SNSTOPIC"],
                    },
                )
                return "Triggered PDF Processing for " + key
            else:
                # Move the item to the 'unacceptableitems' folder
                new_key = 'unacceptableitems/{}'.format(os.path.basename(key))
                
                # Download the object
                downloaded_object = s3.get_object(Bucket=bucket, Key=key)['Body'].read()
                
                # Upload the object to the 'unacceptableitems' folder
                s3.put_object(Bucket=bucket, Key=new_key, Body=downloaded_object)
                
                # Delete the original object
                s3.delete_object(Bucket=bucket, Key=key)
                
                print(f"{error_message} Moved to 'unacceptableitems' folder.")
                return error_message

        else:
            print(f"File {key} is not a supported format (PDF or JPG). Skipping analysis.")
            return "Skipped processing for unsupported file format: " + key

    except Exception as e:
        print(e)
        print(
            "Error getting object {} from bucket {}. Make sure they exist and your bucket is in the same region as this function.".format(
                key, bucket
            )
        )
        raise e
