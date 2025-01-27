# streamlit for client
# https://endpoint-cancer.francecentral.inference.ml.azure.com/score
import requests
import json
import streamlit as st
from dotenv import load_dotenv
import os

load_dotenv()
API_KEY = os.getenv("API_KEY")

st.title("Breast Cancer Recurrence Prediction")

age = st.slider("Age", 20, 90)
menopause = st.selectbox("Menopause", 
                         ["lt40", "ge40", "premeno"])
tumor_size = st.slider("Tumor Size", 0, 54)
inv_nodes = st.slider("Inv Nodes", 0, 26)
node_caps = st.selectbox("Node Caps", 
                         ["yes", "no"])
breast = st.selectbox("Breast", 
                      ["left", "right"])
breast_quad = st.selectbox("Breast Quad", 
                           ["left_low", "left_up", "right_low", "right_up", "central"])
irradiat = st.selectbox("Irradiat", 
                        ["yes", "no"])
deg_malig = st.slider("Degree of Malignancy", 1, 3)

# submit the request using button
if st.button("Submit"):
    # treat the data
    age = age/10
    tumor_size = tumor_size/5
    inv_nodes = inv_nodes/3
    menopause = 1 if menopause == "lt40" else (2 if menopause == "ge40" else 3)
    node_caps = 1 if node_caps == "yes" else 0
    breast = 1 if breast == "left" else 0
    breast_quad_central = 1 if breast_quad == "central" else 0
    breast_quad_left_low = 1 if breast_quad == "left_low" else 0
    breast_quad_left_up = 1 if breast_quad == "left_up" else 0
    breast_quad_right_low = 1 if breast_quad == "right_low" else 0
    breast_quad_right_up = 1 if breast_quad == "right_up" else 0
    irradiat = 1 if irradiat == "yes" else 0

    data = {
        "input_data": {
            "columns": [
                "age",
                "menopause",
                "tumor-size", 
                "inv-nodes",
                "node-caps",
                "deg-malig", 
                "breast", 
                "irradiat",
                "breast-quad_central",
                "breast-quad_left_low",
                "breast-quad_left_up",
                "breast-quad_right_low",
                "breast-quad_right_up"
            ],
            "index": [1],
            "data": [
                [age, menopause, tumor_size, inv_nodes, node_caps, deg_malig, breast, irradiat, breast_quad_central, breast_quad_left_low, breast_quad_left_up, breast_quad_right_low, breast_quad_right_up]
            ]
        }
    }

    endpoint_url = "https://endpoint-cancer.francecentral.inference.ml.azure.com/score"

    # Set the headers, including the API key
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {API_KEY}"
    }

    # Make the POST request
    response = requests.post(endpoint_url, json=data, headers=headers, timeout=60)

    if response.status_code == 200:
        try:
            result = response.json()
            
            if result[0] == 1:
                st.write("Recurrence possible, schedule a follow-up")
            else:
                st.write("No need to schedule a follow-up")
            
        except requests.exceptions.JSONDecodeError:
            st.write("Error: Received invalid JSON response")
    else:
        st.write(f"Error: Received response with status code {response.status_code}")