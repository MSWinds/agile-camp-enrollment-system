from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

def create_acceptance_letter(row):
    pdf_name = f"files/{row['CamperID']}_{row['Date']}_Accpt.pdf"
    c = canvas.Canvas(pdf_name, pagesize=letter)

    c.setFont('Helvetica-Bold', 14)
    c.drawString(50, 750, 'Acceptance Letter')

    c.setFont('Helvetica', 12)
    c.drawString(50, 700, f"Camper ID: {row['CamperID']}")
    c.drawString(50, 680, f"Name: {row['First Name']} {row['Last Name']}")
    c.drawString(50, 660, f"Session: {row['Session']}")

    c.save()


def create_acceptance_letters(df):
    df_to_send = df[df['Mailing Status'] == 'neg']

    for _, row in df_to_send.iterrows():
        create_acceptance_letter(row)

    df.loc[df['Mailing Status'] == 'neg', 'Mailing Status'] = 'pos' # update mailing status
    df.to_csv('mailing_accpt.csv', index=False)