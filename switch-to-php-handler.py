"""Switch all forms from FormSubmit to PHP form handler."""
import glob, os, re

ROOT = r'C:\Users\willw\Projects\tad-oliphant-construction'
os.chdir(ROOT)

html_files = glob.glob('*.html') + glob.glob('services/*.html') + glob.glob('blog/*.html')
exclude = {'businesscard.html', 'doorhanger.html', 'postcard.html'}
html_files = [f for f in html_files if os.path.basename(f) not in exclude]

fixed = 0
for fpath in html_files:
    with open(fpath, 'r', encoding='utf-8') as f:
        content = f.read()
    original = content

    if 'formsubmit.co' not in content:
        continue

    # --- REPLACE FORMSUBMIT FETCH WITH PHP HANDLER ---

    # Pattern 1: Service/blog pages - one-line submitEstimate with FormData
    # fetch('https://formsubmit.co/ajax/will@supportwellnessglobal.com', { method: 'POST', body: new FormData(form) })
    content = content.replace(
        "fetch('https://formsubmit.co/ajax/will@supportwellnessglobal.com', { method: 'POST', body: new FormData(form) })",
        "fetch('/form-handler.php', { method: 'POST', headers: {'Content-Type': 'application/json'}, body: JSON.stringify(Object.fromEntries(new FormData(form))) })"
    )

    # Pattern 2: Contact page - multi-line submitEstimate/submitContact with FormData variable
    # fetch('https://formsubmit.co/ajax/will@supportwellnessglobal.com', { method: 'POST', body: data })
    content = content.replace(
        "fetch('https://formsubmit.co/ajax/will@supportwellnessglobal.com', { method: 'POST', body: data })",
        "fetch('/form-handler.php', { method: 'POST', headers: {'Content-Type': 'application/json'}, body: JSON.stringify(Object.fromEntries(data)) })"
    )

    # --- REMOVE FORMSUBMIT-SPECIFIC HIDDEN FIELDS ---
    # Remove _cc, _captcha, _autoresponse, _replyto, _subject, _template, _honey fields
    for field_name in ['_cc', '_captcha', '_autoresponse', '_replyto', '_subject', '_template', '_honey']:
        # Match hidden input lines with this name (various indentation and spacing)
        pattern = r'\s*<input type="hidden" name="' + re.escape(field_name) + r'" [^>]*>\s*\n?'
        content = re.sub(pattern, '\n', content)
        # Also match honeypot with display:none
        if field_name == '_honey':
            pattern = r'\s*<input type="text" name="' + re.escape(field_name) + r'" [^>]*>\s*\n?'
            content = re.sub(pattern, '\n', content)

    # --- REMOVE GLOBAL REPLYTO SCRIPT ---
    content = content.replace(
        """<script>document.addEventListener('submit',function(e){var f=e.target;var rt=f.querySelector('[name="_replyto"]');var em=f.querySelector('[name="email"]');if(rt&&em&&em.value)rt.value=em.value;});</script>\n""",
        ''
    )
    # Also without trailing newline
    content = content.replace(
        """<script>document.addEventListener('submit',function(e){var f=e.target;var rt=f.querySelector('[name="_replyto"]');var em=f.querySelector('[name="email"]');if(rt&&em&&em.value)rt.value=em.value;});</script>""",
        ''
    )

    # Clean up multiple blank lines
    content = re.sub(r'\n{3,}', '\n\n', content)

    if content != original:
        with open(fpath, 'w', encoding='utf-8') as f:
            f.write(content)
        fixed += 1

print(f'Switched {fixed} files from FormSubmit to PHP handler')
