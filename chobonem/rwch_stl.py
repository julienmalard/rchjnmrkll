from ruwäch_setul import wchbl_setul
from tinamit.Geog.Geog import Geografía as RwchSetul

iximulew = RwchSetul('Perulew Iximulew', archivo='setul/Ruwächulew Iximulew.csv')
iximulew.agregar_frm_regiones('setul/Territorios_v2_-2013-03-15.shp', col_id='COD_MUNI')

wchbl_setul(
    "tunujuch'/pa_perulew_tnjch_pa_rtl_jlj.json", iximulew,
    pa='Municipio',
    jjnkl={f'{i}.0': f'T{i}' for i in range(1, 11)},
    ochochibäl="wchbl_setul"
)
