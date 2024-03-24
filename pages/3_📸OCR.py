import streamlit as st
import requests
import pandas as pd
import os
import dotenv
from dotenv import load_dotenv
from msrest.authentication import CognitiveServicesCredentials
from PIL import Image
from io import BytesIO
from azure.ai.formrecognizer import DocumentAnalysisClient
from azure.core.credentials import AzureKeyCredential
from scripts.auth import azure_ad_auth

# Load environment variables
ENV = dotenv.dotenv_values("key.env")

# Azure Cognitive Services credentials
subscription_key = ENV["AZURE_KEY"]
endpoint = ENV["ENDPOINT"]
model_id = ENV["MODEL"]
document_analysis_client = DocumentAnalysisClient(
    endpoint=endpoint, credential=AzureKeyCredential(subscription_key)
)

# Function to analyze image using Azure OCR
def analyze_image(image_bytes):
    analysis = document_analysis_client.begin_analyze_document(model_id, image_bytes)
    result = analysis.result()
    return result

# Function to display analysis result in a DataFrame
def display_analysis(analysis):
    table_data = []
    for i, table in enumerate(analysis.tables):
        num_rows = max(cell.row_index for cell in table.cells) + 1
        num_columns = max(cell.column_index for cell in table.cells) + 1

        table_rows = [["" for _ in range(num_columns)] for _ in range(num_rows)]

        for cell in table.cells:
            table_rows[cell.row_index][cell.column_index] = cell.content

        table_data.extend(table_rows)

    # Define column headers based on the number of columns
    columns = ["Nutrisi", "%AKG", "%DV", ...]  # Update with actual column names

    df = pd.DataFrame(table_data, columns=columns)
    return df

# Streamlit app
st.title("Analyze Nutrition of ur Food🍪")
st.write("This app uses Azure's Computer Vision service to analyze an image and provide information from the image")

# Image upload
email, username, full_name, uid = azure_ad_auth('home', True)
if email is None:
    st.stop()

uploaded_image = st.file_uploader(label="Upload your image here", type=['png', 'jpg', 'jpeg'])
url = st.text_input("Or enter Image URL: ")

if uploaded_image is not None:
    input_image = uploaded_image.read()  # read image
    st.image(input_image, caption="Uploaded Image.", use_column_width=True)
    st.write("")
    with st.spinner("AI sedang bekerja, sabar ya!"):
        analysis_result = analyze_image(input_image)
    df = display_analysis(analysis_result)
    st.write("Analysis Result:")
    st.dataframe(df)

elif url:
    try:
        response = requests.get(url)
        response.raise_for_status()

        content_type = response.headers.get('Content-Type', '')
        if 'image' in content_type:
            input_image = Image.open(BytesIO(response.content))
            st.image(input_image, caption='Image from URL.', use_column_width=True)
            with st.spinner("AI at work, sabar ya!"):
                analysis_result = analyze_image(response.content)
            df = display_analysis(analysis_result)
            st.write("Analysis Result:")
            st.dataframe(df)
        else:
            st.error("The URL does not point to a valid image. Content-Type received was " + content_type)

    except requests.RequestException as e:
        st.error(f"Failed to fetch image due to request exception: {str(e)}")

    except requests.HTTPError as e:
        st.error(f"HTTP Error occurred: {str(e)}")

    except Exception as e:
        st.error(f"An unexpected error occurred: {str(e)}")

st.caption("Made by @Team4 Talenta AI")
