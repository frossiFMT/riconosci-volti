# Riconosci Vacche — versione 3.0 (21/11/2026)

Web app per riconoscere le singole vacche **Frisone** dal disegno del mantello.
Registri una vacca (matricola, nome, date, note). Quando la inquadri di nuovo,
l'app la riconosce e mostra la sua scheda sul video.

## Come si usa
1. **➕ Nuova vacca**: inquadra il **dorso della vacca dall'alto** dentro il
   riquadro verde e muoviti piano lungo l'animale. L'app prende 8 campioni
   (circa 10 secondi), poi apre la scheda da compilare (la matricola è obbligatoria).
2. **Riconoscimento**: basta inquadrare il dorso. Il riquadro diventa:
   - **verde** con la scheda: vacca riconosciuta (confermata in almeno 3 delle ultime 5 letture);
   - **arancione** "Forse …?": somiglianza vicina alla soglia;
   - **bianco** "non riconosciuta": nessuna vacca dell'archivio è abbastanza simile.
3. **Tocca la scheda verde** per aprirla e modificarla.
4. **Aggiungi campioni** (dalla scheda): conviene farlo in giorni diversi, con luce
   diversa e con la vacca girata nell'altro verso. È il modo più efficace per
   migliorare il riconoscimento.
5. **⚙️ Impostazioni**: versione, severità del riconoscimento (consigliata 0.35),
   distanze a schermo per le prove, cambio fotocamera.

## Da sapere
- **Modello**: rete dell'Università di Bristol addestrata su Frisone riprese
  **dall'alto** (W. Andrew et al., 2021, licenza MIT). Da altre angolazioni
  funziona peggio. Se proprio serve un'altra angolazione, registra e riconosci
  sempre dalla stessa.
- **Prove fatte**: su 25 vacche di esempio (immagini pubbliche della stessa
  università) con soglia 0.35 nessuna vacca registrata è stata scambiata con
  un'altra. Nel 29% dei casi la singola lettura risulta "incerta", ma il voto
  su più letture lo compensa. In una prova live simulata la vacca registrata è
  stata riconosciuta sempre e l'altra vacca mai confusa con lei. **Sono prove
  su immagini di esempio**: l'accuratezza vera va misurata sulle vostre vacche.
- **Archivio**: salvato solo sul telefono (IndexedDB). Esporta/Importa per il
  backup o per passarlo a un altro telefono. Il passaggio a Firebase è il
  prossimo passo.
- Il calcolo avviene tutto sul telefono (circa 0,3 s per lettura): non serve
  la rete, dopo la prima apertura.

## Aggiornare l'app
La versione si cambia **solo in `version.js`**: la usano sia la pagina (la
mostra in alto) sia `sw.js` (la cache). Poi commit e push: alla riapertura
l'iPhone scarica la versione nuova e mostra "App aggiornata alla versione …".

## Componenti
- `models/frisona_reid.onnx`: rete ResNet-50 di Bristol convertita in ONNX
  (pesi int8, 23 MB; impronta da 128 valori). Licenza in `models/`.
- `ort/`: ONNX Runtime Web 1.31.1 (Microsoft, MIT) per eseguire la rete nel browser.

## Storico versioni
- **3.0** (21/11/2026): riconoscimento delle vacche Frisone dal mantello; numero di versione a schermo.
- 2.0 (20/11/2026): Riconosci Volti, correzione per Safari su iPhone.
- 1.0 (20/11/2026): Riconosci Volti, prima versione.
