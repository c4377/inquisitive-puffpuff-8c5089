"""karten445: neuer Look „frech“ (Beere & Creme, Serif mit kursiven Akzentwörtern).

Legt BS_MARKEN["frech"] an und bringt den Kachel-Zeichner (FA "marke") dazu,
*Sternwörter* bei `akzentKursiv` kursiv in der Titelschrift zu setzen:
auf hellen Kacheln in `akzentFarbeDunkel`, auf dunklen in `akzentPlatte`.
"""
import json, sys
A = sys.argv[1]; Z = sys.argv[2]
s = open(A, encoding='utf-8').read()

def ersetze(alt, neu, anzahl=1):
    global s
    n = s.count(alt)
    if n != anzahl:
        sys.exit(f'{n}x statt {anzahl}x: {alt[:80]}')
    s = s.replace(alt, neu)

BEERE = '#5C808C'  # Petrol aus Carinas Canva-Palette (vorher Grün #4F6E5D, davor Beere #A3215F)
LIME = '#CEDF92'; GRAU = '#C9D1D8'; TINTE = '#1E2B30'
SERIF = 'Poppins'  # vorher Instrument Serif
frech = {
    **{k: SERIF for k in ['fotoSchrift', 'deckblattFamilie', 'folgeFamilie', 'kastenSchrift', 'lisaSchrift',
                          'folgeSchrift', 'ablaufTitel', 'schriftart', 'unterSchrift']},
    'gewicht': '600', 'unterGewicht': '600', 'deckblattGewicht': '600', 'folgeGewicht': '600',
    'fotoLaufweite': -25, 'fotoZeile': 1.0, 'laufweite': -25, 'zeile': 1.02,
    'akzentFarbe': LIME, 'akzentGewicht': '600', 'akzentKursiv': 1,
    'akzentFarbeDunkel': '#46697A', 'akzentPlatte': LIME,
    'grundA': BEERE, 'grundB': BEERE, 'schriftA': '#FFFFFF', 'schriftB': '#FFFFFF',
    'platteReihe': LIME + '/' + TINTE + '|' + BEERE + '/#FFFFFF|' + GRAU + '/' + TINTE, 'platteReiheSchritt': 2, 'platteLinks': 1,
    'name': 'CARINA ANNA PRAV', 'nameText': 'CARINA ANNA PRAV', 'nameSchrift': 'HelveticaNeueBrand',
    'nameGewicht': '500', 'nameLaufweite': 220, 'nameAnteil': 0.021, 'nameDeckkraft': 0.9,
    'nameFarbe': '#FFFFFF', 'nameMitte': 1, 'nameUnten': 0.945, 'nameSchatten': 'rgba(20,32,38,0.35)',
    'fliessSchrift': 'HelveticaNeueBrand', 'fliessVersal': 0, 'fliessGroesse': 0.03,
    # Fotos hell und klar, kein Schwarz-Weiß
    'kino': 1, 'kinoSaettigung': 1.05, 'kinoHeben': 6, 'kinoKontrast': 1.05, 'kinoWarm': 0.1,
    'kinoSchwarz': 2, 'kinoWeiss': 255, 'kinoGamma': 0.85, 'kinoSplit': 1, 'kinoVignette': 0,
    'kinoBlauAnteil': 2,
    # Verlauf unter dem Text in Beere
    'scrimZiel': 42, 'scrimMin': 0.35, 'scrimMax': 0.8, 'scrimAuslauf': 0.2, 'bildTon': '92,128,140',
    'textSchatten': 'rgba(20,32,38,0.45)', 'textSchattenBlur': 14,
    'zuschnittZoom': 1.25, 'zoomOben': 1, 'gesichtMaxHoehe': 0.4, 'gesichtLuft': 0.14, 'gesichtAbstand': -0.05,
    'saettigungReihe': '0', 'saettigungWechsel': 1,
    # größer und frecher als Kino
    'groesseAnteil': 0.15, 'maxhoehe': 0.6, 'deckblattGroesse': 230, 'fotoGroesse': 175,
    # ab und zu eine kleine, schicke Kachel: klein, Regular, mittig
    'kleinReihe': '0|1|0|0|1', 'kleinAnteil': 0.055, 'kleinGewicht': '400', 'kleinLaufweite': 10, 'kleinMitte': 1,
}
# Zehn Schwestern von „frech“: gleiche Wirkung, andere Farben.
# Je Palette: A hell und frisch (dunkle Schrift), B gedeckt-mitteldunkel (weiße Schrift),
# C helles Neutral (dunkle Schrift). Kontraste werden nachgezogen wie bei Lime/Petrol/Grau:
# Weiß auf B >= 4, Akzent (dunkles B) auf A und C >= 4,5, A auf B >= 3.
def _rgb(h): h = h.lstrip('#'); return [int(h[i:i + 2], 16) for i in (0, 2, 4)]
def _hex(c): return '#%02X%02X%02X' % tuple(max(0, min(255, round(x))) for x in c)
def _lum(h):
    def k(v):
        v /= 255
        return v / 12.92 if v <= 0.03928 else ((v + 0.055) / 1.055) ** 2.4
    r, g, b = (k(v) for v in _rgb(h))
    return 0.2126 * r + 0.7152 * g + 0.0722 * b
