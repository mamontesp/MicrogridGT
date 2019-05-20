from __future__ import print_function
import csv
import sys
import numpy as np
from datetime import datetime

def openFile(file, enable_grid):
	t  = []
	pv = []
	wt = []
	ld = []
	bt = []
	de = []
	teg = []
	
	csv_file = open(file,'rb')
	csv_reader = csv.reader(csv_file)
	line_count = 0

	for row in csv_reader:
		if line_count == 0:	
			if(enable_grid == True):	
				print ('Columns name are {}, {}, {}, {}, {}, {}, {}'.format(row[0], row[1], row[2], row[3], row[4], row[5], row[6]))
			else:
				print ('Columns name are {}, {}, {}, {}, {}, {}'.format(row[0], row[1], row[2], row[3], row[4], row[5]))
		else:
			date = row[0]
			dateformat = '%H:%M'
			t.append(datetime.strptime(date,'%H:%M'))
			pv.append(float(row[1]))
			wt.append(float(row[2]))
			ld.append(float(row[3]))
			bt.append(float(row[4]))
			de.append(float(row[5]))
			if(enable_grid == True):
				teg.append(float(row[6]))
			else:
				teg.append(float(0))
		line_count += 1
	print('Processed %d lines.', line_count)
	return t, pv, wt, ld, bt, de, teg



    