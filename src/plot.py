
import csv
import pandas as pd
import numpy as np
import Gnuplot as gp


def parseFile(filename):

	f = open(filename)
	b = open('test.csv', 'w')
	a = csv.writer(b)
	i=0

	result =[]
	caption = []
	cap=False

	for line in f:
		
		if line[0]=="*":
			i=0
			#continue
			if not cap:	
				a.writerow(caption)
				cap = True
			a.writerow(result)
			result=[]
			caption=[]
			continue
		data = line.split(",")
		size = len(data)
		result.append(data[0].strip('\n'))
		caption.append(data[size-1].strip('\n'))
	b.close()

#parseFile('out')


def Plot(filename,x_value,y_values,outfile,log_x,log_y):

	open_file = pd.read_csv(filename)
	x = np.array(open_file[x_value])

	# instantiate gnuplot
	g = gp.Gnuplot()

	# initialize an array for plot data
	plot_data = []

	# create gnuplot data
	for y_value in y_values:
		y = np.array(open_file[y_value])
		y_label = y_value.replace("_"," ")
		plot_data.append(gp.Data(x,y,with_="lp",title=y_label))


	# set the labels
	x_label = x_value.replace("_"," ")

	#formatting options
	#g("set grid")
	#g("set style pt 4")
	g("set key left")
	g("set terminal pslatex")
	g("set output '"+outfile+".pdf'")
	#g("set format y '%sx10^{%S}'")
	g("set xlabel '"+x_label+"'")
	g("set format y '%1.2e'")
	if log_x:
		g("set logscale x")
	if log_x:
		g("set logscale y")




	#plot
	g.plot(plot_data[0],plot_data[1],plot_data[2],plot_data[3])
	g("set output '"+outfile+"_log.pdf'")
	g.plot(plot_data[0],plot_data[1],plot_data[2],plot_data[3])
	#g.plot(plot_data[0])

def PlotSimple(filename,x_value,y_values,outfile,log):

	open_file = pd.read_csv(filename)
	print open_file
	x = np.array(open_file[x_value])
	print x
	# instantiate gnuplot
	g = gp.Gnuplot()

	# initialize an array for plot data
	plot_data = []

	# create gnuplot data
	for y_value in y_values:
		y = np.array(open_file[y_value])
		y_label = y_value.replace("_"," ")
		plot_data.append(gp.Data(x,y,with_="lp",title=y_label))


	# set the labels
	x_label = x_value.replace("_"," ")

	#formatting options
	#g("set grid")
	#g("set style pt 4")
	g("set key left")
	g("set terminal svg")
	g("set output '"+outfile+".svg")
	#g("set format y '%sx10^{%S}'")
	g("set xlabel '"+x_label+"'")
	g("set format y '%1.2e'")
	if log:
		g("set logscale x 2c")




	#plot
	g.plot(plot_data[0])
	g("set logscale y 2")
	g("set output '"+outfile+"_log.svg'")
	g.plot(plot_data[0])
	#g.plot(plot_data[0])


def Plot_scaling(filename,x_value,y_value,outfile,log):

	open_file = pd.read_csv(filename)
	
	x = np.array(open_file[x_value])
	x_label = x_value.replace("_"," ")
	baseline=1.0/x
	
	# instantiate gnuplot
	g = gp.Gnuplot()
	
	y = np.array(open_file[y_value])

	y=y/y[0]


	plot_data=[];
	#print x
	#print y
	#print baseline

	g("set key left")
	g("set terminal pdf enhanced font 'times,12'")
	g("set output '"+outfile+".pdf'")
	#g("set format y '%sx10^{%S}'")
	g("set xlabel '"+x_label+"'")
	g("set format y '%1.2e'")
	if log:
		g("set logscale x 2")

	plot_data.append(gp.Data(x,y,with_="lp",title="Observed scaling"))
	plot_data.append(gp.Data(x,baseline,with_="lp", title="Perfect scaling"))
	g.plot(plot_data[0],plot_data[1])


def collapse(filename,col_num):
	open_file = pd.read_csv(filename)
	data = np.array(open_file)
	
	a={}

	for d in data:
		if d[0] not in a.keys():
			a[d[0]]=[]
		a[d[0]].append(d[col_num])
	
	f = open(filename+"_"+str(col_num)+".csv","wb")
	for k in sorted(a.keys()):
		f.write(str(k)+","+str(np.mean(np.absolute(a[k])))+","+str(np.std(np.absolute(a[k])))+"\n")