def _kon(a, b):
    la, lb = sorted((_lum(a), _lum(b)), reverse=True)
    return (la + 0.05) / (lb + 0.05)
def _dunkler(h, f=0.94): return _hex([v * f for v in _rgb(h)])
def _bis(h, gegen, ziel):
    for _ in range(60):
        if _kon(h, gegen) >= ziel: break
        h = _dunkler(h)
    return h
PALETTEN = [
    ('zitrone', 'Zitrone & Navy', '#F2E58F', '#4A5D82', '#D6D9E0'),
    ('pfirsich', 'Pfirsich & Tanne', '#F6C8A8', '#4F7363', '#DCD6CF'),
    ('mint', 'Mint & Pflaume', '#BFE3CF', '#7A5470', '#D9D3D8'),
    ('rose', 'Rosé & Olive', '#F0C6CF', '#6E7445', '#D8D4CC'),
    ('himmel', 'Himmelblau & Terracotta', '#BFDDF0', '#A0583F', '#DAD3CD'),
    ('lavendel', 'Lavendel & Moos', '#D4CBF0', '#5E6E4C', '#D3D3D6'),
    ('vanille', 'Vanille & Bordeaux', '#F1E3B8', '#7D3442', '#DAD2CC'),
    ('aqua', 'Aqua & Schiefer', '#A9E0DA', '#5A6372', '#CFD4D6'),
    ('apricot', 'Apricot & Petrol', '#F8D49A', '#3F6E78', '#D5D9D9'),
    ('pistazie', 'Pistazie & Mokka', '#D3E2A8', '#6F5646', '#D8D2CA'),
]
schwestern = {}
for key, _name, A_, B_, C_ in PALETTEN:
    B2 = _bis(B_, '#FFFFFF', 4.0)
    tinte = _hex([v * 0.28 for v in _rgb(B2)])
    akz = _bis(B2, A_, 4.5); akz = _bis(akz, C_, 4.5)
    d = dict(frech)
    d.update({
        'akzentFarbe': A_, 'akzentFarbeDunkel': akz, 'akzentPlatte': A_,
        'grundA': B2, 'grundB': B2,
        'platteReihe': f'{A_}/{tinte}|{B2}/#FFFFFF|{C_}/{tinte}',
        'bildTon': ','.join(str(v) for v in _rgb(B2)),
    })
    schwestern['frech-' + key] = d
    print(f'{key:9s} B {B_}->{B2} weiss {_kon(B2, "#FFFFFF"):.1f}  A auf B {_kon(A_, B2):.1f}  Akzent {akz} auf A {_kon(akz, A_):.1f} auf C {_kon(akz, C_):.1f}  Tinte {tinte}')

