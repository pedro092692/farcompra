line = '25510163750AFLAMAX 12,5MG 6SUP OFTALMI             MNN00000200000010154000000000000000000040000007591196006424'
cod = line[0:11]
des = line[11:51]
stock = int(line[54:60])
price = int(line[60:70]) / 10
discount = int(line[71:75]) / 100
final_price = round(price * (1 - discount), 2)
barcode = line[97:115]

print(len(line))
print(cod)
print(des)
print(stock)
print(round(final_price / 36.54, 2))
print(barcode)