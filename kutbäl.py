import json
import os

import numpy as np
import pymc3 as pm

from achlajil import Achlajil
from beyalil import Beyalil
from rujunamil import Rujunamil
from wachibäl import wchbl_tunujuch, wchbl_sankey


class KutbälPyMC(object):
    def __init__(ri, achljl=None):
        ri.achlajil = set()
        ri.rujunamil = set()

        if achljl is not None:
            ri.ruyaik_achlajil(achljl)

    def ruyaik_achlajil(ri, achljl):
        if isinstance(achljl, Achlajil):
            achljl = [achljl]

        ri.achlajil.clear()
        for ach in achljl:
            ri.achlajil.add(ach)

        ri._ruchmsxk_rujunumalil()

    def retal_jaloj(ri):
        return {rjn.meruyonil for rjn in ri.rujunamil}

    def _ruchmsxk_rujunumalil(ri):
        ri.rujunamil.clear()

        retal_jaloj = {j for a in ri.achlajil for j in [a.meruyonil, a.ruyonil]}

        ri.rujunamil.update({
            Rujunamil(r, [a.ruyonil for a in ri.achlajil if a.meruyonil is r])
            for r in retal_jaloj
        })

    def rubeyalem(ri, rxl_tzj, a_kamulunem=None, a_poroj=None, pa=None, rchn_pymc3=None):

        return Beyalil(
            rjnml=ri.rujunamil, rxltzij=rxl_tzj,
            a_kamulunem=a_kamulunem, a_poroj=a_poroj, pa=pa, rchn_pymc3=rchn_pymc3
        )
