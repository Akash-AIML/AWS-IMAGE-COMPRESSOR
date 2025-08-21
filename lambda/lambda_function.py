import json
import boto3
import base64
from PIL import Image
import io
import os

s3_client = boto3.client('s3')
sns_client = boto3.client('sns')

# CORS headers to attach to all responses
CORS_HEADERS = {
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Headers': 'Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token',
    'Access-Control-Allow-Methods': 'POST, OPTIONS',
    'Content-Type': 'application/json'
}

def lambda_handler(event, context):
    try:
        # Debug print for the incoming event
        print(f"Received event: {json.dumps(event)}")

        http_method = event.get('httpMethod')

        # Handle CORS preflight
        if http_method == 'OPTIONS':
            return {
                'statusCode': 200,
                'headers': CORS_HEADERS,
                'body': 'OK'
            }

        # Handle direct compress POST
        if http_method == 'POST':
            return handle_direct_compression(event)

        return {
            'statusCode': 400,
            'headers': CORS_HEADERS,
            'body': json.dumps({'error': 'Invalid request method'})
        }

    except Exception as e:
        print(f"Error: {str(e)}")
        return {
            'statusCode': 500,
            'headers': CORS_HEADERS,
            'body': json.dumps({'error': str(e)})
        }

def handle_direct_compression(event):
    try:
        body = json.loads(event['body'])
        image_data = base64.b64decode(body['imageData'])
        filename = body['filename']
        quality = int(body.get('quality', 80))

        print(f"Processing {filename} with quality {quality}%")

        compressed_data = compress_image(image_data, quality)
        compressed_b64 = base64.b64encode(compressed_data).decode('utf-8')

        original_size = len(image_data)
        compressed_size = len(compressed_data)

        send_notification(filename, original_size, compressed_size, quality)

        return {
            'statusCode': 200,
            'headers': CORS_HEADERS,
            'body': json.dumps({
                'success': True,
                'filename': f"{filename}_compressed_{quality}%.jpg",
                'originalSize': original_size,
                'compressedSize': compressed_size,
                'imageData': compressed_b64,
                'savings': f"{((original_size - compressed_size) / original_size * 100):.1f}%"
            })
        }

    except Exception as e:
        print(f"Compression error: {str(e)}")
        return {
            'statusCode': 500,
            'headers': CORS_HEADERS,
            'body': json.dumps({'error': f'Compression failed: {str(e)}'})
        }

def compress_image(image_data, quality=80):
    try:
        image = Image.open(io.BytesIO(image_data))

        if image.mode in ('RGBA', 'LA', 'P'):
            image = image.convert('RGB')

        output = io.BytesIO()
        image.save(output, format='JPEG', quality=quality, optimize=True)
        return output.getvalue()

    except Exception as e:
        print(f"Image processing error: {str(e)}")
        raise

def send_notification(filename, original_size, compressed_size, quality):
    try:
        savings = ((original_size - compressed_size) / original_size * 100)
        message = f"Image Compressed Successfully!\n\nFile: {filename}\nQuality: {quality}%\nOriginal Size: {original_size:,} bytes ({original_size/1024/1024:.2f} MB)\nCompressed Size: {compressed_size:,} bytes ({compressed_size/1024/1024:.2f} MB)\nSavings: {savings:.1f}% reduction\n\nImage ready for download!"

        sns_client.publish(
            TopicArn=os.environ['SNS_TOPIC_ARN'],
            Message=message,
            Subject=f"Compressed: {filename}"
        )

    except Exception as e:
        print(f"Notification error: {str(e)}")
