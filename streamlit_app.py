import streamlit as st
import requests
import json

# Fixed sender address (from)
FROM_ADDRESS = {
    "countryCode": "US",
    "stateCode": "CA",
    "city": "Walnut",
    "addressLine1": "20632 Currier Rd.",
    "addressLine2": "",
    "zipCode": "91789"
}

# API endpoints and keys (replace with actual values)
API1_URL = "https://ezeeship.com/api/ezeeship-openapi/shipment/estimateRate"
API1_KEY = st.secrets.get("API1_KEY", "")  # Use Streamlit secrets for security, or input below

# For API2, add similar: API2_URL = "...", API2_KEY = "..."
# Assume API2 has similar structure; adjust the function accordingly when details are provided

def estimate_rate_api1(to_address, carrier_code, service_code, parcels, api_key):
    payload = {
        "from": FROM_ADDRESS,
        "to": to_address,
        "carrierCode": carrier_code,
        "serviceCode": service_code,
        "isTest": False,
        "parcels": parcels
    }
    
    headers = {
        "Authorization": api_key,
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.post(API1_URL, headers=headers, data=json.dumps(payload))
        response.raise_for_status()
        result = response.json()
        if result.get("result") == "OK" and result.get("data", {}).get("isSuccess"):
            return result["data"]
        else:
            return {"error": result.get("message") or "Unknown error"}
    except Exception as e:
        return {"error": str(e)}

# For API2, define a similar function: def estimate_rate_api2(...): ...

# Streamlit app
st.title("US Shipping Rate Estimator")

# API Key input (for security, better to use secrets.toml, but fallback to input)
if not API1_KEY:
    api1_key = st.text_input("Enter API1 Key:", type="password")
else:
    api1_key = API1_KEY

# For API2 key, add similar

# Recipient address input
st.header("Recipient Address")
to_country = "US"  # Fixed to US
to_state = st.text_input("State Code (e.g., CA):")
to_city = st.text_input("City:")
to_address1 = st.text_input("Address Line 1:")
to_address2 = st.text_input("Address Line 2 (optional):")
to_zip = st.text_input("Zip Code:")

to_address = {
    "countryCode": to_country,
    "stateCode": to_state,
    "city": to_city,
    "addressLine1": to_address1,
    "addressLine2": to_address2,
    "zipCode": to_zip,
    "isResidential": true
}

# Carrier and Service (example: fedex, fedex_2_day; make dropdowns if multiple options)
carrier_code = st.text_input("Carrier Code (e.g., fedex):", value="fedex")
service_code = st.text_input("Service Code (e.g., fedex_2_day):", value="fedex_home_delivery")

# Parcels input (support multiple boxes)
st.header("Parcels")
num_parcels = st.number_input("Number of Parcels:", min_value=1, value=1)

parcels = []
for i in range(num_parcels):
    st.subheader(f"Parcel {i+1}")
    length = st.text_input(f"Length (in):", key=f"len_{i}", value="5")
    width = st.text_input(f"Width (in):", key=f"wid_{i}", value="5")
    height = st.text_input(f"Height (in):", key=f"hei_{i}", value="5")
    weight = st.text_input(f"Weight (lb):", key=f"wei_{i}", value="4")
    
    # Extra fields (optional, based on example)
    insurance = st.number_input(f"Insurance Amount:", key=f"ins_{i}", value=0)
    is_cod = st.checkbox(f"Is COD?", key=f"cod_{i}", value=False)
    cod_amount = st.number_input(f"COD Amount:", key=f"cod_amt_{i}", value=0) if is_cod else 0
    payment_method = st.text_input(f"Payment Method:", key=f"pay_{i}", value="any") if is_cod else ""
    dry_ice_weight = st.number_input(f"Dry Ice Weight:", key=f"dry_{i}", value=0)
    
    parcel = {
        "packageNum": i+1,
        "length": length,
        "width": width,
        "height": height,
        "distanceUnit": "in",
        "weight": weight,
        "massUnit": "lb",
        "packageCode": "your_package",  # Fixed as per example
        "extra": {
            "insurance": insurance,
            "isCod": is_cod,
            "codAmount": cod_amount,
            "paymentMethod": payment_method,
            "dryIceWeight": dry_ice_weight
        }
    }
    parcels.append(parcel)

# Button to calculate
if st.button("Estimate Rates"):
    if not all([to_state, to_city, to_address1, to_zip, api1_key]):
        st.error("Please fill in all required fields.")
    else:
        # Call API1
        result1 = estimate_rate_api1(to_address, carrier_code, service_code, parcels, api1_key)
        st.subheader("API1 Result")
        if "error" in result1:
            st.error(f"Error: {result1['error']}")
        else:
            st.write(f"Rate: ${result1['rate']}")
            st.write(f"Delivery Time: {result1['deliveryTime']}")
            st.write("Fee Details:")
            st.json(result1['feeDetail'])
        
        # For API2, add similar: result2 = estimate_rate_api2(...); st.subheader("API2 Result"); ...

# To run: streamlit run this_script.py
# For secrets: create .streamlit/secrets.toml with API1_KEY = "your_key"
