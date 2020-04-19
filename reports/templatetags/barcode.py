import barcode
from barcode.writer import ImageWriter
from barcode import generate
import os


def barcode():
    EAN = barcode.get_barcode_class('ean8')
    ean = EAN(u'0000001', writer=ImageWriter())
    fullname = ean.save(os.path.join('media/barcodes/' + auto_id_barang()))
    return fullname