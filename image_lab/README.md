# 光影實驗室 / Image Lab
Python 3.11 recommended. All processing runs locally in the Streamlit server.

## Windows PowerShell
```powershell
cd path\to\image_lab
py -3.11 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m streamlit run app.py
```
Open http://localhost:8501 . Activation and uv are not required.

## Tests
```powershell
.\.venv\Scripts\python.exe test_core.py
```

## Public deployment (account action required)
Create a public GitHub repository and upload this folder (including models and samples).
In https://share.streamlit.io create an app, select the repository and app.py, Python 3.11.
Set viewer access to Public and verify from a private browser window.
Put the actual GitHub and live URL into submission.json, then run build_report.py after installing reportlab.
The current PDF explicitly records that these URLs are pending; it must be regenerated before submission.

## Model / sample attribution
YuNet: OpenCV Zoo face_detection_yunet_2023mar.onnx, MIT model license (included).
Astronaut: scikit-image astronaut sample, Eileen Collins / NASA, public domain.
Multi-face test: two identical copies of the astronaut image (controlled test, not a natural crowd).

## Scope
PNG/JPEG/BMP; 20 MB and 20 megapixels; 1–15 odd square kernels, finite weights <=10000.
Convolution flips the kernel; reflect101 border; rounding/clipping to uint8 before PSNR.
Transparency is composited on white. RGB input converted from grayscale/CMYK.
No fabricated public links or detector confidence values.
