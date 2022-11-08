# ราคาปกติ Normal price
norm_pri = input("Enter normal price : ")

norm_temp = norm_pri.replace(".","")
if norm_temp.isnumeric() == False:
    print("Normal price cannot be String")
    print()
    quit()

# ส่วนลด Discount
discount = input("Enter discount percent : ")

dis_temp = discount.replace(".","")
if dis_temp.isnumeric():
    if float(discount) >= 100:
        print("Discount percentage cannot be more than 100 %")
        print()
        quit()

else:
    print("Discount percentage cannot be String")
    print()
    quit()

# แปลงค่าเป็น Float
norm_pri = float(norm_pri)
discount = float(discount)

# ราคาสุดท้าย
dis_pri = (norm_pri / 100 * (100 - discount ) )
# ราคาที่ลด
dis_val = norm_pri - dis_pri

# ตัดเหลือ 2 ตำแหน่ง
dis_pri = round(dis_pri, 2)
dis_val = round(dis_val, 2)

print("Normal price : ", '{:,}'.format(norm_pri))
#print("Normal price : ", norm_pri)

print("discount : ", discount, "%")

print("discount value : ", '{:,}'.format(dis_val))
#print("discount value :", dis_val)

print("Final price : ", '{:,}'.format(dis_pri))
#print("Final price :", dis_pri)
print()