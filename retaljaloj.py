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


class RetalWajun(RetalJaloj):
    def ruqaxik_pymc(ri, rnjml):
        if rnjml is not None:
            return pm.Bernoulli(logit_p=rnjml, observed=ri.tzij)
        else:
            return ri.tzij


class RetalCholanem(RetalJaloj):
    def __init__(ri, rubi, kulbat):
        super().__init__(rubi)
        ri.kulbat = kulbat

    def ruqaxik_pymc(ri, rnjml):
        nmlxl, nmjchl = ri.kulbat
        if rnjml is None:
            return ri.tzij

        rjchnm = pm.HalfNormal(name='sg_' + str(jlj), sd=10000)  # rujechunem chijun
        if nmlxl is None:
            if nmjchl is None:
                return pm.Normal(name=str(ri), mu=rnjml, sd=rjchnm, observed=ri.tzij)
            else:
                raise NotImplementedError
        else:
            if nmjchl is None:
                raise NotImplementedError
            else:
                raise NotImplementedError
