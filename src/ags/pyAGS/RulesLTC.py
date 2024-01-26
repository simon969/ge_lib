
from datetime import timedelta,datetime
from ags.pyAGS.AGSQuery import ags_query_collection, ags_query
from ags.pyAGS.rules.LOCA import *
from ags.pyAGS.rules.PROJ import *
from ags.pyAGS.rules.HORN import *
from ags.pyAGS.rules.HDPH import *
from ags.pyAGS.rules.PTIM import *
from ags.pyAGS.rules.HDIA import *
from ags.pyAGS.rules.CDIA import *
from ags.pyAGS.rules.FLSH import *
from ags.pyAGS.rules.CORE import *
from ags.pyAGS.rules.DREM import *
from ags.pyAGS.rules.DOBS import *
from ags.pyAGS.rules.CHIS import *
from ags.pyAGS.rules.WADD import *
from ags.pyAGS.rules.WSTG import *
from ags.pyAGS.rules.WSTD import *
from ags.pyAGS.rules.GEOL import *
from ags.pyAGS.rules.DETL import *
from ags.pyAGS.rules.FRAC import *
from ags.pyAGS.rules.DETL import *
from ags.pyAGS.rules.FRAC import *
from ags.pyAGS.rules.DISC import *
from ags.pyAGS.rules.WETH import *
from ags.pyAGS.rules.ISPT import *
from ags.pyAGS.rules.IPRG import *
from ags.pyAGS.rules.IPRT import *
from ags.pyAGS.rules.ICBR import *
from ags.pyAGS.rules.PLTG import *
from ags.pyAGS.rules.PLTD import *
from ags.pyAGS.rules.SAMP import *
from ags.pyAGS.rules.CBRG import *
from ags.pyAGS.rules.CBRT import *
from ags.pyAGS.rules.CMPG import *
from ags.pyAGS.rules.CMPT import *
from ags.pyAGS.rules.GCHM import *
from ags.pyAGS.rules.GRAG import *
from ags.pyAGS.rules.GRAT import *
from ags.pyAGS.rules.LDEN import *
from ags.pyAGS.rules.LLPL import *
from ags.pyAGS.rules.LNMC import *
from ags.pyAGS.rules.LPDN import *
from ags.pyAGS.rules.RDEN import *
from ags.pyAGS.rules.RPLT import *
from ags.pyAGS.rules.RTEN import *
from ags.pyAGS.rules.RUCS import *
from ags.pyAGS.rules.RWCO import *
from ags.pyAGS.rules.SHBG import *
from ags.pyAGS.rules.SHBT import *
from ags.pyAGS.rules.TREG import *
from ags.pyAGS.rules.TRET import *
from ags.pyAGS.rules.TRIG import *
from ags.pyAGS.rules.TRIT import *
from ags.pyAGS.rules.PIPE import *
from ags.pyAGS.rules.MONG import *
from ags.pyAGS.rules.MOND import *

