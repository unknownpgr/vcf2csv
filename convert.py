import quopri
import csv

arr = []
with open("contact.vcf", "r") as f:
    contacts = f.read().split("BEGIN:VCARD")
    for contact in contacts:
        contact = contact.replace("END:VCARD", "")

        # Some hard-coded, dirty parsing. Anyway it works.
        contact = contact.replace("VERSION:2.1", "")
        contact = contact.replace("\n", "")
        contact = contact.replace(":", ";")
        contact = contact.replace(";;;;", ";")
        contact = contact.replace(";;;", ";")
        contact = contact.replace(";;", ";")
        contact = contact.replace("==", "=")
        contact = contact.replace("TEL", "")
        contact = contact.split(";")
        if len(contact) == 1:
            continue
        assert len(contact) % 2 == 0

        # Convert array to dictionary
        d = {}
        for i in range(0, len(contact), 2):
            d[contact[i]] = contact[i + 1]
        name = quopri.decodestring(d["ENCODING=QUOTED-PRINTABLE"]).decode("utf-8")
        phone = ""
        if "CELL" in d:
            phone = d["CELL"]
        elif "WORK" in d:
            phone = d["WORK"]
        elif "HOME" in d:
            phone = d["HOME"]
        else:
            print("Cannotr parse this contact :")
            print(d)
            continue
        arr.append([name, phone])

arr = sorted(arr, key=lambda x: x[0])

with open("out.csv", "w", newline="") as o:
    w = csv.writer(o)
    w.writerow(["Name", "Phone"])
    w.writerows(arr)
