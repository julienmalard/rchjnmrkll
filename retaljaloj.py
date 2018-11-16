import numpy as np
import pymc3 as pm


class RetalJaloj(object):
    def __init__(ri, rubi):
        ri.rubi = rubi

    def ruqaxik_pymc(ri, rjnml, rxl_tzj):
        tzij = ri._rukexonem_tzij(rxl_tzj[ri])

        if rjnml is not None:
            return ri._rubanom_jlj_pymc(rjnml, tzij)
        else:
            if tzij is not None:
                return tzij
            else:
                raise ValueError("Majun tzij roma ri retal jaloj \"{rjlj}\" rub'i'.".format(rjlj=ri))

    def _rubanom_jlj_pymc(ri, rjnml, tzij):
        raise NotImplementedError

    def _rukexonem_tzij(ri, tzij):
        raise NotImplementedError

    def __str__(ri, ):
        return ri.rubi


class RetalCholanil(RetalJaloj):
    def _rubanom_jlj_pymc(ri, rjnml, rxl_tzj):
        if rjnml is not None:
            raise TypeError
        else:
            raise NotImplementedError

    def _rukexonem_tzij(ri, tzij):
        raise NotImplementedError


class RetalCholajibäl(RetalJaloj):
    def __init__(ri, rubi, ruchlnl):
        super().__init__(rubi)
        ri.ruchlnl = ruchlnl

    def _rubanom_jlj_pymc(ri, rjnml, tzij):
        qupinïk = pm.Normal(
            name='ruqupinïk_' + str(ri), mu=[-1, 0, 1], sd=10, shape=ri.ruchlnl - 1,
            transform=pm.distributions.transforms.ordered
        )
        return pm.OrderedLogistic(name=str(ri), cutpoints=qupinïk, eta=rjnml, observed=tzij)

    def _rukexonem_tzij(ri, tzij):
        return tzij


class RetalWajun(RetalCholajibäl):
    def __init__(ri, rubi):
        super().__init__(rubi, ruchlnl=2)

    def _rubanom_jlj_pymc(ri, rjnml, tzij):
        b = pm.Normal(
            name='junelïk_' + str(ri), mu=0, sd=100
        )
        return pm.Bernoulli(name=str(ri), logit_p=rjnml + b, observed=tzij)

    def _rukexonem_tzij(ri, tzij):
        return tzij


class RetalCholanem(RetalJaloj):
    def __init__(ri, rubi, kulbat):
        super().__init__(rubi)
        ri.kulbat = kulbat

    def _rubanom_jlj_pymc(ri, rjnml, tzij):

        klbt = ri.kulbat

        if klbt[0] is None:
            if klbt[1] is None:
                b = pm.Normal(
                    name='junelïk_' + str(ri), mu=0, sd=100
                )
                sigma = pm.HalfNormal(name='sg_' + str(ri), sd=10)  # rujechunem chijun
                jachonem = pm.Normal(name=str(ri), mu=rjnml + b, sd=sigma, observed=tzij)
            else:
                jachonem = pm.Normal(name=str(ri), mu=rjnml + b, sd=sigma,
                                     observed=tzij)  # jachonem = -pm.Gamma(name=str(ri), mu=pm.math.exp(rjnml + b), sd=sigma, observed=tzij) + klbt[1]
        else:
            if klbt[1] is None:
                b = pm.Normal(
                    name='junelïk_' + str(ri), mu=0, sd=100
                )
                sigma = pm.HalfNormal(name='sg_' + str(ri), sd=10)  # rujechunem chijun
                jachonem = pm.Normal(name=str(ri), mu=rjnml + b, sd=sigma, observed=tzij)
                # jachonem = pm.Gamma(name=str(ri), mu=pm.math.exp(rjnml + b), sd=sigma, observed=tzij) + klbt[0]
            else:
                b = pm.Normal(
                    name='junelïk_' + str(ri), mu=0, sd=100
                )
                sigma = pm.HalfNormal(name='sg_' + str(ri), sd=10)  # rujechunem chijun
                jachonem = pm.Normal(name=str(ri), mu=rjnml + b, sd=sigma, observed=tzij)

        return jachonem

    def _rukexonem_tzij(ri, tzij):
        if tzij is None:
            return tzij

        klbt = ri.kulbat

        if klbt[0] is None:
            if klbt[1] is None:
                # (-mk's, +mk's)
                return (tzij - np.mean(tzij)) / np.std(tzij)
            else:
                # (-mk's, Q]
                raise NotImplementedError
        else:
            if klbt[1] is None:
                # [Q, +mk's)
                return (tzij - klbt[0]) / np.std(tzij)
            else:
                # [Q, Q]
                return _ajilatik((tzij - klbt[0]) / (klbt[1] - klbt[0]), eps=1e-5)


def _me_ajilatik(x):
    return 1 / (np.exp(-x) + 1)


def _ajilatik(x, eps):
    x = x * (1 - eps) + (eps / 2)
    return np.log(x / (1 - x))
