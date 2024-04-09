import json
import boto3
import base64
import os
import cv2
import numpy as np
import fitz

s3 = boto3.client('s3')

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
    return (height/width)*100

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



def lambda_handler(event, context):
    try:
        if 'httpMethod' in event and event['httpMethod'] == 'POST':
            data = json.loads(event['body'])
            name = data['name']
            file_data = data['file']

            # Decode base64
            file_data = file_data[file_data.find(",") + 1:]
            dec = base64.b64decode(file_data + "===")

            # Check if it's a PDF
            if dec[:4] == b'%PDF':
                color_images = convert_pdf_to_images(dec)
            else:
                # Save to a temporary file
                temp_filename = "/tmp/temp_image.png"
                with open(temp_filename, "wb") as temp_file:
                    temp_file.write(dec)

                # Read the color image using OpenCV
                color_images = [cv2.imread(temp_filename)]

                # Clean up temporary file
                os.remove(temp_filename)

            for color_image in color_images:
                # Convert color image to grayscale
                gray_image = cv2.cvtColor(color_image, cv2.COLOR_BGR2GRAY)

                # Get image dimensions and skewness
                height, width = get_height_width(gray_image)
                dpi = get_dpi(gray_image)
                skewness = skew_angle_hough_transform(gray_image)

                # Threshold values, modify as required
                min_height = 700  # in pixels
                min_width = 700   # in pixels
                max_skewness = 5  # in degrees
                min_dpi = 120   # dots per inch

                skewness_str = str(skewness)
                if height > min_height and width > min_width and dpi >= min_dpi:
                    if abs(skewness) > 90 - max_skewness and abs(skewness) < 90 + max_skewness:
                        # Upload the processed image to S3 in the "documents/" folder
                        s3.put_object(Bucket='#YOURBUCKETNAME', Key='documents/{}'.format(name), Body=dec)
                        
                        # Print a success message
                        print(f"Image uploaded successfully. Name: {name}, Height: {height}, Width: {width}, DPI: {dpi}, Skewness: {skewness_str}")
                        
                        return {'statusCode': 200, 'body': json.dumps({'message': 'successful lambda function call',
                                                                        'height': height, 'width': width, 'dpi': dpi,
                                                                        'skewness': skewness_str}),
                                'headers': {'Access-Control-Allow-Origin': '*'}}
                    else:
                        print(f'Skewness does not meet requirements. Image not uploaded. Skewness: {skewness_str}')
                        return {'statusCode': 400, 'body': json.dumps({'error': f'Skewness does not meet requirements. Image not uploaded. Skewness: {skewness_str}'})}
                else:
                    print(f'Image dimensions do not meet requirements. Image not uploaded. Height: {height}, Width: {width}, DPI: {dpi}')
                    return {'statusCode': 400, 'body': json.dumps({'error': f'Image dimensions do not meet requirements. Image not uploaded. Height: {height}, Width: {width}, DPI: {dpi}'})}
    except Exception as e:
        # Log the error
        print(f"Error: {str(e)}")
        return {'statusCode': 500, 'body': json.dumps({'error': str(e)})}