class RulesLTC(ags_query_collection):

    def __init__(self):
        super().__init__(id='01', description="LTC AGS Rules Checker", version="LTC 00.01.00")
    
    def _init_queries(self):
        
        DATE_MAX = datetime.now()
        DATE_MIN = DATE_MAX- timedelta(days=365)
        
        DURATION_MIN = timedelta(minutes=1)
        DURATION_MAX = timedelta(hours=6)

        self.add_query (PROJ001())
        self.add_query (PROJ002()) 
        self.add_query (PROJ003())
        self.add_query (PROJ004()) 
        self.add_query (PROJ005()) 
        self.add_query (PROJ006()) 
        
        self.add_query (LOCA001(LOCA_COUNT_MIN=1, LOCA_COUNT_MAX=100))
        self.add_query (LOCA002())
        self.add_query (LOCA003())
        self.add_query (LOCA004())
        self.add_query (LOCA005())
        self.add_query (LOCA006())
        self.add_query (LOCA007(LOCA_NATE_MIN=0, LOCA_NATE_MAX=700000))
        self.add_query (LOCA008(LOCA_NATN_MIN=0, LOCA_NATN_MAX=1300000))
        self.add_query (LOCA009())
        self.add_query (LOCA010(LOCA_GL_MIN=-100, LOCA_GL_MAX=100))
        self.add_query (LOCA011())
        self.add_query (LOCA012(LOCA_STAR_MIN=DATE_MIN, LOCA_STAR_MAX=DATE_MAX))
        self.add_query (LOCA013(LOCA_ENDD_MIN=DATE_MIN, LOCA_ENDD_MAX=DATE_MAX))
        self.add_query (LOCA014())
        self.add_query (LOCA015())
        self.add_query (LOCA016(LOCA_LOCX_MIN=0,LOCA_LOCX_MAX=200))
        self.add_query (LOCA017(LOCA_LOCY_MIN=0,LOCA_LOCY_MAX=200))
        self.add_query (LOCA018())
        self.add_query (LOCA019(LOCA_LOCZ_MIN=0,LOCA_LOCZ_MAX=200))
        self.add_query (LOCA020())
        self.add_query (LOCA021(LOCA_LAT_MIN=-90,LOCA_LAT_MAX=90))
        self.add_query (LOCA022(LOCA_LON_MIN=-180,LOCA_LON_MAX=180))
        self.add_query (LOCA023(LOCA_CKDT_MIN=DATE_MIN, LOCA_CKDT_MAX=DATE_MAX))
        
        self.add_query (HORN001())
        self.add_query (HORN002())
        self.add_query (HORN003())
        self.add_query (HORN004())
        self.add_query (HORN005(HORN_ORNT_MIN=0,HORN_ORNT_MAX=360))
        self.add_query (HORN006(HORN_INCL_MIN=0,HORN_INCL_MAX=90))

        self.add_query (HDPH001())
        self.add_query (HDPH002())
        self.add_query (HDPH003())
        self.add_query (HDPH004())
        self.add_query (HDPH005())
        self.add_query (HDPH006(HDPH_STAR_MIN=DATE_MIN,HDPH_STAR_MAX=DATE_MAX))
        self.add_query (HDPH007(HDPH_ENDD_MIN=DATE_MIN,HDPH_ENDD_MAX=DATE_MAX))

        self.add_query (PTIM001())
        self.add_query (PTIM002())
        self.add_query (PTIM003(PTIM_PTIM_MIN=DATE_MIN, PTIM_PTIM_MAX=DATE_MAX))
        self.add_query (PTIM004())
        self.add_query (PTIM005())
        self.add_query (PTIM006())
        self.add_query (PTIM007(PTIM_WAT_TEXT_ALLOWED=['Dry','DRY']))

        self.add_query (HDIA001())
        self.add_query (HDIA002())
        self.add_query (HDIA003())
        self.add_query (HDIA004(HDIA_DIAM_MIN=50, HDIA_DIAM_MAX=300))
       
        self.add_query (CDIA001())
        self.add_query (CDIA002())
        self.add_query (CDIA003())
        self.add_query (CDIA004(CDIA_DIAM_MIN=50, CDIA_DIAM_MAX=300))

        self.add_query (FLSH001())
        self.add_query (FLSH002())
        self.add_query (FLSH003())
        
        self.add_query (CORE001())
        self.add_query (CORE002(LOCA_TYPE_MUST=['RC','CP+RC']))
        self.add_query (CORE003())
        self.add_query (CORE004())
        self.add_query (CORE005())
        self.add_query (CORE006())
        self.add_query (CORE007(CORE_DIAM_MIN=50, CORE_DIAM_MAX=300))
        self.add_query (CORE008(CORE_DURN_MIN=DURATION_MIN, CORE_DURN_MAX=DURATION_MAX))

        self.add_query (DREM001())
        self.add_query (DREM002(LOCA_TYPE_MUST=['RC','CP+RC']))
        self.add_query (DREM003())
        self.add_query (DREM004())

        self.add_query (DOBS001())
        self.add_query (DOBS002())
        self.add_query (DOBS003())
        
        self.add_query (CHIS001())
        self.add_query (CHIS002())
        self.add_query (CHIS003(CHIS_TIME_MIN=DURATION_MIN, CHIS_TIME_MAX=DURATION_MAX))
        
        self.add_query (WADD001())
        self.add_query (WADD002())
        self.add_query (WADD003(WADD_VOLM_MIN=0.5, WADD_VOLM_MAX=100))
        
        self.add_query (WSTG001())
        self.add_query (WSTG002())
        self.add_query (WSTG003(WSTG_DTIM_MIN=DATE_MIN, WSTG_DTIM_MAX=DATE_MAX))
        self.add_query (WSTG004())
        self.add_query (WSTG005())
        self.add_query (WSTG006())
       
        self.add_query (WSTD001())
        self.add_query (WSTD002())
        self.add_query (WSTD003(WSTD_NMIN_MIN=DURATION_MIN, WSTD_NMIN_MAX=DURATION_MAX))
        self.add_query (WSTD004())
        self.add_query (WSTD005())
                        
        self.add_query (GEOL001())
        self.add_query (GEOL002())
        self.add_query (GEOL003())
        self.add_query (GEOL004())
        self.add_query (GEOL005())
        self.add_query (GEOL006())
        self.add_query (GEOL007())
        self.add_query (GEOL008())
        self.add_query (GEOL009())
        self.add_query (GEOL010())
        self.add_query (GEOL011(GEOL_LEG_MIN=0, GEOL_LEG_MAX=256))
        
        self.add_query (DETL001())
        self.add_query (DETL002())
        self.add_query (DETL003())

        self.add_query (FRAC001())
        self.add_query (FRAC002())
        self.add_query (FRAC003())
        self.add_query (FRAC004(FRAC_FI_MIN=1,FRAC_FI_MAX=100))

        self.add_query (DISC001())
        self.add_query (DISC002())
        self.add_query (DISC003())
        self.add_query (DISC004())
        self.add_query (DISC005())
        self.add_query (DISC006(DISC_DIP_MIN=0,DISC_DIP_MAX=90))
        self.add_query (DISC007(DISC_DIR_MIN=0,DISC_DIR_MAX=360))
        self.add_query (DISC008())

        self.add_query (WETH001())
        self.add_query (WETH002())
        self.add_query (WETH003(WETH_SCH_ALLOWED=['BS 5930:2015','BS 5930:1999 AMEND 1','BS 5930:1999','BS EN 14689-1:2003','CIRIA C574 CHALK']))
        self.add_query (WETH004(WETH_SYS_ALLOWED=['MASS CLASS','MATERIAL CLASS','MAT CLASS','MASS GRADE']))
        self.add_query (WETH005())
        
        self.add_query (ISPT001())
        self.add_query (ISPT002(LOCA_TYPE_MUST=['CP','RC+CP']))
        self.add_query (ISPT003())
        self.add_query (ISPT004())
        self.add_query (ISPT005())
        self.add_query (ISPT006())
        self.add_query (ISPT007(ISPT_NVAL_MIN=0,ISPT_NVAL_MAX=50))
        self.add_query (ISPT008())
        self.add_query (ISPT009())
        self.add_query (ISPT010(ISPT_WAT_TEXT_ALLOWED=['Dry','DRY']))
        self.add_query (ISPT011(ISPT_TYPE_ALLOWED=['C','S']))
        self.add_query (ISPT012())
        self.add_query (ISPT013())
        self.add_query (ISPT014())
        self.add_query (ISPT015())
        self.add_query (ISPT016())
        self.add_query (ISPT017(ISPT_ROCK_ALLOWED=['Yes','Y','No','N']))
        self.add_query (ISPT018())
        self.add_query (ISPT019())
        self.add_query (ISPT020(ISPT_METH_ALLOWED=['BS EN ISO 22476-3:2005','BS 1377:Part 9:1990']))
        
        self.add_query (IPRG001())
        self.add_query (IPRG002())
        self.add_query (IPRG003())
        self.add_query (IPRG004())
        self.add_query (IPRG005(IPRG_TYPE_ALLOWED=['Constant Head','Falling Head']))
        self.add_query (IPRG006())
        self.add_query (IPRG007())
        self.add_query (IPRG008(IPRG_TDIA_MIN=50,IPRG_TDIA_MAX=300))
        self.add_query (IPRG009(IPRG_SDIA_MIN=50,IPRG_SDIA_MAX=300))
        self.add_query (IPRG010())
        self.add_query (IPRG011())
        self.add_query (IPRG012())
        self.add_query (IPRG013())
        self.add_query (IPRG014(IPRG_DATE_MIN=DATE_MIN, IPRG_DATE_MAX=DATE_MAX))
        self.add_query (IPRG015())
        self.add_query (IPRG016())
        self.add_query (IPRG017(IPRG_METH_ALLOWED=['BS5930']))
        
        self.add_query (IPRT001())
        self.add_query (IPRT002())
        self.add_query (IPRT003())
        self.add_query (IPRT004())
        self.add_query (IPRT005(IPRT_TIME_MIN=DURATION_MIN, IPRT_TIME_MAX=DURATION_MAX))
        self.add_query (IPRT006())
        
        self.add_query (ICBR001())
        self.add_query (ICBR002())
        self.add_query (ICBR003())
        self.add_query (ICBR004())
        self.add_query (ICBR005())
        self.add_query (ICBR006())

        self.add_query (PLTG001())
        self.add_query (PLTG002())
        self.add_query (PLTG003())
        self.add_query (PLTG004())
        self.add_query (PLTG005())
        self.add_query (PLTG006(PLTG_METH_ALLOWED=['DIN18134 Strain Modulus']))
        
        self.add_query (PLTD001())
        self.add_query (PLTD002())
        self.add_query (PLTD003())
        self.add_query (PLTD004())
        self.add_query (PLTD005())
        self.add_query (PLTD006(PLTD_TIME_MIN=DURATION_MIN, PLTD_TIME_MAX=DURATION_MAX))
        
        self.add_query (SAMP001())
        self.add_query (SAMP002())
        self.add_query (SAMP003())
        self.add_query (SAMP004(SAMP_TYPE_ALLOWED=['B','C','D','ES','EW','UT']))
        self.add_query (SAMP005())
        self.add_query (SAMP006(SAMP_DTIM_MIN=DATE_MIN, SAMP_DTIM_MAX=DATE_MAX))
        self.add_query (SAMP007(SAMP_UBLO_TYPES=['UT'],SAMP_UBLO_MIN=1,SAMP_UBLO_MAX=100))
        self.add_query (SAMP008(SAMP_CONT_ALLOWED=['Tub','Bag']))
        self.add_query (SAMP009(SAMP_SDIA_MIN=60, SAMP_SDIA_MAX=100))
        self.add_query (SAMP010())
        self.add_query (SAMP011())
        self.add_query (SAMP012(SAMP_DESD_MIN=DATE_MIN, SAMP_DESD_MAX=DATE_MAX))

        self.add_query (CBRG001())
        self.add_query (CBRG002())
        self.add_query (CBRG003())
        self.add_query (CBRG004(SAMP_TYPE_ALLOWED=['B','D']))
        self.add_query (CBRG005())
        self.add_query (CBRG006())
        self.add_query (CBRG007())
        self.add_query (CBRG008())
        self.add_query (CBRG009())
        
        self.add_query (CBRT001())
        self.add_query (CBRT002())
        self.add_query (CBRT003())
        self.add_query (CBRT004(SAMP_TYPE_ALLOWED=['B','D']))
        self.add_query (CBRT005())
        self.add_query (CBRT006())
        self.add_query (CBRT007())
        self.add_query (CBRT008())
        self.add_query (CBRT009())
        self.add_query (CBRT010())
        self.add_query (CBRT011())
        self.add_query (CBRT012())

        self.add_query (CMPG001())
        self.add_query (CMPG002())
        self.add_query (CMPG003())
        self.add_query (CMPG004(SAMP_TYPE_ALLOWED=['B','D']))
        self.add_query (CMPG005())
        self.add_query (CMPG006())
        self.add_query (CMPG007())
        self.add_query (CMPG008())
        self.add_query (CMPG009())
        self.add_query (CMPG010(CMPG_TYPE_ALLOWED=['2.5KG','4.5KG']))
        self.add_query (CMPG011(CMPG_MOLD_ALLOWED=['1 LITRE','1ltr']))
        self.add_query (CMPG012())
        self.add_query (CMPG013())

        self.add_query (CMPT001())
        self.add_query (CMPT002())
        self.add_query (CMPT003())
        self.add_query (CMPT004(SAMP_TYPE_ALLOWED=['B','D']))
        self.add_query (CMPT005())
        self.add_query (CMPT006())
        self.add_query (CMPT007())
        self.add_query (CMPT008())
        self.add_query (CMPT009())
        self.add_query (CMPT010())
        self.add_query (CMPT011())
     
        self.add_query (GCHM001())
        self.add_query (GCHM002())
        self.add_query (GCHM003())
        self.add_query (GCHM004(SAMP_TYPE_ALLOWED=['B','D','ES']))
        self.add_query (GCHM005())
        self.add_query (GCHM006())
        self.add_query (GCHM007())
        self.add_query (GCHM008())
        self.add_query (GCHM009())
        self.add_query (GCHM010())
        self.add_query (GCHM011())

        self.add_query (GRAG001())
        self.add_query (GRAG002())
        self.add_query (GRAG003())
        self.add_query (GRAG004(SAMP_TYPE_ALLOWED=['B','D','ES']))
        self.add_query (GRAG005())
        self.add_query (GRAG006())
        self.add_query (GRAG007())
        self.add_query (GRAG008())
        self.add_query (GRAG009())
        self.add_query (GRAG010())
        self.add_query (GRAG011())

        self.add_query (GRAT001())
        self.add_query (GRAT002())
        self.add_query (GRAT003())
        self.add_query (GRAT004(SAMP_TYPE_ALLOWED=['B','D','ES']))
        self.add_query (GRAT005())
        self.add_query (GRAT006())
        self.add_query (GRAT007())
        self.add_query (GRAT008())
        self.add_query (GRAT009())
        self.add_query (GRAT010())
      
        self.add_query (LDEN001())
        self.add_query (LDEN002())
        self.add_query (LDEN003())
        self.add_query (LDEN004(SAMP_TYPE_ALLOWED=['B','D','ES']))
        self.add_query (LDEN005())
        self.add_query (LDEN006())
        self.add_query (LDEN007())
        self.add_query (LDEN008())
        self.add_query (LDEN009(LDEN_METH_ALLOWED=['BS1377: Part 2: 1990: Clause 7.2']))
        self.add_query (LDEN010())
        self.add_query (LDEN011())
        self.add_query (LDEN012())

        self.add_query (LLPL001())
        self.add_query (LLPL002())
        self.add_query (LLPL003())
        self.add_query (LLPL004(SAMP_TYPE_ALLOWED=['B','D','ES']))
        self.add_query (LLPL005())
        self.add_query (LLPL006())
        self.add_query (LLPL007())
        self.add_query (LLPL008())
        self.add_query (LLPL009(LLPL_METH_ALLOWED=['BS1377: Part 2: 1990: Clause 4.4 and 5']))
        self.add_query (LLPL010())
        self.add_query (LLPL011())
    
        self.add_query (LNMC001())
        self.add_query (LNMC002())
        self.add_query (LNMC003())
        self.add_query (LNMC004(SAMP_TYPE_ALLOWED=['B','D','ES']))
        self.add_query (LNMC005())
        self.add_query (LNMC006())
        self.add_query (LNMC007())
        self.add_query (LNMC008())
        self.add_query (LNMC009(LNMC_METH_ALLOWED=['BS1377: Part 2: 1990: Clause 7.2']))
        self.add_query (LNMC010())

        self.add_query (LPDN001())
        self.add_query (LPDN002())
        self.add_query (LPDN003())
        self.add_query (LPDN004(SAMP_TYPE_ALLOWED=['B','D','ES']))
        self.add_query (LPDN005())
        self.add_query (LPDN006())
        self.add_query (LPDN007())
        self.add_query (LPDN008())
        self.add_query (LPDN009(LPDN_METH_ALLOWED= ['BS1377: Part 2: 1990: Clause 8.3']))

        self.add_query (RDEN001())
        self.add_query (RDEN002())
        self.add_query (RDEN003())
        self.add_query (RDEN004(SAMP_TYPE_ALLOWED=['B','D','ES']))
        self.add_query (RDEN005())
        self.add_query (RDEN006())
        self.add_query (RDEN007())
        self.add_query (RDEN008())
        self.add_query (RDEN009(RDEN_METH_ALLOWED=['BS1377: Part 2: 1990: Clause 7.2']))
        self.add_query (RDEN010())
        self.add_query (RDEN011())
        self.add_query (RDEN012())        

        self.add_query (RPLT001())
        self.add_query (RPLT002())
        self.add_query (RPLT003())
        self.add_query (RPLT004(SAMP_TYPE_ALLOWED=['B','D','ES']))
        self.add_query (RPLT005())
        self.add_query (RPLT006())
        self.add_query (RPLT007())
        self.add_query (RPLT008())
        self.add_query (RPLT009(RPLT_METH_ALLOWED=['ISRM: 2007 : Suggested method for determining point load strength. Int J Rock Mech Min Sci & Geomech Abstr, Vol 22, No 2, pp 51-60 ']))
        self.add_query (RPLT010())
        self.add_query (RPLT011())
        self.add_query (RPLT012(RPLT_PLTF_ALLOWED=['A+L','A+D','A','D','L'])) 
        
        self.add_query (RTEN001())
        self.add_query (RTEN002())
        self.add_query (RTEN003())
        self.add_query (RTEN004(SAMP_TYPE_ALLOWED=['B','D','ES']))
        self.add_query (RTEN005())
        self.add_query (RTEN006())
        self.add_query (RTEN007())
        self.add_query (RTEN008())
        self.add_query (RTEN009(RTEN_METH_ALLOWED=['BS1377: Part 2: 1990: Clause 7.2']))
        self.add_query (RTEN010(RTEN_SDIA_MIN=50,RTEN_SDIA_MAX=100))
        self.add_query (RTEN011())
        self.add_query (RTEN012()) 

        self.add_query (RUCS001())
        self.add_query (RUCS002())
        self.add_query (RUCS003())
        self.add_query (RUCS004(SAMP_TYPE_ALLOWED=['B','D','ES']))
        self.add_query (RUCS005())
        self.add_query (RUCS006())
        self.add_query (RUCS007())
        self.add_query (RUCS008())
        self.add_query (RUCS009(RUCS_METH_ALLOWED=['BS1377: Part 2: 1990: Clause 7.2']))
        self.add_query (RUCS010(RUCS_SDIA_MIN=50, RUCS_SDIA_MAX=300))
        self.add_query (RUCS011())
        self.add_query (RUCS012())         
        self.add_query (RUCS013(RUCS_DURN_MIN=DURATION_MIN,RUCS_DURN_MAX=DURATION_MAX))
        self.add_query (RUCS014(RUCS_STRA_MIN=100,RUCS_STRA_MAX=1000))        
        self.add_query (RUCS015())
        self.add_query (RUCS016())
        self.add_query (RUCS017()) 
        self.add_query (RUCS018()) 
        self.add_query (RUCS019(RUCS_ETYP_ALLOWED=[]))
       
        self.add_query (RWCO001())
        self.add_query (RWCO002())
        self.add_query (RWCO003())
        self.add_query (RWCO004(SAMP_TYPE_ALLOWED=['B','D','ES']))
        self.add_query (RWCO005())
        self.add_query (RWCO006())
        self.add_query (RWCO007())
        self.add_query (RWCO008(RWCO_METH_ALLOWED=['BS1377: Part 2: 1990: Clause 7.2']))
        self.add_query (RWCO009())
        
        self.add_query (SHBG001())
        self.add_query (SHBG002())
        self.add_query (SHBG003())
        self.add_query (SHBG004(SAMP_TYPE_ALLOWED=['B','D']))
        self.add_query (SHBG005())
        self.add_query (SHBG006())
        self.add_query (SHBG007(SHBG_TYPE_ALLOWED=['SMALL SBOX','LARGE SBOX']))
        self.add_query (SHBG008())
        self.add_query (SHBG009(SHBG_METH_ALLOWED=['BS1377 Part 7']))
        
        self.add_query (SHBT001())
        self.add_query (SHBT002())
        self.add_query (SHBT003())
        self.add_query (SHBT004(SAMP_TYPE_ALLOWED=['B','D']))
        self.add_query (SHBT005())
        self.add_query (SHBT006())
        self.add_query (SHBT007())
        self.add_query (SHBT008())
        self.add_query (SHBT009())
        self.add_query (SHBT010())
        self.add_query (SHBT011())
        self.add_query (SHBT012())

        self.add_query (TREG001())
        self.add_query (TREG002())
        self.add_query (TREG003())
        self.add_query (TREG004(SAMP_TYPE_ALLOWED=['UT']))
        self.add_query (TREG005())
        self.add_query (TREG006())
        self.add_query (TREG007(TREG_TYPE_ALLOWED=['CU']))
        self.add_query (TREG008())
        self.add_query (TREG009(TREG_METH_ALLOWED=['BS1377: Part 8']))
        self.add_query (TREG010())
        self.add_query (TREG011())
        self.add_query (TREG012())
        self.add_query (TREG013())
        
        self.add_query (TRET001())
        self.add_query (TRET002())
        self.add_query (TRET003())
        self.add_query (TRET004(SAMP_TYPE_ALLOWED=['UT']))
        self.add_query (TRET005())
        self.add_query (TRET006())
        self.add_query (TRET007())
        self.add_query (TRET008())
        self.add_query (TRET009())
        self.add_query (TRET010())
        self.add_query (TRET011())
        self.add_query (TRET012())
        self.add_query (TRET013())
        self.add_query (TRET014())
        self.add_query (TRET015())
        self.add_query (TRET016())
        self.add_query (TRET017())
        self.add_query (TRET018())
        self.add_query (TRET019())
        self.add_query (TRET020())
        self.add_query (TRET021())
        self.add_query (TRET022())
        self.add_query (TRET023())
        self.add_query (TRET024())
        self.add_query (TRET025())
        
        self.add_query (TRIG001())
        self.add_query (TRIG002())
        self.add_query (TRIG003())
        self.add_query (TRIG004(SAMP_TYPE_ALLOWED=['UT']))
        self.add_query (TRIG005())
        self.add_query (TRIG006())
        self.add_query (TRIG007(TRIG_TYPE_ALLOWED=['UU']))
        self.add_query (TRIG008())
        self.add_query (TRIG009(TRIG_METH_ALLOWED=['BS EN ISO 17892-8']))
        self.add_query (TRIG010())
        
        self.add_query (TRIT001())
        self.add_query (TRIT002())
        self.add_query (TRIT003())
        self.add_query (TRIT004(SAMP_TYPE_ALLOWED=['UT']))
        self.add_query (TRIT005())
        self.add_query (TRIT006())
        self.add_query (TRIT007())
        self.add_query (TRIT008())
        self.add_query (TRIT009())
        self.add_query (TRIT010())
        self.add_query (TRIT011())
        self.add_query (TRIT012())
        self.add_query (TRIT016())
        self.add_query (TRIT019())
        self.add_query (TRIT020())
        self.add_query (TRIT022())
        self.add_query (TRIT023())
        self.add_query (TRIT024())
        self.add_query (TRIT025())
        
        self.add_query (PIPE001())
        self.add_query (PIPE002())
        self.add_query (PIPE003())
        self.add_query (PIPE004(PIPE_DIAM_MIN=50, PIPE_DIAM_MAX=100))
        self.add_query (PIPE005(PIPE_TYPE_ALLOWED=['SOLID','SLOTTED']))
        self.add_query (PIPE006())
        self.add_query (PIPE007())

        self.add_query (MONG001())
        self.add_query (MONG002())
        self.add_query (MONG003())
        self.add_query (MONG004(MONG_TYPE_ALLOWED=['UT']))
        self.add_query (MONG005(MONG_DATE_MIN=DATE_MIN, MONG_DATE_MAX=DATE_MAX))
        self.add_query (MONG006())
        self.add_query (MONG007())
        self.add_query (MONG008())
        self.add_query (MONG009())
        self.add_query (MONG010(MONG_BRGA_MIN=0,MONG_BRGA_MAX=360))
        self.add_query (MONG011(MONG_BRGB_MIN=0,MONG_BRGB_MAX=360))
        self.add_query (MONG012(MONG_BRGC_MIN=0,MONG_BRGC_MAX=360))
        self.add_query (MONG013(MONG_INCA_MIN=0,MONG_INCA_MAX=90))
        self.add_query (MONG014(MONG_INCB_MIN=0,MONG_INCB_MAX=90))
        self.add_query (MONG015(MONG_INCC_MIN=0,MONG_INCC_MAX=90))
        self.add_query (MONG016())
        self.add_query (MONG017())
        self.add_query (MONG018())
        self.add_query (MONG019())

        self.add_query (MOND001())
        self.add_query (MOND002())
        self.add_query (MOND003())
        self.add_query (MOND004(MOND_TYPE_ALLOWED=['SP','SPIE','BAR','BLEV','DBSE','DNAPL','GCM','GCMP','GFLOP','GFLOS','GM','GMP','GOX','GOXP','GPRS','GPRSP','HYS','HYSP','LNAPL','PRES','TEMP','TGM','TGMP','VOC','WDEP','WLEV']))
        self.add_query (MOND005(MOND_DTIM_MIN=DATE_MIN,MOND_DTIM_MAX=DATE_MAX))
       
        self.add_query (MOND006())
        self.add_query (MOND007())
        self.add_query (MOND008())
        self.add_query (MOND009())
        self.add_query (MOND010())
        self.add_query (MOND011())
        self.add_query (MOND012())
        self.add_query (MOND013())
        self.add_query (MOND014())
        self.add_query (MOND015())

        # Project specific checks
        self.add_query (NEOM_LOCA001(LOCA_CKDT_FORMAT='yyyy-MM-dd'))
        self.add_query (NEOM_HORN001(HORN_BASE_TYPE_ALLOWED='2DP'))
        self.add_query (NEOM_GRAG001())


