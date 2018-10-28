from wachibäl import wchbl_sankey, wchbl_tunujuch

wchbl_sankey("tunujuch'/pa_amaq_tnjch.json", "wchbl_amaq/sankey")
wchbl_sankey("tunujuch'/pa_perulew_tnjch_pa_rtl_jlj.json", "wchbl_prlw/sankey", pa_rtl_jlj=True)
wchbl_sankey("tunujuch'/pa_ruk'ojlem_tnjch_pa_rtl_jlj.json", "wchbl_ruk'ojnem/sankey", pa_rtl_jlj=True)

wchbl_tunujuch("tunujuch'/pa_amaq_tnjch.json", "wchbl_amaq/tnjch")
wchbl_tunujuch("tunujuch'/pa_perulew_tnjch_pa_rtl_jlj.json", "wchbl_prlw/tnjch", pa_rtl_jlj=True)
wchbl_tunujuch("tunujuch'/pa_ruk'ojlem_tnjch_pa_rtl_jlj.json", "wchbl_ruk'ojnem/tnjch", pa_rtl_jlj=True)
