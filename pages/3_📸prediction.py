import streamlit as st
import requests
import os
import pandas as pd
from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from msrest.authentication import CognitiveServicesCredentials
from PIL import Image, ImageDraw 
from PIL import Image 
from io import BytesIO
from azure.ai.formrecognizer import DocumentAnalysisClient
from azure.core.credentials import AzureKeyCredential

#----endpoint----
def scoring(image_bytes) -> pd.DataFrame:
    subscription_key = "92868981c15942fa9e73ecc69a1cc88c"
    endpoint = "https://yenirsm.cognitiveservices.azure.com/"
    
    model_id = "coba2"
    #az_key = st.secrets["92868981c15942fa9e73ecc69a1cc88c"]
    document_analysis_client = DocumentAnalysisClient(
        endpoint=endpoint, credential=AzureKeyCredential(subscription_key)
        )
    analysis = document_analysis_client.begin_analyze_document(model_id, image_bytes)
    result = analysis.result()
    #computervision_client = ComputerVisionClient(endpoint, CognitiveServicesCredentials(subscription_key))

    for idx, document in enumerate(result.documents):
        print("--------Analyzing document #{}--------".format(idx + 1))
        print("Document has type {}".format(document.doc_type))
        print("Document has confidence {}".format(document.confidence))
        print("Document was analyzed by model with ID {}".format(result.model_id))
        for name, field in document.fields.items():
            field_value = field.value if field.value else field.content
            print("......found field of type '{}' with value '{}' and with confidence {}".format(field.value_type, field_value, field.confidence))

    # iterate over tables, lines, and selection marks on each page
    for page in result.pages:
        print("\nLines found on page {}".format(page.page_number))
        for line in page.lines:
            print("...Line '{}'".format(line.content.encode('utf-8')))
        for word in page.words:
            print(
                "...Word '{}' has a confidence of {}".format(
                    word.content.encode('utf-8'), word.confidence
                )
            )
        for selection_mark in page.selection_marks:
            print(
                "...Selection mark is '{}' and has a confidence of {}".format(
                    selection_mark.state, selection_mark.confidence
                )
            )

    for i, table in enumerate(result.tables):
        print("\nTable {} can be found on page:".format(i + 1))
        for region in table.bounding_regions:
            print("...{}".format(i + 1, region.page_number))
            
        for cell in table.cells:
            print(
                "...Cell[{}][{}] has content '{}'".format(
                    cell.row_index, cell.column_index, cell.content.encode('utf-8')
                )
            )
    print("-----------------------------------")

#----title----
st.title("Prediction Nutrition of a Food😭")
st.write(
    "This app uses Azure's Computer Vision service to analyze an image and provide information from image"
)

#----image upload----
uploaded_image = st.file_uploader(label = "Upload your image here", type=['png','jpg','jpeg'])
url = st.text_input("Or enter Image URL: ")

if uploaded_image is not None:
    input_image = uploaded_image.getvalue() #read image
    st.image(input_image, caption="Uploaded Image.", use_column_width=True)
    st.write("")
    st.write("AI at work, sabar ya!")
    analysis = scoring(input_image)

elif url:
    try:
        response = requests.get(url)
        response.raise_for_status()
        
        content_type = response.headers.get('Content-Type', '')
        if 'image' in content_type:
            input_image = Image.open(BytesIO(response.content))
            st.image(input_image, caption='Image from URL.', use_column_width=True)
            st.write("")
            st.write("AI at work, sabar ya!")
            analysis = scoring(input_image)
        else:
            st.error("The URL does not point to a valid image. Content-Type received was " + content_type)
            
    except requests.RequestException as e:
        st.error(f"Failed to fetch image due to request exception: {str(e)}")
        
    except requests.HTTPError as e:
        st.error(f"HTTP Error occurred: {str(e)}")
        
    except Exception as e:
        st.error(f"An unexpected error occurred: {str(e)}")

st.caption("Made by @Team4 Talenta AI")