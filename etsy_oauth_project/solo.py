import json
import requests
import time

# Load tax rates for each country
tax_rates = {
    "AT": 20,
    "BE": 21,
    "BG": 20,
    "CY": 19,
    "CZ": 21,
    "DE": 19,
    "DK": 25,
    "EE": 20,
    "EL": 24,
    "ES": 21,
    "FI": 24,
    "FR": 20,
    "HR": 25,
    "HU": 27,
    "IE": 23,
    "IT": 22,
    "LT": 21,
    "LU": 17,
    "LV": 21,
    "MT": 18,
    "N": 21,
    "PL": 23,
    "PT": 23,
    "RO": 19,
    "SE": 25,
    "SI": 22,
    "SK": 20,
}

# Load data from the JSON file
with open('new_orders_response.json', 'r') as file:
    order_data = json.load(file)

# Extract relevant information for each receipt
for receipt in order_data['results']:
    # Extract relevant information for the current receipt
    token = '79eb04a7e610bcebb3fcfa0ffb3f78b0d'
    tip_usluge = 1
    prikazi_porez = 1
    tip_racuna = 4
    kupac_naziv = receipt['name']
    kupac_adresa = receipt['formatted_address']
    usluga = 1
    opis_usluge_1 = receipt['transactions'][0]['title']
    jed_mjera_1 = 1  # You may need to adjust this based on your data

    # Use the original format for the price and convert it to a string
    cijena_1 = str(receipt['transactions'][0]['price']['amount'] / receipt['transactions'][0]['price']['divisor'])

    # Replace the dot with a comma (if needed)
    cijena_1 = cijena_1.replace('.', ',')

    kolicina_1 = receipt['transactions'][0]['quantity']
    popust_1 = 0

    # Get the country code from the JSON data
    country_code = receipt.get('country_iso', 'N')

    # Get the tax rate based on the country code, default to 0 if not found
    porez_stopa_1 = tax_rates.get(country_code, 0)

    nacin_placanja = 1
    datum_racuna = receipt['create_timestamp']
    rok_placanja = datum_racuna
    datum_isporuke = datum_racuna
    jezik_racuna = 2
    valuta_racuna = 14
    status = 5

    # Prepare the data for the POST request
    data = {
        'token': token,
        'tip_usluge': tip_usluge,
        'prikazi_porez': prikazi_porez,
        'tip_racuna': tip_racuna,
        'kupac_naziv': kupac_naziv,
        'kupac_adresa': kupac_adresa,
        'usluga': usluga,
        'opis_usluge_1': opis_usluge_1,
        'jed_mjera_1': jed_mjera_1,
        'cijena_1': cijena_1,
        'kolicina_1': kolicina_1,
        'popust_1': popust_1,
        'porez_stopa_1': porez_stopa_1,
        'nacin_placanja': nacin_placanja,
        'datum_racuna': datum_racuna,
        'rok_placanja': rok_placanja,
        'datum_isporuke': datum_isporuke,
        'jezik_racuna': jezik_racuna,
        'valuta_racuna': valuta_racuna,
        'status': status,
    }

    # Make the POST request
    url = 'https://api.solo.com.hr/racun'
    response = requests.post(url, data=data)

    # Print the response for each receipt
    print(f"Receipt ID {receipt['receipt_id']} - Response: {response.text}")

    # Sleep for 11 seconds
    time.sleep(11)
