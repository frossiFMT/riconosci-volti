# Riconosci Volti — prototipo

Registri il volto di una persona insieme alle sue caratteristiche (nome, data di
nascita, altezza, altre informazioni, note). Ogni volta che la inquadri, l'app la
riconosce e mostra queste informazioni sopra il video, in tempo reale.

È il banco di prova del progetto di riconoscimento delle vacche: stessa logica
(impronta numerica di 128 valori → archivio → confronto), cambia solo il modello.

## Come si usa
- **➕ Nuova persona**: inquadra il volto da vicino e muovi piano la testa. L'app
  prende 8 campioni, poi apre la scheda da compilare.
- **Tocca un volto "Sconosciuto"** sul video per registrarlo direttamente.
- **Tocca un volto riconosciuto** per aprire e modificare la sua scheda.
- **Aggiungi campioni** (dalla scheda): rende il riconoscimento più affidabile.
  Conviene farlo con luce e angolazioni diverse.
- **📇 Archivio**: elenco delle persone, più Esporta/Importa per il backup o per
  passare l'archivio a un altro telefono.
- **🔄**: passa dalla fotocamera posteriore a quella frontale.

Colori del riquadro: verde = riconosciuto, arancione = "forse", bianco = sconosciuto.

## Pubblicazione (GitHub Pages)
Carica tutti i file nel repository, poi Settings › Pages › Branch "main" / root.
Apri l'indirizzo https://NOMEUTENTE.github.io/NOME-REPOSITORY/ con Safari, poi
Condividi › Aggiungi alla schermata Home.

Quando modifichi i file, aumenta la versione in `sw.js` (`riconosci-volti-v1` → `v2`),
altrimenti il telefono continua a usare la copia in cache.

## Privacy
Archivio e foto restano solo sul telefono (IndexedDB del browser): niente viene
inviato in rete. Registra solo persone che sono d'accordo.

## Soglie (in index.html)
- `T_OK = 0.52`: sotto questa distanza la persona è riconosciuta.
- `T_MAYBE = 0.60`: tra 0.52 e 0.60 l'app mostra "Forse …?".
Se confonde due persone, abbassa T_OK. Se fatica a riconoscere, aggiungi campioni.

## Componenti
- face-api (@vladmandic/face-api, licenza MIT): rilevamento del volto,
  68 punti del viso e impronta a 128 valori.
