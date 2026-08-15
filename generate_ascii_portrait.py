from PIL import Image, ImageEnhance, ImageFilter

# Load image
img = Image.open('profile_photo_source.png').convert('RGB')
w, h = img.size

# Target dimensions for portrait in SVG: ~76 width, ~52 height
target_w = 76
target_h = 52

# Create a clean mask for the background
# The photo has a solid red background: (131, 28, 21)
mask = Image.new('L', (w, h), 0)
for y in range(h):
    for x in range(w):
        r, g, b = img.getpixel((x, y))
        # Precise red background threshold
        if (r > 65 and r > g * 1.35 and r > b * 1.35) or (r > 95 and g < 65 and b < 65):
            mask.putpixel((x, y), 0) # Background
        else:
            mask.putpixel((x, y), 255) # Foreground person

# Smooth mask to remove speckles
mask = mask.filter(ImageFilter.MedianFilter(size=5))

# Convert foreground to high-contrast grayscale
gray = img.convert('L')
enhancer = ImageEnhance.Contrast(gray)
gray = enhancer.enhance(1.45)
enhancer = ImageEnhance.Sharpness(gray)
gray = enhancer.enhance(1.6)

# Resize to target ASCII grid
resized = gray.resize((target_w, target_h), Image.Resampling.LANCZOS)
resized_mask = mask.resize((target_w, target_h), Image.Resampling.LANCZOS)

# ASCII ramp - 10 levels
ramp = " .:-=+*#%@"

out_lines = []
for y in range(target_h):
    line = ""
    for x in range(target_w):
        m_val = resized_mask.getpixel((x, y))
        val = resized.getpixel((x, y))
        
        # In the top 8 rows (above head), filter out noise
        if y < 8:
            line += " "
            continue
            
        # Only render if foreground mask is strong (>130)
        if m_val < 130 or val < 12:
            line += " "
        else:
            idx = 1 + int((val / 255.0) * (len(ramp) - 2))
            idx = max(1, min(len(ramp) - 1, idx))
            line += ramp[idx]
    out_lines.append(line.rstrip())

with open('portrait.txt', 'w', encoding='utf-8') as f:
    f.write('\n'.join(out_lines))

print(f"Generated clean portrait.txt ({len(out_lines)} lines)")
