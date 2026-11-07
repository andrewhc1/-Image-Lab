import io,json
import numpy as np
import streamlit as st
import matplotlib.pyplot as plt
from PIL import Image
from core import load_image,parse_kernel,convolve,psnr,view,detect,ROOT
st.set_page_config(page_title='光影實驗室',page_icon='🔬',layout='wide')
st.title('光影實驗室 · Image Lab')
st.caption('互動式影像處理與人臉分析｜C113151168 曾偉錢')
with st.sidebar:
 st.header('影像來源')
 upload=st.file_uploader('上傳 PNG / JPG / BMP',type=['png','jpg','jpeg','bmp'])
 sample=st.selectbox('或使用內建測試影像',['astronaut.png','multi.png','gradient.png'])
 st.caption('上限 20 MB / 2000 萬像素。透明影像以白底合成；灰階轉為 RGB。')
try:
 data=upload.getvalue() if upload else (ROOT/'samples'/sample).read_bytes()
 rgb,meta=load_image(data)
except Exception as e:
 st.error(f'影像載入失敗：{e}'); st.stop()
a,b,c,d=st.columns(4)
a.metric('解析度',f"{meta['width']} × {meta['height']}")
b.metric('處理色彩維度','RGB · 3 通道')
c.metric('檔案大小',f"{meta['bytes']/1024:.1f} KB")
d.metric('來源格式 / 模式',f"{meta['format']} / {meta['original_mode']}")
t1,t2,t3=st.tabs(['01 色彩與直方圖','02 卷積濾波 / PSNR','03 人臉偵測'])
with t1:
 mode=st.radio('顯示通道',['Original','R','G','B','Y','U','V'],horizontal=True)
 shown=view(rgb,mode); left,right=st.columns(2)
 left.image(shown,caption=mode,clamp=True,width='stretch')
 fig,ax=plt.subplots(figsize=(6,4))
 if shown.ndim==3:
  for i,color in enumerate(['red','green','blue']): ax.plot(np.arange(256),np.bincount(shown[:,:,i].ravel(),minlength=256),color=color,label='RGB'[i])
  ax.legend()
 else: ax.bar(np.arange(256),np.bincount(shown.ravel(),minlength=256),width=1,color='#4263eb')
 ax.set(xlim=(0,255),xlabel='Pixel intensity (0–255)',ylabel='Pixel count',title=mode+' histogram')
 right.pyplot(fig); plt.close(fig)
 st.caption('YUV 使用 OpenCV 8-bit YUV；U/V 以 128 為中性色度。各通道顯示其原始 0–255 數值，不另做對比拉伸。')
with t2:
 presets={'Identity':[[0,0,0],[0,1,0],[0,0,0]],'Gaussian':[[1,2,1],[2,4,2],[1,2,1]],'Sharpen':[[0,-1,0],[-1,5,-1],[0,-1,0]],'Emboss':[[-2,-1,0],[-1,1,1],[0,1,2]]}
 preset=st.selectbox('預設矩陣',list(presets))
 text=st.text_area('JSON 卷積核（可直接修改）',json.dumps(presets[preset]),key='kernel_'+preset)
 norm=st.checkbox('除以權重總和（正規化）',value=preset=='Gaussian',key='norm_'+preset)
 try:
  k=parse_kernel(text,norm); filtered=convolve(rgb,k)
  l,r=st.columns(2); l.image(rgb,caption='原始影像',width='stretch'); r.image(filtered,caption='濾波結果',width='stretch')
  score=psnr(rgb,filtered); st.metric('PSNR', '∞ dB（完全相同）' if np.isinf(score) else f'{score:.3f} dB')
  st.caption('真正卷積：核心旋轉 180°；邊界 REFLECT_101。浮點運算後四捨五入並截斷至 0–255。PSNR 比較最終輸出；高 PSNR 僅表示與原圖接近。')
  buff=io.BytesIO(); Image.fromarray(filtered).save(buff,format='PNG')
  st.download_button('下載濾波影像',buff.getvalue(),'filtered.png','image/png')
 except ValueError as e: st.error(str(e))
with t3:
 threshold=st.slider('信心門檻',.1,.99,.8,.01)
 if st.button('偵測全部人臉',type='primary'):
  try:
   with st.spinner('YuNet 偵測中…'): annotated,rows=detect(rgb,threshold)
   st.metric('偵測人臉數',len(rows)); st.image(annotated,width='stretch'); st.dataframe(rows)
   st.caption('Confidence 是模型分數，並非經校準的正確率。小臉、遮擋、側臉可能漏判；本工具不辨識身分。')
  except Exception as e: st.error(f'模型執行失敗：{e}')
