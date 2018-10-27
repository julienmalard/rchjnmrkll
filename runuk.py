import pymc3 as pm


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
        with pm.Model():
            ri._chmrsxk_kutbäl()
            ri.tunujuch = pm.sample(a_kamulunem, n_init=a_poroj)

    def kaibäl(ri):
        pass

    def _chmrsxk_kutbäl(ri):
        retal_jaloj = {r: None for a in ri.achlajil for r in a.retal_jaloj()}
        rujunamil_ko_na = {
            Rujunamil(r, [a.ruyonil for a in ri.achlajil if a.meyuronil is r])
            for r in retal_jaloj
        }
        while len(rujunamil_ko_na):
            for rjnml in list(rujunamil_ko_na):
                if all(retal_jaloj[r] is not None for r in rjnml.ruyonil):

                    jlj_pymc = rjnml.ruqaxik_pymc(retal_jaloj)
                    retal_jaloj[rjnml.meruyonil] = jlj_pymc

                    rujunamil_ko_na.remove(rjnml)


class RuxeelTzij(object):
    def __init__(ri, yakbäl):
        ri.yakbäl = yakbäl

    def ruyaik_jaloj(símismo, jaloj, rubi):
        pass


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
        rnjml =

        return jlj.ruqaxik_pymc(rnjml)
