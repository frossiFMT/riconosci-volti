import numpy as np, onnxruntime as ort
from PIL import Image
sess=ort.InferenceSession('../../models/frisona_reid.onnx')
def emb(img):
    w,h=img.size; r=224/max(w,h); im=img.resize((max(1,int(w*r)),max(1,int(h*r))),Image.BILINEAR)
    c=Image.new('RGB',(224,224)); c.paste(im,((224-im.width)//2,(224-im.height)//2))
    e=sess.run(None,{'input':np.array(c,dtype=np.float32).transpose(2,0,1)[None]})[0][0]; return e/np.linalg.norm(e)
