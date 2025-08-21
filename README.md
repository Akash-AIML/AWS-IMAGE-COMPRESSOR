# AWS Serverless Image Compressor

This project is a real-time, serverless image compression tool built entirely on AWS. It allows users to upload images, compress them with adjustable quality settings, and download the optimized files instantly.

## Features
- **Modern Web Interface**: Responsive frontend for easy image uploads.
- **Adjustable Quality**: Users can select compression levels from 20% to 100%.
- **Direct Download**: Compressed images are available for immediate download.
- **Serverless Backend**: Powered by AWS Lambda for scalability and cost-efficiency.
- **Real-time Notifications**: SNS sends email notifications upon successful compression.

## Architecture
The application uses a serverless architecture composed of the following AWS services:
- **Amazon S3**: Hosts the static frontend (`index.html`).
- **AWS Lambda**: Executes the core image compression logic using Python and the Pillow library.
- **API Gateway**: Provides a RESTful API to trigger the Lambda function.
- **Amazon SNS**: Sends email notifications to users.

## Getting Started

### Prerequisites
- AWS Account
- Python 3.9
- AWS CLI configured

### Setup and Deployment
1. **Frontend**: Upload the `index.html` file to an S3 bucket and enable static website hosting.
2. **Backend**:
   - Create a Lambda function with the provided `lambda_function.py`.
   - Add a Lambda Layer for the Pillow library.
   - Configure environment variables for the S3 bucket and SNS topic ARN.
3. **API**:
   - Create a REST API in API Gateway with a `/compress` resource.
   - Set up a `POST` method with Lambda Proxy integration.
   - Enable CORS and deploy the API.

## Usage
To use the compressor, simply open the `index.html` file in your browser, upload an image, select your desired quality, and click "Compress & Download."
```

### **Step 4: Push Your Project to GitHub**

Now, you will use the command line to push your project to a new GitHub repository.

1. **Create a New Repository on GitHub**:
   - Go to [GitHub](https://github.com) and log in.
   - Click the **+** icon in the top-right corner and select **New repository**.
   - Name your repository (e.g., `aws-image-compressor`), add a short description, and keep it public.
   - Do not initialize with a `README` or `.gitignore`, as you've already created them.
   - Click **Create repository**.

2. **Initialize Git and Push Your Project**:
   - Open your terminal or command prompt and navigate to your project's root directory (`ImageCompressorAWS/`).
   - Follow these commands:

     ```bash
     # Initialize a new Git repository in your project folder
     git init

     # Add all files to the staging area
     git add .

     # Commit the files with a descriptive message
     git commit -m "Initial commit: Add serverless image compressor project"

     # Add the remote repository URL (replace with your repository's URL)
     git remote add origin https://github.com/your-username/aws-image-compressor.git

     # Push your code to the main branch on GitHub
     git push -u origin main
     ```
   **Note**: If your default branch is `master`, use `git push -u origin master` instead.

### **Step 5: Verify on GitHub**

Refresh your GitHub repository page. You should now see all your files, including the `README.md` and `.gitignore`, neatly organized.

By following these steps, you will have a professional, well-documented project on your GitHub profile that effectively showcases your skills in serverless architecture and AWS.
