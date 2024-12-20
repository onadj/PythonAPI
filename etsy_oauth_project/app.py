from flask import Flask, render_template, send_file, redirect, url_for, request, session

import os
import requests
import time
import json
import subprocess
import csv
import datetime
from fulfillOrder import fulfill_order

app = Flask(__name__)
app.secret_key = '123456789'  

etsy_keystring = "0ljrt44eg7klh1c5t4rmfrph"
shop_id = "34038896"
carrier_name = "hrvatska-posta"


USERNAME = 'onadj'
PASSWORD = '1234'

def refresh_token(api_key, refresh_token):
    endpoint = "https://api.etsy.com/v3/public/oauth/token"
    data = {
        "grant_type": "refresh_token",
        "client_id": api_key,
        "refresh_token": refresh_token
    }

    r = requests.post(endpoint, data=data)
    response_data = r.json()

    if 'access_token' in response_data:
        return response_data
    else:
        print("Failed to refresh access token.")
        return None

def get_existing_orders(api_key, token, shop_id):
    if time.time() > token['expires_in']:
        token_response = refresh_token(api_key, token['refresh_token'])
        token['access_token'] = token_response['access_token']
        token['token_type'] = token_response['token_type']
        token['expires_in'] = time.time() + float(token_response['expires_in'])
        token['refresh_token'] = token_response['refresh_token']

        print("Access Token refreshed.")

    headers = {
        "Accept": "application/json",
        "Content-Type": "application/x-www-form-urlencoded",
        "x-api-key": api_key,
        "Authorization": f"{token['token_type']} {token['access_token']}",
    }

    params = {"receipt_ids": ",".join(map(str, range(1, 2)))}
    endpoint = f"https://openapi.etsy.com/v3/application/shops/{shop_id}/receipts"
    r = requests.get(endpoint, headers=headers, params=params)

    print("Existing Orders - Status Code:", r.status_code)
    response_content = r.text 
    print("Existing Orders - Response Content:", response_content)

    try:
        response_dict = json.loads(response_content)

        with open("existing_orders_response.json", "w", encoding="utf-8") as json_file:
            json.dump(response_dict, json_file, indent=4, ensure_ascii=False)
            print("Existing Orders - Response saved to 'existing_orders_response.json'")
        
        existing_orders = []
        if response_dict.get('count', 0) > 0:
            print("Existing orders found.")
            existing_orders = response_dict.get("results", [])

        return existing_orders

    except json.JSONDecodeError as e:
        print(f"Existing Orders - Error decoding JSON: {e}")
        print("Existing Orders - Raw response:", response_content)
        return []

def get_new_orders(api_key, token, shop_id):
    if time.time() > token['expires_in']:
        token_response = refresh_token(api_key, token['refresh_token'])
        token['access_token'] = token_response['access_token']
        token['token_type'] = token_response['token_type']
        token['expires_in'] = time.time() + float(token_response['expires_in'])
        token['refresh_token'] = token_response['refresh_token']

        print("Access Token refreshed.")

    headers = {
        "Accept": "application/json",
        "Content-Type": "application/x-www-form-urlencoded",
        "x-api-key": api_key,
        "Authorization": f"{token['token_type']} {token['access_token']}",
    }

    params = {"was_paid": "true", "was_shipped": "false", "was_canceled": "false"}
    endpoint = f"https://openapi.etsy.com/v3/application/shops/{shop_id}/receipts"
    r = requests.get(endpoint, headers=headers, params=params)

    print("New Orders - Status Code:", r.status_code)
    response_content = r.text 
    print("New Orders - Response Content:", response_content)

    try:
        response_dict = json.loads(response_content)

        with open("new_orders_response.json", "w", encoding="utf-8") as json_file:
            json.dump(response_dict, json_file, indent=4, ensure_ascii=False)
            print("New Orders - Response saved to 'new_orders_response.json'")
        
        new_orders = []
        if response_dict.get('count', 0) > 0:
            print("There are new orders!")

            for order in response_dict.get("results", []):
                transaction = order.get("transactions", [])[0] if order.get("transactions", []) else {}
                address = order.get("formatted_address", "")

                order_data = {
                    "receipt_id": order.get("receipt_id", ""),  
                    "item_name": transaction.get("title", ""),
                    "quantity": transaction.get("quantity", ""),
                    "price": transaction.get("price", {}).get("amount", ""),
                    "create_timestamp": order.get("create_timestamp", ""),
                    "address": address,
                    "grandtotal": order.get("grandtotal", {}).get("amount", "")  # Adjusted to handle grandtotal
                }
                
                order_data["create_timestamp"] = timestamp_to_string(order_data["create_timestamp"])
                new_orders.append(order_data)

            with open("new_orders_response.csv", "w", newline="", encoding="utf-8") as csv_file:
                csv_writer = csv.writer(csv_file)
                header = ["Order ID", "Item Name", "Quantity", "Price", "Created Timestamp", "Address", "Grandtotal"]
                csv_writer.writerow(header)
                for order_data in new_orders:
                    csv_writer.writerow([order_data["receipt_id"], order_data["item_name"],
                                         order_data["quantity"], order_data["price"], order_data["create_timestamp"],
                                         order_data["address"], order_data["grandtotal"]])

            print("New Orders - CSV file saved successfully!")

        return new_orders

    except json.JSONDecodeError as e:
        print(f"New Orders - Error decoding JSON: {e}")
        print("New Orders - Raw response:", response_content)
        return []

