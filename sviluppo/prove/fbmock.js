// Firebase finto per le prove automatiche
(function(){
  const db={vacche:{},foto:{}}; const listeners=[]; let authCb=[]; let user=null; let seq=0;
  window.__mockdb=db;
  const notify=()=>{ for(const l of listeners){ const docs=Object.entries(db[l.col]).map(([id,d])=>({id,data:()=>d})); l.cb({docs,metadata:{fromCache:false}}); } };
  const ts=()=>({__ts:Date.now()});
  window.FB={
    initializeApp:c=>({c}), getAuth:a=>({a}), setPersistence:async()=>{}, indexedDBLocalPersistence:{},
    onAuthStateChanged:(a,cb)=>{ authCb.push(cb); setTimeout(()=>cb(user),10); },
    signInWithEmailAndPassword:async(a,e,p)=>{ await new Promise(r=>setTimeout(r,200)); if(p!=='segreta'){ const er=new Error('bad'); er.code='auth/invalid-credential'; throw er; } user={email:e}; return {user}; },
    signOut:async()=>{ user=null; },
    initializeFirestore:()=>({}), persistentLocalCache:o=>o, persistentSingleTabManager:()=>({}),
    collection:(d,name)=>({name}), doc:(d,col,id)=>({col,id}),
    setDoc:async(ref,data,opt)=>{ db[ref.col][ref.id]=Object.assign(opt&&opt.merge?(db[ref.col][ref.id]||{}):{},data); notify(); await new Promise(r=>setTimeout(r,300)); },
    addDoc:async(col,data)=>{ const id='f'+(++seq); db[col.name][id]=data; await new Promise(r=>setTimeout(r,300)); return {id}; },
    deleteDoc:async(ref)=>{ delete db[ref.col][ref.id]; notify(); },
    updateDoc:async(ref,data)=>{ const d=db[ref.col][ref.id]||{}; for(const k in data){ const v=data[k]; d[k]= (v&&v.__inc!=null)? (d[k]||0)+v.__inc : v; } db[ref.col][ref.id]=d; notify(); },
    increment:n=>({__inc:n}), getDocs:async(col)=>({docs:Object.entries(db[col.name]).filter(([id,d])=>!col.cond||d[col.cond.f]===col.cond.v).map(([id,d])=>({id,data:()=>d}))}), query:(col,c)=>({name:col.name,cond:c}), where:(f,op,v)=>({f,v}), serverTimestamp:ts,
    onSnapshot:(col,opts,cb,err)=>{ listeners.push({col:col.name,cb}); setTimeout(notify,10); return ()=>{}; }
  };
  window.FIREBASE_CONFIG={projectId:'prova'};
})();
