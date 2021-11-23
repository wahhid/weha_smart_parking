from escpos.printer import Usb
#from xmlescpos.printer import Usb


class ReceiptEntry:

     def print(self, vals):
        """ Seiko Epson Corp. Receipt Printer (EPSON TM-T88III) """
        try:
            p = Usb(0x0483, 0x5840, 0, 0x81, 0x03)
       
                
            #p = Usb(0x1504, 0x002a, 0, 0x81, 0x02)
            # with open("image.jpg", "rb") as image_file:
            #     data = base64.b64encode(image_file.read())

            # receipt = ''
            # receipt  += '<receipt>'        
            # # receipt  += '<img src="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABAAAAAQAQMAA..." />'
            # receipt  += '<h1 align="center">Mal Taman Anggrek</h1>'
            # receipt  += '<div align="center">Smart PARK</div>'
            # receipt  += '<div align="center">Jakarta Barat</div>'
            # receipt  += '<br/>'
            # receipt  += '<br/>'
            # receipt  += '<hr/>'
            # receipt  += '<div align="center">' + vals['name'] + '</div>'
            # receipt  += '<div align="center">' + vals['entry_datetime'] + '</div>'
            # receipt  += '<div align="center">' + vals['entry_booth_id'] + '</div>'
            # receipt  += '<div align="center">' + vals['entry_operator_id'] + '</div>'
            # receipt  += '<barcode encoding="EAN13">5400113509509</barcode>'
            # receipt  += '</receipt>'        
        
            # p.receipt(receipt)
            # # Print top logo
            p.set(align="center")
            # #logo_path = os.path.join(self.app_path, "ui/widget_product.ui")
            # #p.image("escpos-php.png", impl="bitImageColumn")
        

            # Name of shop
            p.set(align="center", width=2)
            p.text("WEHA Mart.\n")
            p.set(align="center")
            p.text("Pamulang No. 42.\n")
            p.text("\n")

            # Title of receipt
            p.set(align="center")
            p.text("SALES RECEIPT\n")

            # Items
            p.set(align="left")
            #p.text(item(name="", price="$"))
            p.set(text_type="B")
            p.barcode(vals['name'], 'CODE39')
            #p.barcode('1324354657687', 'EAN13', 64, 2, '', '')
            #p.qr(vals['name'])
            p.set(align="left")
            # for line in pos_order_lines:
            #     print(line)
            #     print(line.name)
            #     print(line.price_subtotal_incl)
            #     it = item(name=line.name[0:24], price=str(line.price_subtotal_incl))
            #     p.text(it)
            #     #it = item(name="", price=str(line.price_subtotal_incl))
            #     #p.text(it)

            # self.subtotal = item(name="Subtotal", price=str(pos_order.amount_total))
            # p.set(text_type="B")
            # p.text(self.subtotal)
            # p.text("\n")

            # Tax and total
            # self.tax = item(name="Tax", price=str(pos_order.amount_tax))
            # p.set()
            # p.text(self.tax)
            # p.set(width=2)
            # self.total = item(name="Total", price=str(pos_order.amount_total))
            # p.text(self.total)

            # Footer
            p.text("\n\n")
            p.set(align="center")
            p.text("Thank you for shopping at\nWEHA Mart.\n")
            p.text("For trading hours, please visit weha-id.com\n")
            p.text("\n\n")
            # p.text(self.date + "\n")
            p.text("\n\n\n\n")
            # Cut the paper
            #p.cut()
        except Exception  as err:
            print(str(err))