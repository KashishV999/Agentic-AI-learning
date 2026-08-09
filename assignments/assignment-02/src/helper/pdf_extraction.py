import requests

# https://github.com/jina-ai/reader/blob/main/cookbooks.md#pdf-ms-office-and-raw-html-uploads
def pdf_extraction(file_path: str) -> str:
    url = "https://r.jina.ai/"
    with open(file_path, "rb") as f:
        files = {"file": f}
        response = requests.post(url, files=files)
        
    # 4. return the text
    if response.status_code == 200:
        return response.text
    else:
        return "Unable to parse the pdf"


# def main():
#     pdf_path = "Job-1.pdf"  # PDF in the same directory

#     text = pdf_extraction_tool(pdf_path)

#     print(text)

#     # # Optional: Save to a Markdown file
#     # with open("doc.md", "w", encoding="utf-8") as f:
#     #     f.write(text)

#     print("Saved extracted text to doc.md")


# if __name__ == "__main__":
#     main()