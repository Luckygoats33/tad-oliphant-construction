"""Fix all SEO/UI/UX audit issues across all HTML files and redeploy."""
import os, re, glob

ROOT = r'C:\Users\willw\Projects\tad-oliphant-construction'
os.chdir(ROOT)

# GA4 snippet to inject (placeholder ID - Tad needs to create a GA4 property)
GA4_SNIPPET = '''<!-- Google Analytics -->
<script async src="https://www.googletagmanager.com/gtag/js?id=G-XXXXXXXXXX"></script>
<script>window.dataLayer=window.dataLayer||[];function gtag(){dataLayer.push(arguments);}gtag('js',new Date());gtag('config','G-XXXXXXXXXX');</script>'''

# Collect all HTML files
html_files = glob.glob('*.html') + glob.glob('services/*.html') + glob.glob('blog/*.html')
# Exclude print materials
exclude = {'businesscard.html', 'doorhanger.html', 'postcard.html', 'onepage.html'}
html_files = [f for f in html_files if os.path.basename(f) not in exclude]

print(f'Processing {len(html_files)} HTML files...')

# Nav block - old (missing 3 services)
OLD_NAV_DROPDOWN = '''<ul class="nav-dropdown">
          <li><a href="services/deck-construction.html">Deck Construction</a></li>
          <li><a href="services/deck-repair.html">Deck Repair</a></li>
          <li><a href="services/siding-repair.html">Siding &amp; Exterior</a></li>
          <li><a href="services/dry-rot-repair.html">Dry-Rot Repair</a></li>
          <li><a href="services/roofing.html">Roofing</a></li>
          <li><a href="services/windows-doors.html">Windows &amp; Doors</a></li>
          <li><a href="services/home-remodeling.html">Remodeling</a></li>
          <li><a href="services/painting.html">Painting</a></li>
          <li><a href="services/fencing.html">Fencing</a></li>
        </ul>'''

NEW_NAV_DROPDOWN = '''<ul class="nav-dropdown">
          <li><a href="services/deck-construction.html">Deck Construction</a></li>
          <li><a href="services/deck-repair.html">Deck Repair</a></li>
          <li><a href="services/siding-repair.html">Siding &amp; Exterior</a></li>
          <li><a href="services/dry-rot-repair.html">Dry-Rot Repair</a></li>
          <li><a href="services/roofing.html">Roofing</a></li>
          <li><a href="services/windows-doors.html">Windows &amp; Doors</a></li>
          <li><a href="services/home-remodeling.html">Remodeling</a></li>
          <li><a href="services/kitchen-remodeling.html">Kitchen Remodeling</a></li>
          <li><a href="services/bathroom-remodeling.html">Bathroom Remodeling</a></li>
          <li><a href="services/framing-structural-repair.html">Framing &amp; Structural</a></li>
          <li><a href="services/painting.html">Painting</a></li>
          <li><a href="services/fencing.html">Fencing</a></li>
        </ul>'''

# For service pages that use relative paths like ../services/
OLD_NAV_DROPDOWN_REL = OLD_NAV_DROPDOWN.replace('services/', '../services/')
NEW_NAV_DROPDOWN_REL = NEW_NAV_DROPDOWN.replace('services/', '../services/')

fixes = {
    'ga4_added': 0,
    'nav_fixed': 0,
    'services_link_fixed': 0,
    'years_fixed': 0,
    'reveal_fixed': 0,
    'social_added': 0,
    'contrast_note': 0,
}

