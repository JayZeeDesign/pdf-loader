# from langchain.document_loaders import UnstructuredFileLoader

# loader = UnstructuredFileLoader("Example Payslip 1.pdf")

# docs = loader.load()

# print(docs)

from pytesseract import image_to_string
import pypdfium2 as pdfium
from io import BytesIO
import multiprocessing
import requests
from PIL import Image

def convert_pdf_to_images(file_path, scale=300/72):
    
    ## 1/ This is used to load local files instead of fetching from url

    pdf_file = pdfium.PdfDocument(file_path)

    page_indices = [i for i in range(len(pdf_file))]

    renderer = pdf_file.render(
        pdfium.PdfBitmap.to_pil,
        page_indices=page_indices,
        scale=scale,
    )

    final_images = []

    for i, image in zip(page_indices, renderer):

        image_byte_array = BytesIO()
        image.save(image_byte_array, format='jpeg', optimize=True)
        image_byte_array = image_byte_array.getvalue()
        final_images.append(dict({i: image_byte_array}))

    return final_images


    ## 2/ Fetch file from url

    # response = requests.get("https://userdata-1e3042.stack.tryrelevance.com/files/temp_public/089c8483-3bee-4b00-8b12-87d3c9900b8c.pdf")
    
    # # Check if the request was successful
    # if response.status_code == 200:
    #     with open("downloaded.pdf", "wb") as f:
    #         f.write(response.content)
    #         pdf_file = pdfium.PdfDocument("downloaded.pdf")            
    #         page_indices = [i for i in range(len(pdf_file))]
        
    #         renderer = pdf_file.render(
    #             pdfium.PdfBitmap.to_pil,
    #             page_indices=page_indices,
    #             scale=scale,
    #         )
        
    #         final_images = []
        
    #         for i, image in zip(page_indices, renderer):
        
    #             image_byte_array = BytesIO()
    #             image.save(image_byte_array, format='jpeg', optimize=True)
    #             image_byte_array = image_byte_array.getvalue()
    #             final_images.append(dict({i: image_byte_array}))
        
    #         return final_images
    # else:
    #     print(f"Failed to download PDF. Status code: {response.status_code}") 


# 2. Extract text from images via pytesseract


def extract_text_from_img(list_dict_final_images):

    image_list = [list(data.values())[0] for data in list_dict_final_images]
    image_content = []

    for index, image_bytes in enumerate(image_list):

        image = Image.open(BytesIO(image_bytes))
        raw_text = str(image_to_string(image))
        image_content.append(raw_text)

    return "\n".join(image_content)


def extract_content_from_url(url: str):
    images_list = convert_pdf_to_images(url)
    text_with_pytesseract = extract_text_from_img(images_list)

    return text_with_pytesseract


def main():
    doc = extract_content_from_url("Example Payslip 1.pdf")
    print(doc)


if __name__ == '__main__':
    multiprocessing.freeze_support()
    main()

