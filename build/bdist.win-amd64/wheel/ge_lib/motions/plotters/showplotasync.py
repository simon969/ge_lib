from multiprocessing import Process as mp_Process
from matplotlib.pyplot import show as plt_show

def _Plot(fig):
    plt_show()

def ShowPlotAsync(fig):
    mp_Process(target=_Plot,args=(fig,)).start()