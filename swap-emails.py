"""Swap form emails: Will becomes primary (activated), Tad becomes CC."""
import glob, os

ROOT = r'C:\Users\willw\Projects\tad-oliphant-construction'
os.chdir(ROOT)

html_files = glob.glob('*.html') + glob.glob('services/*.html') + glob.glob('blog/*.html')
exclude = {'businesscard.html', 'doorhanger.html', 'postcard.html'}
html_files = [f for f in html_files if os.path.basename(f) not in exclude]

swapped = 0
for fpath in html_files:
    with open(fpath, 'r', encoding='utf-8') as f:
        content = f.read()
    original = content
    content = content.replace(
        'formsubmit.co/ajax/oliphant454@yahoo.com',
        'formsubmit.co/ajax/will@supportwellnessglobal.com'
    )
    content = content.replace(
        'name="_cc" value="will@supportwellnessglobal.com"',
        'name="_cc" value="oliphant454@yahoo.com"'
    )
    if content != original:
        with open(fpath, 'w', encoding='utf-8') as f:
            f.write(content)
        swapped += 1

print(f'Swapped emails in {swapped} files')
