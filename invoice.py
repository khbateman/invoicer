import datetime
import math

class Item:
    beg_date = ""
    end_date = ""
    item = ""
    description = ""
    discount = 0
    cost = 0
    style = ''
    show_dollar = '$'

    def __init__(self, item, cost = 0, description = "", discount = 0, style = '', beg_date = '', end_date = ''):
        self.item = item
        self.cost = cost
        self.description = description
        
        if end_date == '':
            self.end_date = None
        else:
            self.end_date = datetime.datetime.strptime(end_date, '%B %d, %Y')
        
        if beg_date == '':
            self.beg_date = None
        else:
            self.beg_date = datetime.datetime.strptime(beg_date, '%B %d, %Y')


        self.discount = discount
        self.style = style
    
    def __str__(self):
        return f'Date - {self.date}\nItem - {self.item}\nDescription - {self.description}\nDiscount - ${self.discount}\nCost - ${self.cost}\nStyle - {self.style}'


class Fixed_Item(Item):
    # Items with a fixed cost attached.
    # This can be used for both fixed-cost labor and fixed-cost materials.   
    cost = 0
    quantity = 1
    quantity_text = ''
    unit_price = 0
    unit_price_text = ''

    def __init__(self, item, unit_price, quantity = 1, description = "", beg_date = "", end_date = "", discount = 0, style = ''):
        super().__init__(item, description=description, beg_date=beg_date, end_date=end_date, discount=discount, style = style)
        self.unit_price = unit_price
        self.quantity = quantity

        if quantity < 1:
            self.cost = unit_price
            self.quantity_text = ''
            self.unit_price_text = ''
            self.show_dollar = ''
        else:
            self.cost = unit_price * quantity
            self.quantity_text = f'Q - {quantity}'
            self.unit_price_text = f'{unit_price:.2f}'
        

    def __str__(self):
        return f'Beg Date - {self.beg_date}\nEnd Date - {self.end_date}\nItem - {self.item}\nDescription - {self.description}\nDiscount - ${self.discount}\nCost - ${self.cost}'



class Hourly_Item(Item):
    # Items that calculate cost based on hourly rate 
    hours = 0
    rate = None
    
    def __init__(self, item, rate, hours, description = "", beg_date = "", end_date = "", discount = 0, style = ''):
        super().__init__(item, description=description, beg_date = beg_date, end_date = end_date, discount=discount, style = style)
        self.hours = hours
        self.rate = rate
        self.cost = hours*rate
    
    def __str__(self):
        return f'Beg Date - {self.beg_date}\nEnd Date - {self.end_date}\nItem - {self.item}\nDescription - {self.description}\nDiscount - ${self.discount}\nRate - ${self.rate}\nHours - {self.hours} hours\nCost - ${self.cost}'


class Invoice:
    cust_id = None
    cust_name = ''
    cust_email = ''
    number = None
    DATE_FORMAT = "%B %d, %Y"
    date = datetime.datetime.strftime(datetime.datetime.today(), DATE_FORMAT)
    payment_time = None
    due_date_datetime = None
    due_date = None

    items = []
    materials = []

    total_materials = 0
    total_labor = 0
    total_paid = 0
    total_taxes = 0
    total = 0
    paypal_due = 0

    def add_items(self, *args):
        for item in args:
            self.items.append(item)

        self.update_totals()
    
    def add_materials(self, *args):
        for material in args:
            self.materials.append(material)
        
        self.update_totals()
    
    def calc_paypal(self):
        self.paypal_due = math.ceil((self.total+0.3) / 0.971)
    
    def update_totals(self):
        def sum_cost(some_list):
            cost = 0
            for item in some_list:
                cost += item.cost
                # print(item.cost)
            return cost
        
        self.total_materials = sum_cost(self.materials)
        self.total_labor = sum_cost(self.items)
        self.total = sum((self.total_materials, self.total_labor, self.total_paid, self.total_taxes))
        self.calc_paypal()
    
    def show_items(self):
        for item in self.items:
            print(item)
            print()
    
    def show_materials(self):
        for material in self.materials:
            print(material)
            print()
    
    def show_totals(self):
        self.update_totals()
        print(f'Materials - ${self.total_materials}')
        print(f'Labor - ${self.total_labor}')
        print(f'Paid - ${self.total_paid}')
        print(f'Taxes - ${self.total_taxes}')
        print(f'Total - ${self.total}')
        print(f'PayPal - ${self.paypal_due}')

    def show_invoice(self):
        print(f"\nInvoice {self.id}\n{self.date}\nDue on {self.due_date}")
        print(f'{len(self.items)} line items\n')
        self.show_items()
        print(f'{len(self.materials)} materials\n')      
        self.show_materials()
        print()
        self.show_totals()
        print()
    
    def __init__(self, cust_id, inv_number, days = 14, date = '', cust_name = '', cust_email = ''):
        self.cust_id = cust_id
        self.cust_name = cust_name
        self.cust_email = cust_email
        self.number = inv_number
        self.id = cust_id + "{:03d}".format(inv_number)
        self.payment_time = datetime.timedelta(days=days)

        if date != '':
            self.date = datetime.datetime.strftime(datetime.datetime.strptime(date, self.DATE_FORMAT), self.DATE_FORMAT)

        self.due_date_datetime = datetime.datetime.strptime(self.date, self.DATE_FORMAT) + self.payment_time
        self.due_date = datetime.datetime.strftime(self.due_date_datetime, self.DATE_FORMAT)


        self.update_totals()

    
    def __str__(self):
        return f'Invoice - {self.id}'
        



if __name__ == '__main__':
    item_one = Fixed_Item("this is an item name", 450, beg_date = "December 14, 2020")
    item_two = Hourly_Item("this is an item", 6.5, 50, beg_date = "January 5, 2020")
    item_three = Fixed_Item("this is an item", 45.50, beg_date = "May 4, 2020")

    mat_one = Fixed_Item("Voiceover", 50)
    mat_two = Fixed_Item("Music", 22.50)
    mat_three = Fixed_Item("Template", 150)


    test_invoice = Invoice("IH", 5, date='February 10, 2022', cust_name = '', cust_email = '')
    test_invoice.add_items(item_one, item_two, item_three)
    test_invoice.add_materials(mat_one, mat_two, mat_three)
    test_invoice.show_invoice()

    print(type(item_two) == Hourly_Item)

