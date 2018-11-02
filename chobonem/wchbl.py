from chobonem.kutbäl_mrc import ktbl
from chobonem.kutbäl_mrc import tzij_iximulew
from wachibäl import wchbl_sankey, wchbl_tunujuch

kibi = {
    'MCR': 'MCR | ISA',
    "meb'a'il": "Meb'a'il | Pobreza",
    "ruq'a'": "Ruq'a' | Rural",
    "tijoxïk": "Tijoxïk | Estudios",
    "ixöq": "Ruk'ojlem | Género",
    "ruyon": 'Ruyon | Solter@',
    "kaxlan": 'Winaqilil | Etnicidad',
    "kaxlan tzij": "Chab'äl | Idioma"

}

wchbl_sankey("tunujuch'/pa_amaq_tnjch.json", ktbl, tzij_iximulew, "wchbl_amaq/sankey", kibi=kibi)
wchbl_sankey(
    "tunujuch'/pa_ruk'ojlem_tnjch_pa_rtl_jlj.json", ktbl, tzij_iximulew, "wchbl_ruk'ojnem/sankey", pa_rtl_jlj='ixöq',
    kibi=kibi
)
wchbl_sankey(
    "tunujuch'/pa_perulew_tnjch_pa_rtl_jlj.json", ktbl, tzij_iximulew, "wchbl_prlw/sankey", pa_rtl_jlj="perulew",
    kibi=kibi
)

wchbl_tunujuch("tunujuch'/pa_amaq_tnjch.json", "wchbl_amaq/tnjch")
wchbl_tunujuch("tunujuch'/pa_perulew_tnjch_pa_rtl_jlj.json", "wchbl_prlw/tnjch", pa_rtl_jlj=True)
wchbl_tunujuch("tunujuch'/pa_ruk'ojlem_tnjch_pa_rtl_jlj.json", "wchbl_ruk'ojnem/tnjch", pa_rtl_jlj=True)
