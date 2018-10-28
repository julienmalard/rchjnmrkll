import os

import numpy as np

from tinamit.Geog.Geog import Geografía as RwchSetul
from wachibäl import _rujaqïk_json


def wchbl_setul(tnjch, setul, pa, jjnkl=None, ochochibäl=''):
    """

    Parameters
    ----------
    tnjch
    setul: RwchSetul
    jjnkl
    ochochibäl

    Returns
    -------

    """

    if isinstance(tnjch, str):
        tnjch = _rujaqïk_json(tnjch)
    if len(ochochibäl) and not os.path.isdir(ochochibäl):
        os.makedirs(ochochibäl)

    retal_jaloj = list(list(tnjch.values())[0])
    for jlj in retal_jaloj:
        wuj = {}
        alphas = {}
        for prj, tnj in tnjch.items():
            rajil = tnj[jlj].mean()
            if rajil < 0:
                alph = np.mean(tnj[jlj] < 0) * .8
            elif rajil > 0:
                alph = np.mean(tnj[jlj] > 0) * .8
            else:
                alph = 0

            prj_stl = prj if jjnkl is None else jjnkl[prj]
            kiyatzuk = setul.obt_lugares_en(prj_stl, escala=pa)
            wuj.update({ky: rajil for ky in kiyatzuk})
            alphas.update({ky: alph for ky in kiyatzuk})
        nmjchl = np.min(list(wuj.values()))
        nmlxl = np.max(list(wuj.values()))
        if nmjchl < 0:
            if nmlxl > 0:
                nmlj = max(abs(nmjchl), abs(nmlxl))
                runimilem = (-nmlj, nmlj)
                rubonil = None
            else:
                rubonil = ['#FF6666', '#FFCC66']
                runimilem = (nmjchl, nmlxl)
        else:
            runimilem = (nmjchl, nmlxl)
            rubonil = ['#FFCC66', '#00CC66']

        setul.dibujar(
            os.path.join(ochochibäl, jlj), valores=wuj, alpha=alphas, título=jlj,
            escala_num=runimilem, colores=rubonil
        )
