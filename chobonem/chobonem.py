from retaljaloj import RetalCholajibäl, RetalWajun, RetalCholanem
from kutbäl import KutbälPyMC
from achlajil import Achlajil
from ruxeeltzij import RuxeelTzij

ktbl = KutbälPyMC()

# Meruchjinem rik'ilal
MCR = RetalCholajibäl('MCR', 4)
mebail = RetalCholanem("meb'a'il", (0, 1))
ruqa = RetalWajun("ruq'a'")
tijoxïk = RetalCholanem("tijoxïk", (0, None))
ixöq = RetalWajun("ixöq")
ruyon = RetalWajun('ruyon')
kaxlan = RetalWajun('kaxlan')
kaxlan_tzij = RetalWajun('kaxlan tzij')

ach_mcr_mbl = Achlajil(MCR, mebail)
ach_mcr_ruq = Achlajil(MCR, ruqa)
ach_mbl_ruq = Achlajil(mebail, ruqa)
ach_mbl_tjxk = Achlajil(mebail, tijoxïk)
ach_tjx_ruq = Achlajil(tijoxïk, ruqa)
ach_mbl_ixq = Achlajil(mebail, ixöq)
ach_ryn_ixq = Achlajil(ruyon, ixöq)
ach_mbl_ryn = Achlajil(mebail, ruyon)
ach_mbl_kxl = Achlajil(mebail, kaxlan)
ach_tjx_kxl = Achlajil(tijoxïk, kaxlan)
ach_kxl_ruq = Achlajil(kaxlan, ruqa)

ach_kxt_kxl = Achlajil(kaxlan_tzij, kaxlan)
ach_kxt_ruq = Achlajil(kaxlan_tzij, ruqa)
ach_tjx_kxt = Achlajil(tijoxïk, kaxlan_tzij)
ach_mbl_kxt = Achlajil(mebail, kaxlan_tzij)
ach_mcr_ixq = Achlajil(MCR, ixöq)
ach_mcr_kxl = Achlajil(MCR, kaxlan)
ach_mcr_kxt = Achlajil(MCR, kaxlan_tzij)

# Ruxeel tzij
tzij_iximulew = RuxeelTzij(
    yakbäl="/Users/julienmalard/Documents/SLAN 2018/Wuj na’owinaqil - Retamab’alil winasolchi’ k'in ruchajinem rikilal"
           "/Ruxe'el tzij roma SLAN.csv",
    r_jlj={
        'ISA': MCR,
        'brecha.pobreza.norm': mebail,
        'rural': ruqa,
        'educación.adultos': tijoxïk,
        'jefa.mujer': ixöq,
        'solteroa': ruyon,
        'etnia.cstlñ': kaxlan,
        'leng.frec.cstlñ': kaxlan_tzij
    }
)

ktbl.ruyaik_achlajil(
    [
        ach_mbl_ruq, ach_mbl_tjxk, ach_mbl_ixq, ach_ryn_ixq, ach_mbl_ryn, ach_mbl_kxl, ach_tjx_kxl, ach_tjx_ruq,
        ach_kxl_ruq,
        ach_kxt_kxl, ach_kxt_ruq, ach_tjx_kxt, ach_mbl_kxt, ach_mcr_ixq, ach_mcr_kxl, ach_mcr_kxt,
        ach_mcr_ruq, ach_mcr_mbl, ach_mbl_ruq
    ]
)

ktbl.rubeyalam(a_poroj=1000, ruxeel_tzij=tzij_iximulew, pa_rtl_jlj=ixöq)
ktbl.rubeyalam(a_poroj=1000, ruxeel_tzij=tzij_iximulew)
ktbl.wachibäl("kaib'äl")
ktbl.tayaka("nab'ey samäj")
