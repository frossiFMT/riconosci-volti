# Riconosci Vacche — versione 3.3 (22/11/2026)

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

## Firebase (dalla versione 3.1)
- Progetto **visionevacche**. La configurazione è in `firebase-config.js`. Se lì
  c'è `null`, l'app torna a funzionare con l'archivio solo sul telefono.
- All'apertura l'app chiede email e password (account creati nella console:
  Authentication › Users). La registrazione autonoma va disattivata.
- Collezione **`vacche`**: un documento per vacca, con id uguale alla matricola
  in maiuscolo. Contiene la scheda, la miniatura, le impronte (`emb`, numeri a
  32 bit in base64, 128 valori ciascuna) e i conteggi delle foto.
- Collezione **`foto`**: un documento per foto, con la JPEG (lato lungo 1280 px,
  massimo 900 KB) in base64 e questi campi: `matricola`, `tipo` (`dorso` |
  `musello`), `sessione`, `ritaglio` (il riquadro del dorso o del musello in
  pixel), `scattata`, `autore`, `versioneApp`.
- Le foto stanno nel database (piano gratuito) e non in Cloud Storage, che
  richiederebbe il piano Blaze.
- Senza rete le scritture restano in coda sul telefono e partono da sole quando
  la connessione torna (in alto compare "⬆︎ N in invio").
- Regole di sicurezza di Firestore (Firestore › Regole):
  ```
  rules_version = '2';
  service cloud.firestore {
    match /databases/{database}/documents {
      match /{document=**} {
        allow read, write: if request.auth != null;
      }
    }
  }
  ```

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
- **3.3** (22/11/2026): eliminando una vacca si cancellano anche le sue foto su Firebase; in Archivio c'è il pulsante "Elimina foto senza vacca" per le foto rimaste. L'esportazione esclude le foto delle vacche eliminate. Gli aggiornamenti dell'app arrivano alla prima apertura.
- **3.2** (22/11/2026): Archivio › Esporta dataset, un file ZIP con tutte le foto da Firebase (intere e ritagliate, divise per matricola e tipo) più foto.csv, vacche.csv e vacche.json.
- **3.1** (21/11/2026): archivio condiviso su Firebase con accesso tramite account, invio delle foto del dorso e del musello, modalità di acquisizione per la raccolta dei dati.
- **3.0** (21/11/2026): riconoscimento delle vacche Frisone dal mantello; numero di versione a schermo.
- 2.0 (20/11/2026): Riconosci Volti, correzione per Safari su iPhone.
- 1.0 (20/11/2026): Riconosci Volti, prima versione.
