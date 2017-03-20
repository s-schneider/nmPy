import numpy as np
import matplotlib.pyplot as plt

def plot_freq(outfile=None):
	data = np.loadtxt('omega.dat')
	data = data.transpose()
	fig, ax = plt.subplots()


	ax.set_title('Normal mode frequencies for $_0S_{3}$, $_0S_{4}$, $_0T_{3}$, $_0T_{4}$')
	ax.set_xlabel('frequency (mHz)')
	ax.set_ylabel('Q')

	ax.plot(data[0], data[1], 'x' )
	fig.set_size_inches(9,7)
	if outfile:
		fig.savefig(outfile + '.ps', dpi=400, orientation='portrait', format='ps')	
		plt.close("all")
	else:
		plt.show()