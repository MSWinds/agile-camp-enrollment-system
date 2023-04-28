import os
import sys
from reportlab.lib.pagesizes import letter
from reportlab.lib.enums import TA_JUSTIFY
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

def create_acceptance_letter(row):
    sys.path.append(os.path.abspath('..'))
    dir_path = f"files/{row['CamperID'].values[0]}"
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)
        
    pdf_name = f"files/{row['CamperID'].values[0]}/{row['CamperID'].values[0]}_{row['Date'].values[0]}_Accpt.pdf"
    
    doc = SimpleDocTemplate(pdf_name, pagesize=letter, rightMargin=72, leftMargin=72, topMargin=72, bottomMargin=18)
    
    content = []
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name='Justify', alignment=TA_JUSTIFY))

    # Acceptance letter content
    letter_content = f"""Acceptance Letter

Dear {row['First Name'].values[0]} {row['Last Name'].values[0]},

We are delighted to inform you that you have been accepted to our summer camp program for {row['Session'].values[0]}. Your acceptance is based on your impressive application and the potential you have shown to make the most out of this experience.

We want to welcome you to our camp community, where you will have the opportunity to make new friends, participate in exciting activities, and develop your skills in various areas. We are confident that you will have a wonderful time and create lasting memories.

Your camper ID is {row['CamperID'].values[0]}.

Please find enclosed a copy of our camp rules and regulations, as well as a list of items to bring with you. We kindly ask that you read these documents carefully and comply with all rules and instructions.

We will be sending out additional information as we approach the camp start date, so please be on the lookout for those messages.

Once again, congratulations on your acceptance to our camp program. We look forward to seeing you soon.

Sincerely,

Camp Gila Breath Admission
{row['Date'].values[0]}
"""

    # Add letter content to the content list
    for line in letter_content.split('\n'):
        ptext = f'<font size="12">{line}</font>'
        content.append(Paragraph(ptext, styles["Normal"]))
        content.append(Spacer(1, 12))

    # Build and save the PDF
    doc.build(content)