def timestamp_to_string(timestamp):
    dt_object = datetime.datetime.fromtimestamp(timestamp)
    return dt_object.strftime("%Y-%m-%d %H:%M:%S")

def create_receipts():
    try:
        subprocess.run(["python", "solo.py"])
        success_message = "All receipts for new orders successfully created."
        return redirect(url_for('index', success_message=success_message))
    except Exception as e:
        return redirect(url_for('index', error_message=f"Error creating receipts: {e}"))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username == USERNAME and password == PASSWORD:
            session['logged_in'] = True
            return redirect(url_for('index'))
        else:
            return render_template('login.html', error_message="Invalid username or password.")
    else:
        return render_template('login.html')

# Route for handling logout
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

@app.route('/')
def index():
    try:
        with open("tokens.txt", "r") as file:
            token_data = file.read()
            token = json.loads(token_data)
    except (FileNotFoundError, json.JSONDecodeError):
        return "Error loading tokens. Please run refresh_token.py."

    try:
        existing_orders = get_existing_orders(etsy_keystring, token, shop_id)
        new_orders = get_new_orders(etsy_keystring, token, shop_id)
    except Exception as e:
        return f"Error fetching orders: {e}"

    token_info = {
        "Token Type": token['token_type'],
        "Access Token": token['access_token'],
        "Expires In": time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(token['expires_in'])),
        "Refresh Token": token['refresh_token']
    }

    success_message = request.args.get('success_message')
    error_message = request.args.get('error_message')

    return render_template('index.html', token_info=token_info, new_orders=new_orders, new_orders_available=bool(new_orders), existing_orders=existing_orders, success_message=success_message, error_message=error_message)


@app.route('/download_existing_orders_json')
def download_existing_orders_json():
    json_path = "existing_orders_response.json"
    return send_file(json_path, as_attachment=True)

@app.route('/download_new_orders_json')
def download_new_orders_json():
    json_path = "new_orders_response.json"
    return send_file(json_path, as_attachment=True)

@app.route('/download_new_orders_csv')
def download_new_orders_csv():
    csv_path = "new_orders_response.csv"
    return send_file(csv_path, as_attachment=True)

@app.route('/create_receipts', methods=['GET'])  # Only allow GET requests for creating receipts
def create_receipts_route():
    return create_receipts()

@app.route('/fulfill_order/<receipt_id>', methods=['POST'])
def fulfill_order_route(receipt_id):
    tracking_code = request.form.get('tracking_id')
    if tracking_code:
        try:
            success = fulfill_order(receipt_id, tracking_code)
            if success:
                return redirect(url_for('index', success_message="Order fulfilled successfully."))
            else:
                return redirect(url_for('index', error_message="Failed to fulfill order."))
        except Exception as e:
            return redirect(url_for('index', error_message=f"Error fulfilling order: {e}"))
    else:
        return redirect(url_for('index', error_message="Tracking ID not provided."))

if __name__ == '__main__':
    app.run(debug=True)
