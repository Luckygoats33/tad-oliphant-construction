"""Add branded FormSubmit fields: _replyto, _autoresponse, _subject, _template to all forms."""
import glob, os, re

ROOT = r'C:\Users\willw\Projects\tad-oliphant-construction'
os.chdir(ROOT)

html_files = glob.glob('*.html') + glob.glob('services/*.html') + glob.glob('blog/*.html')
exclude = {'businesscard.html', 'doorhanger.html', 'postcard.html'}
html_files = [f for f in html_files if os.path.basename(f) not in exclude]

AUTORESPONSE_MSG = (
    "Thanks for reaching out to Tad Oliphant Construction! "
    "We received your request and will get back to you within one business day. "
    "For faster service, call us at (541) 270-0274. "
    "- Tad Oliphant Construction, Siletz, OR | CCB #206723"
)

fixes = {'subject': 0, 'template': 0, 'replyto': 0, 'autoresponse': 0, 'captcha': 0}

for fpath in html_files:
    with open(fpath, 'r', encoding='utf-8') as f:
        content = f.read()
    original = content

    # Only process files with formsubmit
    if 'formsubmit.co' not in content:
        continue

    # Add _subject if missing (for estimate forms that don't have it yet)
    if '_subject' not in content:
        # Add before submit button in estimate form
        for btn in ['<button type="submit" class="form-submit">', '<button type="submit" class="btn-primary"']:
            if btn in content:
                content = content.replace(btn,
                    '<input type="hidden" name="_subject" value="New Estimate Request - Tad Oliphant Construction">\n      ' + btn)
                fixes['subject'] += 1
                break

    # Add _template if missing
    if '_template' not in content:
        for btn in ['<button type="submit" class="form-submit">', '<button type="submit" class="btn-primary"']:
            if btn in content:
                content = content.replace(btn,
                    '<input type="hidden" name="_template" value="table">\n      ' + btn)
                fixes['template'] += 1
                break

    # Add _replyto if missing (uses the email field value dynamically)
    # FormSubmit supports _replyto as a hidden field referencing a form field name
    if '_replyto' not in content:
        # Add after _cc field
        content = content.replace(
            '<input type="hidden" name="_cc" value="oliphant454@yahoo.com">',
            '<input type="hidden" name="_cc" value="oliphant454@yahoo.com">\n          <input type="hidden" name="_replyto" value="">'
        )
        fixes['replyto'] += 1

    # Add _autoresponse if missing
    if '_autoresponse' not in content:
        content = content.replace(
            '<input type="hidden" name="_cc" value="oliphant454@yahoo.com">',
            '<input type="hidden" name="_cc" value="oliphant454@yahoo.com">\n          <input type="hidden" name="_autoresponse" value="' + AUTORESPONSE_MSG + '">'
        )
        fixes['autoresponse'] += 1

    # Disable captcha (FormSubmit sometimes adds one)
    if '_captcha' not in content:
        content = content.replace(
            '<input type="hidden" name="_cc" value="oliphant454@yahoo.com">',
            '<input type="hidden" name="_cc" value="oliphant454@yahoo.com">\n          <input type="hidden" name="_captcha" value="false">'
        )
        fixes['captcha'] += 1

    if content != original:
        with open(fpath, 'w', encoding='utf-8') as f:
            f.write(content)

print(f'Subject added: {fixes["subject"]}')
print(f'Template added: {fixes["template"]}')
print(f'Reply-to added: {fixes["replyto"]}')
print(f'Auto-response added: {fixes["autoresponse"]}')
print(f'Captcha disabled: {fixes["captcha"]}')
