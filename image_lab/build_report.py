from pathlib import Path
import json,sys,platform
import numpy as np,cv2,streamlit
from PIL import Image as PILImage
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.colors import HexColor
from core import *
ROOT=Path(__file__).parent
pdfmetrics.registerFont(TTFont('MSung-Light',str(ROOT/'fonts/NotoSansTC.ttf')))
meta=json.loads((ROOT/'submission.json').read_text())
OUT=ROOT/f"{meta['student_id']}_{meta['name']}_期中專題.pdf"
c=canvas.Canvas(str(OUT),pagesize=(595,842)); c.setTitle('光影實驗室｜期中專題報告'); n=0; y=0

def txt(s,size=11):
 global y
 # Fixed character wrapping: CJK fullwidth conservatively measured by font metrics.
 for line in s.split('\n'):
  buf=''
  for ch in line:
   if pdfmetrics.stringWidth(buf+ch,'MSung-Light',size)>495:
    
    if y < 75: page('附錄｜原始題目與 AI 協作紀錄（續）')
    c.setFont('MSung-Light',size); c.drawString(50,y,buf); y-=size*1.65; buf=''
   buf+=ch
  
  if y < 75: page('附錄｜原始題目與 AI 協作紀錄（續）')
  c.setFont('MSung-Light',size); c.setFillColor(HexColor('#25334d')); c.drawString(50,y,buf); y-=size*1.65
 y-=7

def page(title):
 global n,y
 if n: c.showPage()
 n+=1; c.setFillColor(HexColor('#173c61')); c.rect(0,770,595,72,fill=1,stroke=0)
 c.setFillColor(HexColor('#ffffff')); c.setFont('MSung-Light',18); c.drawString(45,797,title)
 c.setFillColor(HexColor('#64748b')); c.setFont('MSung-Light',9); c.drawString(45,25,f'光影實驗室 | {meta["student_id"]} {meta["name"]} | 2026-11-05'); c.drawRightString(550,25,str(n)); y=739

def picture(name,height=290):
 global y
 path=ROOT/'evidence'/name
 im=PILImage.open(path); w,h=im.size; scale=min(495/w,height/h)
 c.drawImage(str(path),50,y-h*scale,width=w*scale,height=h*scale); y-=h*scale+14

