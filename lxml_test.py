from lxml import etree
from lxml.cssselect import CSSSelector
import os
import os.path as op
from time import process_time

start = process_time()
count_sig = 0
sel = CSSSelector('[gedi_type="DLSignature"]')

for root, folders, files in os.walk("datasets/train_xml"):
    for file in files:
        tree = etree.parse(op.join(root, file))
        xml_root = tree.getroot()
        if sel(xml_root):
            count_sig += 1

end = process_time()
print(f"Found {count_sig} XML files with a signature in {end - start:.2f}s")

