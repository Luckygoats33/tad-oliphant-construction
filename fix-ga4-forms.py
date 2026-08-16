"""Update GA4 ID, fix forms like Brothers Gutters pattern, add CC email, phone tracking."""
import os, re, glob

ROOT = r'C:\Users\willw\Projects\tad-oliphant-construction'
os.chdir(ROOT)

GA4_ID = 'G-QM5ZJ1L7PC'
CC_EMAIL = 'will@supportwellnessglobal.com'

html_files = glob.glob('*.html') + glob.glob('services/*.html') + glob.glob('blog/*.html')
exclude = {'businesscard.html', 'doorhanger.html', 'postcard.html', 'onepage.html'}
html_files = [f for f in html_files if os.path.basename(f) not in exclude]

print(f'Processing {len(html_files)} HTML files...')

fixes = {'ga4': 0, 'form_btn': 0, 'form_event': 0, 'cc_added': 0, 'phone_track': 0}

# Phone click tracking script (matches Brothers Gutters)
PHONE_TRACK = '<script>document.addEventListener(\'click\',function(e){var a=e.target.closest(\'a[href^="tel:"]\');if(a)gtag(\'event\',\'phone_click\',{event_category:\'contact\',event_label:a.href,transport_type:\'beacon\'})});</script>'

# CC hidden field
CC_FIELD = f'<input type="hidden" name="_cc" value="{CC_EMAIL}">'

