from .Plaxis3dResults2023 import Plaxis3dResults2023

class Plaxis3dResults2024 (Plaxis3dResults2023): 
    def __init__(self,
                server=None, host=None, port=None, password=None
                 ):
        super(Plaxis3dResults2024, self).__init__(server, host, port, password)
    def version (self):
        return "Plaxis3d2024"