for fpath in html_files:
    with open(fpath, 'r', encoding='utf-8') as f:
        content = f.read()

    original = content
    is_service = fpath.startswith('services')
    is_blog = fpath.startswith('blog')

    # 1. ADD GA4 SNIPPET after <link rel="stylesheet" href="styles.css">
    if 'gtag/js?id=G-' not in content:
        # Find the stylesheet link to inject after
        if '<link rel="stylesheet" href="styles.css">' in content:
            content = content.replace(
                '<link rel="stylesheet" href="styles.css">',
                '<link rel="stylesheet" href="styles.css">\n' + GA4_SNIPPET
            )
            fixes['ga4_added'] += 1
        elif '<link rel="stylesheet" href="../styles.css">' in content:
            content = content.replace(
                '<link rel="stylesheet" href="../styles.css">',
                '<link rel="stylesheet" href="../styles.css">\n' + GA4_SNIPPET
            )
            fixes['ga4_added'] += 1

    # 2. FIX NAV - Add missing services + make Services parent link a service-areas page
    if is_service or is_blog:
        if OLD_NAV_DROPDOWN_REL in content:
            content = content.replace(OLD_NAV_DROPDOWN_REL, NEW_NAV_DROPDOWN_REL)
            fixes['nav_fixed'] += 1
        # Fix services parent link
        content = content.replace(
            '<a href="../services/deck-construction.html">Services <span class="caret"></span></a>',
            '<a href="../service-areas.html">Services <span class="caret"></span></a>'
        )
    else:
        if OLD_NAV_DROPDOWN in content:
            content = content.replace(OLD_NAV_DROPDOWN, NEW_NAV_DROPDOWN)
            fixes['nav_fixed'] += 1
        # Fix services parent link
        content = content.replace(
            '<a href="services/deck-construction.html">Services <span class="caret"></span></a>',
            '<a href="service-areas.html">Services <span class="caret"></span></a>'
        )

    # 3. FIX YEARS CONSISTENCY - "since 2015" -> "with 20+ years of experience"
    # In meta descriptions
    content = content.replace('Serving Lincoln County since 2015.', 'Serving Lincoln County with 20+ years of experience.')
    # In JSON-LD description
    content = content.replace('Serving Lincoln County since 2015."', 'Serving Lincoln County with 20+ years of experience."')
    # Badge "Since 2015" -> "20+ Years"
    content = content.replace(
        '<div class="badge"><span class="badge-icon">&#128736;</span> Since 2015</div>',
        '<div class="badge"><span class="badge-icon">&#128736;</span> 20+ Years Experience</div>'
    )
    # "10+ Years" variants
    content = content.replace('10+ Years of Experience', '20+ Years of Experience')
    content = content.replace('10+ years of experience', '20+ years of experience')
    # Footer text
    content = content.replace(
        'Serving Lincoln County since 2015. Licensed',
        'Serving Lincoln County with 20+ years of experience. Licensed'
    )
    if 'since 2015' in content.lower() or '10+ year' in content.lower():
        fixes['years_fixed'] += 1

    # 4. ADD SOCIAL LINKS TO FOOTER (before footer-bottom)
    social_block = '''    <div class="footer-social" style="text-align:center;padding:1rem 0 0;">
      <a href="https://www.google.com/maps/place/Tad+Oliphant+Construction+LLC" target="_blank" rel="noopener" style="display:inline-flex;align-items:center;gap:0.4rem;color:#E8913A;font-weight:700;text-decoration:none;font-size:0.95rem;">
        <svg width="20" height="20" viewBox="0 0 48 48" xmlns="http://www.w3.org/2000/svg"><path fill="#EA4335" d="M24 9.5c3.54 0 6.71 1.22 9.21 3.6l6.85-6.85C35.9 2.38 30.47 0 24 0 14.62 0 6.51 5.38 2.56 13.22l7.98 6.19C12.43 13.72 17.74 9.5 24 9.5z"/><path fill="#4285F4" d="M46.98 24.55c0-1.57-.15-3.09-.38-4.55H24v9.02h12.94c-.58 2.96-2.26 5.48-4.78 7.18l7.73 6c4.51-4.18 7.09-10.36 7.09-17.65z"/><path fill="#34A853" d="M10.53 28.59A14.5 14.5 0 019.5 24c0-1.59.28-3.14.76-4.59l-7.98-6.19A23.99 23.99 0 000 24c0 3.77.9 7.35 2.56 10.54l7.97-5.95z"/><path fill="#FBBC05" d="M24 48c6.48 0 11.93-2.13 15.89-5.81l-7.73-6c-2.15 1.45-4.92 2.3-8.16 2.3-6.26 0-11.57-4.22-13.47-9.91l-7.98 5.95C6.51 42.62 14.62 48 24 48z"/></svg>
        Find Us on Google
      </a>
      &nbsp;&nbsp;&middot;&nbsp;&nbsp;
      <a href="https://www.bbb.org/us/or/siletz/profile/general-contractor/tad-oliphant-construction-llc-1296-22580820" target="_blank" rel="noopener" style="display:inline-flex;align-items:center;gap:0.4rem;color:#E8913A;font-weight:700;text-decoration:none;font-size:0.95rem;">
        BBB Profile
      </a>
    </div>
'''
    if 'footer-social' not in content and '<div class="footer-bottom">' in content:
        content = content.replace(
            '    <div class="footer-bottom">',
            social_block + '    <div class="footer-bottom">'
        )
        fixes['social_added'] += 1

    if content != original:
        with open(fpath, 'w', encoding='utf-8') as f:
            f.write(content)

