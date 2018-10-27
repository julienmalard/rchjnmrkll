import pymc3 as pm


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
                rnjml = a * retal_jaloj[rynl]
            else:
                rnjml = rnjml + a * retal_jaloj[rynl]

        return jlj.ruqaxik_pymc(rnjml)

    def __str__(ri):
        return str(ri.meyuronil)