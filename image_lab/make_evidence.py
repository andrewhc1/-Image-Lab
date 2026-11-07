from core import *
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
rgb,_=load_image((ROOT/'samples/astronaut.png').read_bytes())
for mode,name in [('Original','ui_color.png'),('Y','ui_y.png')]:
 a=view(rgb,mode); fig,ax=plt.subplots(1,2,figsize=(11,4))
 ax[0].imshow(a,cmap='gray',vmin=0,vmax=255); ax[0].set_title(mode); ax[0].axis('off')
 if a.ndim==3:
  for i,c in enumerate(['red','green','blue']): ax[1].plot(np.arange(256),np.bincount(a[:,:,i].ravel(),minlength=256),color=c,label='RGB'[i])
  ax[1].legend()
 else: ax[1].bar(np.arange(256),np.bincount(a.ravel(),minlength=256),width=1)
 ax[1].set(xlim=(0,255),xlabel='Pixel intensity',ylabel='Pixel count'); fig.tight_layout(); fig.savefig(ROOT/'evidence'/name,dpi=140); plt.close(fig)
k=np.array([[1,2,1],[2,4,2],[1,2,1]])/16
f=convolve(rgb,k); fig,ax=plt.subplots(1,2,figsize=(10,4))
for a,im,title in zip(ax,[rgb,f],['Original',f'Gaussian / PSNR {psnr(rgb,f):.3f} dB']): a.imshow(im); a.set_title(title); a.axis('off')
fig.tight_layout(); fig.savefig(ROOT/'evidence/ui_filter.png',dpi=140); plt.close(fig)
multi,_=load_image((ROOT/'samples/multi.png').read_bytes()); annotated,rows=detect(multi)
fig,ax=plt.subplots(figsize=(10,4)); ax.imshow(annotated); ax.axis('off'); ax.set_title(f'YuNet / {len(rows)} faces / threshold 0.8'); fig.tight_layout(); fig.savefig(ROOT/'evidence/ui_face.png',dpi=140); plt.close(fig)
