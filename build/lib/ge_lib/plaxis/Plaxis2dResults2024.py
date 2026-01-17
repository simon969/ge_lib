from .Plaxis2dResults2023 import Plaxis2dResults2023

class Plaxis2dResults2024 (Plaxis2dResults2023): 
    def __init__(self,
                server=None, host=None, port=None, password=None
                 ):
        super(Plaxis2dResults2024, self).__init__(server, host, port, password)
    def version (self):
        return "Plaxis2d2024"