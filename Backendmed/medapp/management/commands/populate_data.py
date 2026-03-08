from django.core.management.base import BaseCommand
from medapp.models import (
    Country_DB, Department_DB, hospital_DB, 
    Doctor_DB, Blog_DB, Pharmacy_DB
)

class Command(BaseCommand):
    help = 'Populate database with sample data'

    def handle(self, *args, **options):
        # Clear existing data
        Country_DB.objects.all().delete()
        Department_DB.objects.all().delete()
        hospital_DB.objects.all().delete()
        Doctor_DB.objects.all().delete()
        Blog_DB.objects.all().delete()
        Pharmacy_DB.objects.all().delete()
        
        self.stdout.write('Cleared existing data...')
        
        # Reset auto-increment counters for SQLite
        from django.db import connection
        cursor = connection.cursor()
        
        # Reset sequences for all models
        models_to_reset = [
            'Country_DB',
            'Department_DB',
            'hospital_DB',
            'Doctor_DB',
            'Blog_DB',
            'Pharmacy_DB',
        ]
        
        for model in models_to_reset:
            try:
                cursor.execute(f"DELETE FROM sqlite_sequence WHERE name = '{model}'")
            except:
                pass  # Table doesn't exist in some databases
        
        self.stdout.write('Reset auto-increment counters...')

        # Create Countries
        countries_data = [
            {'CON_name': 'United States'},
            {'CON_name': 'United Kingdom'},
            {'CON_name': 'Canada'},
            {'CON_name': 'Australia'},
            {'CON_name': 'India'},
        ]
        for country in countries_data:
            Country_DB.objects.create(**country)
        self.stdout.write(self.style.SUCCESS(f'✓ Created {len(countries_data)} countries'))

        # Create Departments
        departments_data = [
            {'DepName': 'Cardiology', 'DepTime': '9:00 AM - 5:00 PM'},
            {'DepName': 'Neurology', 'DepTime': '8:00 AM - 4:00 PM'},
            {'DepName': 'Orthopedics', 'DepTime': '9:00 AM - 5:00 PM'},
            {'DepName': 'Dermatology', 'DepTime': '10:00 AM - 6:00 PM'},
            {'DepName': 'Pediatrics', 'DepTime': '8:00 AM - 4:00 PM'},
            {'DepName': 'Surgery', 'DepTime': '7:00 AM - 3:00 PM'},
        ]
        for dept in departments_data:
            Department_DB.objects.create(**dept)
        self.stdout.write(self.style.SUCCESS(f'✓ Created {len(departments_data)} departments'))

        # Create Hospitals
        hospitals_data = [
            {
                'HosName': 'City General Hospital',
                'HosDept1': 'Cardiology',
                'HosDept2': 'Neurology',
                'HosDept3': 'Orthopedics',
                'HosDept4': 'Dermatology',
                'HosDept5': 'Pediatrics',
                'HosDept6': 'Surgery',
                'HosEmail': 'info@cityhospital.com',
                'HosWebsite': 'www.cityhospital.com',
                'HosCountry': 'United States',
                'HosNumber': '+1-555-0101',
            },
            {
                'HosName': 'Royal Medical Centre',
                'HosDept1': 'Cardiology',
                'HosDept2': 'Neurology',
                'HosDept3': 'Orthopedics',
                'HosDept4': 'Surgery',
                'HosDept5': 'Pediatrics',
                'HosDept6': 'Dermatology',
                'HosEmail': 'info@royalmedical.com',
                'HosWebsite': 'www.royalmedical.com',
                'HosCountry': 'United Kingdom',
                'HosNumber': '+44-20-7946',
            },
            {
                'HosName': 'Maple Leaf Healthcare',
                'HosDept1': 'Cardiology',
                'HosDept2': 'Dermatology',
                'HosDept3': 'Surgery',
                'HosDept4': 'Neurology',
                'HosDept5': 'Pediatrics',
                'HosDept6': 'Orthopedics',
                'HosEmail': 'contact@mapleleaf.ca',
                'HosWebsite': 'www.mapleleaf.ca',
                'HosCountry': 'Canada',
                'HosNumber': '+1-416-555',
            },
            {
                'HosName': 'Sydney Medical Institute',
                'HosDept1': 'Cardiology',
                'HosDept2': 'Neurology',
                'HosDept3': 'Orthopedics',
                'HosDept4': 'Dermatology',
                'HosDept5': 'Surgery',
                'HosDept6': 'Pediatrics',
                'HosEmail': 'info@sydneymedical.com',
                'HosWebsite': 'www.sydneymedical.com',
                'HosCountry': 'Australia',
                'HosNumber': '+61-2-9555',
            },
            {
                'HosName': 'Apollo Hospitals',
                'HosDept1': 'Cardiology',
                'HosDept2': 'Neurology',
                'HosDept3': 'Surgery',
                'HosDept4': 'Orthopedics',
                'HosDept5': 'Pediatrics',
                'HosDept6': 'Dermatology',
                'HosEmail': 'info@apollohospitals.com',
                'HosWebsite': 'www.apollohospitals.com',
                'HosCountry': 'India',
                'HosNumber': '+91-40-2333',
            },
        ]
        for hospital in hospitals_data:
            hospital_DB.objects.create(**hospital)
        self.stdout.write(self.style.SUCCESS(f'✓ Created {len(hospitals_data)} hospitals'))

        # Create Doctors
        doctors_data = [
            {
                'D_hospital': 'City General Hospital',
                'D_department': 'Cardiology',
                'D_name': 'Dr. Michael Johnson',
                'D_phone': '+1-555-0102',
                'D_email': 'michael.johnson@cityhospital.com',
                'D_age': '52',
                'D_gender': 'Male',
                'D_country': 'United States',
                'D_bio': 'Board-certified cardiologist with 20+ years of experience',
                'D_contract': True,
            },
            {
                'D_hospital': 'City General Hospital',
                'D_department': 'Neurology',
                'D_name': 'Dr. Sarah Williams',
                'D_phone': '+1-555-0103',
                'D_email': 'sarah.williams@cityhospital.com',
                'D_age': '48',
                'D_gender': 'Female',
                'D_country': 'United States',
                'D_bio': 'Specialist in neurological disorders and spine conditions',
                'D_contract': True,
            },
            {
                'D_hospital': 'Royal Medical Centre',
                'D_department': 'Orthopedics',
                'D_name': 'Dr. James Smith',
                'D_phone': '+44-20-7947',
                'D_email': 'james.smith@royalmedical.com',
                'D_age': '55',
                'D_gender': 'Male',
                'D_country': 'United Kingdom',
                'D_bio': 'Expert in joint replacement and sports medicine',
                'D_contract': True,
            },
            {
                'D_hospital': 'Royal Medical Centre',
                'D_department': 'Surgery',
                'D_name': 'Dr. Emily Brown',
                'D_phone': '+44-20-7948',
                'D_email': 'emily.brown@royalmedical.com',
                'D_age': '50',
                'D_gender': 'Female',
                'D_country': 'United Kingdom',
                'D_bio': 'General and laparoscopic surgeon with advanced training',
                'D_contract': True,
            },
            {
                'D_hospital': 'Maple Leaf Healthcare',
                'D_department': 'Pediatrics',
                'D_name': 'Dr. David Chen',
                'D_phone': '+1-416-556',
                'D_email': 'david.chen@mapleleaf.ca',
                'D_age': '45',
                'D_gender': 'Male',
                'D_country': 'Canada',
                'D_bio': 'Pediatrician specializing in developmental disorders',
                'D_contract': True,
            },
            {
                'D_hospital': 'Sydney Medical Institute',
                'D_department': 'Dermatology',
                'D_name': 'Dr. Lisa Anderson',
                'D_phone': '+61-2-9556',
                'D_email': 'lisa.anderson@sydneymedical.com',
                'D_age': '47',
                'D_gender': 'Female',
                'D_country': 'Australia',
                'D_bio': 'Dermatologist with expertise in skin cancer prevention',
                'D_contract': True,
            },
            {
                'D_hospital': 'Apollo Hospitals',
                'D_department': 'Cardiology',
                'D_name': 'Dr. Rajesh Kumar',
                'D_phone': '+91-40-2334',
                'D_email': 'rajesh.kumar@apollohospitals.com',
                'D_age': '54',
                'D_gender': 'Male',
                'D_country': 'India',
                'D_bio': 'Interventional cardiologist with advanced training abroad',
                'D_contract': True,
            },
            {
                'D_hospital': 'Apollo Hospitals',
                'D_department': 'Surgery',
                'D_name': 'Dr. Priya Sharma',
                'D_phone': '+91-40-2335',
                'D_email': 'priya.sharma@apollohospitals.com',
                'D_age': '49',
                'D_gender': 'Female',
                'D_country': 'India',
                'D_bio': 'Trauma and critical care surgeon with expertise in emergency surgery',
                'D_contract': True,
            },
        ]
        for doctor in doctors_data:
            Doctor_DB.objects.create(**doctor)
        self.stdout.write(self.style.SUCCESS(f'✓ Created {len(doctors_data)} doctors'))

        # Create Blogs
        blogs_data = [
            {
                'Btitle': 'Heart Health: Prevention is Better Than Cure',
                'Bcontent': 'Learn about the best practices to maintain a healthy heart. Regular exercise, balanced diet, and stress management are key factors in preventing cardiovascular diseases.',
                'Bwriter': 'Dr. Michael Johnson',
            },
            {
                'Btitle': 'Understanding Neurological Disorders',
                'Bcontent': 'This article explores common neurological conditions, their symptoms, and modern treatment approaches. Early diagnosis can significantly improve outcomes.',
                'Bwriter': 'Dr. Sarah Williams',
            },
            {
                'Btitle': 'Joint Health and Mobility',
                'Bcontent': 'Discover ways to maintain healthy joints and improve mobility as you age. Physical therapy and preventive measures are essential.',
                'Bwriter': 'Dr. James Smith',
            },
            {
                'Btitle': 'Surgical Advances in 2026',
                'Bcontent': 'Modern surgical techniques continue to evolve with minimally invasive procedures offering faster recovery times and better outcomes.',
                'Bwriter': 'Dr. Emily Brown',
            },
            {
                'Btitle': 'Pediatric Wellness: Growing Up Healthy',
                'Bcontent': 'Important tips for parents to ensure their children develop into healthy adults, from nutrition to mental health awareness.',
                'Bwriter': 'Dr. David Chen',
            },
            {
                'Btitle': 'Skin Care and Prevention',
                'Bcontent': 'Practical advice on protecting your skin from sun damage and maintaining healthy skin throughout your life.',
                'Bwriter': 'Dr. Lisa Anderson',
            },
        ]
        for blog in blogs_data:
            Blog_DB.objects.create(**blog)
        self.stdout.write(self.style.SUCCESS(f'✓ Created {len(blogs_data)} blogs'))

        # Create Pharmacy Items (WITHOUT IMAGES to avoid errors)
        pharmacy_data = [
            {
                'Medname': 'Aspirin 500mg',
                'Medprice': '$5.99',
                'Medqty': '100 tablets',
                'Medmanufacture': 'Bayer Healthcare',
                'Meduses': 'Pain relief, anti-inflammatory, blood thinner',
                'Medside': 'Mild stomach upset, allergic reactions in sensitive individuals',
                'Meddesc': 'Effective painkiller for mild to moderate pain and fever relief',
            },
            {
                'Medname': 'Amoxicillin 250mg',
                'Medprice': '$12.99',
                'Medqty': '30 capsules',
                'Medmanufacture': 'GlaxoSmithKline',
                'Meduses': 'Antibiotic for bacterial infections',
                'Medside': 'Nausea, diarrhea, allergic reactions',
                'Meddesc': 'Prescription antibiotic for treating various bacterial infections',
            },
            {
                'Medname': 'Vitamin C 1000mg',
                'Medprice': '$8.99',
                'Medqty': '60 tablets',
                'Medmanufacture': 'Nature Made',
                'Meduses': 'Immune support, antioxidant',
                'Medside': 'Generally well tolerated, may cause mild stomach upset in high doses',
                'Meddesc': 'Essential vitamin for immune system support and general wellness',
            },
            {
                'Medname': 'Ibuprofen 200mg',
                'Medprice': '$6.49',
                'Medqty': '40 tablets',
                'Medmanufacture': 'Advil',
                'Meduses': 'Anti-inflammatory, pain relief, fever reduction',
                'Medside': 'Stomach upset, headache, dizziness',
                'Meddesc': 'Fast-acting pain relief for headaches, minor aches and fever',
            },
            {
                'Medname': 'Metformin 500mg',
                'Medprice': '$15.99',
                'Medqty': '60 tablets',
                'Medmanufacture': 'Merck',
                'Meduses': 'Type 2 diabetes management',
                'Medside': 'Nausea, diarrhea, metallic taste',
                'Meddesc': 'First-line medication for managing type 2 diabetes',
            },
            {
                'Medname': 'Lisinopril 10mg',
                'Medprice': '$22.99',
                'Medqty': '30 tablets',
                'Medmanufacture': 'AstraZeneca',
                'Meduses': 'Blood pressure control',
                'Medside': 'Dizziness, persistent cough, fatigue',
                'Meddesc': 'ACE inhibitor for hypertension and heart failure management',
            },
            {
                'Medname': 'Omeprazole 20mg',
                'Medprice': '$18.99',
                'Medqty': '30 capsules',
                'Medmanufacture': 'Astellas Pharma',
                'Meduses': 'Acid reflux, GERD, ulcer prevention',
                'Medside': 'Headache, abdominal pain, nausea',
                'Meddesc': 'Proton pump inhibitor for managing gastric acid disorders',
            },
            {
                'Medname': 'Atorvastatin 20mg',
                'Medprice': '$24.99',
                'Medqty': '30 tablets',
                'Medmanufacture': 'Pfizer',
                'Meduses': 'Cholesterol management',
                'Medside': 'Muscle pain, liver enzyme changes, nausea',
                'Meddesc': 'Statin medication for lowering cholesterol levels',
            },
        ]
        for med in pharmacy_data:
            Pharmacy_DB.objects.create(**med)
        self.stdout.write(self.style.SUCCESS(f'✓ Created {len(pharmacy_data)} pharmacy items'))

        # Summary
        self.stdout.write(self.style.SUCCESS('\n✓ Database populated successfully with sample data!'))
        self.stdout.write(f'\nSummary:')
        self.stdout.write(f'  Countries: {Country_DB.objects.count()}')
        self.stdout.write(f'  Departments: {Department_DB.objects.count()}')
        self.stdout.write(f'  Hospitals: {hospital_DB.objects.count()}')
        self.stdout.write(f'  Doctors: {Doctor_DB.objects.count()}')
        self.stdout.write(f'  Blogs: {Blog_DB.objects.count()}')
        self.stdout.write(f'  Pharmacy Items: {Pharmacy_DB.objects.count()}')
