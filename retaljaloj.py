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

    def r2(ri, rxl_tzj, tnjch, ryn):
        raise NotImplementedError

    def __str__(ri, ):
        return ri.rubi


class RetalCholanil(RetalJaloj):
    def ruqaxik_pymc(ri, rnjml):
        if rnjml is not None:
            raise TypeError
        else:
            raise NotImplementedError


class RetalCholajibäl(RetalJaloj):
    def __init__(ri, rubi, ruchlnl):
        super().__init__(rubi)
        ri.ruchlnl = ruchlnl

    def ruqaxik_pymc(ri, rnjml):
        qupinïk = pm.Normal(
            name='ruqupinïk_' + str(ri), mu=[-1, 0, 1], sd=10, shape=ri.ruchlnl - 1,
            transform=pm.distributions.transforms.ordered
        )
        return pm.OrderedLogistic(name=str(ri), cutpoints=qupinïk, eta=rnjml, observed=ri.tzij)

    def r2(ri, rxl_tzj, tnjch, ryn):
        return 1
        # qitzij = rxl_tzj[ri].astype(int)
        #
        # qupinïk = tnjch[f'ruqupinïk_{ri}']
        # nu = np.sum(np.array([tnjch[f'rutikik_{r}_chwch_{ri}'][..., np.newaxis] * rxl_tzj[r] for r in ryn]), axis=0)
        #
        # kuxbej_0 = np.array([np.mean(qitzij == x) for x in range(ri.ruchlnl)])
        # ajilatikoj_0 = -np.mean(np.log(kuxbej_0[qitzij]))
        #
        # return 1 - ri._ajilatikoj_kuxbej(qitzij, qupinïk, nu) / ajilatikoj_0

    def _ajilatikoj_kuxbej(ri, qitzij, qupinïk, nu):
        f = np.zeros(qitzij.shape)
        waix = qitzij == 0
        f[waix] = np.mean(1 - _me_ajilatik(nu[:, waix] - qupinïk[:, 0:1]), axis=0)
        chpm = np.logical_and(np.less(0, qitzij), np.less(qitzij, ri.ruchlnl - 1))
        f[chpm] = np.mean(
            _me_ajilatik(nu[:, chpm] - qupinïk[:, qitzij[chpm] - 1]) -
            _me_ajilatik(nu[:, chpm] - qupinïk[:, qitzij[chpm]]),
            axis=0
        )
        nim = qitzij == (ri.ruchlnl - 1)
        f[nim] = np.mean(_me_ajilatik(nu[:, nim] - qupinïk[:, -1:None]), axis=0)
        return -np.mean(np.log(f))


class RetalWajun(RetalCholajibäl):
    def __init__(ri, rubi):
        super().__init__(rubi, ruchlnl=2)

    def ruqaxik_pymc(ri, rnjml):
        if rnjml is not None:
            b = pm.Normal(
                name='junelïk_' + str(ri), mu=0, sd=100
            )
            return pm.Bernoulli(name=str(ri), logit_p=rnjml + b, observed=ri.tzij)
        else:
            if ri.tzij is not None:
                return ri.tzij
            else:
                raise ValueError("Majun tzij roma ri retal jaloj \"{rjlj}\" rub'i'.".format(rjlj=ri))

    def r2(ri, rxl_tzj, tnjch, ryn):
        return 1
        if not len(ryn):
            return 1
        qitzij = rxl_tzj[ri].astype(int)

        nu = np.sum(np.array([tnjch[f'rutikik_{r}_chwch_{ri}'][..., np.newaxis] * rxl_tzj[r] for r in ryn]), axis=0)
        b = tnjch[f'junelïk_{ri}'][..., np.newaxis]
        eps = 1e-15
        f = np.clip(nu + b, eps, 1 - eps)
        kuxbej = _me_ajilatik(np.mean(f, axis=0))

        kuxbej_0 = np.mean(qitzij)

        return 1 - ri._ajilatikoj(qitzij, kuxbej) / ri._ajilatikoj(qitzij, kuxbej_0)

    def _ajilatikoj(ri, qtzj, kxbj):
        return -np.mean(np.log(np.where(qtzj, kxbj, 1 - kxbj)))


class RetalCholanem(RetalJaloj):
    def __init__(ri, rubi, kulbat):
        super().__init__(rubi)
        ri.kulbat = kulbat

    def ruqaxik_pymc(ri, rnjml):
        if rnjml is None:
            return ri.tzij

        rjchnm = pm.HalfNormal(name='sg_' + str(ri), sd=10)  # rujechunem chijun
        b = pm.Normal(
            name='junelïk_' + str(ri), mu=0, sd=100
        )
        return pm.Normal(name=str(ri), mu=rnjml + b, sd=rjchnm, observed=ri.tzij)

    def r2(ri, rxl_tzj, tnjch, ryn):
        return 1-np.mean(tnjch[f'sg_{ri}']) / np.std(rxl_tzj[ri])

        # qitzij = rxl_tzj[ri].astype(int)
        # nu = np.sum(np.array([tnjch[f'rutikik_{r}_chwch_{ri}'][..., np.newaxis] * rxl_tzj[r] for r in ryn]), axis=0)
        # rejqalem = np.mean(nu + tnjch[f'junelïk_{ri}'][..., np.newaxis], axis=0)
        #
        # r2 = 1 - np.sum(np.square(qitzij - rejqalem)) / np.sum(np.square(qitzij - np.mean(qitzij)))
        #
        # return r2

    def _rukexonem(ri, x):
        nmjchl, nmlxl = ri.kulbat
        if nmjchl is None:
            if nmlxl is None:
                return x
            else:
                return np.log(-(x - nmlxl) + 1e-5)
        else:
            if nmlxl is None:
                return np.log(x-nmjchl + 1e-5)
            else:
                x = np.clip(x, nmjchl + 1e-5, nmlxl-1e-5)
                y = (x-nmjchl) / (nmlxl - nmjchl)
                return np.log(y / (1-y))


def _me_ajilatik(x):
    return 1 / (np.exp(-x) + 1)


def _ajilatik(x):
    return np.log(x / (1 - x))
