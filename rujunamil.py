import pymc3 as pm


class Rujunamil(object):
    def __init__(ri, meruyonil, ruyonil):
        ri.meruyonil = meruyonil
        ri.ruyonil = ruyonil

    def ruqaxik_pymc(ri, retal_jaloj, rxl_tzj):
        jlj = ri.meruyonil
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

        return jlj.ruqaxik_pymc(rnjml, rxl_tzj=rxl_tzj)

    def __str__(ri):
        return str(ri.meruyonil) + '~' + ' + '.join([str(j) for j in ri.ruyonil])
