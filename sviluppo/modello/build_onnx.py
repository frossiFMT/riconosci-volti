import sys
import numpy as np, onnx
from onnx import helper as h, TensorProto as TP, numpy_helper as nh
from load_legacy import load
sd=load(sys.argv[1] if len(sys.argv)>1 else 'pesi_bristol.pkl')['model_state']
inits=[]; nodes=[]; cnt=[0]
def name(p): cnt[0]+=1; return f"{p}_{cnt[0]}"
def fold(conv, bn, eps=1e-5):
    W=sd[conv+'.weight']; g,b,m,v=(sd[bn+x] for x in ('.weight','.bias','.running_mean','.running_var'))
    s=g/np.sqrt(v+eps); return (W*s[:,None,None,None]).astype(np.float32),(b-m*s).astype(np.float32)
def conv(x, convk, bnk, stride=1, pad=0, relu=True):
    W,B=fold(convk,bnk); wn,bn_=name('W'),name('B')
    inits.extend([nh.from_array(W,wn),nh.from_array(B,bn_)]); y=name('conv')
    k=W.shape[2]
    nodes.append(h.make_node('Conv',[x,wn,bn_],[y],kernel_shape=[k,k],strides=[stride,stride],pads=[pad]*4))
    if relu: z=name('relu'); nodes.append(h.make_node('Relu',[y],[z])); return z
    return y
x=conv('input','conv1','bn1',2,3)
mp=name('pool'); nodes.append(h.make_node('MaxPool',[x],[mp],kernel_shape=[3,3],strides=[2,2],pads=[1,1,1,1])); x=mp
for li,(n,st) in enumerate(zip([3,4,6,3],[1,2,2,2]),1):
    for bi in range(n):
        p=f'layer{li}.{bi}'; s=st if bi==0 else 1
        y=conv(x,p+'.conv1',p+'.bn1')
        y=conv(y,p+'.conv2',p+'.bn2',s,1)
        y=conv(y,p+'.conv3',p+'.bn3',relu=False)
        r=conv(x,p+'.downsample.0',p+'.downsample.1',s,relu=False) if (p+'.downsample.0.weight') in sd else x
        a=name('add'); nodes.append(h.make_node('Add',[y,r],[a])); z=name('relu'); nodes.append(h.make_node('Relu',[a],[z])); x=z
g=name('gap'); nodes.append(h.make_node('GlobalAveragePool',[x],[g]))
f=name('flat'); nodes.append(h.make_node('Flatten',[g],[f]))
# fc e fc_embedding sono lineari consecutive (senza attivazione in inferenza): si fondono in una sola
Wf,bf,We,be=sd['fc.weight'],sd['fc.bias'],sd['fc_embedding.weight'],sd['fc_embedding.bias']
W=(We@Wf).astype(np.float32); B=(We@bf+be).astype(np.float32)
inits+= [nh.from_array(W,'Wemb'),nh.from_array(B,'Bemb')]
nodes.append(h.make_node('Gemm',[f,'Wemb','Bemb'],['embedding'],transB=1))
graph=h.make_graph(nodes,'cow_reid',[h.make_tensor_value_info('input',TP.FLOAT,[1,3,224,224])],[h.make_tensor_value_info('embedding',TP.FLOAT,[1,128])],inits)
m=h.make_model(graph,opset_imports=[h.make_opsetid('',13)]); m.ir_version=8
onnx.checker.check_model(m); onnx.save(m,'cow_reid_fp32.onnx'); print('ok')
