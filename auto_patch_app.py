#!/usr/bin/env python3
"""
AUTO-PATCH SCRIPT: Fix render_invite_modal() in app.py
Version: 1.0
Author: Claude + MS Hadianto
Date: 2025-12-06

This script automatically fixes the HTML rendering issue in render_invite_modal()
"""

import re
import sys
from pathlib import Path

# ============================================
# FIXED FUNCTION CODE
# ============================================
FIXED_FUNCTION = '''# ============================================
# FIXED: render_invite_modal - HTML RENDERING  
# ============================================
def render_invite_modal(referral_code):
    """Render invite modal with proper HTML rendering - FIXED VERSION v3.5.1"""
    share_url = f"https://labbaik.streamlit.app?ref={referral_code}"
    
    # Build HTML content separately for better parsing
    html_content = f"""
<div style="background: linear-gradient(135deg, #1A1A1A 0%, #1E3D2F 100%);
            border-radius: 25px; padding: 30px; margin: 20px 0;
            border: 2px solid #4CAF5040; text-align: center;">
    
    <div style="font-size: 3rem; margin-bottom: 15px;">🎁</div>
    <div style="color: white; font-size: 1.5rem; font-weight: 700; margin-bottom: 10px;">
        Ajak Teman, Dapat Bonus!
    </div>
    <div style="color: #C9A86C; margin-bottom: 25px;">
        Kamu dan temanmu masing-masing dapat <strong style="color: #D4AF37;">bonus LP!</strong>
    </div>
    
    <div style="display: flex; justify-content: center; gap: 30px; margin-bottom: 25px; flex-wrap: wrap;">
        <div style="background: #1A1A1A; border-radius: 15px; padding: 15px 25px;">
            <div style="color: #C9A86C; font-size: 0.8rem;">Kamu Dapat</div>
            <div style="color: #D4AF37; font-size: 1.5rem; font-weight: 700;">+200 LP</div>
        </div>
        <div style="background: #1A1A1A; border-radius: 15px; padding: 15px 25px;">
            <div style="color: #C9A86C; font-size: 0.8rem;">Teman Dapat</div>
            <div style="color: #4CAF50; font-size: 1.5rem; font-weight: 700;">+75 LP</div>
        </div>
    </div>
    
    <div style="background: #1A1A1A; border: 2px dashed #D4AF3750;
                border-radius: 15px; padding: 15px; margin-bottom: 20px;">
        <div style="color: #C9A86C; font-size: 0.8rem; margin-bottom: 5px;">Kode Referral</div>
        <div style="color: #D4AF37; font-size: 2rem; font-weight: 800; letter-spacing: 4px;">
            {referral_code}
        </div>
    </div>
    
    <div style="background: #2D2D2D; border-radius: 10px; padding: 12px;
                margin-bottom: 20px;">
        <span style="color: #C9A86C; font-size: 0.85rem; word-break: break-all;">
            {share_url}
        </span>
    </div>
    
    <div style="display: flex; justify-content: center; gap: 10px; flex-wrap: wrap;">
        <a href="https://wa.me/?text=Yuk%20rencanakan%20umrah%20bareng%20LABBAIK!%20Pakai%20kode%20{referral_code}%20untuk%20bonus%20LP!%20{share_url}" 
           target="_blank" style="background: #25D366; color: white; padding: 10px 20px; 
           border-radius: 25px; text-decoration: none; font-weight: 600;">
            📱 WhatsApp
        </a>
        <a href="https://t.me/share/url?url={share_url}&text=Yuk%20rencanakan%20umrah%20bareng%20LABBAIK!" 
           target="_blank" style="background: #0088cc; color: white; padding: 10px 20px; 
           border-radius: 25px; text-decoration: none; font-weight: 600;">
            ✈️ Telegram
        </a>
    </div>
</div>
"""
    
    # CRITICAL: Render with unsafe_allow_html=True
    st.markdown(html_content, unsafe_allow_html=True)
'''


def backup_file(filepath):
    """Create backup of original file"""
    backup_path = filepath.parent / f"{filepath.name}.backup"
    if backup_path.exists():
        print(f"⚠️  Backup already exists: {backup_path}")
        response = input("Overwrite backup? (y/n): ")
        if response.lower() != 'y':
            print("❌ Backup cancelled")
            return False
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    with open(backup_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"✅ Backup created: {backup_path}")
    return True