class NEOM_LOCA001(ags_query):
    def __init__(self, LOCA_CKDT_FORMAT):
        self.LOCA_CKDT_FORMAT = LOCA_CKDT_FORMAT
        super().__init__(id='NEOM_LOCA001', 
                        description="Is the LOCA_CKDT date type in the ISO format {}".format(self.LOCA_CKDT_FORMAT),
                        requirement = "Neom PTS",
                        action = "Check that the LOCA_CKDT is completed in the correct format for all records in the LOCA group")
        
    def run_query(self,  tables, headings):
        LOCA = self.get_group(tables, "LOCA", True)
        
        if (LOCA is not None):  
            self.check_unit_string(LOCA,"LOCA","LOCA_CKDT",self.LOCA_CKDT_FORMAT)
  
class NEOM_HORN001(ags_query):
    def __init__(self, HORN_BASE_TYPE_ALLOWED):
        self.HORN_BASE_TYPE_ALLOWED = HORN_BASE_TYPE_ALLOWED
        super().__init__(id='NEOM_HORN001', 
                        description="Is the HORN_BASE value to {0}".format(self.HORN_BASE_TYPE_ALLOWED),
                        requirement = "Neom PTS",
                        action = "Check that the HORN_BASE value for all records is reported to {0}".format(self.HORN_BASE_TYPE_ALLOWED))
        
    def run_query(self,  tables, headings):
        HORN = self.get_group(tables, "HORN", True)
        
        if (HORN is not None):  
            self.check_type_string(HORN,"HORN","HORN_BASE",self.HORN_BASE_TYPE)      
