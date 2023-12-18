import subprocess

# Fetch data from Etsy
subprocess.run(['python', 'turbo.py'])

# Generate template using the fetched data
subprocess.run(['python', 'generate_template.py'])
