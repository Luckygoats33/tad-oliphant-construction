"""Add _replyto population to form submit handlers so Reply goes to customer."""
import glob, os

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

    # For one-line submitEstimate: add replyto population after button disable
    # Pattern: var btn = form.querySelector('button[type="submit"]'); if(btn){btn.disabled=true;btn.textContent='Sending...';}
    # Add: var rt=form.querySelector('[name="_replyto"]');var em=form.querySelector('[name="email"]');if(rt&&em)rt.value=em.value;
    replyto_code = "var rt=form.querySelector('[name=\"_replyto\"]');var em=form.querySelector('[name=\"email\"]');if(rt&&em)rt.value=em.value;"

    if replyto_code not in content:
        # One-line estimate pattern
        content = content.replace(
            "if(btn){btn.disabled=true;btn.textContent='Sending...';} fetch('https://formsubmit.co/ajax/will@supportwellnessglobal.com'",
            "if(btn){btn.disabled=true;btn.textContent='Sending...';} " + replyto_code + " fetch('https://formsubmit.co/ajax/will@supportwellnessglobal.com'"
        )
        # Multi-line estimate pattern (contact.html)
        content = content.replace(
            "if(btn){btn.disabled=true;btn.textContent='Sending...';}\n  var data = new FormData(form);\n  fetch('https://formsubmit.co/ajax/will@supportwellnessglobal.com'",
            "if(btn){btn.disabled=true;btn.textContent='Sending...';}\n  " + replyto_code + "\n  var data = new FormData(form);\n  fetch('https://formsubmit.co/ajax/will@supportwellnessglobal.com'"
        )

    if content != original:
        with open(fpath, 'w', encoding='utf-8') as f:
            f.write(content)
        fixed += 1

print(f'Reply-to JS added to {fixed} files')
