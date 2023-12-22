from flask import Flask, render_template, jsonify
import subprocess
import json

app = Flask(__name__)

def fetch_data_and_generate_template():
    try:
        # Fetch data from Etsy
        subprocess.run(['python', 'turbo.py'], check=True)

        # Generate template using the fetched data
        result = subprocess.run(['python', 'generate_template.py'], check=True, capture_output=True, text=True)

        rendered_template_data = json.loads(result.stdout)

        # Log created_timestamp for debugging
        for receipt in rendered_template_data.get('receipts', []):
            print(f"Timestamp: {receipt.get('created_timestamp')}")

        return rendered_template_data

    except subprocess.CalledProcessError as e:
        return {'status': 'error', 'message': f'Error: {e}', 'error_output': e.stderr}


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/fetch_and_generate')
def fetch_and_generate():
    # Add your data fetching and processing logic here
    response = fetch_data_and_generate_template()

    if response.get('status') == 'success':
        return render_template('rendered_template.html')
    else:
        return render_template('error.html', error_message=response.get('message'))

@app.route('/rendered_template.html')
def rendered_template():
    # Add logic to render the rendered_template.html page
    return render_template('rendered_template.html')

if __name__ == '__main__':
    app.run(debug=True, port=8080)