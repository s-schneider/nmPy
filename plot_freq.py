from __future__ import absolute_import, print_function
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec

from matplotlib.ticker import MultipleLocator, FormatStrFormatter

def plot_freq(infile, outfile=None, newfigure=True, marker='.', size=1, fig_size=[7,10], multiplot=False, limits=[[1.855, 1.87],[321, 323]], title=None):
	"""
	param	infile:	filename or list of filenames
	type	infile:	string or list of strings
	"""
	flen = len(infile)

	if type(infile) == str:
		data = np.loadtxt(infile)
		data = data.transpose()
		_doplot(data, outfile, newfigure, marker, size, infile, limits)		

	elif type(infile) == list and flen == 1:
		data = np.loadtxt(infile[0])
		data = data.transpose()
		_doplot(data, outfile, newfigure, marker, size, infile[0], limits)

	elif type(infile) == list and flen != 1:

		
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
				
				title_tmp = file.split("_")
				model 	= title_tmp[1]

				title_tmp.reverse()
				ellip 	= int(title_tmp[0].split('.')[0][0])
				rot		= int(title_tmp[0].split('.')[0][2])
				
				if ellip == 0 :
					ellip = 'off'
				else:
					ellip = 'on'

				if rot == 0:
					rot = 'off'
				else:
					rot = 'on'

				stitle 	= model + ", " + "rot. " + rot + ", ellip." + ellip

				_domultiplot(data, i, j, gs, marker=marker, size=size, title=stitle, label=None,  limits=limits)

			else:
				_doplot(data, newfigure=False, marker=marker, size=size, label=file, limits=limits)

		fig = plt.gcf()
		fig.tight_layout()

		if multiplot: plt.suptitle(title)

		fig.set_size_inches(fig_size[0], fig_size[1])

		if outfile:
			fig.savefig(outfile, dpi=400, orientation='portrait')	
			plt.close("all")

		else:
			plt.ion()
			print('No output format specified')
			plt.show()
			plt.ioff()

def _doplot(data, newfigure=True, marker='.', size=1, label=None, limits=None):
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

 
def _domultiplot(data, x, y, gs, marker='.', size=1, title=None, label=None, limits=None):
	
	ax = plt.subplot(gs[x, y])
	ax.set_title(title)

	XmajorLocator = MultipleLocator(0.005)
	XmajorFormatter = FormatStrFormatter('%1.3f')
	XminorLocator = MultipleLocator(0.001)

	ax.set_xlabel('frequency (mHz)')
	ax.set_xlim(limits[0])
	ax.xaxis.set_major_locator(XmajorLocator)
	ax.xaxis.set_major_formatter(XmajorFormatter)
	ax.xaxis.set_minor_locator(XminorLocator)

	YmajorLocator = MultipleLocator(0.5)
	YmajorFormatter = FormatStrFormatter('%1.3f')
	YminorLocator = MultipleLocator(0.1)

	ax.set_ylabel('Q')
	ax.set_ylim(limits[1])
	ax.yaxis.set_major_locator(YmajorLocator)
	ax.yaxis.set_major_formatter(YmajorFormatter)
	ax.yaxis.set_minor_locator(YminorLocator)

	plt.scatter(data[0], data[1], s=size, label=label, marker=marker)


