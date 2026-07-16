// Story-Strategie: Was jemand, der wegen eines Angebotsdesign-Reels folgt,
// in den Stories lesen muss — als 6-Tage-Loop, der sich endlos wiederholt.
// Sprache: ruhig, ehrlich, szenisch (Eva-Stil). CTA: Angebotscheck.

export const storyStrategyIntro = {
  title: 'Die Story-Logik',
  text: `Jemand folgt dir wegen eines Reels über Angebotsdesign. In den Stories muss diese Person — in dieser Reihenfolge — lesen:

1. Ich bin hier richtig (Wiedererkennung)
2. Das ist mein Problem, tiefer erklärt (das stille Kämmerchen)
3. Sie kann das wirklich (Beweis aus echten Checks)
4. Wer ist die Frau? (Nahbar)
5. Mein Zögern ist normal — und genau falsch (Einwand)
6. Das ist mein nächster Schritt (Angebotscheck)

Ein Set pro Tag. Nach Tag 6 beginnt der Loop von vorn — neue Follower steigen an jedem Punkt ein und holen den Rest im nächsten Durchlauf.`,
};

export const storyStrategySets = [
  {
    title: 'Tag 1 — Ankommen',
    zweck: 'Neue Follower aus dem Reel bestätigen: Hier geht es genau um dein Problem.',
    sticker: 'Sticker: „Erinner mich"',
    slides: [
      'Wenn du neu hier bist: Wahrscheinlich hat dich ein Reel hergebracht.',
      'Eins über Angebote, die nicht verkaufen.',
      'Dann bist du richtig. Genau darum geht es hier. Jeden Tag.',
      'Ich schau mir Angebote an und sag dir, warum niemand kauft.',
      'Bleib da. Morgen zeig ich dir den häufigsten Fehler.',
    ],
  },
  {
    title: 'Tag 2 — Das stille Kämmerchen',
    zweck: 'Das Kernproblem vertiefen: Warum allein gebaute Angebote nicht verkaufen.',
    sticker: 'Umfrage: „Hast du dein Angebot allein gebaut?" — Ja / Komplett',
    slides: [
      'Die meisten Angebote entstehen am selben Ort.',
      'Im stillen Kämmerchen. Am Schreibtisch. Allein.',
      'Ohne ein einziges Gespräch mit einer echten Kundin.',
      'Und dann wundern wir uns, dass niemand versteht, für wen es ist.',
      'Du bist nicht schlecht. Du hast nur nie gefragt.',
    ],
  },
  {
    title: 'Tag 3 — Beweis',
    zweck: 'Zeigen, wie die Diagnose konkret aussieht — Vertrauen in den Check.',
    sticker: '',
    slides: [
      'Diese Woche lag wieder ein Angebot bei mir im Postfach.',
      'Schön gemacht. Sauber aufgebaut. Man sieht die Arbeit.',
      'Ich hab fünf Sätze markiert.',
      'Fünf Sätze, die erklären, warum niemand kauft.',
      'Sie hat sie an einem Nachmittag geändert. Das Angebot steht jetzt anders da.',
      'So sieht Diagnose aus. Kein Coaching. Ein Befund.',
    ],
  },
  {
    title: 'Tag 4 — Nahbar',
    zweck: 'Der Person hinter der Diagnose ein Gesicht geben.',
    sticker: '',
    slides: [
      'Falls wir uns noch nicht kennen:',
      'Ich hab über dreißig Angebote auf dem Tisch gehabt.',
      'Coaches, Beraterinnen, eine, die Hotels macht.',
      'Der Fehler war fast immer derselbe.',
      'Und ich sehe ihn meistens in den ersten zwanzig Minuten.',
    ],
  },
  {
    title: 'Tag 5 — Der Einwand',
    zweck: 'Das häufigste Zögern vor dem Check entkräften: „Ich überarbeite erst noch."',
    sticker: '',
    slides: [
      '„Ich schick es dir, wenn ich es nochmal überarbeitet hab."',
      'Bitte nicht.',
      'Ich will es sehen, wie es jetzt ist.',
      'Genau da steckt die Antwort drin, warum es nicht verkauft.',
      'Die überarbeitete Version versteckt sie nur besser.',
    ],
  },
  {
    title: 'Tag 6 — Das Angebot',
    zweck: 'Der Angebotscheck als klarer nächster Schritt.',
    sticker: 'Link-Sticker zum Angebotscheck + DM-Sticker „Schick mir dein Angebot."',
    slides: [
      'Wenn dein Angebot nicht verkauft, rate nicht weiter.',
      'Schick es mir. So wie es jetzt ist.',
      'Ich sag dir, warum es nicht verkauft — und was du konkret änderst.',
      'Angebotsdesign-Check mit Lösung. Alles Weitere steht im Link.',
    ],
  },
];
