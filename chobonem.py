from runuk import KutbälPyMC, Achlajil
from retaljaloj import RetalCholajibäl, RetalWajun, RetalCholanem

ktbl = KutbälPyMC()

# Meruchjinem rik'ilal
MCR = RetalCholajibäl('MCR', [0, 1, 2, 3])
mebail = RetalCholanem("meb'a'il", (0, None))
ruqa = RetalWajun("ruq'a'")

ach_mcr_mbl = Achlajil(MCR, mebail)
ach_mcr_ruqa = Achlajil(MCR, ruqa)

ktbl.ruyaik_achlajil(
    [ach_mcr_mbl, ach_mcr_ruqa]
)

ktbl.rubeyalam()
ktbl.kaibäl()
