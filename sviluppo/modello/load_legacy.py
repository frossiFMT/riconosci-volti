"""Legge un checkpoint PyTorch in formato legacy (pre-1.6) senza installare torch."""
import pickle, struct, collections, numpy as np

DT = {'FloatStorage':np.float32,'DoubleStorage':np.float64,'HalfStorage':np.float16,'LongStorage':np.int64,
      'IntStorage':np.int32,'ShortStorage':np.int16,'CharStorage':np.int8,'ByteStorage':np.uint8,'BoolStorage':np.bool_}

class StorageType:
    def __init__(s,name): s.dtype=DT[name]
class TensorRef:
    def __init__(s,key,offset,size,stride): s.key,s.offset,s.size,s.stride=key,offset,tuple(size),tuple(stride)

def load(path):
    f=open(path,'rb')
    pickle.load(f); pickle.load(f); pickle.load(f)   # magic, protocol, sys info
    storages={}
    class U(pickle.Unpickler):
        def find_class(s,mod,name):
            if mod=='torch._utils' and name in ('_rebuild_tensor_v2','_rebuild_tensor'):
                return lambda storage,offset,size,stride,*a: TensorRef(storage,offset,size,stride)
            if mod=='torch' and name in DT: return StorageType(name)
            if mod=='collections' and name=='OrderedDict': return collections.OrderedDict
            if mod=='torch._utils' and name=='_rebuild_parameter':
                return lambda t,*a: t
            return super().find_class(mod,name)
        def persistent_load(s,pid):
            _,stype,key,loc,size,view=pid
            storages[key]=(stype.dtype,size)
            return key
    obj=U(f).load()
    keys=pickle.load(f)
    data={}
    for k in keys:
        n=struct.unpack('<q',f.read(8))[0]
        dt=storages[k][0]
        data[k]=np.frombuffer(f.read(n*np.dtype(dt).itemsize),dtype=dt)
    def mat(t):
        if isinstance(t,TensorRef):
            buf=data[t.key]; it=buf.itemsize
            return np.lib.stride_tricks.as_strided(buf[t.offset:],shape=t.size,strides=[x*it for x in t.stride]).copy()
        if isinstance(t,dict): return collections.OrderedDict((k,mat(v)) for k,v in t.items())
        return t
    return mat(obj)
