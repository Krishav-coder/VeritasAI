from pathlib import Path
p = Path('streamlit_app.py')
text = p.read_text('utf-8')
for i, line in enumerate(text.splitlines(), start=1):
    if i <= 40 or 480 <= i <= 520:
        print(f'{i}: {line!r}')
