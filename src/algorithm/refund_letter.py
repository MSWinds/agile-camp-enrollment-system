import os
import sys
from reportlab.lib.pagesizes import letter
from reportlab.lib.enums import TA_JUSTIFY
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

def create_refund_letter(row):

    sys.path.append(os.path.abspath('..'))
    dir_path = f"files/refund"
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)

    pdf_name = f"files/refund/{row['CamperID']}_Refund.pdf"
    doc = SimpleDocTemplate(pdf_name, pagesize=letter, rightMargin=72, leftMargin=72, topMargin=72, bottomMargin=18)
    
    content = []
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name='Justify', alignment=TA_JUSTIFY))

    # Refund letter content
    letter_content = f"""Refund Letter

Dear Camper,

We have received your request for a refund in the amount of {row['Refund Amount'].values[0]}, 
for the payment made on {row['Date of Original Payment'].values[0]} for the {row['Session'].values[0]} camp. 
We apologize for any inconvenience this may cause and will do our best to process your refund promptly.

Your refund request was made on {row['Date of Request'].values[0]} and we will process it as soon as possible. 
Please note that it may take a few days for the refund to be reflected in your account.
Sincerely,

Camp Gila Breath Admission

"""

    # Add letter content to the content list
    for line in letter_content.split('\n'):
        ptext = f'<font size="12">{line}</font>'
        content.append(Paragraph(ptext, styles["Normal"]))
        content.append(Spacer(1, 12))

    # Build and save the PDF
    doc.build(content)