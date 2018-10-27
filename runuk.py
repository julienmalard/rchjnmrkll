import numpy as np
import pymc3 as pm
import scipy.stats as estad
from matplotlib.backends.backend_agg import FigureCanvasAgg as TelaFigura
from matplotlib.figure import Figure as Figura


class KutbälPyMC(object):
    def __init__(ri):
        ri.achlajil = set()
        ri.tunujuch = None

    def ruyaik_achlajil(ri, achljl):

        for ach in achljl:
            ri.achlajil.add(ach)

    def elesaj_achlajil(ri, achljl):
        ri.achlajil.remove(achljl)

    def rubeyalam(ri, a_kamulunem=None, a_poroj=None):
        wuj_rbyl_rynl = {}
        if a_kamulunem is not None:
            wuj_rbyl_rynl['draws'] = a_kamulunem
        if a_poroj is not None:
            wuj_rbyl_rynl['tune'] = a_poroj
        with pm.Model():
            ri._chmrsxk_kutbäl()
            ri.tunujuch = pm.sample(**wuj_rbyl_rynl)

    def kaibäl(ri):

        for r_jlj in ri.tunujuch.varnames:

            tzij = ri.tunujuch[r_jlj]
            x = np.arange(tzij.min(), tzij.max(), (tzij.max() - tzij.min()) / 1000)

            if len(tzij.shape) == 2:
                for i in range(tzij.shape[1]):
                    ri._ruwachibäl_tunujuch(x, tzij[:, i], str(r_jlj) + str(i))
            else:
                ri._ruwachibäl_tunujuch(x, tzij, str(r_jlj))

    @staticmethod
    def _ruwachibäl_tunujuch(x, tzij, rubi):

        fig = Figura()
        TelaFigura(fig)
        etajuch = fig.subplots(1, 2)

        y = estad.gaussian_kde(tzij)(x)

        etajuch[0].plot(x, y, 'b-', lw=2, alpha=0.6)
        etajuch[0].set_title('Jachonem')

        etajuch[1].plot(tzij)
        etajuch[1].set_title("Tunujuch'")
        fig.suptitle(rubi)
        fig.savefig('wchbl_' + rubi + '.png')

    def _chmrsxk_kutbäl(ri):
        ruwuj_retal_jaloj = {r: None for a in ri.achlajil for r in a.retal_jaloj()}
        rujunamil_ko_na = {
            Rujunamil(r, [a.ruyonil for a in ri.achlajil if a.meyuronil is r])
            for r in ruwuj_retal_jaloj
        }
        while len(rujunamil_ko_na):
            for rjnml in list(rujunamil_ko_na):
                if all(ruwuj_retal_jaloj[r] is not None for r in rjnml.ruyonil):
                    jlj_pymc = rjnml.ruqaxik_pymc(ruwuj_retal_jaloj)
                    ruwuj_retal_jaloj[rjnml.meyuronil] = jlj_pymc

                    rujunamil_ko_na.remove(rjnml)


class Achlajil(object):

    def __init__(ri, meyuronil, ruyonil):
        ri.meyuronil = meyuronil
        ri.ruyonil = ruyonil

    def retal_jaloj(ri):
        return [ri.meyuronil, ri.ruyonil]


class Rujunamil(object):
    def __init__(ri, meyuronil, ruyonil):
        ri.meyuronil = meyuronil
        ri.ruyonil = ruyonil

    def ruqaxik_pymc(ri, retal_jaloj):
        jlj = ri.meyuronil
        rnjml = None
        for rynl in ri.ruyonil:
            a = pm.Normal(
                name='rutikik_' + str(rynl) + '_chwch_' + str(jlj),
                mu=0, sd=100
            )

            if rnjml is None:
                b = pm.Normal(
                    name='junelïk_' + str(jlj), mu=0, sd=100
                )
                rnjml = a * retal_jaloj[rynl] + b
            else:
                rnjml = rnjml + a * retal_jaloj[rynl]

        return jlj.ruqaxik_pymc(rnjml)

    def __str__(ri):
        return str(ri.meyuronil)
