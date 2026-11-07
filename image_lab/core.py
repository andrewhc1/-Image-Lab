import json
import io
import numpy as np
import cv2
from PIL import Image, ImageOps
from pathlib import Path

ROOT = Path(__file__).parent

def load_image(data):
    if len(data) > 20*1024*1024: raise ValueError('檔案不可超過 20 MB')
    im = Image.open(io.BytesIO(data))
    if im.format not in ('PNG','JPEG','BMP'): raise ValueError('僅支援 PNG/JPEG/BMP')
    if im.width*im.height > 20_000_000: raise ValueError('影像不可超過 2000 萬像素')
    meta = dict(format=im.format, original_mode=im.mode, bytes=len(data))
    im = ImageOps.exif_transpose(im)
    if 'A' in im.getbands():
        rgba=im.convert('RGBA'); bg=Image.new('RGBA',rgba.size,'white'); bg.alpha_composite(rgba); im=bg
    arr=np.asarray(im.convert('RGB')).copy()
    meta.update(width=arr.shape[1],height=arr.shape[0],channels=3)
    return arr,meta

def parse_kernel(text, normalize=False):
    try: k=np.asarray(json.loads(text),dtype=np.float64)
    except Exception as e: raise ValueError('請輸入合法 JSON 二維數值矩陣') from e
    if k.ndim!=2 or k.shape[0]!=k.shape[1] or k.shape[0]%2!=1 or not 1<=k.shape[0]<=15:
        raise ValueError('矩陣必須為 1～15 的奇數階方陣')
    if not np.isfinite(k).all() or np.abs(k).max()>10000: raise ValueError('權重必須有限且絕對值不超過 10000')
    if normalize:
        s=k.sum()
        if abs(s)<1e-12: raise ValueError('權重總和為零，無法正規化；請取消正規化')
        k=k/s
    return k

def convolve(rgb,k):
    # filter2D computes correlation: flip kernel for mathematical convolution.
    raw=cv2.filter2D(rgb.astype(np.float64),cv2.CV_64F,np.flip(k,(0,1)),borderType=cv2.BORDER_REFLECT_101)
    return np.clip(np.rint(raw),0,255).astype(np.uint8)

def psnr(a,b):
    mse=float(np.mean((a.astype(np.float64)-b.astype(np.float64))**2))
    return float('inf') if mse==0 else float(10*np.log10(255**2/mse))

def view(rgb,mode):
    if mode=='Original': return rgb
    if mode in ('R','G','B'): return rgb[:,:,'RGB'.index(mode)]
    return cv2.cvtColor(rgb,cv2.COLOR_RGB2YUV)[:,:,'YUV'.index(mode)]

def detect(rgb,threshold=.8):
    h,w=rgb.shape[:2]; scale=min(1,1280/max(h,w))
    small=cv2.resize(rgb,(max(1,round(w*scale)),max(1,round(h*scale))))
    detector=cv2.FaceDetectorYN.create(str(ROOT/'models/yunet.onnx'),'',(small.shape[1],small.shape[0]),threshold,.3,5000)
    _,faces=detector.detect(cv2.cvtColor(small,cv2.COLOR_RGB2BGR))
    output=rgb.copy(); rows=[]
    for f in [] if faces is None else faces:
        x,y,bw,bh=(f[:4]/scale).round().astype(int)
        x1=max(0,x); y1=max(0,y); x2=min(w,x+bw); y2=min(h,y+bh)
        score=float(f[-1]); rows.append(dict(x=x1,y=y1,width=x2-x1,height=y2-y1,confidence=score))
        cv2.rectangle(output,(x1,y1),(x2,y2),(0,220,120),max(1,w//400))
        cv2.putText(output,f'{score:.3f}',(x1,max(14,y1-5)),cv2.FONT_HERSHEY_SIMPLEX,.5,(0,180,80),1)
    return output,rows