for fpath in html_files:
    with open(fpath, 'r', encoding='utf-8') as f:
        content = f.read()

    original = content

    # 1. REPLACE GA4 PLACEHOLDER ID
    if 'G-XXXXXXXXXX' in content:
        content = content.replace('G-XXXXXXXXXX', GA4_ID)
        fixes['ga4'] += 1

    # 2. ADD CC HIDDEN FIELD to forms (before submit button, if not already present)
    if '_cc' not in content and 'formsubmit.co' in content:
        # Add CC field before submit buttons in estimate forms
        for btn_pattern in [
            '<button type="submit" class="btn-primary" id="est-submit">',
            '<button type="submit" class="form-submit">',
        ]:
            if btn_pattern in content:
                content = content.replace(btn_pattern, CC_FIELD + '\n      ' + btn_pattern)
                fixes['cc_added'] += 1
                break

    # 3. FIX FORM SUBMISSION - Add button state + GA4 event tracking
    # Pattern A: One-line submitEstimate (service pages, area pages, gallery, reviews, etc.)
    old_one_line = """function submitEstimate(e) { e.preventDefault(); var form = document.getElementById('estimateForm'); fetch('https://formsubmit.co/ajax/oliphant454@yahoo.com', { method: 'POST', body: new FormData(form) }).then(function(r) { return r.json(); }).then(function() { form.style.display = 'none'; document.getElementById('estimateSuccess').classList.add('show'); }).catch(function() { form.style.display = 'none'; document.getElementById('estimateSuccess').classList.add('show'); }); }"""

    new_one_line = """function submitEstimate(e) { e.preventDefault(); var form = document.getElementById('estimateForm'); var btn = form.querySelector('button[type="submit"]'); if(btn){btn.disabled=true;btn.textContent='Sending...';} fetch('https://formsubmit.co/ajax/oliphant454@yahoo.com', { method: 'POST', body: new FormData(form) }).then(function(r) { return r.json(); }).then(function() { gtag('event','generate_lead',{event_category:'estimate',event_label:'free_estimate_form'}); form.style.display = 'none'; document.getElementById('estimateSuccess').classList.add('show'); }).catch(function() { gtag('event','generate_lead',{event_category:'estimate',event_label:'free_estimate_form'}); form.style.display = 'none'; document.getElementById('estimateSuccess').classList.add('show'); }); }"""

    if old_one_line in content:
        content = content.replace(old_one_line, new_one_line)
        fixes['form_btn'] += 1

    # Pattern B: Multi-line submitEstimate in contact.html
    old_multi_est = """function submitEstimate(e) {
  e.preventDefault();
  var form = document.getElementById('estimateForm');
  var data = new FormData(form);
  fetch('https://formsubmit.co/ajax/oliphant454@yahoo.com', { method: 'POST', body: data })
  .then(function(r) { return r.json(); }).then(function() {
    form.style.display = 'none';
    document.getElementById('estimateSuccess').classList.add('show');
  })
  .catch(function() {
    form.style.display = 'none';
    document.getElementById('estimateSuccess').classList.add('show');
  });
}"""

    new_multi_est = """function submitEstimate(e) {
  e.preventDefault();
  var form = document.getElementById('estimateForm');
  var btn = form.querySelector('button[type="submit"]');
  if(btn){btn.disabled=true;btn.textContent='Sending...';}
  var data = new FormData(form);
  fetch('https://formsubmit.co/ajax/oliphant454@yahoo.com', { method: 'POST', body: data })
  .then(function(r) { return r.json(); }).then(function() {
    gtag('event','generate_lead',{event_category:'estimate',event_label:'free_estimate_form'});
    form.style.display = 'none';
    document.getElementById('estimateSuccess').classList.add('show');
  })
  .catch(function() {
    gtag('event','generate_lead',{event_category:'estimate',event_label:'free_estimate_form'});
    form.style.display = 'none';
    document.getElementById('estimateSuccess').classList.add('show');
  });
}"""

    if old_multi_est in content:
        content = content.replace(old_multi_est, new_multi_est)
        fixes['form_btn'] += 1

    # Pattern C: Multi-line submitContact in contact.html
    old_contact = """function submitContact(e) {
  e.preventDefault();
  var form = document.getElementById('contactForm');
  var data = new FormData(form);
  fetch('https://formsubmit.co/ajax/oliphant454@yahoo.com', { method: 'POST', body: data })
  .then(function(r) { return r.json(); }).then(function() {
    form.style.display = 'none';
    document.getElementById('contactSuccess').classList.add('show');
  })
  .catch(function() {
    form.style.display = 'none';
    document.getElementById('contactSuccess').classList.add('show');
  });
}"""

    new_contact = """function submitContact(e) {
  e.preventDefault();
  var form = document.getElementById('contactForm');
  var btn = form.querySelector('button[type="submit"]');
  if(btn){btn.disabled=true;btn.textContent='Sending...';}
  var data = new FormData(form);
  fetch('https://formsubmit.co/ajax/oliphant454@yahoo.com', { method: 'POST', body: data })
  .then(function(r) { return r.json(); }).then(function() {
    gtag('event','generate_lead',{event_category:'contact',event_label:'contact_form'});
    form.style.display = 'none';
    document.getElementById('contactSuccess').classList.add('show');
  })
  .catch(function() {
    gtag('event','generate_lead',{event_category:'contact',event_label:'contact_form'});
    form.style.display = 'none';
    document.getElementById('contactSuccess').classList.add('show');
  });
}"""

    if old_contact in content:
        content = content.replace(old_contact, new_contact)
        fixes['form_event'] += 1

    # Pattern D: index.html multi-line submitEstimate (slightly different formatting)
    # Check for any remaining unpatched submitEstimate that uses formsubmit
    if 'formsubmit.co' in content and 'generate_lead' not in content:
        # Inject GA4 event tracking into any remaining form handlers
        content = content.replace(
            "form.style.display = 'none';\n    document.getElementById('estimateSuccess').classList.add('show');",
            "gtag('event','generate_lead',{event_category:'estimate',event_label:'free_estimate_form'});\n    form.style.display = 'none';\n    document.getElementById('estimateSuccess').classList.add('show');"
        )
        fixes['form_event'] += 1

    # 4. ADD PHONE CLICK TRACKING (before </body>)
    if 'phone_click' not in content and '</body>' in content:
        content = content.replace('</body>', PHONE_TRACK + '\n</body>')
        fixes['phone_track'] += 1

    if content != original:
        with open(fpath, 'w', encoding='utf-8') as f:
            f.write(content)

print(f'GA4 ID updated: {fixes["ga4"]} files')
print(f'Form button state added: {fixes["form_btn"]} files')
print(f'Form GA4 events added: {fixes["form_event"]} files')
print(f'CC email added: {fixes["cc_added"]} files')
print(f'Phone click tracking added: {fixes["phone_track"]} files')
print(f'\nGA4 Measurement ID: {GA4_ID}')
print('Done!')
