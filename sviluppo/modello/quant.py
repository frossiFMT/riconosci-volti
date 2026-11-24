# Pesi salvati in int8 per canale + DequantizeLinear: file ~4x più piccolo, calcolo sempre in float32
import onnx, numpy as np
from onnx import numpy_helper as nh, helper as h
m=onnx.load('cow_reid_fp32.onnx'); g=m.graph
new_inits=[]; new_nodes=[]
for t in list(g.initializer):
    a=nh.to_array(t)
    if a.ndim>=2 and a.size>4096:
        ax=0; red=tuple(range(1,a.ndim))
        sc=(np.abs(a).max(axis=red)/127.0).astype(np.float32); sc[sc==0]=1e-8
        q=np.clip(np.round(a/sc.reshape((-1,)+(1,)*(a.ndim-1))),-127,127).astype(np.int8)
        new_inits+= [nh.from_array(q,t.name+'_q'),nh.from_array(sc,t.name+'_s'),nh.from_array(np.zeros_like(sc,dtype=np.int8),t.name+'_z')]
        new_nodes.append(h.make_node('DequantizeLinear',[t.name+'_q',t.name+'_s',t.name+'_z'],[t.name],axis=ax))
    else: new_inits.append(t)
del g.initializer[:]; g.initializer.extend(new_inits)
nodes=list(g.node); del g.node[:]; g.node.extend(new_nodes+nodes)
onnx.checker.check_model(m); onnx.save(m,'cow_reid_int8w.onnx')
import onnxruntime as ort
rng=np.random.default_rng(1); x=rng.uniform(0,255,(4,1,3,224,224)).astype(np.float32)
a=ort.InferenceSession('cow_reid_fp32.onnx'); b=ort.InferenceSession('cow_reid_int8w.onnx')
for i in range(4):
    ea=a.run(None,{'input':x[i]})[0][0]; eb=b.run(None,{'input':x[i]})[0][0]
    print('cos',float(ea@eb/np.linalg.norm(ea)/np.linalg.norm(eb)))
