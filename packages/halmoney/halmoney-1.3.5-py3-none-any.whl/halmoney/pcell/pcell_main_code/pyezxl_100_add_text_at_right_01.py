# -*- coding: utf-8 -*-
from halmoney import pcell, youtil, scolor, pynal, anydb, jfinder, basic_data

basic_value = basic_data.basic_data()
excel = pcell.pcell()
color =scolor.scolor()
yt = youtil.youtil()
jf = jfinder.jfinder()
nal = pynal.pynal()
ab = anydb.anydb()

sheet_name = excel.read_activesheet_name()
[x1, y1, x2, y2] = excel.read_select_address()

input_text=excel.read_messagebox_value("Please input text")

for x in range(x1, x2+1):
	for y in range(y1, y2+1):
		cell_value = str(excel.read_cell_value(sheet_name,[x, y]))
		if cell_value == "None" :
			cell_value = ""
		excel.write_cell_value(sheet_name,[x, y],(str(cell_value)+str(input_text)))