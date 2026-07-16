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
    zweck: 'Neue Follower aus dem Reel abholen — szenisch, nicht als Ansage.',
    sticker: 'Sticker: „Erinner mich"',
    slides: [
      'Kurz zu dir, wenn du neu hier bist.',
      'Dich hat wahrscheinlich ein Reel hergebracht. Eins über ein Angebot, das nicht verkauft.',
      'Vielleicht hast du beim Zuschauen an dein eigenes gedacht.',
      'Genau darüber rede ich hier. Jeden Tag, ohne Drama.',
      'Morgen erzähl ich dir, wo die meisten Angebote entstehen. Der Ort ist das Problem.',
    ],
  },
  {
    title: 'Tag 2 — Das stille Kämmerchen',
    zweck: 'Der Mechanismus als erlebte Szene aus einem Check — nicht als These.',
    sticker: 'Umfrage: „Kommt dir das bekannt vor?" — Ja / Zu sehr',
    slides: [
      'Letzte Woche hat mir eine Frau ihr Angebot geschickt.',
      'Man hat sofort gesehen, wie viel Arbeit drinsteckt. Jedes Wort gewählt.',
      'Ich hab sie gefragt, mit wem sie darüber gesprochen hat, bevor sie es gebaut hat.',
      'Stille.',
      'Es ist am Schreibtisch entstanden. Tür zu, Kopf voll, ganz allein.',
      'Genau da verlieren die meisten Angebote ihre Käuferinnen. Nicht am Preis. Am stillen Kämmerchen.',
    ],
  },
  {
    title: 'Tag 3 — Beweis',
    zweck: 'Ein Check-Moment als kleine Geschichte — zeigt die Diagnose, ohne zu behaupten.',
    sticker: '',
    slides: [
      'Gestern hab ich wieder ein Angebot auseinandergenommen.',
      'Nicht böse. Das ist mein Job.',
      'Ich hab fünf Sätze markiert und danebengeschrieben, was eine Kundin fühlt, wenn sie sie liest.',
      'Sie hat zurückgeschrieben: „Das hat mir noch nie jemand so gezeigt."',
      'Einen Nachmittag später stand ihr Angebot anders da.',
      'Das ist keine Magie. Das ist ein Blick von außen.',
    ],
  },
  {
    title: 'Tag 4 — Nahbar',
    zweck: 'Wer dahintersteht — Autorität aus dem Muster, das du immer wieder siehst.',
    sticker: '',
    slides: [
      'Falls wir uns noch nicht kennen: Ich bin Carina.',
      'Ich hab über dreißig Angebote auf dem Tisch gehabt. Coaches, Beraterinnen, eine, die Hotels macht.',
      'Verschiedene Preise, verschiedene Branchen. Und trotzdem war es fast immer dasselbe.',
      'Ich seh den Fehler meistens in den ersten zwanzig Minuten.',
      'Nicht, weil ich hellsehen kann. Sondern weil er immer an derselben Stelle sitzt.',
    ],
  },
  {
    title: 'Tag 5 — Der Einwand',
    zweck: 'Das Zögern („erst noch überarbeiten") als erlebte Geschichte entkräften.',
    sticker: '',
    slides: [
      'Eine Frau hat mir mal geschrieben: „Ich schick dir mein Angebot, wenn ich es überarbeitet hab."',
      'Drei Wochen später kam es. Glattgeschliffen.',
      'Und genau die Stellen, an denen ich gesehen hätte, warum es nicht verkauft — waren wegpoliert.',
      'Deshalb sag ich es so deutlich: Schick es mir, wie es jetzt ist.',
      'Die ungeschminkte Version erzählt mir alles. Die überarbeitete versteckt es nur.',
    ],
  },
  {
    title: 'Tag 6 — Das Angebot',
    zweck: 'Der Check als leiser, klarer nächster Schritt — kein Verkaufston.',
    sticker: 'Link-Sticker zum Angebotscheck + DM-Sticker „Schick mir dein Angebot."',
    slides: [
      'Wenn du hier mitliest und denkst: Das bin ich.',
      'Dann mach es dir einfach.',
      'Schick mir dein Angebot. So wie es jetzt ist, ohne es vorher noch schnell zu überarbeiten.',
      'Ich sag dir, warum es nicht verkauft — und was du konkret änderst.',
      'Angebotsdesign-Check mit Lösung. Der Link ist hier.',
    ],
  },
];
