from __future__ import absolute_import, print_function
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec

from matplotlib.ticker import MultipleLocator, FormatStrFormatter

def plot_freq(infile, outfile=None, newfigure=True, marker='D', size=10, 
				fig_size=[7,10], multiplot=False, limits=[[1.855, 1.87],[321, 323]], 
				ticks=[None, None], title=None, papertype='A4', spacing=True):
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

				gs = gridspec.GridSpec( int(np.ceil(flen/2)), 2 ) 
				
				title_tmp = file.split("_")
				title_tmp.reverse()

				model 	= title_tmp[3]
				ellip 	= int(title_tmp[0].split('.')[0])
				rot		= int(title_tmp[1])
				
				if ellip == 0 and rot == 0:

					stitle = 'SNREI'

				else:

					if ellip == 0 :
						ellip = ''
					else:
						ellip = ' + ellip.'

					if rot == 0:
						rot = ''
					else:
						rot = ' + rot.'

					stitle = model + rot + ellip

				_domultiplot(data, i, j, gs, marker=marker, size=size, title=stitle, label=None,  limits=limits, ticks=ticks, newfigure=newfigure)

			else:
				_doplot(data, newfigure=False, marker=marker, size=size, label=file, limits=limits)

		fig = plt.gcf()

		if spacing:
			fig.tight_layout(w_pad=.6, h_pad=.4)

		if multiplot: 
			fig.suptitle(title)

		fig.set_size_inches(fig_size)

		plt.subplots

		if outfile:
			fig.savefig(outfile, dpi=400, orientation='portrait', papertype=papertype) #, bbox_extra_artis=(suptitle,)) #, bbox_inches="tight")	
			plt.close("all")

		else:
			plt.ion()
			print('No output format specified')
			plt.show()
			#plt.ioff()

def _doplot(data, newfigure=True, marker='.', size=1, label=None, limits=None):
		if newfigure:
			fig, ax = plt.subplots()
		else:
			ax = plt.gca()
			fig= plt.gcf()

		ax.set_title('Normal mode frequencies for $_0S_{3}$, $_0S_{4}$, $_0T_{3}$, $_0T_{4}$')
		ax.set_xlabel('frequency (mHz)')
		ax.set_ylabel('Q')
		if limits:
			ax.set_xlim(limits[0])
			ax.set_ylim(limits[1])
		ax.scatter(data[0], data[1], s=size, label=label, marker=marker)
		ax.legend()

 
def _domultiplot(data, x, y, gs, marker='.', size=1, title=None, label=None, limits=None, ticks=None, newfigure=True):
	

	ax = plt.subplot(gs[x, y])
	ax.set_title(title)
	ax.set_ylabel('Q')
	ax.set_xlabel('frequency (mHz)')

	if limits:
		if limits[0]:
			ax.set_xlim(limits[0])

		if ticks[0]:
			XmajorLocator = MultipleLocator(ticks[0][0])
			XmajorFormatter = FormatStrFormatter('%1.3f')
			XminorLocator = MultipleLocator(ticks[0][1])
			ax.xaxis.set_major_locator(XmajorLocator)
			ax.xaxis.set_major_formatter(XmajorFormatter)
			ax.xaxis.set_minor_locator(XminorLocator)

		if limits[1]:
			ax.set_ylim(limits[1])

		if ticks[1]:
			YmajorLocator = MultipleLocator(ticks[1][0])
			YmajorFormatter = FormatStrFormatter('%1.1f')
			YminorLocator = MultipleLocator(ticks[1][1])
			ax.yaxis.set_major_locator(YmajorLocator)
			ax.yaxis.set_major_formatter(YmajorFormatter)
			ax.yaxis.set_minor_locator(YminorLocator)


		

	plt.scatter(data[0], data[1], s=size, label=label, marker=marker)


 