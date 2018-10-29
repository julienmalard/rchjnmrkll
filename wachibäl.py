import json
import os

import numpy as np
import plotly.offline as py
import seaborn as sns
from matplotlib.backends.backend_agg import FigureCanvasAgg as TelaFigura
from matplotlib.figure import Figure as Figura
from scipy import stats as estad


def wchbl_tunujuch(tnjch, ochochibäl='', pa_rtl_jlj=False):
    if isinstance(tnjch, str):
        tnjch = _rujaqïk_json(tnjch)

    if not pa_rtl_jlj:
        for r_jlj, tzij in tnjch.items():

            x = np.arange(tzij.min(), tzij.max(), (tzij.max() - tzij.min()) / 1000)

            if len(tzij.shape) == 2:
                for i in range(tzij.shape[1]):
                    _wchbl_tunujuch(x, tzij[:, i], str(r_jlj) + str(i), ochochibäl=ochochibäl)
            else:
                _wchbl_tunujuch(x, tzij, str(r_jlj), ochochibäl=ochochibäl)
    else:
        retal_jaloj = list(list(tnjch.values())[0])
        for r_jlj in retal_jaloj:
            wuj = {}
            kiy = False
            for rajil, tnj in tnjch.items():
                tzij = tnj[r_jlj]
                wuj[rajil] = tzij
                kiy = tzij.shape

            nmchjl = min(tz.min() for tz in wuj.values())
            nmlxl = max(tz.max() for tz in wuj.values())
            x = np.arange(nmchjl, nmlxl, (nmlxl - nmchjl) / 1000)
            if len(kiy) == 2:
                for i in range(kiy[1]):
                    _wchbl_tunujuch(
                        x, {raj: wuj[raj][:, i] for raj in wuj},
                        rubi='pajlj_' + str(r_jlj) + str(i), ochochibäl=ochochibäl
                    )
            else:
                _wchbl_tunujuch(x=x, tzij=wuj, rubi='pajlj_' + str(r_jlj), ochochibäl=ochochibäl)


def _wchbl_tunujuch(x, tzij, rubi, ochochibäl):
    fig = Figura()
    TelaFigura(fig)
    etajuch = fig.subplots(1, 2)

    etajuch[0].set_title('Jachonem')
    etajuch[1].set_title("Tunujuch'")

    def ruyaik_juch(tz, rb_tz=None):
        y = estad.gaussian_kde(tz)(x)
        etajuch[0].plot(x, y, 'b-', lw=2, alpha=0.6, label=rb_tz, color=None)
        etajuch[1].plot(tz)

    if isinstance(tzij, dict):
        for rb, tzj in tzij.items():
            ruyaik_juch(tzj, rb)
        fig.legend()

    else:
        ruyaik_juch(tz=tzij)

    fig.suptitle(rubi)
    rubi_wuj = 'wchbl_' + rubi + '.png'
    if len(ochochibäl) and not os.path.isdir(ochochibäl):
        os.makedirs(ochochibäl)
    fig.savefig(os.path.join(ochochibäl, rubi_wuj))


def wchbl_sankey(tnjch, kutbäl, rxl_tzij, ochochibäl='', pa_rtl_jlj=None):
    if isinstance(tnjch, str):
        tnjch = _rujaqïk_json(tnjch)

    if len(ochochibäl) and not os.path.isdir(ochochibäl):
        os.makedirs(ochochibäl)

    rubi = "rutojtob'enïk"

    if pa_rtl_jlj is None:
        _wchbl_sankey(tnjch, kutbäl, rubi=rubi, rxl_tzj=rxl_tzij, ochochibäl=ochochibäl)
    else:
        for rjl, tnj in tnjch.items():
            _wchbl_sankey(
                tnj, kutbäl, rubi=rubi + str(rjl), rxl_tzj=rxl_tzij, elesaj=pa_rtl_jlj, ochochibäl=ochochibäl
            )


