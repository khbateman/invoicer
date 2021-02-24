import Excel2Invoice
import invoice
import styler
import webbrowser
import subprocess
import datetime


show_due_date = True

client = input('\n\n\n                Invoice Generator \n\n                Client >>  ')
invoice_number = int(input('             Invoice # >>  '))
show_date = input('   Show due date (Y/N) >>  ').upper()

if show_date == 'N':
    show_due_date = False


# new_invoice = Excel2Invoice.Excel2Invoice("Escape Chandler", 5, 'Old_Files_1For_Dev/Client Hours SANDBOX.xlsx').return_invoice()
# new_invoice = Excel2Invoice.Excel2Invoice(client, invoice_number, '/Users/Kenan/OneDrive/Taxes/Client Hours.xlsx').return_invoice()


current_year = datetime.datetime.strftime(datetime.datetime.now(), '%Y')
file_path = f'/Users/Kenan/OneDrive/Taxes/{current_year}/Invoices'
output_filename = f'''{file_path}/{new_invoice.cust_id}-{new_invoice.number:03d} Invoice.pdf'''



recipient = new_invoice.cust_name.split()[0]
recipient_email = new_invoice.cust_email
email_subject = f'Invoice {new_invoice.cust_id}-{new_invoice.number:03d}'
message = f'''Hi {recipient}!

Thank you for the recent work! I've attached the invoice below for our most recent projects together.

Please let me know if you have any questions or concerns and I'd be happy to address.

Thank you!

'''

def create_pdf():
    styled_pdf = styler.Styler(output_filename, new_invoice, show_due_date=show_due_date)
    styled_pdf.save_pdf()



if __name__ == '__main__':
    create_pdf() 
    webbrowser.open(f"mailto:?to={recipient_email}&subject={email_subject}&body={message}", new=1)

    file_to_show = output_filename
    subprocess.call(["open", "-R", file_to_show])
