<h1 align="center" id="title">Textract Response Parser</h1>

<p align="center"><img src="https://socialify.git.ci/fahaddalwai/Textract-Response-Parser-Usage/image?font=Inter&amp;forks=1&amp;language=1&amp;logo=https%3A%2F%2Fencrypted-tbn0.gstatic.com%2Fimages%3Fq%3Dtbn%3AANd9GcQghwiHvCWRk0ONHC88_WFbL4JEwCVogNRv2QcSa2NddA%26s&amp;name=1&amp;owner=1&amp;stargazers=1&amp;theme=Light" alt="project-image"></p>

<p id="description">A project using AWS Textract to extract text from multi-page PDF documents and insert into a database. Firstly validates the document in the S3 bucket and checks rotation, height, width, etc. and sends the job to AWS Textract. The resulting JSON containing the tables and key-values is cleaned and inserted into an SQL database. Viola!</p>

<h2>Project Screenshots:</h2>

<img src="https://private-user-images.githubusercontent.com/71600359/322206332-8cc1723b-d20e-4445-82ff-a486bba8929b.png?jwt=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJnaXRodWIuY29tIiwiYXVkIjoicmF3LmdpdGh1YnVzZXJjb250ZW50LmNvbSIsImtleSI6ImtleTUiLCJleHAiOjE3MTQzOTczNDUsIm5iZiI6MTcxNDM5NzA0NSwicGF0aCI6Ii83MTYwMDM1OS8zMjIyMDYzMzItOGNjMTcyM2ItZDIwZS00NDQ1LTgyZmYtYTQ4NmJiYTg5MjliLnBuZz9YLUFtei1BbGdvcml0aG09QVdTNC1ITUFDLVNIQTI1NiZYLUFtei1DcmVkZW50aWFsPUFLSUFWQ09EWUxTQTUzUFFLNFpBJTJGMjAyNDA0MjklMkZ1cy1lYXN0LTElMkZzMyUyRmF3czRfcmVxdWVzdCZYLUFtei1EYXRlPTIwMjQwNDI5VDEzMjQwNVomWC1BbXotRXhwaXJlcz0zMDAmWC1BbXotU2lnbmF0dXJlPTc2ZjljZGIxMzBjODYyMTRiOTkzZTlhYzFkNTM2ZmM5YWE1ZmFmNDkxYjRiNjM4MTg5NDBjMWRlMDAyOGUxYjImWC1BbXotU2lnbmVkSGVhZGVycz1ob3N0JmFjdG9yX2lkPTAma2V5X2lkPTAmcmVwb19pZD0wIn0.IfZ3iFDlPKlc_w4zjmbiaX5G0ckWa4l1rmXDuPYQ_nQ" alt="project-screenshot" width="600" height="400/">

  
  
<h2>🧐 Features</h2>

Here're some of the best features:

*   Converts multi-page pdf's and images
*   Document rotation check using Hough Transform
*   Asynchronous processing
*   JSON and SQL outputs
*   Page-wise extraction

<h2>🛠️ Installation Steps:</h2>

<p>1. Deploy AWS RDS MySQL database. Define your VPC.</p>

<p>2. Define the 3 lambda functions as above and connect to your own S3 buckets</p>

<p>3. Create an AWS SNS Textract service and allow WriteFunction to access it.</p>

<p>4. Start uploading your documents in the S3 bucket!</p>

<h2>🍰 Contribution Guidelines:</h2>

Contributions are what make the open source community such an amazing place to learn inspire and create. Any contributions you make are greatly appreciated. If you have a suggestion that would make this better please fork the repo and create a pull request. You can also simply open an issue with the tag "enhancement".

  
  
<h2>💻 Built with</h2>

Technologies used in the project:

*   AWS Lambda
*   AWS RDS
*   AWS Simple Notification Service
*   AWS Textract
*   AWS S3 Bucket
*   Python

<h2>🛡️ License:</h2>

Distributed under the MIT License.