def _wchbl_sankey(tnjch, kutbäl, rubi, rxl_tzj, ochochibäl, elesaj=None):
    retal_jaloj = [x for x in kutbäl.retal_jaloj() if str(x) != elesaj]

    achlajil = [a for a in kutbäl.achlajil if elesaj not in [str(a.ruyonil), str(a.meruyonil)]]
    ruxeel = np.array(
        [retal_jaloj.index(a.ruyonil) for a in achlajil])
    chuwäch = np.array([
        retal_jaloj.index(a.meruyonil) for a in achlajil
    ])

    rajil = np.array([
        tnjch[f'rutikik_{retal_jaloj[ryn]}_chwch_{retal_jaloj[mryn]}'].mean()
        for ryn, mryn in zip(ruxeel, chuwäch)
    ])

    alphas = [
        np.mean(np.sign(tnjch[f'rutikik_{retal_jaloj[ryn]}_chwch_{retal_jaloj[mryn]}']) == np.sign(rjl))
        for ryn, mryn, rjl in zip(ruxeel, chuwäch, rajil)
    ]

    rajil = np.abs(rajil)
    rajil *= np.array([np.std(rxl_tzj[retal_jaloj[ryn]]) for ryn in ruxeel])

    runimilem = {jlj: None for jlj in retal_jaloj}
    while any(rnml is None for rnml in runimilem.values()):
        for jlj in [j for j in retal_jaloj if runimilem[j] is None]:
            i_jlj = retal_jaloj.index(jlj)
            jlj_mrynl = [a.meruyonil for a in achlajil if a.ruyonil is jlj]
            kinimilem_mrynl = [runimilem[j] for j in jlj_mrynl]
            if all([nmlm is not None for nmlm in kinimilem_mrynl]):
                rjl = rajil[
                    np.where(np.logical_and(ruxeel == i_jlj,
                                            np.isin(chuwäch, [retal_jaloj.index(mryn) for mryn in jlj_mrynl])))

                ]
                rnmlm = 1 if not len(kinimilem_mrynl) else np.sum(kinimilem_mrynl * rjl)
                runimilem[jlj] = rnmlm

                i_chw = np.where(chuwäch == i_jlj)
                knjl = np.sum(rajil[i_chw])
                rajil[i_chw] *= rnmlm / knjl
    rubonil = [r for r in sns.color_palette('Dark2', len(retal_jaloj))]
    rubonil_jlj = [f'rgb({int(r[0]*255)}, {int(r[1]*255)}, {int(r[2]*255)})' for r in rubonil]

    rubonil_achljl = [
        f'rgba({int(rubonil[j][0]*255)}, {int(rubonil[j][1]*255)}, {int(rubonil[j][2]*255)}, {a*.7})'
        for j, a in zip(ruxeel, alphas)
    ]
    tzij = dict(
        type='sankey',
        node=dict(
            pad=15,
            thickness=20,
            line=dict(
                color="black",
                width=0.5
            ),
            label=[str(j) for j in retal_jaloj],
            color=rubonil_jlj
        ),
        link=dict(
            source=ruxeel,
            target=chuwäch,
            value=rajil,
            color=rubonil_achljl
        ))
    rbyl = dict(
        title=rubi,
        font=dict(
            size=10
        )
    )
    wchbl = dict(data=[tzij], layout=rbyl)

    py.plot(
        wchbl, image='jpeg', filename=os.path.join(ochochibäl, rubi) + '.html', image_filename='rtjtbnk',
        show_link=False, auto_open=False
    )


def _rujaqïk_json(rubi):
    with open(rubi, mode='r', encoding='utf-8') as w:
        js = json.load(w)

    def ruqaxïk_np(x):
        for rep, rajil in x.items():
            if isinstance(rajil, dict):
                ruqaxïk_np(rajil)
            else:
                if isinstance(rajil, list):
                    x[rep] = np.array(rajil)

    ruqaxïk_np(js)
    return js
