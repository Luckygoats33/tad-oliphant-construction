"""Add global submit listener to populate _replyto from email field before submission."""
import glob, os

ROOT = r'C:\Users\willw\Projects\tad-oliphant-construction'
os.chdir(ROOT)

html_files = glob.glob('*.html') + glob.glob('services/*.html') + glob.glob('blog/*.html')
exclude = {'businesscard.html', 'doorhanger.html', 'postcard.html'}
html_files = [f for f in html_files if os.path.basename(f) not in exclude]

# Global script to auto-populate _replyto from email field on any form submit
REPLYTO_SCRIPT = """<script>document.addEventListener('submit',function(e){var f=e.target;var rt=f.querySelector('[name="_replyto"]');var em=f.querySelector('[name="email"]');if(rt&&em&&em.value)rt.value=em.value;});</script>"""

# Remove any inline replyto code from submit handlers (cleanup from fix-replyto.py)
INLINE_REPLYTO = """var rt=form.querySelector('[name="_replyto"]');var em=form.querySelector('[name="email"]');if(rt&&em)rt.value=em.value;"""

fixed = 0
for fpath in html_files:
    with open(fpath, 'r', encoding='utf-8') as f:
        content = f.read()
    original = content

    if 'formsubmit.co' not in content:
        continue

    # Remove inline replyto JS if present (from earlier fix)
    content = content.replace(' ' + INLINE_REPLYTO + ' ', ' ')
    content = content.replace('  ' + INLINE_REPLYTO + '\n', '')

    # Add global replyto script before phone_click script (or before </body>)
    if 'submit.*_replyto' not in content and REPLYTO_SCRIPT not in content:
        # Insert before the phone click tracking script
        phone_script = "<script>document.addEventListener('click',function(e)"
        if phone_script in content:
            content = content.replace(phone_script, REPLYTO_SCRIPT + '\n' + phone_script)
        else:
            content = content.replace('</body>', REPLYTO_SCRIPT + '\n</body>')

    if content != original:
        with open(fpath, 'w', encoding='utf-8') as f:
            f.write(content)
        fixed += 1

print(f'Global replyto listener added to {fixed} files')
