# -*- coding: utf-8 -*-
from halmoney import pcell

excel = pcell.pcell()

sheet_name = excel.read_activesheet_name()
[x1, y1, x2, y2] = excel.read_select_address()
color = excel.color()
all_data=excel.read_range_value("", [x1, y1, x2, y2])

#읽어온 값중에서 열별로 최소값구한후 색칠 하기
if not(x1==x2 and y1==y2) :
	for line_no in range(len(all_data)):
		line_data = all_data[line_no]
		filteredList = list(filter(lambda x: type(x) == type(1) or type(x) == type(1.0), line_data))
		if filteredList == []:
			pass
		else:
			max_value = min(filteredList)
			x_location = x1 + line_no
			for no in range(len(line_data)):
				y_location = y1 + no
				if (line_data[no]) == max_value:
					excel.set_cell_color(sheet_name, [x_location, y_location], color["pink_p"])
else:
	print("Please re-check selection area")