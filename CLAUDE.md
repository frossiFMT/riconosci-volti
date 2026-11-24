# Riconosci Vacche — contesto per Claude Code

Questo file riassume lo stato del progetto, portato avanti finora in una chat di claude.ai. Rispondi a Francesco in italiano.

## Il progetto
- Francesco (FMT S.r.l., automazione industriale: PLC Siemens, HMI) e un suo amico che ha una stalla di **Frisone**.
- Obiettivo: inquadri una vacca con il telefono, l'app la riconosce dal **disegno del mantello visto dall'alto** e mostra i suoi dati: matricola, scheda e, in futuro, i dati dei macchinari della stalla.
- Fase attuale: l'amico deve acquisire **10 vacche** (dorso più musello facoltativo) con l'app. Le foto vanno su Firebase e servono a misurare il riconoscimento sulle vacche vere.

## Com'è fatta l'app (web app installabile, PWA)
- Pubblicata con GitHub Pages: https://frossifmt.github.io/riconosci-volti/ (repository `frossiFMT/riconosci-volti`; il nome è rimasto quello del prototipo dei volti). Si installa su iPhone da Safari con "Aggiungi alla schermata Home". Francesco non ha un Mac, quindi niente app iOS nativa.
- `index.html`: tutta l'app (HTML, CSS e JS in un file).
- `version.js`: **l'unico punto in cui si cambia la versione** (`APP_VERSION`, `APP_DATE`). La versione compare in alto a destra nell'app.
- `sw.js`: service worker. Prende dalla rete index.html, version.js, firebase-config.js e manifest.json; prende dalla cache i file grandi. La pagina lo registra come `sw.js?v=<versione>` con `updateViaCache:'none'` e, dopo un aggiornamento, si ricarica da sola.
- `models/frisona_reid.onnx`: ResNet-50 dell'Università di Bristol (W. Andrew et al., CWOA/MetricLearningIdentification, licenza MIT, pesi SoftmaxRTL) convertita in ONNX, pesi int8, 23 MB. Restituisce un'impronta di 128 valori.
  - Preprocessing: ritaglio con il lato lungo a 224 px, centrato su sfondo nero, valori 0..255, **nessuna normalizzazione**.
- `ort/`: onnxruntime-web 1.31.1 (solo WASM, 1 thread, proxy worker). Circa 0,3 s per impronta.
- `firebase-bundle.js` (SDK Firebase raccolto in un file con esbuild) e `firebase-config.js` (progetto **visionevacche**). Se nella config c'è `null`, l'app usa un archivio solo locale in IndexedDB.

