import re

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

html = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Condo Gallery - Paul and Gligor IT</title>
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
            <img src="photos/{filename}" alt="{location}" loading="lazy">
            <div class="overlay">
                <div class="desc">{location}</div>
            </div>
        </div>\n'''

html += '''    </div>
    
    <div id="lightbox" class="lightbox">
        <span class="lightbox-close" onclick="closeLightbox()">&times;</span>
        <img id="lightbox-img" class="lightbox-content" src="">
        <div id="lightbox-caption" class="lightbox-caption"></div>
    </div>
    
    <script>
        function openLightbox(src, desc) {
            document.getElementById('lightbox-img').src = src;
            document.getElementById('lightbox-caption').textContent = desc;
            document.getElementById('lightbox').classList.add('active');
        }
        function closeLightbox() {
            document.getElementById('lightbox').classList.remove('active');
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
