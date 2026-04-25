import re
import os
from PIL import Image

THUMB_DIR = 'c:/Users/dckra/Desktop/website/photos/thumbs'
PHOTO_DIR = 'c:/Users/dckra/Desktop/website/photos'
THUMB_SIZE = (600, 600)
THUMB_QUALITY = 75

def get_location(desc):
    desc_lower = desc.lower()
    if 'pool' in desc_lower: return 'Pool Area'
    if 'bedroom' in desc_lower or 'bed' in desc_lower or 'nightstand' in desc_lower: return 'Bedroom'
    if 'kitchen' in desc_lower: return 'Kitchen'
    if 'living' in desc_lower or 'dining' in desc_lower: return 'Living & Dining Area'
    if 'balcony' in desc_lower: return 'Balcony'
    if 'exterior' in desc_lower or 'building' in desc_lower or 'tower' in desc_lower: return 'Exterior'
    if 'entrance' in desc_lower or 'sign' in desc_lower: return 'Entrance'
    if 'closet' in desc_lower: return 'Walk-in Closet'
    if 'bathroom' in desc_lower: return 'Bathroom'
    return 'Condo'

def generate_thumbnail(filename):
    """Generate a compressed thumbnail for a photo."""
    src = os.path.join(PHOTO_DIR, filename)
    dst = os.path.join(THUMB_DIR, filename)
    
    # Skip if thumbnail already exists and is newer than source
    if os.path.exists(dst) and os.path.getmtime(dst) >= os.path.getmtime(src):
        return
    
    try:
        with Image.open(src) as img:
            # Auto-orient based on EXIF data
            img = apply_exif_orientation(img)
            # Create thumbnail preserving aspect ratio
            img.thumbnail(THUMB_SIZE, Image.LANCZOS)
            # Convert to RGB if needed (handles RGBA, P mode etc.)
            if img.mode != 'RGB':
                img = img.convert('RGB')
            img.save(dst, 'JPEG', quality=THUMB_QUALITY, optimize=True)
            
            src_size = os.path.getsize(src) / 1024
            dst_size = os.path.getsize(dst) / 1024
            print(f'  Thumbnail: {filename} ({src_size:.0f}KB -> {dst_size:.0f}KB)')
    except Exception as e:
        print(f'  ERROR generating thumbnail for {filename}: {e}')

def apply_exif_orientation(img):
    """Apply EXIF orientation tag to correctly orient the image."""
    try:
        exif = img.getexif()
        orientation = exif.get(0x0112)  # 0x0112 = Orientation tag
        if orientation == 2:
            img = img.transpose(Image.FLIP_LEFT_RIGHT)
        elif orientation == 3:
            img = img.transpose(Image.ROTATE_180)
        elif orientation == 4:
            img = img.transpose(Image.FLIP_TOP_BOTTOM)
        elif orientation == 5:
            img = img.transpose(Image.ROTATE_270).transpose(Image.FLIP_LEFT_RIGHT)
        elif orientation == 6:
            img = img.transpose(Image.ROTATE_270)
        elif orientation == 7:
            img = img.transpose(Image.ROTATE_90).transpose(Image.FLIP_LEFT_RIGHT)
        elif orientation == 8:
            img = img.transpose(Image.ROTATE_90)
    except (AttributeError, KeyError):
        pass
    return img

# Ensure thumbs directory exists
os.makedirs(THUMB_DIR, exist_ok=True)

with open('c:/Users/dckra/Desktop/website/photo_review.md', 'r', encoding='utf-8') as f:
    lines = f.readlines()

photos = []
for line in lines:
    if line.startswith('|') and 'File Name' not in line and '---' not in line:
        parts = [p.strip() for p in line.split('|')]
        if len(parts) >= 4:
            filename = parts[1]
            desc = parts[2]
            rating_str = parts[3].split('/')[0].strip()
            try:
                rating = float(rating_str)
                if rating >= 4.0:
                    photos.append((rating, filename, desc))
            except ValueError:
                pass

