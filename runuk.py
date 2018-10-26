import pymc3 as pm


class KutbälPyMC(object):
    def __init__(ri):
        ri.achlajil = set()

    def junumaj_achlajil(ri, achljl):
        ri.achlajil.add(achljl)

    def elesaj_achlajil(ri, achljl):
        ri.achlajil.remove(achljl)

    def rubeyalam(ri, a_kamulunem, a_poroj):
        with pm.Model() as mod:
            trz = pm.sample()

    def kaibäl(ri):
        pass


class Achlajil(object):

    def __init__(ri, ruyonil, meyuronil):

        ri.meyuronil = meyuronil
        ri.ruyonil = ruyonil


class RetalJaloj(object):
    def __init__(ri, rubi):
        ri.rubi = rubi

class RetalCholanil(RetalJaloj):
    pass