print(f'GA4 snippet added: {fixes["ga4_added"]} files')
print(f'Nav dropdown fixed (3 services added): {fixes["nav_fixed"]} files')
print(f'Years consistency fixed: {fixes["years_fixed"]} files')
print(f'Social/GBP links added to footer: {fixes["social_added"]} files')

# 5. FIX REVEAL ANIMATION in styles.css
print('\nFixing styles.css...')
with open('styles.css', 'r', encoding='utf-8') as f:
    css = f.read()

# Make reveal start at partial opacity so content isn't invisible
css = css.replace(
    '.reveal {\n  opacity: 0; transform: translateY(28px);',
    '.reveal {\n  opacity: 0.15; transform: translateY(12px);'
)
# Also handle single-line variant
css = re.sub(
    r'\.reveal\s*\{\s*opacity:\s*0;\s*transform:\s*translateY\(28px\)',
    '.reveal { opacity: 0.15; transform: translateY(12px)',
    css
)
css = css.replace(
    '.reveal-left { opacity: 0; transform: translateX(-40px)',
    '.reveal-left { opacity: 0.15; transform: translateX(-20px)'
)
css = css.replace(
    '.reveal-right { opacity: 0; transform: translateX(40px)',
    '.reveal-right { opacity: 0.15; transform: translateX(20px)'
)
css = css.replace(
    '.reveal-scale { opacity: 0; transform: scale(0.92)',
    '.reveal-scale { opacity: 0.15; transform: scale(0.96)'
)

# 6. IMPROVE TEXT CONTRAST - darken light grays
# Common low-contrast patterns
css = css.replace('color: rgba(255,255,255,0.55)', 'color: rgba(255,255,255,0.78)')
css = css.replace('color:rgba(255,255,255,0.55)', 'color:rgba(255,255,255,0.78)')
css = css.replace('color: rgba(255,255,255,0.6)', 'color: rgba(255,255,255,0.8)')
css = css.replace('color:rgba(255,255,255,0.6)', 'color:rgba(255,255,255,0.8)')

with open('styles.css', 'w', encoding='utf-8') as f:
    f.write(css)
print('Reveal animations softened (partial opacity start)')
print('Text contrast improved')

# 7. UPDATE 404.html to be a proper error page with navigation
print('\nUpdating 404.html...')
with open('404.html', 'r', encoding='utf-8') as f:
    four04 = f.read()

# Check if it already has nav - if so, it's probably fine
if '<nav' in four04:
    print('404.html already has navigation - checking for clean URL redirect script')

# Add a JS snippet for clean URL redirects at end of body
redirect_script = '''
<script>
// Handle clean URLs - redirect /about to /about.html etc.
(function() {
  var path = window.location.pathname;
  if (path !== '/' && !path.match(/\\.\\w+$/) && !path.endsWith('/')) {
    window.location.replace(path + '.html');
  }
})();
</script>
'''
if 'Handle clean URLs' not in four04:
    four04 = four04.replace('</body>', redirect_script + '</body>')
    if '</body>' not in four04:
        four04 += redirect_script
    with open('404.html', 'w', encoding='utf-8') as f:
        f.write(four04)
    print('Added clean URL redirect script to 404.html')

print('\nAll fixes applied!')
