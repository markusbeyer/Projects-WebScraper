import xlsxwriter

list1 = ["name1","name2","name3" ]
list2 = ["bla1","bla2","bla3"]
list3 = ["data1","data2","data3"]
zipped = zip(list1,list2,list3)

with xlsxwriter.Workbook("test.xlsx") as workbook:
    worksheet = workbook.add_worksheet()
    for row_num, data in enumerate(zipped):
        worksheet.write_row(row_num, 0, data)
