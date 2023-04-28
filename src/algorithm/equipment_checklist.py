import os
import sys
from reportlab.lib.pagesizes import letter
from reportlab.lib.enums import TA_JUSTIFY
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

def create_equipment_checklist(row):
    sys.path.append(os.path.abspath('..'))
    dir_path = f"files/{row['CamperID'].values[0]}"
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)
        
    pdf_name = f"files/{row['CamperID'].values[0]}/{row['CamperID'].values[0]}_Equipment_Checklist.pdf"
    
    doc = SimpleDocTemplate(pdf_name, pagesize=letter, rightMargin=72, leftMargin=72, topMargin=72, bottomMargin=18)
    
    content = []
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name='Justify', alignment=TA_JUSTIFY))

    # Equipment Checklist content
    equipment_checklist_content = f"""EQUIPMENT CHECK LIST 

Dear {row['CamperID'].values[0]}

This equipment checklist is designed to ensure that all necessary equipment is available and in working order for the upcoming camp. The following items should be inspected and checked off prior to the start of the camp:

[ ] Tents (sufficient for all participants)
[ ] Sleeping bags (sufficient for all participants)
[ ] Sleeping pads (sufficient for all participants)
[ ] Camp stoves (sufficient for all groups)
[ ] Fuel canisters for stoves (sufficient for all groups)
[ ] Cooking pots and pans (sufficient for all groups)
[ ] Cooking utensils (sufficient for all groups)
[ ] Coolers and ice (sufficient for all groups)
[ ] Water filters and treatment (sufficient for all participants)
[ ] First aid kits (sufficient for all participants)
[ ] Headlamps/flashlights (sufficient for all participants)
[ ] Batteries (sufficient for all participants)
[ ] Map and compass (sufficient for all groups)
[ ] Whistles (sufficient for all participants)
[ ] Backpacks (sufficient for all participants)
[ ] Trekking poles (sufficient for all participants)
[ ] Hand sanitizer (sufficient for all participants)
[ ] Sunscreen (sufficient for all participants)
[ ] Insect repellent (sufficient for all participants)

Note: If any of the items on this checklist are not available, please check with the camp store. The camp store will be ready to sell things that are not available. 

Sincerely,
Camp Gila Breath Admission
"""

    # Add Equipment Checklist content to the content list
    for line in equipment_checklist_content.split('\n'):
        ptext = f'<font size="12">{line}</font>'
        content.append(Paragraph(ptext, styles["Normal"]))
        content.append(Spacer(1, 12))

    # Build and save the PDF
    doc.build(content)
