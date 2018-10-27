import json
import os

import numpy as np
import pymc3 as pm
import scipy.stats as estad
from matplotlib.backends.backend_agg import FigureCanvasAgg as TelaFigura
from matplotlib.figure import Figure as Figura

from achlajil import Achlajil
from rujunamil import Rujunamil


class KutbälPyMC(object):
    def __init__(ri):
        ri.achlajil = set()
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
                ruxeel_tzij.ruyaik_tzij_jlj(chuyu=(pa_rtl_jlj, rajil))
                with pm.Model():
                    ri._chmrsxk_kutbäl(elesaj=pa_rtl_jlj)
                    ri.tunujuch_pa_rtl_jlj[str(rajil)] = pm.sample(**wuj_rbyl_rynl)

    def tayaka(ri, rubi):
        if ri.tunujuch is not None:
            tnjch = {r_jlj: ri.tunujuch[r_jlj].tolist() for r_jlj in ri.tunujuch.varnames}
            with open(rubi + '_tnjch' + '.json', 'w', encoding='utf8') as w:
                json.dump(tnjch, w, ensure_ascii=False)
        if len(ri.tunujuch_pa_rtl_jlj):
            wuj_pa_jlj = {
                rajil: {r_jlj: tnj[r_jlj].tolist() for r_jlj in tnj.varnames}
                for rajil, tnj in ri.tunujuch_pa_rtl_jlj.items()
            }
            with open(rubi + '_tnjch_pa_rtl_jlj' + '.json', 'w', encoding='utf8') as w:
                json.dump(wuj_pa_jlj, w, ensure_ascii=False)

    def wachibäl(ri, ochochibäl=''):

        if ri.tunujuch is not None:
            for r_jlj in ri.tunujuch.varnames:

                tzij = ri.tunujuch[r_jlj]
                x = np.arange(tzij.min(), tzij.max(), (tzij.max() - tzij.min()) / 1000)

                if len(tzij.shape) == 2:
                    for i in range(tzij.shape[1]):
                        ri._ruwachibäl_tunujuch(x, tzij[:, i], str(r_jlj) + str(i), ochochibäl=ochochibäl)
                else:
                    ri._ruwachibäl_tunujuch(x, tzij, str(r_jlj), ochochibäl=ochochibäl)

        if len(ri.tunujuch_pa_rtl_jlj):
            retal_jaloj = list(ri.tunujuch_pa_rtl_jlj.values())[0].varnames
            for r_jlj in retal_jaloj:
                wuj = {}
                kiy = False
                for rajil, tnjch in ri.tunujuch_pa_rtl_jlj.items():
                    tzij = tnjch[r_jlj]
                    wuj[rajil] = tzij
                    kiy = tzij.shape

                nmchjl = min(tz.min() for tz in wuj.values())
                nmlxl = max(tz.max() for tz in wuj.values())
                x = np.arange(nmchjl, nmlxl, (nmlxl - nmchjl) / 1000)
                if len(kiy) == 2:
                    for i in range(kiy[1]):
                        ri._ruwachibäl_tunujuch(
                            x, {raj: wuj[raj][:, i] for raj in wuj},
                            rubi='pajlj_' + str(r_jlj) + str(i), ochochibäl=ochochibäl
                        )
                else:
                    ri._ruwachibäl_tunujuch(x=x, tzij=wuj, rubi='pajlj_' + str(r_jlj), ochochibäl=ochochibäl)

    @staticmethod
    def _ruwachibäl_tunujuch(x, tzij, rubi, ochochibäl=''):

        fig = Figura()
        TelaFigura(fig)
        etajuch = fig.subplots(1, 2)

        etajuch[0].set_title('Jachonem')
        etajuch[1].set_title("Tunujuch'")

        def ruyaik_juch(tz, rb_tz=None):
            y = estad.gaussian_kde(tz)(x)
            etajuch[0].plot(x, y, 'b-', lw=2, alpha=0.6, label=rb_tz, color=None)
            etajuch[1].plot(tz)

        if isinstance(tzij, dict):
            for rb, tzj in tzij.items():
                ruyaik_juch(tzj, rb)
            fig.legend()

        else:
            ruyaik_juch(tz=tzij)

        fig.suptitle(rubi)
        rubi_wuj = 'wchbl_' + rubi + '.png'
        if not os.path.isdir(ochochibäl):
            os.makedirs(ochochibäl)
        fig.savefig(os.path.join(ochochibäl, rubi_wuj))

    def _chmrsxk_kutbäl(ri, elesaj=None):
        if elesaj is None:
            achlajil = ri.achlajil
        else:
            achlajil = [a for a in ri.achlajil if a.ruyonil is not elesaj and a.meyuronil is not elesaj]
        ruwuj_retal_jaloj = {r: None for a in achlajil for r in a.retal_jaloj()}
        rujunamil_ko_na = {
            Rujunamil(r, [a.ruyonil for a in achlajil if a.meyuronil is r])
            for r in ruwuj_retal_jaloj
        }
        while len(rujunamil_ko_na):
            for rjnml in list(rujunamil_ko_na):
                if all(ruwuj_retal_jaloj[r] is not None for r in rjnml.ruyonil):
                    jlj_pymc = rjnml.ruqaxik_pymc(ruwuj_retal_jaloj)
                    ruwuj_retal_jaloj[rjnml.meyuronil] = jlj_pymc

                    rujunamil_ko_na.remove(rjnml)
