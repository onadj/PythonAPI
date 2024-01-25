import json
import requests
import time
from decimal import Decimal, ROUND_HALF_UP

# Load data from the JSON file
with open('new_orders_response.json', 'r') as file:
    order_data = json.load(file)

# Solo API token
token = '79eb04a7e610bcebb3fcfa0ffb3f78b0d'

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

# Country names mapping
country_names = {
    "AT": "Austrija",
    "BE": "Belgija",
    "BG": "Bugarska",
    "CY": "Cipar",
    "CZ": "Češka",
    "DE": "Njemačka",
    "DK": "Danska",
    "EE": "Estonija",
    "EL": "Grčka",
    "ES": "Španjolska",
    "FI": "Finska",
    "FR": "Francuska",
    "HR": "Hrvatska",
    "HU": "Mađarska",
    "IE": "Irska",
    "IT": "Italija",
    "LT": "Litva",
    "LU": "Luksemburg",
    "LV": "Latvija",
    "MT": "Malta",
    "N": "Nizozemska",
    "PL": "Poljska",
    "PT": "Portugal",
    "RO": "Rumunjska",
    "SE": "Švedska",
    "SI": "Slovenija",
    "SK": "Slovačka",
}

# Extract relevant information for each receipt
for receipt in order_data['results']:
    # Extract relevant information for the current receipt
    country_code = receipt.get('country_iso', 'N')

    # Check if country_iso is in the tax_rates dictionary
    if country_code in tax_rates:
        prikazi_porez = 1
        napomene = None
    else:
        prikazi_porez = 0
        napomene = 'Oslobođeno PDV-a temeljem članka 45.'

    grandtotal_data = receipt['grandtotal']
    grandtotal = Decimal(grandtotal_data['amount']) / Decimal(grandtotal_data['divisor'])

    # Check if country_iso is in the country_names dictionary
    if country_code in country_names:
        country_name = country_names[country_code]
    else:
        country_name = country_code  # Use the country code if not found in country_names

    tip_usluge = 1
    tip_racuna = 4
    kupac_naziv = receipt['name']
    usluga = 1
    opis_usluge_1 = 'Usluga 3D Ispisa'

    # Calculate tax amount
    porez_stopa_1 = tax_rates.get(country_code, 0)
    tax_amount = grandtotal * Decimal(porez_stopa_1) / (Decimal(100) + Decimal(porez_stopa_1))

    # Calculate cijena_1 based on the grandtotal and tax_amount
    cijena_1 = grandtotal - tax_amount

    # Format cijena_1 as a string with comma as decimal separator
    cijena_1_formatted = '{:.2f}'.format(cijena_1).replace('.', ',')

    kolicina_1 = receipt['transactions'][0]['quantity']
    popust_1 = 0
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
        'kupac_adresa': country_name,
        'usluga': usluga,
        'opis_usluge_1': opis_usluge_1,
        'jed_mjera_1': 1,
        'cijena_1': cijena_1_formatted,
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
        'napomene': napomene,
    }

    # Make the POST request
    url = 'https://api.solo.com.hr/racun'
    response = requests.post(url, data=data)

    # Print the response for each receipt
    print(f"Receipt ID {receipt['receipt_id']} - Response: {response.text}")

    # Sleep for 11 seconds
    time.sleep(11)
