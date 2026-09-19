#!/usr/bin/env python3
"""Prueft, dass die index.html auf ein Bundle zeigt, das es wirklich gibt.

Aufruf:  python3 tools/ziel-pruefen.py

Warum es das gibt: die Testlaeufe schreiben site/index.html auf das gerade
gepruefte Bundle um. Wird diese Probe danach geloescht und das Nachziehen
greift daneben, bleibt ein Verweis auf eine Datei stehen, die es nicht mehr
gibt. Netlify antwortet mit 404 und die Seite bleibt weiss - ohne jede
Fehlermeldung im Browser.

Vor JEDEM Commit laufen lassen. Rueckgabewert 1 heisst: nicht einspielen.
"""
import os, re, sys

WURZEL = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SEITEN = ["site/index.html", "site/dunkel/index.html"]
ASSETS = os.path.join(WURZEL, "site", "assets")

def kette(name, gesehen=None):
    """Folgt den Weiterleitungen bis zum echten Bundle."""
    gesehen = gesehen or []
    if name in gesehen:
        raise ValueError("Weiterleitung im Kreis: " + " -> ".join(gesehen + [name]))
    pfad = os.path.join(ASSETS, name)
    if not os.path.exists(pfad):
        raise ValueError("Datei fehlt: site/assets/" + name)
    inhalt = open(pfad, encoding="utf-8").read()
    weiter = re.search(r'import\s+"\./(index-B5[A-Za-z0-9_]+\.js)"', inhalt)
    if weiter:
        return kette(weiter.group(1), gesehen + [name])
    if len(inhalt) < 100000:
        raise ValueError("Zieldatei ist verdaechtig klein: %s (%d Byte)" % (name, len(inhalt)))
    return name, len(inhalt)

fehler = []
for seite in SEITEN:
    pfad = os.path.join(WURZEL, seite)
    treffer = re.findall(r'index-B5[A-Za-z0-9_]+\.js', open(pfad, encoding="utf-8").read())
    if len(treffer) != 1:
        fehler.append("%s nennt %d Bundles, erwartet genau eins" % (seite, len(treffer)))
        continue
    try:
        ziel, groesse = kette(treffer[0])
        print("  OK  %-24s -> %s -> %s (%d Byte)" % (seite, treffer[0], ziel, groesse))
    except ValueError as f:
        fehler.append("%s: %s" % (seite, f))

# Alle Weiterleitungen muessen ebenfalls irgendwo ankommen.
for datei in sorted(os.listdir(ASSETS)):
    if not re.match(r'^index-B5.*\.js$', datei):
        continue
    if os.path.getsize(os.path.join(ASSETS, datei)) > 100000:
        continue
    try:
        kette(datei)
    except ValueError as f:
        fehler.append("Weiterleitung %s zeigt ins Leere: %s" % (datei, f))

if fehler:
    print("\nABBRUCH - nicht einspielen:")
    for f in fehler:
        print("  " + f)
    sys.exit(1)
print("\nAlle Verweise loesen sich auf.")
