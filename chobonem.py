from retaljaloj import RetalCholajibäl, RetalWajun, RetalCholanem
from runuk import KutbälPyMC, Achlajil
from ruxeeltzij import RuxeelTzij

ktbl = KutbälPyMC()

# Meruchjinem rik'ilal
MCR = RetalCholajibäl('MCR', 4)
mebail = RetalCholanem("meb'a'il", (0, 1))
ruqa = RetalWajun("ruq'a'")
tijoxïk = RetalCholanem("tijoxïk", (0, None))

ach_mcr_mbl = Achlajil(MCR, mebail)
ach_mcr_ruqa = Achlajil(MCR, ruqa)
ach_mbl_ruqa = Achlajil(mebail, ruqa)
ach_mbl_tjxk = Achlajil(mebail, tijoxïk)
ach_tjxk_ruqa = Achlajil(tijoxïk, ruqa)

# Ruxeel tzij
tzij_iximulew = RuxeelTzij(
    yakbäl="/Users/julienmalard/Documents/SLAN 2018/Wuj na’owinaqil - Retamab’alil winasolchi’ k'in ruchajinem rikilal"
           "/Ruxe'el tzij roma SLAN.csv",
    r_jlj={
        'ISA': MCR,
        'brecha.pobreza.norm': mebail,
        'rural': ruqa,
        'educación.adultos': tijoxïk
    }
)

ktbl.ruyaik_achlajil(
    [ach_mbl_tjxk, ach_mbl_ruqa, ach_tjxk_ruqa]
    #[ach_mcr_ruqa, ach_mcr_mbl, ach_mbl_ruqa]
)

ktbl.rubeyalam(a_poroj=1000)
ktbl.kaibäl()
