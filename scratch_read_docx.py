import zipfile
import xml.etree.ElementTree as ET
import os

docx_path = r"d:\zaalima\project-1-zaalima-developement-main\project-1-zaalima-developement-main\Customer Churn Prediction.docx"
output_path = r"d:\zaalima\project-1-zaalima-developement-main\project-1-zaalima-developement-main\Customer_Churn_Prediction.txt"

def docx_to_text(path):
    if not os.path.exists(path):
        print(f"File not found: {path}")
        return
    
    with zipfile.ZipFile(path) as z:
        xml_content = z.read('word/document.xml')
        root = ET.fromstring(xml_content)
        
        # namespaces
        ns = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
        
        paragraphs = []
        for paragraph in root.iter('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}p'):
            texts = [node.text for node in paragraph.iter('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}t') if node.text]
            if texts:
                paragraphs.append("".join(texts))
            else:
                paragraphs.append("")
                
        return "\n".join(paragraphs)

text = docx_to_text(docx_path)
if text:
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(text)
    print(f"Successfully wrote DOCX text to {output_path}")
