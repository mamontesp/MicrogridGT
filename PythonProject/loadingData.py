from __future__ import print_function
import csv
import sys
import numpy as np
from datetime import datetime

def openFile(file):
	t  = []
	pv = []
	wt = []
	ld = []
	bt = []
	de = []
	
	csv_file = open(file,'rb')
	csv_reader = csv.reader(csv_file)
	line_count = 0
	for row in csv_reader:
		if line_count == 0:		
			print ('Columns name are {}, {}, {}, {}, {}, {}'.format(row[0], row[1], row[2], row[3], row[4], row[5]))
		else:
			#t.append(pd.to_datetime(row[0]).strftime('%H:%M'))
			date = row[0]
			dateformat = '%H:%M'
			t.append(datetime.strptime(date,'%H:%M'))
			pv.append(float(row[1]))
			wt.append(float(row[2]))
			ld.append(4*float(row[3]))
			bt.append(float(row[4]))
			de.append(float(row[5]))
		line_count += 1
	print('Processed %d lines.', line_count)
	return t, pv, wt, ld, bt, de
    