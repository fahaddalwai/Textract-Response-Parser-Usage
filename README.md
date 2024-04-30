<h1 align="center" id="title">Textractify-PDF to RDS</h1>

<p align="center"><img src="https://socialify.git.ci/fahaddalwai/Textractify/image?forks=1&amp;language=1&amp;logo=https%3A%2F%2Fencrypted-tbn0.gstatic.com%2Fimages%3Fq%3Dtbn%3AANd9GcS8eApmowWup45_PzJojSQvmqViTJhpK_J38G5SFcOdmg%26s&amp;name=1&amp;owner=1&amp;stargazers=1&amp;theme=Light" alt="project-image"></p>

<p id="description">A project using AWS Textract to extract text from multi-page PDF documents and insert into a database. Firstly validates the document in the S3 bucket and checks rotation, height, width, etc. and sends the job to AWS Textract. The resulting JSON containing the tables and key-values is cleaned and inserted into an SQL database. Viola!</p>

<h2>Project Screenshots:</h2>

![image](https://github.com/fahaddalwai/Textractify/assets/71600359/978ef1b2-3bf9-4e08-8a89-38062e6f8bdb)


  
  
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

Make Pull requests which improve the functionality of the application in any sorts. It should conform with the following conditions:

*   Clear, short, crisp description of the PR.
*   Should add on to the value of the application.

  
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
