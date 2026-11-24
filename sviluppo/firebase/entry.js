import { initializeApp } from 'firebase/app';
import { getAuth, signInWithEmailAndPassword, onAuthStateChanged, signOut, setPersistence, indexedDBLocalPersistence } from 'firebase/auth';
import { initializeFirestore, persistentLocalCache, persistentSingleTabManager, collection, doc, setDoc, addDoc, deleteDoc, onSnapshot, serverTimestamp, updateDoc, increment, getDocs, query, where } from 'firebase/firestore';
window.FB = { initializeApp, getAuth, signInWithEmailAndPassword, onAuthStateChanged, signOut, setPersistence, indexedDBLocalPersistence,
  initializeFirestore, persistentLocalCache, persistentSingleTabManager, collection, doc, setDoc, addDoc, deleteDoc, onSnapshot, serverTimestamp, updateDoc, increment, getDocs, query, where };
