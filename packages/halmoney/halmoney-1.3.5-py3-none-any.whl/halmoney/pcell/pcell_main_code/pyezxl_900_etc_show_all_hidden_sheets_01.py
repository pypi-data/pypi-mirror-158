# -*- coding: utf-8 -*-
from halmoney import pcell

excel = pcell.pcell()
sheet_names = excel.read_sheet_name()

# 모든 숨겨진 시트를 전부 보여주는것
for sheet_name in sheet_names:
	excel.set_sheet_hide(sheet_name, 1)