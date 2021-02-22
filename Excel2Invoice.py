# import xlrd
import pandas as pd
import invoice
import datetime

class Excel2Invoice:
    
    COLUMNS = ['Style', 'Date', 'Inv #', 'Type', 'Material', 'Time', 'Hours', 'Mins', 'Q','Rate', 'Cost', 'Item', 'Details']
    file_path = ''
    client_name = ''
    cust_name = ''
    cust_email = ''
    cust_id = ''
    inv_num = 0
    excel_file = None
    all_dfs = None
    worksheet = None
    filtered_rows = None
    item_names = None
    grouped_items_sum = None

    items = []
    materials = []

    def create_items(self):        
        for item in self.item_names:
            name = item
            
            if self.grouped_items_sum['Style'][item] != 0:
                style = self.grouped_items_sum['Style'][item]
            else:
                style = ''
            
            # list of all elements in date column for a given item
            date_list = self.filtered_rows.loc[self.filtered_rows['Item'] == item]['Date'].unique()

            # narrows date_list down to just the datetime objects
            filtered_dates = [date for date in date_list if isinstance(date, datetime.datetime)]
            
            # checks to see if there are any dates present, then assigns the date values
            if len(filtered_dates) > 0:
                beg_date = datetime.datetime.strftime(min(filtered_dates), '%B %d, %Y')
                end_date = datetime.datetime.strftime(max(filtered_dates), '%B %d, %Y')

            else:
                beg_date = ''
                end_date = ''
            
            
            # Takes all of the rows, filters it down to just the item we're looping
            # Then it checks if any of the listed "Type" cells are "Fixed"
            # The same checking format is used below as well
            if 'Fixed' in self.filtered_rows.loc[self.filtered_rows['Item'] == item]['Type'].unique():

                # ----------- OLD VERSION --------------
                # unit_price = max(self.filtered_rows.loc[self.filtered_rows['Item'] == item]['Rate'].unique())
                quantity = self.filtered_rows.loc[self.filtered_rows['Item'] == item]['Q'].sum()
                # fixed_item = invoice.Fixed_Item(name, unit_price, quantity = quantity, beg_date = beg_date, end_date = end_date, style = style)
                # ----------- OLD VERSION --------------



                # check to see if item is a material or not
                if 'M' in self.filtered_rows.loc[self.filtered_rows['Item'] == item]['Material'].unique():
                    # gets the biggest unit price of a material item
                    # materials *should* have same unit prices, but this will get the biggest one if different ones are entered
                    unit_price = max(self.filtered_rows.loc[self.filtered_rows['Item'] == item]['Rate'].unique())
                    fixed_item = invoice.Fixed_Item(name, unit_price, quantity = quantity, beg_date = beg_date, end_date = end_date, style = style)
                    self.materials.append(fixed_item)

                else:
                    # we know it's fixed item labor
                    # create fixed item and append it to items
                    
                    # gets the sum of all of the unit prices for labor fixed prices
                    # different from materials since those unit prices aren't added together
                    unit_price = self.filtered_rows.loc[self.filtered_rows['Item'] == item]['Rate'].sum()
                    fixed_item = invoice.Fixed_Item(name, unit_price, quantity = quantity, beg_date = beg_date, end_date = end_date, style = style)
                    self.items.append(fixed_item)
                    pass

            else:
                # We know item is hourly labor (hourly materials don't exist)
                hourly_rate = self.filtered_rows.loc[self.filtered_rows['Item'] == item]['Rate'].mean()
                hours = self.filtered_rows.loc[self.filtered_rows['Item'] == item]['Time'].sum()

                hourly_item = invoice.Hourly_Item(name, hourly_rate, hours, beg_date = beg_date, end_date = end_date, style = style)
                self.items.append(hourly_item)

            # if 'M' in self.filtered_rows.loc[self.filtered_rows['Item'] == item]['Material'].unique():
            #     print(f'{item} is a material')
            #     # append item to materials
            # else:
            #     print(f'{item} is labor')
                
            #     # you either have a fixed cost discount
                
            #     # append item to labor items


        
        # test_item = invoice.Fixed_Item('some item name', 50, 2, beg_date = 'January 1, 2020', style = '')
        # test_item = invoice.Hourly_Item('some hourly item', 50.00, 4.25, beg_date = 'February 1, 2020', style = '')

    def return_invoice(self, days = 14, date = ''):
        new_invoice = invoice.Invoice(self.cust_id, self.inv_num, days = days, date = date, cust_name=self.cust_name, cust_email=self.cust_email)
        new_invoice.add_items(*self.items)
        new_invoice.add_materials(*self.materials)
        return new_invoice



    def __init__(self, client, inv_num, file):
        # pd.set_option("xlsx", "openpyxl")
        self.file_path = file
        self.client_name = client
        self.inv_num = inv_num

        self.all_dfs = pd.read_excel(self.file_path, sheet_name=None, engine = "openpyxl", usecols = "A:M", header=None)
        self.worksheet = self.all_dfs[self.client_name]
        self.worksheet.columns = self.COLUMNS
        self.filtered_rows = self.worksheet.loc[self.worksheet['Inv #'] == self.inv_num]

        self.item_names = self.filtered_rows['Item'].unique()
        self.grouped_items_sum = self.filtered_rows.groupby(['Item']).sum()

        self.cust_id = self.worksheet.iloc[0, 2]
        self.cust_name = self.worksheet.iloc[0, 5]
        self.cust_email = self.worksheet.iloc[0, 9]

        self.create_items()







if __name__ == '__main__':
    # records = Excel2Invoice('Escape Chandler', 1, '/Users/Kenan/OneDrive/Taxes/Client Hours.xlsx')
    records = Excel2Invoice('Escape Chandler', 1, 'Client Hours.xlsx')

    records.return_invoice()
    # print(records.return_invoice())
    # print(records.ws_two.iloc[0])




    # print(records.worksheet.loc[records.worksheet['Inv #'] == 2])

    # for index, row in records.filtered_rows.iterrows():
    #     print(row['Item'])

    # print(records.filtered_rows)
    # print(records.filtered_rows.groupby('Item')['Inv #'].sum())

    # pd.DataFrame.groupby()




# item name
# style
# beg date
# end date

# Check if Fixed
    # get unit price
    # 
    # check if it's material
        # we know it's a fixed material
        # get quantity

        # create fixed item and append to materials
        # mat_one = invoice.Fixed_Item("Voiceover", 50, quantity = 3, style = '')


    # else it's not a material
        # we know it's a fixed item labor
        # create fixed item and append to items
        # item_one = invoice.Fixed_Item("this is an item name", 450, quantity = 1, beg_date = "December 14, 2020", end_date = '', style = '')


# Else it's hourly item

    # rate
    # number hours
    # create hourly item and append to items

    