page('AI 輔助之互動式影像處理與人臉分析')
txt('期中專題報告',24); txt(f"學號：{meta['student_id']}　姓名：{meta['name']}",14)
txt('專案名稱：光影實驗室 / Image Lab\n開發日期：2026 年 11 月 5 日\n應用形式：Python + Streamlit 互動式 Web App',13)
txt('成果摘要',16)
txt('本專題實作影像載入、RGB / YUV 分量與同步直方圖、自訂卷積核與 PSNR，以及 YuNet 人臉偵測。使用者可調整矩陣與偵測門檻，觀察處理結果並下載濾波影像。所有分析皆於執行應用程式的伺服器完成。')
txt('驗收狀態',16)
txt('核心演算法 7 項自動測試通過，另以 Streamlit AppTest 驗證介面狀態；本環境無法取得瀏覽器介面截圖。本版各圖是實際演算法輸出，非 UI 截圖。UI 截圖仍需在可開啟瀏覽器的電腦補上。線上 Public Demo 與 GitHub 連結尚待帳號部署，故本版是待補部署資訊的報告，尚不可視為符合全部繳交條件。')
txt('章節索引\n1. 專案概述與環境建置\n2. 可執行連結與部署\n3. 程式功能、操作、量化分析與測試\n4. AI 協作歷程與限制')
page('Chapter 1｜專案概述與環境建置')
txt('開發環境與安裝',16)
txt(f'本次驗證：Python {platform.python_version()}、OpenCV {cv2.__version__}、Streamlit {streamlit.__version__}、NumPy {np.__version__}。建議使用 Python 3.11 建立獨立虛擬環境。')
for s in ['streamlit：頁面、上傳、參數控制、互動重算與下載。','numpy：矩陣、像素計算、直方圖統計與 MSE。','opencv-python-headless：RGB/YUV、卷積及 YuNet 推論。','Pillow：PNG/JPEG/BMP 解碼、EXIF 方向與透明通道。','matplotlib：0–255 像素直方圖。','reportlab：產生本報告；僅重建 PDF 時需要。'] : txt(s)
txt('Windows PowerShell 操作',16)
for s in ['py -3.11 -m venv .venv',r'.\.venv\Scripts\python.exe -m pip install -r requirements.txt',r'.\.venv\Scripts\python.exe -m streamlit run app.py'] : txt(s,10)
txt('啟動後開啟 http://localhost:8501。無須安裝 uv 或啟用虛擬環境。models/yunet.onnx 已隨專案附上，推論時無須下載模型。')
txt('程式檔案分工',16)
txt('app.py：介面與使用者互動。\ncore.py：載入、矩陣驗證、卷積、PSNR、通道與偵測。\ntest_core.py：可重複執行的自動測試。\nsamples/：單人臉、雙人臉及梯度測試影像。\nevidence/：實際演算法結果圖與實測數值。\nsubmission.json：學號、姓名及待補連結。')
page('Chapter 2｜可執行連結與部署')
txt('Public Live Demo',16); txt(meta['live_url'])
txt('GitHub / GitLab 完整程式碼',16); txt(meta['source_url'])
txt('尚未完成的必要步驟',16)
txt('1. 登入自己的 GitHub，建立 Public 儲存庫並上傳專案。\n2. 登入 Streamlit Community Cloud，選取該儲存庫與 app.py。\n3. 選擇 Python 3.11，確認 requirements.txt、models/、samples/ 完整。\n4. 將檢閱權限設為 Public，以未登入的無痕視窗實測。\n5. 在 submission.json 填入實際網址，重新執行 build_report.py。\n6. 確認 PDF 的兩個網址可開啟後，再繳交本 PDF。')
txt('目前提供完整原始碼壓縮包與本機啟動方式，但壓縮包不能替代評分要求的公開 GitHub 連結。本報告不使用虛構網址，也不宣稱已完成公開部署。')
txt('部署參考文件',16)
txt('Streamlit 官方：\nhttps://docs.streamlit.io/deploy/streamlit-community-cloud/deploy-your-app/deploy',10)
txt('重建報告：安裝 reportlab 後，在專案資料夾執行 python build_report.py。演算法結果圖與模型已包含，不必重新訓練。')
page('Chapter 3｜架構與影像載入')
txt('資料流與模組架構',16)
# branching architecture, precise vector boxes
boxes=[(190,650,210,38,'上傳檔案 / 內建範例'),(190,580,210,38,'Pillow 解碼 → RGB uint8'),(45,490,155,48,'通道與直方圖'),(220,490,155,48,'卷積與 PSNR'),(395,490,155,48,'YuNet 偵測')]
for x,b,w,h,label in boxes:
 c.setStrokeColor(HexColor('#84a6c9')); c.setFillColor(HexColor('#edf4fb')); c.roundRect(x,b,w,h,5,fill=1); c.setFillColor(HexColor('#173c61')); c.setFont('MSung-Light',10); c.drawCentredString(x+w/2,b+h/2-3,label)
