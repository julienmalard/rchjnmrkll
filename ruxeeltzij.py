import csv

import numpy as np
import pandas as pd


class RuxeelTzij(object):
    def __init__(ri, yakbäl, r_jlj, menaon='NA'):
        ri.yakbäl = yakbäl
        ri.r_jlj = r_jlj
        ri.menaon = menaon

        ri.tzij = ri._rusikij_tzij()

    def _rusikij_tzij(ri):

        with open(ri.yakbäl, 'r') as w:
            rusikinel = csv.DictReader(w)
            wuj = {j: [] for j in ri.r_jlj}
            for ch in rusikinel:
                for j, rxl in wuj.items():
                    rxl.append(float(ch[j]) if ch[j] != ri.menaon else np.nan)

            wuj_pd = pd.DataFrame(wuj)
            wuj_pd.dropna(inplace=True)

        return wuj_pd

    def ruyaik_tzij_jlj(ri, chuyu=None):
        for rubi, j in ri.r_jlj.items():
            if chuyu is None:
                rajil = ri.tzij[rubi].values
            else:
                rajil = ri.tzij[rubi][ri[chuyu[0]] == chuyu[1]].values
            j.ruyaik_tzij(rajil)

    def __getitem__(ri, wchnq):
        if isinstance(wchnq, str):
            return ri.tzij[wchnq].values
        else:
            return ri.tzij[next(x for x in ri.r_jlj if ri.r_jlj[x] == wchnq)].values