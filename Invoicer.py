import Excel2Invoice
import invoice
import styler
import webbrowser
import subprocess
import datetime
from os import path


class Invoicer():
    
    show_due_date = True

    def create_pdf(self):
        styled_pdf = styler.Styler(self.output_filename, self.new_invoice, show_due_date=self.show_due_date)
        styled_pdf.save_pdf()
    
    def show_created_file(self):
        subprocess.call(["open", "-R", self.output_filename])
    
    def send_email(self):
        webbrowser.open(f"mailto:?to={self.recipient_email}&subject={self.email_subject}&body={self.message}", new=1)


    def __init__(self):
        if path.exists("filepaths.txt"):
            with open("filepaths.txt") as file:
                lines = file.readlines()
                data_souce_index = lines.index('---- Data Source ----\n') + 1
                export_filepath_index = lines.index('---- Export Filepath ----\n') + 1
                current_year = datetime.datetime.strftime(datetime.datetime.now(), '%Y')
                self.source_data_path = lines[data_souce_index].rstrip('\n')
                export_string = lines[export_filepath_index].rstrip('\n')
                self.export_path = f'''{export_string}{current_year}/Invoices'''
        else:
            self.source_data_path = 'Data/Sandbox_Data.xlsx'
            self.export_path = 'Exported_Invoices'
        
        self.client = input('\n\n\n                Invoice Generator \n\n                Client >>  ')
        self.invoice_number = int(input('             Invoice # >>  '))
        self.show_date = input('   Show due date (Y/N) >>  ').upper()

        if self.show_date == 'N':
            self.show_due_date = False
        
        self.new_invoice = Excel2Invoice.Excel2Invoice(self.client, self.invoice_number, self.source_data_path).return_invoice()

        self.output_filename = f'''{self.export_path}/{self.new_invoice.cust_id}-{self.new_invoice.number:03d} Invoice.pdf'''

        self.recipient = self.new_invoice.cust_name.split()[0]
        self.recipient_email = self.new_invoice.cust_email
        self.email_subject = f'Invoice {self.new_invoice.cust_id}-{self.new_invoice.number:03d}'
        self.message = f'''Hi {self.recipient}!

        Thank you for the recent work! I've attached the invoice below for our most recent projects together.

        Please let me know if you have any questions or concerns and I'd be happy to address.

        Thank you!

        '''




# if path.exists("filepaths.txt"):
#     with open("filepaths.txt") as file:
#         lines = file.readlines()
#         data_souce_index = lines.index('---- Data Source ----\n') + 1
#         export_filepath_index = lines.index('---- Export Filepath ----\n') + 1
#         current_year = datetime.datetime.strftime(datetime.datetime.now(), '%Y')
#         source_data_path = lines[data_souce_index].rstrip('\n')
#         export_string = lines[export_filepath_index].rstrip('\n')
#         export_path = f'''{export_string}{current_year}/Invoices'''
# else:
#     source_data_path = 'Data/Sandbox_Data.xlsx'
#     export_path = 'Exported_Invoices'


# show_due_date = True

# client = input('\n\n\n                Invoice Generator \n\n                Client >>  ')
# invoice_number = int(input('             Invoice # >>  '))
# show_date = input('   Show due date (Y/N) >>  ').upper()

# if show_date == 'N':
#     show_due_date = False


# new_invoice = Excel2Invoice.Excel2Invoice("Escape Chandler", 1, source_data_path).return_invoice()
# new_invoice = Excel2Invoice.Excel2Invoice(client, invoice_number, source_data_path).return_invoice()


# # file_path = f'{export_path}{current_year}/Invoices'
# output_filename = f'''{export_path}/{new_invoice.cust_id}-{new_invoice.number:03d} Invoice.pdf'''



# recipient = new_invoice.cust_name.split()[0]
# recipient_email = new_invoice.cust_email
# email_subject = f'Invoice {new_invoice.cust_id}-{new_invoice.number:03d}'
# message = f'''Hi {recipient}!

# Thank you for the recent work! I've attached the invoice below for our most recent projects together.

# Please let me know if you have any questions or concerns and I'd be happy to address.

# Thank you!

# '''

# def create_pdf():
#     styled_pdf = styler.Styler(output_filename, new_invoice, show_due_date=show_due_date)
#     styled_pdf.save_pdf()



if __name__ == '__main__':
    # --- OLD VERSION ----
    # create_pdf() 
    # # webbrowser.open(f"mailto:?to={recipient_email}&subject={email_subject}&body={message}", new=1)

    # file_to_show = output_filename
    # subprocess.call(["open", "-R", file_to_show])

    # ---- end old version


    new_invoice = Invoicer()
    new_invoice.create_pdf()
    new_invoice.show_created_file()
    new_invoice.send_email()