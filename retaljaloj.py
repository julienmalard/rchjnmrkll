import numpy as np
import pymc3 as pm


class RetalJaloj(object):
    def __init__(ri, rubi):
        ri.rubi = rubi
        ri.tzij = None

    def ruyaik_tzij(ri, tzij):
        ri.tzij = tzij

    def ruqaxik_pymc(ri, rnjml):
        raise NotImplementedError

    def __str__(ri):
        return ri.rubi


# class RetalCholanil(RetalJaloj):
#     def ruqaxik_pymc(ri, rnjml):
#         if rnjml is not None:
#             raise TypeError
#         else:
#             raise NotImplementedError

class RetalCholajibäl(RetalJaloj):
    def __init__(ri, rubi, ruchlnl):
        super().__init__(rubi)
        ri.ruchlnl = ruchlnl

    def ruqaxik_pymc(ri, rnjml):
        qupinïk = pm.Normal(
            name='ruqupinïk_' + str(ri), mu=0, sd=10, shape=ri.ruchlnl, testval=np.zeros(ri.ruchlnl),
            transform=pm.distributions.transforms.ordered
        )
        return pm.OrderedLogistic(name=str(ri), cutpoints=qupinïk, eta=rnjml, observed=ri.tzij)


class RetalWajun(RetalJaloj):
    def ruqaxik_pymc(ri, rnjml):
        if rnjml is not None:
            return pm.Bernoulli(logit_p=rnjml, observed=ri.tzij)
        else:
            if ri.tzij is not None:
                return ri.tzij
            else:
                raise ValueError("Majun tzij roma ri retal jaloj \"{rjlj}\" rub'i'.".format(rjlj=ri))


class RetalCholanem(RetalJaloj):
    def __init__(ri, rubi, kulbat):
        super().__init__(rubi)
        ri.kulbat = kulbat

    def ruqaxik_pymc(ri, rnjml):
        nmjchl, nmlxl = ri.kulbat
        if rnjml is None:
            return ri.tzij

        if nmjchl is None:
            if nmlxl is None:
                rukexonem = None
            else:
                rukexonem = pm.distributions.transforms.upperbound(nmlxl)

        else:
            if nmlxl is None:
                rukexonem = pm.distributions.transforms.lowerbound(nmjchl)
            else:
                rukexonem = pm.distributions.transforms.interval(nmjchl, nmlxl)

        rjchnm = pm.HalfNormal(name='sg_' + str(ri), sd=10000)  # rujechunem chijun
        return pm.Normal(name=str(ri), mu=rnjml, sd=rjchnm, observed=ri.tzij, transform=rukexonem)
