from pathlib import Path
import re

tspan_content = Path('portrait_tspan.txt').read_text(encoding='utf-8').strip()

for filename in ['dark.svg', 'light.svg']:
    content = Path(filename).read_text(encoding='utf-8')
    
    # Pattern to match the <g transform="...">...</g> containing the ascii portrait
    pattern = r'(<g transform="[^"]*">\s*<text[^>]*class="ascii"[^>]*>)(.*?)(</text>\s*</g>)'
    
    def replacer(match):
        return f"{match.group(1)}{tspan_content}{match.group(3)}"
    
    new_content, count = re.subn(pattern, replacer, content, flags=re.DOTALL)
    if count > 0:
        Path(filename).write_text(new_content, encoding='utf-8')
        print(f"Successfully updated portrait in {filename}")
    else:
        print(f"Could not find portrait pattern in {filename}")
