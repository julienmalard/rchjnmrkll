import json
import os

import pymc3 as pm

from wachibäl import wchbl_tunujuch, wchbl_sankey


class Beyalil(object):
    def __init__(ri, rjnml, rxltzij, a_kamulunem=None, a_poroj=None, pa=None, rchn_pymc3=None):
        ri.rujunamil = rjnml
        ri.rxltzij = rxltzij

        if rchn_pymc3 is None:
            rchn_pymc3 = {}
        if a_kamulunem is not None:
            rchn_pymc3['draws'] = a_kamulunem
        if a_poroj is not None:
            rchn_pymc3['tune'] = a_poroj

        with pm.Model():
            ri._chmrsxk_kutbäl(pa=pa)
            ri.tunujuch = Tunujuch(pm.sample(**rchn_pymc3))

    def rubanom(ri, rtl_jlj, chirij):
        if ri.tunujuch is None:
            raise ValueError()

        rubi_jlj = f'rutikik_{rtl_jlj}_chirij_{chirij}'

        return ri.tunujuch[rubi_jlj]

    def _chmrsxk_kutbäl(ri, pa=None):
        if pa is None:
            konojel_rjnml = set(ri.rujunamil)
        else:
            konojel_rjnml = set(rjn for rjn in ri.rujunamil if rjn.ruyonil is not pa and pa not in rjn.meruyonil)

        ruwuj_retal_jaloj = {rjn.meruyonil: None for rjn in ri.rujunamil}

        while len(konojel_rjnml):
            for rjnml in list(konojel_rjnml):
                if all(ruwuj_retal_jaloj[r] is not None for r in rjnml.ruyonil):
                    jlj_pymc = rjnml.ruqaxik_pymc(ruwuj_retal_jaloj, ri.rxltzij)
                    ruwuj_retal_jaloj[rjnml.meruyonil] = jlj_pymc

                    konojel_rjnml.remove(rjnml)

    def ruyaik(ri, rubi, ochochibäl=''):

        if not os.path.isdir(ochochibäl):
            os.makedirs(ochochibäl)

        tnjch = {r_jlj: ri.tunujuch[r_jlj].tolist() for r_jlj in ri.tunujuch}
        rb_tnjch = rubi + '_tnjch' + '.json'

        if ochochibäl is not None:
            rb_tnjch = os.path.join(ochochibäl, rb_tnjch)
        with open(rb_tnjch, 'w', encoding='utf8') as w:
            json.dump(tnjch, w, ensure_ascii=False)

    def wachibäl(ri, ochochibäl='', rubeyal='tnjch'):

        if ri.tunujuch is not None:
            wuj_tnjch = {r_jlj: ri.tunujuch[r_jlj] for r_jlj in ri.tunujuch}
            if rubeyal == 'tnjch':
                wchbl_tunujuch(wuj_tnjch, ochochibäl=ochochibäl)
            elif rubeyal == 'sankey':
                wchbl_sankey(wuj_tnjch, ri.rujunamil, ochochibäl=ochochibäl)


class Tunujuch(object):
    def __init__(ri, tnjch_pymc3):
        ri.tunujuch = {jlj: tnjch_pymc3[jlj] for jlj in tnjch_pymc3.varnames}

    def __getitem__(ri, wchnq):
        return ri.tunujuch[wchnq]

    def __iter__(ri):
        for jlj in ri.tunujuch:
            yield jlj
