import numpy as np
import matplotlib.pyplot as plt

def plot_freq(infile=None, outfile=None, format=None, newfigure=True, marker='.', size=1, label=None):
	data = np.loadtxt(infile)
	data = data.transpose()
	plt.ion()
	if newfigure:
		fig, ax = plt.subplots()
	else:
		ax = plt.gca()
		fig= plt.gcf()

	ax.set_title('Normal mode frequencies for $_0S_{3}$, $_0S_{4}$, $_0T_{3}$, $_0T_{4}$')
	ax.set_xlabel('frequency (mHz)')
	ax.set_ylabel('Q')

	ax.scatter(data[0], data[1], s=size, label=label)
	ax.legend()
	fig.set_size_inches(6,5)
	if outfile:
		if not format:
			format = outfile.split('.')[::-1][0]
			
		if format in plt.gcf().canvas.get_supported_filetypes():
			plt.ioff()
			fig.savefig(outfile + '.' + format, dpi=400, orientation='landscape', format=format)	
			plt.close("all")
	else:
		print('No output format specified')
		plt.show()
		plt.ioff()