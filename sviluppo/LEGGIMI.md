# Strumenti di sviluppo

Non servono all'app pubblicata: sono gli strumenti usati per costruirla e provarla.

## modello/ — rete di Bristol → ONNX
1. Scarica i pesi (Git LFS, ~103 MB):
   https://media.githubusercontent.com/media/CWOA/MetricLearningIdentification/master/weights/SoftmaxRTL/50-50_fold-1.pkl
2. `python build_onnx.py 50-50_fold-1.pkl` → `cow_reid_fp32.onnx` (non serve torch: `load_legacy.py` legge il checkpoint PyTorch in formato vecchio).
   fc e fc_embedding sono fuse in un'unica Gemm (in inferenza non c'è attivazione tra le due, come nel test.py originale).
3. `python quant.py` → `cow_reid_int8w.onnx` (pesi int8 per canale + DequantizeLinear; coseno con fp32 ≈ 0,9995). Copialo in `models/frisona_reid.onnx`.
4. `impronta_python.py`: calcolo dell'impronta in Python con lo stesso preprocessing dell'app (verifica JS ≈ Python: coseno 0,9995).
Pacchetti: numpy, onnx, onnxruntime, pillow.

## firebase/ — libreria Firebase in un file
`entry.js` elenca le funzioni usate dall'app. Per rigenerare `firebase-bundle.js`:
```
npm install firebase esbuild
npx esbuild entry.js --bundle --minify --format=iife --target=es2020 --legal-comments=eof --outfile=../../firebase-bundle.js
```
Se l'app usa una funzione nuova di Firebase va aggiunta qui, poi si rigenera il bundle.

## prove/ — prove automatiche in Chrome senza telefono
- `fbmock.js`: Firebase finto in memoria (accesso: password `segreta`; `window.__mockdb` per leggere i dati).
- `genera_video.py`: crea `vacche.y4m`, il video usato come fotocamera finta.
- `prova_completa.py`: accesso (sbagliato e giusto), registrazione con 8 foto del dorso, scheda, 3 foto del musello, riconoscimento, esportazione del dataset, pulizia foto orfane, eliminazione della vacca con le sue foto.
  Richiede: `pip install playwright`, Chrome (variabile CHROME), ffmpeg per il video.
Nota: con `http.server` le copie dei file con la stessa data rispondono 304; nelle prove di aggiornamento usa `touch` sui file nuovi.
