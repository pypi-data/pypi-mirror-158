# -*- coding: utf-8 -*-
from halmoney import pcell

excel = pcell.pcell()

sheet_name = excel.read_activesheet_name()
[x1, y1, x2, y2] = excel.read_select_address()

# 선택한 영역의 y행을 하나씩 새로운 행을 추가하는 것이다
for y in range(y2, y1, -1):
	excel.insert_y_line(sheet_name, y)