ersetze('}};try{if(typeof window<"u"&&window.BS_STIL==="v3"&&window.BS_MARKE&&BS_MARKEN[window.BS_MARKE])',
        '},"frech":' + json.dumps(frech, ensure_ascii=False, separators=(',', ':')) +
        ''.join(',' + json.dumps(k) + ':' + json.dumps(v, ensure_ascii=False, separators=(',', ':')) for k, v in schwestern.items()) +
        '};try{if(typeof window<"u"&&window.BS_STIL==="v3"&&window.BS_MARKE&&BS_MARKEN[window.BS_MARKE])')
ersetze('&&!BS_KACHEL.platteGold&&!BS_KACHEL.akzentNeon)return null;',
        '&&!BS_KACHEL.platteGold&&!BS_KACHEL.akzentNeon&&!BS_KACHEL.akzentKursiv)return null;')
ersetze('(BS_KACHEL.sternHand===1||BS_KACHEL.platteGold||BS_KACHEL.akzentNeon)',
        '(BS_KACHEL.sternHand===1||BS_KACHEL.platteGold||BS_KACHEL.akzentNeon||BS_KACHEL.akzentKursiv)')
ersetze('zHF=K.platteGold||K.akzentNeon?FAM(ix)', 'zHF=K.platteGold||K.akzentNeon||K.akzentKursiv?FAM(ix)')
ersetze('zHS=g2*(K.platteGold||K.akzentNeon?1', 'zHS=g2*(K.platteGold||K.akzentNeon||K.akzentKursiv?1')
ersetze('fontStyle:zf==="f"&&K.fettKursiv===1?"italic":"normal",charSpacing:zf==="h"&&!(K.platteGold||K.akzentNeon)?0:LW,',
        'fontStyle:zf==="f"&&K.fettKursiv===1||zf==="h"&&K.akzentKursiv?"italic":"normal",charSpacing:zf==="h"&&!(K.platteGold||K.akzentNeon||K.akzentKursiv)?0:LW,')
ersetze('fontWeight:zf==="f"?(K.betontGewicht||"700"):zf?"400":GEW(ix),',
        'fontWeight:zf==="f"?(K.betontGewicht||"700"):zf==="h"&&K.akzentKursiv?GEW(ix):zf?"400":GEW(ix),')
ersetze(':zf==="h"&&K.platteGold?K.platteGold:SCH,',
        ':zf==="h"&&K.akzentKursiv?(zNH?(K.akzentFarbeDunkel||SCH):(K.akzentPlatte||SCH)):zf==="h"&&K.platteGold?K.platteGold:SCH,')
ersetze('length>K.versalMaxZeichen);K.platteRahmen&&',
        'length>K.versalMaxZeichen);const zKL=(()=>{try{if(!K.kleinReihe)return!1;const zl=String(K.kleinReihe).split("|"),zt0=typeof t._tag=="number"?t._tag:0,zt1=K.platteReiheSchritt>1?Math.floor(zt0/K.platteReiheSchritt):zt0;return zl[((zt1%zl.length)+zl.length)%zl.length]==="1"}catch(zz){return!1}})();K.platteRahmen&&')
ersetze('const LW=zVT?(K.versalLaufweite||0):(K.laufweite||0),MESS',
        'const LW=zVT?(K.versalLaufweite||0):zKL&&K.kleinLaufweite!=null?K.kleinLaufweite:(K.laufweite||0),MESS')
ersetze('const GEW=ix=>zVT&&K.versalGewicht?K.versalGewicht:',
        'const GEW=ix=>zKL&&K.kleinGewicht?K.kleinGewicht:zVT&&K.versalGewicht?K.versalGewicht:')
ersetze('const LI=K.platteLinks===1||FOLGE&&K.folgeAusrichtung==="links",GA=(FOLGE&&K.folgeGroesseAnteil)||K.groesseAnteil||.098',
        'const LI=!(zKL&&K.kleinMitte===1)&&(K.platteLinks===1||FOLGE&&K.folgeAusrichtung==="links"),GA=zKL&&K.kleinAnteil?K.kleinAnteil:(FOLGE&&K.folgeGroesseAnteil)||K.groesseAnteil||.098')
ersetze('title:"Geladene Datei",children:"karten444"', 'title:"Geladene Datei",children:"karten450"')
open(Z, 'w', encoding='utf-8').write(s)
print('ok')
