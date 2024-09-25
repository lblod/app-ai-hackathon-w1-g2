import os
import numpy as np
import cv2
import pytesseract
from pdf2image import convert_from_path
import json


def ocr_tess_folder_to_json(folder_path):
    # List of dictionaries to hold the result
    ocr_results = []

    # Get a list of all PDF files in the folder
    pdf_files = [f for f in os.listdir(folder_path) if f.endswith('.pdf')]

    for pdf_file in pdf_files:
        pdf_path = os.path.join(folder_path, pdf_file)

        # Dictionary to store text per PDF
        pdf_data = {
            "pdf_name": pdf_file,
            "pages": []
        }

        # Process the PDF
        pages = convert_from_path(pdf_path, 500)

        for count, page in enumerate(pages):
            img_cv = np.array(page)
            img_gray = cv2.cvtColor(img_cv, cv2.COLOR_BGR2GRAY)
            _, thresh = cv2.threshold(img_gray, 150, 255, cv2.THRESH_BINARY)
            text = pytesseract.image_to_string(thresh)

            # Append the extracted text for this page to the pdf_data
            pdf_data["pages"].append({
                "page_number": count + 1,
                "text": text
            })

        # Append the pdf_data to the list of results
        ocr_results.append(pdf_data)

    # Output JSON file path
    output_json_path = os.path.join(folder_path, "ocr_output.json")

    # Write the results to a JSON file
    with open(output_json_path, 'w', encoding='utf-8') as json_file:
        json.dump(ocr_results, json_file, ensure_ascii=False, indent=4)

    print(f"OCR processing complete. Results saved to {output_json_path}")

# Example usage:
# folder_path = '/path/to/pdf/folder'
# ocr_tess_folder_to_json(folder_path)
