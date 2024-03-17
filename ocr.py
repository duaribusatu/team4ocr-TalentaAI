reader = ocr.Reader(['en'],model_storage_directory='')
result = reader.readtext("")
for text in result:
    print(text[1])