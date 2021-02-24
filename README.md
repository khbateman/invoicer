# Invoicer
## Running
After cloning the repo locally, navigate to the folder and run Invoicer.py

```
$  cd /Invoicer
$  python3 Invoicer.py
```

1. Input the client name (example file will work with 'ACME Inc')
2. Input the invoice number (example file will work with 1)
3. If you want to hide the due date, enter 'N'. You can also just hit ENTER to bypass this and default to showing the due date.
4. Invoice will be saved in ***/Exported_Invoices***


## Item Styles Examples
### Hourly Labor
| Style | Date | Inv # | Type | Mat | Time | HRS | MINS | Q   | Rate | Cost | Project | Details |
| ---   | ---  | ---   | ---  | --- | ---  | --- | ---  | --- | ---  | ---  | ---     | ---     |
|  | 12/7/1970 | 1 |  |  | 1.25 | 1 | 15 |  | $100 | $125.00 | Front-end Development | Updating the home page |
|  | 12/8/1970 | 1 |  |  | 3.50 | 3 | 30 |  | $100 | $350.00 | Front-end Development | Adding interactions |
|  | 12/9/1970 | 1 |  |  | 1.25 | 2 | 00 |  | $100 | $200.00 | Front-end Development | Revisions |
|  | 12/15/1970 | 1 |  |  | 0.75 | 0 | 45 |  | $100 | $75.00 | Front-end Development | Second-round revisions |

### Fixed Price Labor
| Style | Date | Inv # | Type | Mat | Time | HRS | MINS | Q   | Rate | Cost | Project | Details |
| ---   | ---  | ---   | ---  | --- | ---  | --- | ---  | --- | ---  | ---  | ---     | ---     |
|  | 12/7/1970 | 1 | Fixed |  |  |  |  | 1 | $100 | $125.00 | Front-end Development | Fixed price entry |
|  | 12/7/1970 | 1 |       |  | 3.50 | 3 | 30 |  | $0 | $0.00 | Front-end Development | Adding interactions |
|  | 12/8/1970 | 1 |       |  | 1.25 | 2 | 00 |  | $0 | $0.00 | Front-end Development | Revisions |

### Fixed Price Item With Styling
| Style | Date | Inv # | Type | Mat | Time | HRS | MINS | Q   | Rate | Cost | Project | Details |
| ---   | ---  | ---   | ---  | --- | ---  | --- | ---  | --- | ---  | ---  | ---     | ---     |
| Right, bold, blue |  | 1 | Fixed |  |  |  |  | -1 | -$100 | -$100.00 | Discount | - |

### Materials
| Style | Date | Inv # | Type | Mat | Time | HRS | MINS | Q   | Rate | Cost | Project | Details |
| ---   | ---  | ---   | ---  | --- | ---  | --- | ---  | --- | ---  | ---  | ---     | ---     |
|       |      | 1     | Fixed |  M |      |     |      | 2 | $50 | $100.00 | Templates | - |


## Calculated Columns
To maintain the formulas in each row, it is recommended to copy and paste an existing row and then change the values where needed. This will avoid formula breaking.

The following columns are calculated and require no user input - 
* Time
* Cost

## Style
To update the style of a line's main text, include any of these values in the **Style** column. If the style appears in any of the cells for a collapsed item, the style will display.

To combine styles, separate them with a comma

   **blue** - turns the text blue

   **right** - right aligns the text

   **center** - centers the text

   **bold** - changes the font to a bold-faced variant

***Example***
| Style |
| --- |
| blue, right, bold |

## Date
When the pdf is exported, it provides a summarized date view for each line item. It will be formatted as an abbreviated beginning and end date (ex - *Feb 12 - Jun 15*)

Please format the date as an Excel Date. Do not change it to plain text or remove the date-time attributes.

## Invoice Number
This is the invoice number the line item is associated with. It should be an integer.

## Type
This cell should either be
* ***blank*** - if the line item is hourly
* **Fixed** - if the line item is fixed-price

## Mat
This cell notes whether or not the line item is a **material**. If an item is listed as a material, it will appear in the lower section of the invoice ('Materials').

This cell should either be
* **M** - if the item is a material
* ***blank*** - not a material

## HRS / MINS
If the item has tracked time, you can list the exact hours and minutes in these cells. This will be used to calcualte the time column.

## Q
If needed, you can put the quantity of an item here.

This cell has a few special values it can use
* **positive integer** - typical values for fixed price items (note - don't repeat quantities or else unexpected values may be calculated)
* **negative integer** - this will remove the quantity value for that line item from the invoice. This is useful for fixed cost elements like discounts.

## Rate
* **Hourly** - rate for the labor
* **Fixed** - per-item cost for the item

**Note** - Make sure the rates match for collapsed line items else unexpected values may be calculated.
***Tip*** - For discounts, enter them in with a negative Rate.

## Project
This is the name that will appear on the invoice. The invoice groups items by this name, so make sure they are identical (else they will appear as separate line items).

## Details
This column does not get shown on the invoice and is used for internal purposes or personal notes about the item.

