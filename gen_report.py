# Created by He at 06.01.2021

# Feature: generation of the analytics report

# Scenario: gets data from the eval_data outputs and generates a .pdf

#---------------------------------------------------------

from fpdf import FPDF
from datetime import datetime

def create_title(day, stock, pdf):
  # Unicode is not yet supported in the py3k version; use windows-1252 standard font
  pdf.set_font('Arial', '', 24)
  pdf.ln(20)
  pdf.write(5, f"Stock Sentiment Analysis")
  pdf.ln(10)
  pdf.set_font('Arial', '', 16)
  pdf.write(4, f'{stock}')
  pdf.set_font('Arial', '', 12)
  pdf.ln(10)
  pdf.write(4, f'{day}')
  pdf.ln(10)


def create_analytics_report(day, stock, filename, WIDTH=210, HEIGHT=297):
    pdf = FPDF()  # A4 (210 by 297 mm)

    ''' First Page '''
    pdf.add_page()
    pdf.image("./resources/THdata.png", 0, 0, WIDTH)
    create_title(day, stock, pdf)

    pdf.image("./tmp/fig_closeprice.png", 5, 50, WIDTH - 10)
    pdf.image("./tmp/fig_vaderscores.png", 5, 180, WIDTH - 10)

    ''' Second Page '''
    pdf.add_page()
    pdf.image("./tmp/fig_countofnewsperday.png", 5, 40, WIDTH - 10)


    pdf.output(filename, 'F')
    print('Report generation successful!')

if __name__ == '__main__':
    today = datetime.today()
    STOCK = 'NVIDIA'
    create_analytics_report(today, STOCK, 'report_{}.pdf'.format(STOCK))