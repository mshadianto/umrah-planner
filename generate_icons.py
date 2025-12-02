#!/usr/bin/env python3
"""
generate_icons.py - Generate PWA icons for LABBAIK

This script generates placeholder SVG icons for PWA.
For production, replace with actual PNG icons.

Usage:
    python generate_icons.py

Or use online generators:
    - https://www.pwabuilder.com/imageGenerator
    - https://realfavicongenerator.net/
"""

import os

# Icon sizes needed for PWA
ICON_SIZES = [16, 32, 72, 96, 128, 144, 152, 167, 180, 192, 384, 512]

# SVG template for LABBAIK icon
def generate_svg_icon(size):
    """Generate a simple SVG icon for LABBAIK"""
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}" viewBox="0 0 512 512">
  <defs>
    <linearGradient id="bg" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" style="stop-color:#1A1A1A"/>
      <stop offset="100%" style="stop-color:#2D2D2D"/>
    </linearGradient>
    <linearGradient id="gold" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" style="stop-color:#D4AF37"/>
      <stop offset="100%" style="stop-color:#C9A86C"/>
    </linearGradient>
  </defs>
  
  <!-- Background -->
  <rect width="512" height="512" rx="100" fill="url(#bg)"/>
  
  <!-- Border -->
  <rect x="20" y="20" width="472" height="472" rx="85" fill="none" stroke="url(#gold)" stroke-width="8"/>
  
  <!-- Kaaba symbol (simplified) -->
  <rect x="180" y="200" width="152" height="152" fill="url(#gold)" rx="10"/>
  <rect x="200" y="220" width="112" height="112" fill="#1A1A1A" rx="5"/>
  
  <!-- Crescent (simplified) -->
  <circle cx="256" cy="130" r="50" fill="url(#gold)"/>
  <circle cx="276" cy="120" r="40" fill="#1A1A1A"/>
  
  <!-- Star -->
  <polygon points="256,380 262,400 284,400 266,414 274,436 256,422 238,436 246,414 228,400 250,400" fill="url(#gold)"/>
</svg>'''


def generate_maskable_svg(size):
    """Generate a maskable icon with safe zone"""
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}" viewBox="0 0 512 512">
  <defs>
    <linearGradient id="bg" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" style="stop-color:#D4AF37"/>
      <stop offset="100%" style="stop-color:#C9A86C"/>
    </linearGradient>
  </defs>
  
  <!-- Full background for maskable -->
  <rect width="512" height="512" fill="url(#bg)"/>
  
  <!-- Content in safe zone (80% = 410px centered) -->
  <g transform="translate(51, 51)">
    <!-- Kaaba symbol -->
    <rect x="129" y="149" width="152" height="152" fill="#1A1A1A" rx="10"/>
    <rect x="149" y="169" width="112" height="112" fill="#D4AF37" rx="5"/>
    <rect x="169" y="189" width="72" height="72" fill="#1A1A1A" rx="3"/>
    
    <!-- Text "L" for LABBAIK -->
    <text x="205" y="245" font-family="Arial, sans-serif" font-size="60" font-weight="bold" fill="#D4AF37" text-anchor="middle">L</text>
  </g>
</svg>'''


def main():
    # Create icons directory
    icons_dir = "static/icons"
    os.makedirs(icons_dir, exist_ok=True)
    
    print("🎨 Generating LABBAIK PWA icons...")
    
    # Generate icons for each size
    for size in ICON_SIZES:
        # Regular icon
        svg_content = generate_svg_icon(size)
        filename = f"{icons_dir}/icon-{size}x{size}.svg"
        with open(filename, 'w') as f:
            f.write(svg_content)
        print(f"  ✓ {filename}")
    
    # Generate maskable icon
    maskable_svg = generate_maskable_svg(512)
    maskable_filename = f"{icons_dir}/maskable-512x512.svg"
    with open(maskable_filename, 'w') as f:
        f.write(maskable_svg)
    print(f"  ✓ {maskable_filename}")
    
    print(f"""
✅ Icons generated in {icons_dir}/

⚠️ IMPORTANT: These are SVG placeholders!
   For production, convert to PNG using:
   
   Option 1: Online converter
   - https://cloudconvert.com/svg-to-png
   - Upload SVGs, download PNGs
   
   Option 2: PWA Builder (Recommended)
   - https://www.pwabuilder.com/imageGenerator
   - Upload a 512x512 PNG logo
   - Download all sizes automatically
   
   Option 3: Python with Pillow + cairosvg
   - pip install pillow cairosvg
   - Convert SVGs programmatically
""")


if __name__ == "__main__":
    main()
