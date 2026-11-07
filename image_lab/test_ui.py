import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).parent))
from streamlit.testing.v1 import AppTest
at=AppTest.from_file(str(Path(__file__).parent/'app.py'),default_timeout=30).run()
assert len(at.exception)==0
at.radio[0].set_value('U').run(); assert len(at.exception)==0
at.text_area[0].set_value('[[0]]').run(); at.checkbox[0].set_value(True).run()
assert any('零' in e.value for e in at.error)
at.checkbox[0].set_value(False).run(); assert not at.error
at.button[0].click().run(); assert len(at.exception)==0
print('PASS: initial render, U channel, zero normalization error/recovery, face button')
