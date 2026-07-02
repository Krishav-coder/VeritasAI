from pathlib import Path

path = Path('streamlit_app.py')
text = path.read_text(encoding='utf-8')
text = text.replace('\\"', '"')
text = text.replace("\\'", "'")
path.write_text(text, encoding='utf-8')
print('Replaced escaped quotes in streamlit_app.py')