class NEOM_PTIM001(ags_query):
    def __init__(self):
        super().__init__(id='NEOM_PTM001', 
                        description="Does the water depth PTIM_WAT contain any duplicate values?",
                        requirement = "Neom PTS",
                        action = "Check that there are no duplicate water depths in the PTIM_WAT {0}".format(self.HORN_BASE_TYPE_ALLOWED))
        
    def run_query(self,  tables, headings):
        LOCA = self.get_group(tables, "LOCA", True)
        PTIM = self.get_group(tables, "PTIM", True)
        
        if (LOCA is not None and PTIM is not None):  
            lLOCA =  LOCA.query("HEADING == 'DATA'")  
            for index, values in lLOCA.iterrows():
                qry = "LOCA_ID == '{0}'".format(values['LOCA_ID'])
                self.check_unique (PTIM,"PTIM",qry,"PTIM_WAT") 

class NEOM_GRAG001(ags_query):
    def __init__(self):
        super().__init__(id='NEOM_GRAG001', 
                        description="Is GRAG_SILT the total percenatage fines (i.e. SILT + CLAY) and the percentage of clay is given as 0 for all PSD tests?",
                        requirement = "Neom PTS",
                        action = "Please populate GRAG_FINES with total fine content (SILT + CLAY), populate GRAG_SILT with percentage SILT and GRAG_CLAY with percentage CLAY")
        
    def run_query(self,  tables, headings):
        GRAG = self.get_group(tables, "GRAG", True)
        
        if (GRAG is not None):  
            lgrag =  GRAG.query("HEADING == 'DATA'")
            table_name = "GRAG"  
            for index, values in lgrag.iterrows():
                grag_silt = pd.to_numeric (values['GRAG_SILT'])
                grag_clay = pd.to_numeric (values['GRAG_CLAY'])
                grag_fines = pd.to_numeric (values['GRAG_FINES'])
                if (grag_silt > 0 and grag_clay == 0):
                    line = values['line_number'][0]
                    desc = 'The GRAG_SILT ({0}) is the total fines (ie SILT+CLAY) and GRAG_CLAY=0 with GRAG_FINES ({1})'.format(grag_silt, grag_fines)
                    res = {'line':line, 'group':table_name, 'desc':desc}
                    self.results_fail.append (res)
                else:
                    if (grag_fines == grag_clay + grag_silt):
                        line =values['line_number'][0]
                        desc = 'The GRAG_SILT ({0}) and GRAG_CLAY ({1}) is equal to the GRAG_FINES ({1})'.format(grag_silt, grag_clay, grag_fines)
                        res = {'line':line, 'group':table_name, 'desc':desc}
                        self.results_pass.append (res)
                    else:
                        line =values['line_number'][0]
                        desc = 'The GRAG_SILT ({0}) and GRAG_CLAY ({1}) is not equal to the GRAG_FINES ({1})'.format(grag_silt, grag_clay, grag_fines)
                        res = {'line':line, 'group':table_name, 'desc':desc}
                        self.results_fail.append (res)    