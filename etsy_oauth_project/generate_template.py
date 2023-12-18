import json
import os
from jinja2 import Template

# Load the JSON response
with open('receipts_response.json', 'r') as file:
    receipts_data = json.load(file)

# Load the Jinja2 template
with open('template.html', 'r') as file:
    template_content = file.read()

# Create a Jinja2 template object
template = Template(template_content)

# Render the template with the receipt data
rendered_template = template.render(receipts=receipts_data['results'])

# Save the rendered HTML to the 'templates' folder
templates_folder = 'templates'
os.makedirs(templates_folder, exist_ok=True)  # Create the folder if it doesn't exist
template_path = os.path.join(templates_folder, 'rendered_template.html')

with open(template_path, 'w') as file:
    file.write(rendered_template)

# Return a JSON response with the path to the generated template
response_data = {'status': 'success', 'message': 'Template generated successfully', 'template_path': template_path}
print(json.dumps(response_data))