def find_function_bounds(content):
    """Find start and end lines of render_invite_modal function"""
    lines = content.split('\n')
    start_line = None
    end_line = None
    indent_level = None
    
    for i, line in enumerate(lines):
        # Find function definition
        if 'def render_invite_modal(' in line:
            start_line = i
            # Get indentation level (count leading spaces)
            indent_level = len(line) - len(line.lstrip())
            continue
        
        # Find end of function
        if start_line is not None and end_line is None:
            # Check if we found a new function at same indent level
            if line.strip() and not line.strip().startswith('#'):
                current_indent = len(line) - len(line.lstrip())
                if current_indent == indent_level and line.strip().startswith('def '):
                    end_line = i - 1
                    break
    
    # If no end found, search for next non-indented line or end of file
    if start_line is not None and end_line is None:
        for i in range(start_line + 1, len(lines)):
            line = lines[i]
            if line.strip() and not line.strip().startswith('#'):
                current_indent = len(line) - len(line.lstrip())
                if current_indent <= indent_level and not line.strip().startswith('"""'):
                    end_line = i - 1
                    break
        if end_line is None:
            end_line = len(lines) - 1
    
    return start_line, end_line


def apply_patch(filepath):
    """Apply patch to app.py"""
    print("=" * 60)
    print("🔧 AUTO-PATCH: Fix render_invite_modal() HTML Rendering")
    print("=" * 60)
    
    # Read file
    print(f"\n📖 Reading: {filepath}")
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find function bounds
    print("🔍 Locating render_invite_modal()...")
    start_line, end_line = find_function_bounds(content)
    
    if start_line is None:
        print("❌ ERROR: Could not find render_invite_modal() function!")
        return False
    
    print(f"✅ Found function at lines {start_line + 1} to {end_line + 1}")
    
    # Create backup
    print("\n💾 Creating backup...")
    if not backup_file(filepath):
        return False
    
    # Replace function
    print("\n✏️  Applying patch...")
    lines = content.split('\n')
    new_lines = lines[:start_line] + [FIXED_FUNCTION] + lines[end_line + 1:]
    new_content = '\n'.join(new_lines)
    
    # Write patched file
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    print(f"✅ Patch applied successfully!")
    print(f"📄 File: {filepath}")
    print(f"🔄 Lines changed: {start_line + 1}-{end_line + 1} replaced with fixed version")
    
    return True


def main():
    """Main entry point"""
    print("\n" + "=" * 60)
    print("   LABBAIK AUTO-PATCH SCRIPT v1.0")
    print("   Fix: render_invite_modal() HTML Rendering")
    print("=" * 60)
    
    # Get app.py path
    if len(sys.argv) > 1:
        filepath = Path(sys.argv[1])
    else:
        filepath = Path('app.py')
    
    if not filepath.exists():
        print(f"\n❌ ERROR: File not found: {filepath}")
        print("\nUsage:")
        print(f"  python {sys.argv[0]} [path/to/app.py]")
        print(f"\nOr place this script in same directory as app.py and run:")
        print(f"  python {sys.argv[0]}")
        sys.exit(1)
    
    print(f"\n📁 Target: {filepath.absolute()}")
    print(f"📊 File size: {filepath.stat().st_size:,} bytes")
    
    # Confirm
    print("\n⚠️  This will modify your app.py file!")
    print("   (A backup will be created as app.py.backup)")
    response = input("\nContinue? (y/n): ")
    
    if response.lower() != 'y':
        print("❌ Patch cancelled by user")
        sys.exit(0)
    
    # Apply patch
    if apply_patch(filepath):
        print("\n" + "=" * 60)
        print("✅ SUCCESS! Patch applied successfully!")
        print("=" * 60)
        print("\n📋 Next steps:")
        print("  1. Review the changes (compare with .backup file)")
        print("  2. Test the app: streamlit run app.py")
        print("  3. Check tab '🎁 Ajak Teman' - HTML should render correctly")
        print("\n🔙 To rollback:")
        print(f"  mv {filepath}.backup {filepath}")
        print("\n✨ Happy coding!")
    else:
        print("\n❌ Patch failed!")
        sys.exit(1)


if __name__ == '__main__':
    main()
