import Excel2Invoice
import invoice
import styler
import webbrowser
import subprocess
import datetime
from os import path

# with open("filepaths.txt") as file:
#     lines = file.readlines()
#     data_souce_index = lines.index('---- Data Source ----\n') + 1
#     export_filepath_index = lines.index('---- Export Filepath ----\n') + 1
#     source_data_path = lines[data_souce_index]
#     export_path = lines[export_filepath_index]



if path.exists("filepaths.txt"):
    with open("filepaths.txt") as file:
        lines = file.readlines()
        data_souce_index = lines.index('---- Data Source ----\n') + 1
        export_filepath_index = lines.index('---- Export Filepath ----\n') + 1
        current_year = datetime.datetime.strftime(datetime.datetime.now(), '%Y')
        source_data_path = lines[data_souce_index].rstrip('\n')
        export_string = lines[export_filepath_index].rstrip('\n')
        export_path = f'''{export_string}{current_year}/Invoices'''
else:
    source_data_path = 'Data/Sandbox_Data.xlsx'
    export_path = 'Exported_Invoices'


show_due_date = True

client = input('\n\n\n                Invoice Generator \n\n                Client >>  ')
invoice_number = int(input('             Invoice # >>  '))
show_date = input('   Show due date (Y/N) >>  ').upper()

if show_date == 'N':
    show_due_date = False


# new_invoice = Excel2Invoice.Excel2Invoice("Escape Chandler", 1, source_data_path).return_invoice()
new_invoice = Excel2Invoice.Excel2Invoice(client, invoice_number, source_data_path).return_invoice()


# file_path = f'{export_path}{current_year}/Invoices'
output_filename = f'''{export_path}/{new_invoice.cust_id}-{new_invoice.number:03d} Invoice.pdf'''



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
    # webbrowser.open(f"mailto:?to={recipient_email}&subject={email_subject}&body={message}", new=1)

    file_to_show = output_filename
    subprocess.call(["open", "-R", file_to_show])