for x in [122,297,472]: c.line(295,580,x,538)
c.line(295,650,295,618); y=465
txt('載入流程：檢查位元組大小與格式 → 檢查像素總量 → EXIF 方向校正 → 透明通道白底合成 → RGB 三通道。資訊列區分來源模式與處理模式，避免將灰階來源誤報為原生 RGB。')
txt('操作：在左側上傳圖片，或選擇內建範例。支援 PNG、JPG/JPEG、BMP。損毀檔案顯示錯誤訊息；最大 20 MB、2000 萬像素，以避免記憶體過量。')
picture('ui_color.png',260)
page('Chapter 3｜色彩空間與同步直方圖')
txt('操作與定義',16)
txt('在第一分頁選取 Original、R、G、B、Y、U、V。Original 顯示三條 RGB 強度分布；單一通道顯示灰階圖及一條像素數量分布。每次切換均由相同陣列同步重新繪製影像與直方圖。')
txt('OpenCV RGB → 8-bit YUV：\nY ≈ 0.299R + 0.587G + 0.114B\nU ≈ 0.492(B − Y) + 128\nV ≈ 0.877(R − Y) + 128\n實際值由 cvtColor 執行，包含量化及飽和截斷。U/V 的 128 表示中性色度，不將 YUV 假裝為 RGB 顯示。')
picture('ui_y.png',340)
txt('驗證：每個通道的 256 個 bin 總和均等於影像寬 × 高。直方圖橫軸固定為 0–255，縱軸為 pixel count，未使用機率密度取代像素數。')
page('Chapter 3｜自訂卷積與 PSNR')
txt('操作與防呆',16)
txt('第二分頁可選 Identity、Gaussian、Sharpen、Emboss，並直接修改 JSON 二維陣列。允許 1–15 奇數階方陣；可輸入負權重及小數。非方陣、偶數階、NaN、無窮大或權重絕對值超過 10000 會拒絕執行。')
txt('若勾選正規化，令 K′ = K / ΣK；當 |ΣK| < 10⁻¹² 時報錯，不進行除以零。零和邊緣核仍可在取消正規化後使用。')
txt('卷積定義與 PSNR 公式',16)
txt('F(x,y,c) = Σi Σj K(i,j) I(x−i,y−j,c)。OpenCV filter2D 原本為相關運算，因此先將核心旋轉 180°，才執行真正卷積。邊界採 REFLECT_101，計算使用 float64；結果四捨五入並截斷到 [0,255]。')
txt('MSE = [Σx Σy Σc (I − F)²] / (H × W × C)\nPSNR = 10 log₁₀(255² / MSE) dB\n由峰值振幅比 20 log₁₀(255 / √MSE) 可得到上述式子。當 MSE = 0 時，PSNR = ∞。相減前轉為浮點數，避免 uint8 溢位。')
picture('ui_filter.png',260)
txt('PSNR 越高表示越接近原圖，並不代表更銳利或更有美感。平滑及邊緣強化本來就可能降低 PSNR；本專題以最終可下載的 uint8 圖進行比較。')
page('Chapter 3｜人臉偵測與實測分析')
txt('方法與操作',16)
txt('第三分頁調整門檻並按「偵測全部人臉」。YuNet 回傳座標與 confidence；經 NMS 後框出各張臉並統計數量。為控制推論成本，長邊最多 1280 像素，框座標再映回原圖。分數為模型輸出，不是已校準的正確率。')
picture('ui_face.png',300)
a,_=load_image((ROOT/'samples/astronaut.png').read_bytes()); multi,_=load_image((ROOT/'samples/multi.png').read_bytes()); ann,rows=detect(multi); PILImage.fromarray(ann).save(ROOT/'evidence/multi_result.png')
txt(f'實測：NASA astronaut 單人圖偵測 1 張臉；將同圖水平拼接後偵測 {len(rows)} 張臉，分數為 '+', '.join(f'{r["confidence"]:.4f}' for r in rows)+'。雙人測試為受控複製影像，不等同自然多人場景準確率。黑色空白圖為 0 張臉。')
txt('限制：側臉、遮擋、模糊、小臉與光線差可能漏判；本測試無法估計一般化 precision / recall，也未執行人臉身分辨識。')
page('Chapter 3｜測試案例與量化結果')
txt('可重現自動測試：python test_core.py',16)
txt('7 項測試群組全部通過：\n1. Identity 輸出逐像素相同，PSNR = ∞。\n2. 全零對全一影像，MSE = 1，PSNR = 48.130804 dB。\n3. 非對稱核心確認左右方向符合卷積，而非相關。\n4. PNG / JPEG / BMP 與灰階載入成功，損毀檔案拒絕。\n5. 各 RGB / YUV 通道 histogram 總和等於像素數。\n6. 偶數、非方陣、ragged、NaN、超限及零和正規化拒絕。\n7. 單人、受控雙人及空白圖，分別得到 1 / 2 / 0。')
txt('同一張 astronaut 影像的濾波 PSNR',16)
results={}
for label,k,norm in [('Identity',[[1]],False),('Gaussian',[[1,2,1],[2,4,2],[1,2,1]],True),('Sharpen',[[0,-1,0],[-1,5,-1],[0,-1,0]],False),('Emboss',[[-2,-1,0],[-1,1,1],[0,1,2]],False)]:
 score=psnr(a,convolve(a,parse_kernel(json.dumps(k),norm))); results[label]='Infinity' if np.isinf(score) else score; txt(f'{label}：'+('∞ dB' if np.isinf(score) else f'{score:.4f} dB'))
