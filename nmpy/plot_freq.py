import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec

def plot_freq(infile, outfile=None, format=None, newfigure=True, marker='.', size=1, multiplot=False, limits=[[1.855, 1.87],[321, 323]]):
	"""
	param	infile:	filename or list of filenames
	type	infile:	string or list of strings
	"""
	flen = len(infile)

	if type(infile) == str:
		data = np.loadtxt(infile)
		data = data.transpose()
		_doplot(data, outfile, format, newfigure, marker, size, infile, limits)		

	elif type(infile) == list and flen == 1:
		data = np.loadtxt(infile[0])
		data = data.transpose()
		_doplot(data, outfile, format, newfigure, marker, size, infile[0], limits)

	elif type(infile) == list and flen != 1:

		plt.ion()
		for i, file in enumerate(infile):
			data = np.loadtxt(file)
			data = data.transpose()
			if multiplot:
				if i % 2 == 0: 
					j = 0
				else: 
					j = 1
				i = int(i/2.)

				gs = gridspec.GridSpec( int(np.ceil(flen/2)) , 2 ) 

				_domultiplot(data, i, j, format, marker, size, file, limits)

			else:
				_doplot(data, outfile, format, False, marker, size, file, limits)

		fig = plt.gcf()
		fig.tight_layout()
		plt.show()
		plt.ioff()

def _doplot(data, outfile=None, format=None, newfigure=True, marker='.', size=1, label=None, limits=None):
		plt.ion()
		if newfigure:
			fig, ax = plt.subplots()
		else:
			ax = plt.gca()
			fig= plt.gcf()

		ax.set_title('Normal mode frequencies for $_0S_{3}$, $_0S_{4}$, $_0T_{3}$, $_0T_{4}$')
		ax.set_xlabel('frequency (mHz)')
		ax.set_ylabel('Q')
		ax.set_xlim(limits[0])
		ax.set_ylim(limits[1])
		ax.scatter(data[0], data[1], s=size, label=label, marker=marker)
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

 
def _domultiplot(data, x, y, format=None, marker='.', size=1, title=None, label=None, limits=None):
	ax = plt.subplot(gs[x, y])
	ax.set_title(title)
	ax.set_xlabel('frequency (mHz)')
	ax.set_ylabel('Q')
	ax.set_xlim(limits[0])
	ax.set_ylim(limits[1])
	plt.scatter(data[0], data[1], s=size, label=label, marker=marker)