# Sort by rating descending
photos.sort(key=lambda x: x[0], reverse=True)

# Generate thumbnails
print(f'Generating thumbnails for {len(photos)} photos...')
for rating, filename, desc in photos:
    generate_thumbnail(filename)

html = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Condo Gallery - Paul and Gligor IT</title>
    <meta name="description" content="Photo gallery of a luxury oceanfront condo in Panama - Paul and Gligor IT">
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Fira+Code:wght@400;600&family=Inter:wght@300;400;600&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="styles.css">
</head>
<body class="gallery-page">
    <div class="gallery-nav">
        <a href="index.html" class="back-link">← Return to Terminal</a>
        <div class="gallery-title">Archival Footage // Highly Rated</div>
    </div>
    
    <div class="fullscreen-gallery">
'''

for rating, filename, desc in photos:
    location = get_location(desc)
    desc_escaped = desc.replace("'", "\\'")
    html += f'''        <div class="gallery-item" onclick="openLightbox('photos/{filename}', '{desc_escaped}')">
            <div class="gallery-item-loader">
                <div class="loader-spinner"></div>
            </div>
            <img src="photos/thumbs/{filename}" alt="{location}" loading="lazy" onload="this.parentElement.querySelector('.gallery-item-loader').style.display='none'; this.style.opacity='1';">
            <div class="overlay">
                <div class="desc">{location}</div>
            </div>
        </div>\n'''

html += '''    </div>
    
    <div id="lightbox" class="lightbox">
        <span class="lightbox-close" onclick="closeLightbox()">&times;</span>
        <div id="lightbox-loader" class="lightbox-loader">
            <div class="loader-spinner large"></div>
        </div>
        <img id="lightbox-img" class="lightbox-content" src="">
        <div id="lightbox-caption" class="lightbox-caption"></div>
    </div>
    
    <script>
        function openLightbox(src, desc) {
            const img = document.getElementById('lightbox-img');
            const loader = document.getElementById('lightbox-loader');
            const lightbox = document.getElementById('lightbox');
            
            // Show lightbox with loader
            img.style.opacity = '0';
            loader.style.display = 'flex';
            lightbox.classList.add('active');
            document.body.style.overflow = 'hidden';
            
            // Set caption immediately
            document.getElementById('lightbox-caption').textContent = desc;
            
            // Load full-resolution image
            img.onload = function() {
                loader.style.display = 'none';
                img.style.opacity = '1';
            };
            img.src = src;
        }
        function closeLightbox() {
            const lightbox = document.getElementById('lightbox');
            lightbox.classList.remove('active');
            document.body.style.overflow = '';
            document.getElementById('lightbox-img').src = '';
        }
        document.getElementById('lightbox').addEventListener('click', function(e) {
            if(e.target === this) {
                closeLightbox();
            }
        });
        document.addEventListener('keydown', function(e) {
            if (e.key === 'Escape') closeLightbox();
        });
    </script>
</body>
</html>'''

with open('c:/Users/dckra/Desktop/website/gallery.html', 'w', encoding='utf-8') as f:
    f.write(html)

print(f'Generated gallery.html with {len(photos)} high-rated photos.')

# Print total size comparison
total_orig = sum(os.path.getsize(os.path.join(PHOTO_DIR, f)) for _, f, _ in photos) / (1024 * 1024)
total_thumb = sum(os.path.getsize(os.path.join(THUMB_DIR, f)) for _, f, _ in photos if os.path.exists(os.path.join(THUMB_DIR, f))) / (1024 * 1024)
print(f'\nTotal original size: {total_orig:.1f} MB')
print(f'Total thumbnail size: {total_thumb:.1f} MB')
print(f'Size reduction: {((total_orig - total_thumb) / total_orig * 100):.0f}%')