### Riconoscimento
- Riquadro guida 2:1 (88% della larghezza). Controllo di qualità prima di calcolare: almeno 8% di nero e 8% di bianco, nitidezza sufficiente, telefono fermo.
- L'impronta viene normalizzata (L2) e confrontata con quelle in archivio (distanza minima per vacca).
- Una vacca è riconosciuta se distanza < `thr` (0.35, regolabile nelle impostazioni) **e** margine sulla seconda vacca ≥ 0.06; il risultato viene mostrato quando concordano **3 letture su 5**. "Forse" se la distanza è sotto thr+0.05.
- In registrazione: 8 campioni, ognuno salvato anche ruotato di 180° (vacca girata dall'altra parte).
- Prove su 25 vacche di esempio (immagini pubbliche Cows2021/OpenCows2020 con variazioni simulate): con soglia 0.35, 71% riconosciute, 0% scambiate, 29% incerte nella singola lettura. **Non ancora misurato su vacche reali.**
- Un rilevatore generico (YOLOX nano, COCO) non trova le vacche viste dall'alto: per questo c'è il riquadro guida.

### Firebase (piano gratuito Spark)
- Accesso con Email/Password. La registrazione autonoma è disattivata e gli account si creano dalla console. L'amico usa l'account di Francesco: la password è nella guida, **non va scritta nel repository**.
- `vacche/{MATRICOLA in maiuscolo}`: matricola, nome, nascita, parto, extra, note, thumb, `emb` (base64 di float32 concatenati, 128 per impronta), nEmb, nFotoDorso, nFotoMusello, aggiornato, aggiornatoDa, versioneApp.
- `foto/{auto}`: matricola, vacca (id della vacca), tipo (`dorso`|`musello`), sessione, ordine, `jpeg` (data URL, lato lungo 1280 px, massimo 900 KB), w, h, ritaglio {x,y,w,h}, scattata, caricata, autore, versioneApp.
  - Le foto stanno in Firestore perché Cloud Storage dal febbraio 2026 richiede il piano Blaze.
- Regole: `allow read, write: if request.auth != null;`
- Cache persistente: l'app funziona offline, le scritture restano in coda e si vede "⬆︎ N in invio".
- Eliminare una vacca cancella anche le sue foto. In Archivio: "Elimina foto senza vacca" ed "Esporta dataset". L'esportazione crea uno ZIP con foto/, ritagli/, foto.csv, vacche.csv, vacche.json e LEGGIMI.txt, ed esclude le foto orfane.

## Come si lavora
- **Pubblicare una versione**: aumenta `APP_VERSION` in version.js, aggiungi una riga nello storico di LEGGIMI.md, poi commit e push (di solito li fa Francesco con GitHub Desktop). Sul telefono l'aggiornamento arriva alla prima o alla seconda apertura.
- **Prima di consegnare, prova**: in `sviluppo/prove/` ci sono il Firebase finto e una prova completa in Chrome headless con fotocamera finta. Le funzioni del Firebase vero vanno provate da Francesco sul telefono.
- **Nuove funzioni Firebase**: aggiungile in `sviluppo/firebase/entry.js` e rigenera il bundle (istruzioni in `sviluppo/LEGGIMI.md`).
- **Il dataset reale delle vacche** va in `../dataset-vacche/`, una cartella accanto al repository. **Non va mai copiato nel repository**, che è pubblico.
- Safari su iPhone: per il calcolo passa sempre da una canvas e non dal `<video>` direttamente, perché altrimenti a volte arrivano fotogrammi neri. `alert`/`confirm` non si usano: per le conferme c'è il "tocca due volte".

## Storico versioni
- 3.3 (22/11): eliminazione delle foto insieme alla vacca, pulizia delle foto orfane, export che esclude le foto orfane.
- 3.2 (22/11): esportazione del dataset in ZIP; correzione del meccanismo di aggiornamento (prima un cambio solo in version.js non arrivava sul telefono).
- 3.1 (21/11): Firebase, accesso, acquisizione del dorso e del musello.
- 3.0 (21/11): riconoscimento delle Frisone.
- 1.x–2.x (20/11): prototipo di riconoscimento dei volti (face-api), sostituito.

## Prossimi passi
1. Quando arriva lo ZIP delle 10 vacche in `../dataset-vacche/`: controllare la qualità delle foto, poi misurare il riconoscimento tra sessioni diverse (distanze tra stessa vacca e vacche diverse) e tarare la soglia. Se non basta, fare il fine-tuning della rete di Bristol con le foto dei ritagli.
2. Connettore per i dati dei macchinari della stalla: si aspetta di sapere da Francesco marche, programmi e come esportare. Il connettore legge soltanto e copia su Firebase, abbinando i dati per matricola. Poi: scheda con avvisi (latte da scartare, mastite, calore).
3. Eventi registrati in stalla (trattamenti, visite, foto); musello come secondo metodo di riconoscimento (non c'è una rete pubblica: dataset su Zenodo, record 6324361); account separati con ruoli; telecamera fissa (Nicla Vision o telecamera IP) all'ingresso della sala di mungitura con RFID.

## Documenti
- Guida per l'amico: https://claude.ai/artifact/WLeS4GTxBXpfQzHVtbxxum (documento claude.ai; dice ancora "3.1", ma il procedimento non è cambiato).
- Nel progetto claude.ai "Arduino Nicla Vision": claude/stato-progetto.md.