(ROOT/'evidence/results.json').write_text(json.dumps(results,indent=2))
txt('分析：Identity 的無限 PSNR 是正確結果，不應顯示為 0。Gaussian 減少局部高頻變化；Sharpen 強化邊界；Emboss 改變明暗且包含較多飽和截斷，因此與原圖的差異較大。上述數值不應解讀為濾波器優劣排名。')
txt('補充邊界：零和核未正規化時可合法執行；超大矩陣採拒絕策略。15×15、透明圖、極大檔案等路徑已設限制，但未將所有可能影像均納入本次實測，故不宣稱完整覆蓋。')
page('Chapter 4｜AI 協作與 Prompt 歷程')
txt('模型與紀錄原則',16)
txt('協作工具：本次 ChatGPT Work Mode 中的 Codex。系統提供的模型識別為 GPT-6；介面未提供可核實的精確後端快照 ID。本報告不冒稱 GPT-4o 或其他版本。以下只記錄本次實際收到的提問與實際開發修正，不補造多輪使用者對話。')
txt('原始 Prompt → 產出',16)
txt('原始 Prompt 為使用者貼上的完整考題與評分表（另見 AI_AUDIT.md），末句為「tolong kerjakan ujian midterm gw ini」。要求四項核心功能、PDF 四章、公開展示與 GitHub 連結、完整 AI Audit Trail。')
txt('AI 產出：Streamlit 三分頁介面、core.py 計算模組、YuNet 模型、安裝清單、自動測試、實際演算法結果圖及本報告。')
txt('實際除錯 / 重構紀錄',16)
txt('1. 環境初期缺少 cv2、streamlit、skimage；pip 執行入口失效，改為 python -m pip 後安裝成功。\n2. PDF 工具的預設絕對路徑不存在，定位本機實際路徑後完成啟動。\n3. filter2D 為相關而非卷積，加入核心旋轉，並用非對稱核心驗證方向。\n4. PSNR 以 float64 相減，並以已知 MSE = 1 與 Identity 測試驗證。\n5. 安裝得到 OpenCV 5.0，將相依範圍調整為 >=4.10,<6 以包含實際測試版本。\n6. confidence 選用 YuNet 真實分數，沒有將 Haar 權重或固定值偽裝成機率。')
txt('紀錄完整性與責任',16)
txt('AI_AUDIT.md 保存原始題目與本次實作決策摘要。工具執行摘要不是額外使用者 Prompt；未聲稱存在沒有發生的 refinement 對話。若教師要求逐字完整 ChatGPT 對話，應另匯出本次對話，而不能以本摘要冒充完整逐字紀錄。')
page('參考資料、授權與繳交前檢查')
txt('官方參考資料',16)
txt('OpenCV：DNN-based Face Detection And Recognition\nhttps://docs.opencv.org/4.13.0/d0/dd4/tutorial_dnn_face.html\nYuNet 原始模型與授權：\nhttps://github.com/opencv/opencv_zoo/tree/main/models/face_detection_yunet\nStreamlit 部署文件：\nhttps://docs.streamlit.io/deploy/streamlit-community-cloud/deploy-your-app/deploy',10)
txt('素材與授權',16)
txt('YuNet 模型附有 OpenCV Zoo 的 MIT LICENSE；astronaut 範例來自 scikit-image（NASA Eileen Collins 照片，公有領域）。雙人測試為同一照片的水平複製，不作為不同人物或自然群像資料集。')
txt('繳交前必須完成',16)
txt('□ 核對學號 C113151168 與姓名曾偉錢。\n□ 建立並填入 Public Demo 與 GitHub 原始碼連結。\n□ 以無痕視窗驗證兩個網址的公開存取權限。\n□ 匯出本次完整對話，依教師要求補入 AI 歷程。\n□ 更新 submission.json 後重建 PDF，檢查截圖與網址。\n□ 最終僅繳交指定命名的 PDF；程式碼由公開連結提供。')
txt('此版本的未完成事項已明確列出，請勿在連結尚未補齊時將其當作全部驗收完成。')
page('附錄｜原始題目與 AI 協作紀錄')
for line in (ROOT/'AI_AUDIT.md').read_text().splitlines():
 txt(line.lstrip('#> '),9)
c.save(); print(OUT)
