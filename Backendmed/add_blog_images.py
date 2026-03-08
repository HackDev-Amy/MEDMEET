#!/usr/bin/env python
import os
import sys
from pathlib import Path
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Backendmed.settings')
sys.path.insert(0, os.path.dirname(__file__))
django.setup()

from django.core.files.base import ContentFile
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
from medapp.models import Blog_DB

# Create placeholder images for each blog
blog_topics = {
    'preventative': ('The Role of Preventative Care', '#FF6B6B'),
    'mental-health': ('Mental Health Awareness', '#4ECDC4'),
    'heart-health': ('Heart Health Foods', '#FFE66D'),
    'exercise': ('Regular Exercise', '#95E1D3'),
    'sleep': ('Sleep & Health', '#A8D8EA'),
    'diabetes': ('Diabetes Management', '#F68084'),
    'stress': ('Stress Management', '#AA96DA'),
}

blogs = Blog_DB.objects.all()

for i, blog in enumerate(blogs):
    if not blog.Bimage:
        # Create a placeholder image
        width, height = 400, 300
        img = Image.new('RGB', (width, height), color=(220, 220, 220))
        draw = ImageDraw.Draw(img)
        
        # Add some color variety
        colors = ['#FF6B6B', '#4ECDC4', '#FFE66D', '#95E1D3', '#A8D8EA', '#F68084', '#AA96DA']
        color = colors[i % len(colors)]
        
        # Draw top colored band
        import colorsys
        hex_color = color.lstrip('#')
        rgb = tuple(int(hex_color[j:j+2], 16) for j in (0, 2, 4))
        draw.rectangle([(0, 0), (width, 100)], fill=rgb)
        
        # Add text
        try:
            # Try to use a default font, fallback to default if not found
            font = ImageFont.load_default()
        except:
            font = ImageFont.load_default()
        
        text = blog.Btitle[:30] + "..." if len(blog.Btitle) > 30 else blog.Btitle
        draw.text((20, 140), text, fill=(100, 100, 100), font=font)
        
        # Save to file
        img_io = BytesIO()
        img.save(img_io, format='JPEG')
        img_io.seek(0)
        
        filename = f'blog_image_{blog.id}.jpg'
        blog.Bimage.save(filename, ContentFile(img_io.read()), save=True)
        print(f"Added image to blog {blog.id}: {blog.Btitle[:40]}")
    else:
        print(f"Blog {blog.id} already has image")

print(f"\nTotal blogs with images: {Blog_DB.objects.exclude(Bimage='').count()} / {Blog_DB.objects.count()}")
