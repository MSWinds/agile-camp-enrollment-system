from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

def create_rejection_letter(row, rejection_result):
    pdf_name = f"files/rejection/{row['First Name']}_{row['Last Name']}_{row['Session']}_Reject.pdf"
    c = canvas.Canvas(pdf_name, pagesize=letter)

    c.setFont('Helvetica-Bold', 14)
    c.drawString(50, 750, 'Rejection Letter')

    c.setFont('Helvetica', 12)
    c.drawString(50, 700, f"Dear {row['First Name']} {row['Last Name']},")
    c.drawString(50, 680, f"We regret to inform you that your application for {row['Session']} of Camp Gila Breath has been rejected.")
    c.drawString(50, 660, "We understand that this news may be disappointing for you, but please know that we had a large number of applications and had to make difficult decisions.")
    c.drawString(50, 640, "Our selection process is highly competitive, and unfortunately, we are not able to offer you a spot at this time.")
    c.drawString(50, 620, "However, we wish you the best of luck in all your future endeavors.")
    c.drawString(50, 600, "Please note that the fees you paid will be refunded to you.")
    c.drawString(50, 580, "Thank you for your interest in Camp Gila Breath, and we hope that you will consider applying again in the future.")
    c.drawString(50, 560, f"Rejection reason: {rejection_result}")
    c.drawString(50, 540, "Sincerely,")
    c.drawString(50, 520, "Camp Gila Breath Admission")

    c.save()

