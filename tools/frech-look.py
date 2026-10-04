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
}
ersetze('}};try{if(typeof window<"u"&&window.BS_STIL==="v3"&&window.BS_MARKE&&BS_MARKEN[window.BS_MARKE])',
        '},"frech":' + json.dumps(frech, ensure_ascii=False, separators=(',', ':')) +
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
ersetze('title:"Geladene Datei",children:"karten444"', 'title:"Geladene Datei",children:"karten448"')
open(Z, 'w', encoding='utf-8').write(s)
print('ok')
