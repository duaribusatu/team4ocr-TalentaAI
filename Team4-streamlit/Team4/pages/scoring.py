import streamlit as st
import pandas as pd
from io import StringIO

from azure.core.credentials import AzureKeyCredential
from azure.ai.formrecognizer import DocumentAnalysisClient

from scripts.auth import azure_ad_auth

def scoring(image_bytes) -> pd.DataFrame:
    endpoint = "https://yenirsm.cognitiveservices.azure.com/"
    key = "92868981c15942fa9e73ecc69a1cc88c"

    model_id = "coba2"
    # formUrl = "https://www.static-src.com/wcsstore/Indraprastha/images/catalog/full//catalog-image/91/MTA-130026491/oreo_1_pcs_-_biskuit_oreo_original_creme_38gr_vanilla-chocolate-_strawberry_full03_h16vnypy.jpg"

    document_analysis_client = DocumentAnalysisClient(
        endpoint=endpoint, credential=AzureKeyCredential(key)
    )

    # Make sure your document's type is included in the list of document types the custom model can analyze
    # poller = document_analysis_client.begin_analyze_document_from_url(model_id, formUrl)
    poller = document_analysis_client.begin_analyze_document(model_id, image_bytes)
    result = poller.result()

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


email, username, full_name = azure_ad_auth('home', False)
if email is None:
    st.stop()

uploaded_file = st.file_uploader("Choose a file")
if uploaded_file:
    bytes_data = uploaded_file.getvalue()
    st.image(bytes_data)


submit = st.button('Submit', type='primary', disabled=uploaded_file is None)
if submit:
    # Call OCR API
    df = scoring(bytes_data)

    # Upload to SQL Database

    # Show Output
    