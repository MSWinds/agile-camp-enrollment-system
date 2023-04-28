import os
import sys
from reportlab.lib.pagesizes import letter
from reportlab.lib.enums import TA_JUSTIFY
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

def create_arrival_form(row):
    sys.path.append(os.path.abspath('..'))
    dir_path = f"files/{row['CamperID'].values[0]}"
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)
        
    pdf_name = f"files/{row['CamperID'].values[0]}/{row['CamperID'].values[0]}_Arrival_Form.pdf"
    
    doc = SimpleDocTemplate(pdf_name, pagesize=letter, rightMargin=72, leftMargin=72, topMargin=72, bottomMargin=18)
    
    content = []
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name='Justify', alignment=TA_JUSTIFY))

    # Arrival Form Guide content
    arrival_guide_content = f"""ARRIVAL FORM GUIDE

Dear {row['CamperID'].values[0]},

Please complete the Arrival Form below with any important information to help us ensure a safe and enjoyable experience for your child.

Medical Obligations:
Please list any medical conditions, allergies, or medications that your child will need while at camp. We want to ensure that our medical staff is aware of any health concerns and that your child receives the proper care.

Food Preferences:
Please indicate any food allergies, dietary restrictions, or special requests. We strive to provide a variety of healthy meal options for all campers, and we want to ensure that your child's dietary needs are met.

Emergency Contact Information:
Please provide us with the name and phone number of at least two emergency contacts. If we are unable to reach you, we want to ensure that we have another point of contact for your child.

Please complete and return this form at your earliest convenience. If you have any questions or concerns, please do not hesitate to contact us.

We look forward to welcoming you to Camp Gila Breath this summer!

Sincerely,

Camp Gila Breath Admission
"""

    # Add Arrival Form Guide content to the content list
    for line in arrival_guide_content.split('\n'):
        ptext = f'<font size="12">{line}</font>'
        content.append(Paragraph(ptext, styles["Normal"]))
        content.append(Spacer(1, 12))

    # Add a page break
    content.append(PageBreak())

    # Arrival Form content
    arrival_form_content = f"""ARRIVAL FORM:

Camper's Full Name: _________________________________________

Medical Obligations: 
______________________________________________________________________________
______________________________________________________________________________
______________________________________________________________________________

Food Preferences:
______________________________________________________________________________
______________________________________________________________________________
______________________________________________________________________________

Emergency Contact Information:
Primary Contact Name: __________________________ Phone Number: __________________
Secondary Contact Name: ______________________ Phone Number: __________________ 

Date Form Completed: ________________________
"""

    # Add Arrival Form content to the content list
    for line in arrival_form_content.split('\n'):
        ptext = f'<font size="12">{line}</font>'
        content.append(Paragraph(ptext, styles["Normal"]))
        content.append(Spacer(1, 12))

    # Build and save the PDF
    doc.build(content)
