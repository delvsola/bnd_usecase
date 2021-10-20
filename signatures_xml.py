import xml.etree.ElementTree as et
import os
import os.path as op
from time import process_time

start = process_time()
count_sig = 0
xml_namespace = "{http://lamp.cfar.umd.edu/GEDI}"
if not op.isdir("datasets/labels/train"):
    os.makedirs("datasets/labels/train")

for root, folders, files in os.walk("datasets/train_xml"):
    for file in files:
        xml_root = et.parse(op.join(root, file)).getroot()
        signatures = []
        for DL in xml_root.findall(f'{xml_namespace}DL_DOCUMENT/{xml_namespace}DL_PAGE'):
            width = int(DL.attrib["width"])
            height = int(DL.attrib["height"])
            for value in DL.findall(f'{xml_namespace}DL_ZONE'):
                if value is None:
                    continue
                elif value.attrib["gedi_type"] == "DLSignature":
                    x = int(value.attrib["col"])
                    y = int(value.attrib["row"])
                    sig_width = int(value.attrib["width"])
                    sig_height = int(value.attrib["height"])
                    center_x = (x + (sig_width/2))/width
                    center_y = (y + (sig_height/2))/height
                    norm_width = sig_width/width
                    norm_height = sig_height/height
                    signatures.append((0, center_x, center_y, norm_width, norm_height))
                    count_sig += 1
        if signatures:
            fp = op.join("datasets/labels/train/", file.replace(".xml", ".txt"))
            with open(fp, "w") as f:
                lines = []
                for sign in signatures:
                    lines.append(" ".join([str(round(x, 6)) for x in sign]))
                f.write("\n".join(lines))


end = process_time()
print(f"Found {count_sig} signatures in {end - start:.2f}s")