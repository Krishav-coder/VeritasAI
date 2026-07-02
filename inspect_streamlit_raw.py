from pathlib import Path
p = Path('streamlit_app.py')
raw = p.read_bytes()
print('raw bytes:', repr(raw[:200]))
text = raw.decode('utf-8')
for i, line in enumerate(text.splitlines(), 1):
    if i <= 40 or 480 <= i <= 520:
        print(f'{i}: {line!r}')
