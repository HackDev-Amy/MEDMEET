#!/usr/bin/env python
import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Backendmed.settings')
sys.path.insert(0, os.path.dirname(__file__))
django.setup()

from medapp.models import Blog_DB

blog_samples = [
    {
        'Btitle': 'Mental Health Awareness: Breaking the Stigma',
        'Bwriter': 'Dr. Sarah Anderson',
        'Bcontent': 'Mental health is just as important as physical health. Understanding mental health conditions helps reduce stigma and encourages people to seek help when needed. This article explores common mental health disorders, their symptoms, and available treatment options.'
    },
    {
        'Btitle': 'Top 10 Foods for Heart Health',
        'Bwriter': 'Nutritionist James Clark',
        'Bcontent': 'A healthy diet is crucial for maintaining a strong cardiovascular system. Learn about the top 10 foods that can improve your heart health, including omega-3 rich fish, leafy greens, whole grains, and more. Incorporate these foods into your daily diet for a healthier heart.'
    },
    {
        'Btitle': 'The Importance of Regular Exercise',
        'Bwriter': 'Fitness Expert Maria Rodriguez',
        'Bcontent': 'Regular physical activity is essential for maintaining good health. Exercise helps strengthen muscles, improve cardiovascular health, boost mental well-being, and maintain a healthy weight. This comprehensive guide covers different types of exercises suitable for all age groups.'
    },
    {
        'Btitle': 'Sleep: The Foundation of Good Health',
        'Bwriter': 'Dr. Michael Thompson',
        'Bcontent': 'Quality sleep is vital for our overall health and well-being. During sleep, our brain and body undergo essential restoration processes. Learn about sleep stages, factors affecting sleep quality, and practical tips for improving your sleep hygiene.'
    },
    {
        'Btitle': 'Understanding Diabetes: Prevention and Management',
        'Bwriter': 'Dr. Emily Watson',
        'Bcontent': 'Diabetes is a chronic condition affecting millions worldwide. Understanding its types, risk factors, and management strategies is crucial. This article provides comprehensive information about Type 1 and Type 2 diabetes, prevention methods, and lifestyle changes for better management.'
    },
    {
        'Btitle': 'Stress Management Techniques for Busy Professionals',
        'Bwriter': 'Wellness Coach Robert Lee',
        'Bcontent': 'Chronic stress can have serious health implications. For busy professionals, finding effective stress management techniques is essential. Explore evidence-based methods including meditation, deep breathing, yoga, and time management strategies to reduce stress effectively.'
    }
]

for blog in blog_samples:
    Blog_DB.objects.create(**blog)
    print(f"Created blog: {blog['Btitle']}")

print(f"\nTotal blogs now: {Blog_DB.objects.count()}")
