import json
import os

import numpy as np
import pymc3 as pm

from achlajil import Achlajil
from rujunamil import Rujunamil
from wachibäl import wchbl_tunujuch, wchbl_sankey


class KutbälPyMC(object):
    def __init__(ri):
        ri.achlajil = set()
        ri.rujunamil = set()

        ri.tunujuch = None
        ri.tunujuch_pa_rtl_jlj = {}

    def ruyaik_achlajil(ri, achljl):
        if isinstance(achljl, Achlajil):
            achljl = [achljl]

        for ach in achljl:
            ri.achlajil.add(ach)

    def elesaj_achlajil(ri, achljl):
        ri.achlajil.remove(achljl)

    def rubeyalam(ri, ruxeel_tzij, a_kamulunem=None, a_poroj=None, pa_rtl_jlj=None):
        wuj_rbyl_rynl = {}
        if a_kamulunem is not None:
            wuj_rbyl_rynl['draws'] = a_kamulunem
        if a_poroj is not None:
            wuj_rbyl_rynl['tune'] = a_poroj

        if pa_rtl_jlj is None:
            ruxeel_tzij.ruyaik_tzij_jlj()
            with pm.Model():
                ri._chmrsxk_kutbäl()
                ri.tunujuch = pm.sample(**wuj_rbyl_rynl)
        else:
            ri.tunujuch_pa_rtl_jlj.clear()
            for rajil in np.unique(ruxeel_tzij[pa_rtl_jlj]):
                print(rajil)
                ruxeel_tzij.ruyaik_tzij_jlj(chuyu=(pa_rtl_jlj, rajil))
                with pm.Model():
                    ri._chmrsxk_kutbäl(elesaj=pa_rtl_jlj)
                    ri.tunujuch_pa_rtl_jlj[str(rajil)] = pm.sample(**wuj_rbyl_rynl)

    def tayaka(ri, rubi, ochochibäl=''):

        if not os.path.isdir(ochochibäl):
            os.makedirs(ochochibäl)

        if ri.tunujuch is not None:
            tnjch = {r_jlj: ri.tunujuch[r_jlj].tolist() for r_jlj in ri.tunujuch.varnames}
            rb_tnjch = rubi + '_tnjch' + '.json'
            if ochochibäl is not None:
                rb_tnjch = os.path.join(ochochibäl, rb_tnjch)
            with open(rb_tnjch, 'w', encoding='utf8') as w:
                json.dump(tnjch, w, ensure_ascii=False)
        if len(ri.tunujuch_pa_rtl_jlj):
            wuj_pa_jlj = {
                rajil: {r_jlj: tnj[r_jlj].tolist() for r_jlj in tnj.varnames}
                for rajil, tnj in ri.tunujuch_pa_rtl_jlj.items()
            }
            rb_pa_rtl_jlj = rubi + '_tnjch_pa_rtl_jlj' + '.json'
            if ochochibäl is not None:
                rb_pa_rtl_jlj = os.path.join(ochochibäl, rb_pa_rtl_jlj)
            with open(rb_pa_rtl_jlj, 'w', encoding='utf8') as w:
                json.dump(wuj_pa_jlj, w, ensure_ascii=False)

    def wachibäl(ri, ochochibäl='', rubeyal='tnjch'):

        if ri.tunujuch is not None:
            wuj_tnjch = {r_jlj: ri.tunujuch[r_jlj] for r_jlj in ri.tunujuch.varnames}
            if rubeyal == 'tnjch':
                wchbl_tunujuch(wuj_tnjch, ochochibäl=ochochibäl)
            elif rubeyal == 'sankey':
                wchbl_sankey(wuj_tnjch, ochochibäl=ochochibäl)

        if len(ri.tunujuch_pa_rtl_jlj):
            wuj_tnjch = {
                rajil: {r_jlj: w_rajil[r_jlj] for r_jlj in w_rajil.varnames}
                for rajil, w_rajil in ri.tunujuch_pa_rtl_jlj.items()
            }
            if rubeyal == 'tnjch':
                wchbl_tunujuch(wuj_tnjch, ochochibäl=ochochibäl, pa_rtl_jlj=True)
            elif rubeyal == 'sankey':
                wchbl_sankey(wuj_tnjch, ochochibäl=ochochibäl, pa_rtl_jlj=True)

    def wachibäl_sankey(ri, ochochibäl=''):
        raise NotImplementedError

    def retal_jaloj(ri):
        return {j for a in ri.achlajil for j in (a.meruyonil, a.ruyonil)}

    def _chmrsxk_kutbäl(ri, elesaj=None):
        if elesaj is None:
            achlajil = ri.achlajil
        else:
            achlajil = [a for a in ri.achlajil if a.ruyonil is not elesaj and a.meruyonil is not elesaj]
        ruwuj_retal_jaloj = {r: None for a in achlajil for r in a.retal_jaloj()}
        rujunamil_ko_na = {
            Rujunamil(r, [a.ruyonil for a in achlajil if a.meruyonil is r])
            for r in ruwuj_retal_jaloj
        }
        while len(rujunamil_ko_na):
            for rjnml in list(rujunamil_ko_na):
                if all(ruwuj_retal_jaloj[r] is not None for r in rjnml.ruyonil):
                    jlj_pymc = rjnml.ruqaxik_pymc(ruwuj_retal_jaloj)
                    ruwuj_retal_jaloj[rjnml.meruyonil] = jlj_pymc

                    rujunamil_ko_na.remove(rjnml)
