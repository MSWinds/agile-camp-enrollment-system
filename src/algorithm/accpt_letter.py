from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

def create_acceptance_letter(row):
    pdf_name = f"files/{row['CamperID']}/{row['CamperID']}_{row['Date']}_Accpt.pdf" 
    c = canvas.Canvas(pdf_name, pagesize=letter)

    c.setFont('Helvetica-Bold', 14)
    c.drawString(50, 750, 'Acceptance Letter')

    c.setFont('Helvetica', 12)
    c.drawString(50, 700, f"Dear {row['First Name']} {row['Last Name']},")

    c.drawString(50, 680, "We are delighted to inform you that you have been accepted to our summer camp program for")
    c.drawString(50, 665, f"{row['Session']}. Your acceptance is based on your impressive application and the")
    c.drawString(50, 650, "potential you have shown to make the most out of this experience.")

    c.drawString(50, 625, "We want to welcome you to our camp community, where you will have the opportunity to")
    c.drawString(50, 610, "make new friends, participate in exciting activities, and develop your skills in various")
    c.drawString(50, 595, "areas. We are confident that you will have a wonderful time and create lasting memories.")

    c.drawString(50, 570, f"Your camper ID is {row['CamperID']}.")

    c.drawString(50, 545, "Please find enclosed a copy of our camp rules and regulations, as well as a list of items")
    c.drawString(50, 530, "to bring with you. We kindly ask that you read these documents carefully and comply")
    c.drawString(50, 515, "with all rules and instructions.")

    c.drawString(50, 490, "We will be sending out additional information as we approach the camp start date, so")
    c.drawString(50, 475, "please be on the lookout for those messages.")

    c.drawString(50, 450, "Once again, congratulations on your acceptance to our camp program. We look forward")
    c.drawString(50, 435, "to seeing you soon.")

    c.drawString(50, 410, "Sincerely,")

    c.drawString(50, 385, "Camp Gila Breath Admission")
    c.drawString(50, 370, row['Date'])

    c.save()