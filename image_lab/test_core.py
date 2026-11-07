import json,io,unittest
import numpy as np
from PIL import Image
from core import *
class Tests(unittest.TestCase):
 def setUp(self): self.a,_=load_image((ROOT/'samples/astronaut.png').read_bytes())
 def test_identity(self): self.assertTrue(np.array_equal(self.a,convolve(self.a,np.ones((1,1))))); self.assertEqual(psnr(self.a,self.a),float('inf'))
 def test_psnr_known(self): self.assertAlmostEqual(psnr(np.zeros((2,2,3)),np.ones((2,2,3))),48.1308036087)
 def test_kernel_invalid(self):
  for s in ['[[1,2],[3,4]]','[[1,2,3]]','[[1],[2,3]]','[[NaN]]','[[10001]]']:
   with self.assertRaises(ValueError): parse_kernel(s)
  with self.assertRaises(ValueError): parse_kernel('[[0]]',True)
 def test_convolution_direction(self):
  a=np.tile(np.arange(5,dtype=np.uint8)[None,:,None],(5,1,3))*10
  k=np.array([[0,0,0],[1,0,0],[0,0,0]])
  self.assertEqual(convolve(a,k)[2,2,0],30)
 def test_formats(self):
  for fmt in ['PNG','JPEG','BMP']:
   b=io.BytesIO(); Image.fromarray(self.a).save(b,format=fmt); a,m=load_image(b.getvalue()); self.assertEqual(a.shape,self.a.shape)
  b=io.BytesIO(); Image.new('L',(5,5),128).save(b,format='PNG'); a,_=load_image(b.getvalue()); self.assertEqual(a.shape,(5,5,3))
  with self.assertRaises(Exception): load_image(b'broken')
 def test_histogram(self):
  for mode in ['R','G','B','Y','U','V']:
   a=view(self.a,mode); self.assertEqual(np.bincount(a.ravel(),minlength=256).sum(),a.size)
 def test_faces(self):
  _,single=detect(self.a); multi,_=load_image((ROOT/'samples/multi.png').read_bytes()); _,many=detect(multi); _,none=detect(np.zeros((512,512,3),dtype=np.uint8))
  self.assertEqual(len(single),1); self.assertEqual(len(many),2); self.assertEqual(len(none),0)
  self.assertTrue(all(.8<=f['confidence']<=1 for f in many))
if __name__=='__main__': unittest.main(verbosity=2)
