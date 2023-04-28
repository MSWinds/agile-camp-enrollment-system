import os
import sys
from reportlab.lib.pagesizes import letter
from reportlab.lib.enums import TA_JUSTIFY
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

def create_rejection_letter(row, rejection_result):
    sys.path.append(os.path.abspath('..'))
    dir_path = f"files/rejection"
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)
    pdf_name = f"files/rejection/{row['First Name'].values[0]}_{row['Last Name'].values[0]}_{row['Session'].values[0]}_Reject.pdf"
    
    doc = SimpleDocTemplate(pdf_name, pagesize=letter, rightMargin=72, leftMargin=72, topMargin=72, bottomMargin=18)
    
    content = []
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name='Justify', alignment=TA_JUSTIFY))

    # Rejection letter content
    letter_content = f"""REJECTION LETTER

Dear {row['First Name'].values[0]} {row['Last Name'].values[0]},

We regret to inform you that your application for {row['Session'].values[0]} of Camp Gila Breath has been rejected. We understand that this news may be disappointing for you, but please know that we had a large number of applications and had to make difficult decisions.

Our selection process is highly competitive, and unfortunately, we are not able to offer you a spot at this time. However, we wish you the best of luck in all your future endeavors.

Please note that the fees you paid will be refunded to you.

Thank you for your interest in Camp Gila Breath, and we hope that you will consider applying again in the future.

Rejection reason: {rejection_result}

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




