import json
import os

import numpy as np
import plotly.io as pio
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


def wchbl_sankey(tnjch, rujunamil, ochochibäl='', pa_rtl_jlj=None, kibi=None, rubi_lema='Sankey'):
    if isinstance(tnjch, str):
        tnjch = _rujaqïk_json(tnjch)

    if len(ochochibäl) and not os.path.isdir(ochochibäl):
        os.makedirs(ochochibäl)

    if pa_rtl_jlj is None:
        _wchbl_sankey(tnjch, rujunamil, rubi=rubi_lema, ochochibäl=ochochibäl, kibi=kibi)
    else:
        for rjl, tnj in tnjch.items():
            _wchbl_sankey(
                tnj, rujunamil, rubi=rubi_lema + str(rjl), elesaj=pa_rtl_jlj, ochochibäl=ochochibäl,
                kibi=kibi
            )


def _wchbl_sankey(tnjch, rujunamil, rubi, ochochibäl, elesaj=None, kibi=None):
    if kibi is None:
        kibi = {}

    retal_jaloj = [rjnml.meruyonil for rjnml in rujunamil]
    retal_jaloj = sorted([x for x in retal_jaloj if str(x) != elesaj], key=lambda x: str(x))

    ruxeel = np.array([
        retal_jaloj.index(ryn) for rjnml in rujunamil for ryn in rjnml.ruyonil
    ])
    chuwäch = np.array([
        retal_jaloj.index(rjnml.meruyonil) for rjnml in rujunamil for _ in rjnml.ruyonil
    ])

    rajil = np.array([
        tnjch[f'rutikik_{retal_jaloj[ryn]}_chwch_{retal_jaloj[mryn]}'].mean()
        for ryn, mryn in zip(ruxeel, chuwäch)
    ])

    alphas = [
        np.mean(np.sign(tnjch[f'rutikik_{retal_jaloj[ryn]}_chwch_{retal_jaloj[mryn]}']) == np.sign(rjl))
        for ryn, mryn, rjl in zip(ruxeel, chuwäch, rajil)
    ]

    # sachoj_kutbäl = [np.mean(tnjch[f'sg_{jlj}']) for jlj in retal_jaloj]

    melil = np.sign(rajil)
    rajil = np.abs(rajil)

    runimilem = {jlj: None for jlj in retal_jaloj}
    while any(rnml is None for rnml in runimilem.values()):
        for jlj in [j for j in retal_jaloj if runimilem[j] is None]:
            i_jlj = retal_jaloj.index(jlj)
            jlj_mrynl = [rjnml.meruyonil for rjnml in rujunamil if jlj in rjnml.ruyonil]
            kinimilem_mrynl = [runimilem[j] for j in jlj_mrynl]
            if all([nmlm is not None for nmlm in kinimilem_mrynl]):
                rjl = rajil[
                    np.where(np.logical_and(ruxeel == i_jlj,
                                            np.isin(chuwäch, [retal_jaloj.index(mryn) for mryn in jlj_mrynl])))

                ]
                rnmlm = 1 if not len(rjl) else np.sum(rjl)
                runimilem[jlj] = rnmlm

                r2 = 1  # jlj.r2(rxl_tzj, tnjch, ryn=[a.ruyonil for a in achlajil if a.meruyonil == jlj])

                i_chw = np.where(chuwäch == i_jlj)
                knjl = np.sum(rajil[i_chw])
                rajil[i_chw] *= rnmlm / knjl * r2

    rubonil = [r for r in sns.color_palette('Set1', len(retal_jaloj))]
    rubonil_jlj = [f'rgba({int(r[0]*255)}, {int(r[1]*255)}, {int(r[2]*255)}, 0.7)' for r in rubonil]

    rubonil_achljl = [
        f'rgba({int(rubonil[j][0]*255)}, {int(rubonil[j][1]*255)}, {int(rubonil[j][2]*255)}, {a*.7})'
        for j, a in zip(ruxeel, alphas)
    ]

    kibi_jaloj = [str(j) if str(j) not in kibi else kibi[str(j)] for j in retal_jaloj]
    tzij = dict(
        type='sankey',
        node=dict(
            pad=30,
            thickness=40,
            line=dict(
                color="black",
                width=1
            ),
            label=kibi_jaloj,
            color=rubonil_jlj
        ),
        link=dict(
            source=ruxeel,
            target=chuwäch,
            value=rajil,
            color=rubonil_achljl,
            label=['-' if x == -1 else '+' for x in melil],
        ))
    rbyl = dict(
        title=rubi,
        font=dict(
            size=50,
            family='Arial'
        )
    )
    wchbl = dict(data=[tzij], layout=rbyl)
    try:
        pio.write_image(wchbl, os.path.join(ochochibäl, rubi) + '.jpeg')
    except ValueError:
        py.plot(
            wchbl, image='jpeg', filename=os.path.join(ochochibäl, rubi) + '.html', image_filename='sankey',
            show_link=False, auto_open=False, image_width=1600 * 2, image_height=1000 * 2
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
