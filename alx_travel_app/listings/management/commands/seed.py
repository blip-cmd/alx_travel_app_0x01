import random
from datetime import datetime, timedelta
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from listings.models import Listing, Booking, Review
from faker import Faker

User = get_user_model()
fake = Faker()

class Command(BaseCommand):
    help = 'Seed the database with sample data'

    def handle(self, *args, **kwargs):
        self.stdout.write('Seeding database...')
        
        # Create sample users
        self.create_users()
        
        # Create sample listings
        self.create_listings()
        
        # Create sample bookings and reviews
        self.create_bookings_and_reviews()
        
        self.stdout.write(self.style.SUCCESS('Successfully seeded database'))

    def create_users(self):
        """Create sample users"""
        roles = ['guest', 'host', 'admin']
        
        for _ in range(10):
            User.objects.create_user(
                email=fake.email(),
                password='password123',
                first_name=fake.first_name(),
                last_name=fake.last_name(),
                phone_number=fake.phone_number(),
                role=random.choice(roles)
            )
        
        self.stdout.write('Created sample users')

    def create_listings(self):
        """Create sample listings"""
        hosts = User.objects.filter(role='host')
        
        for host in hosts:
            for _ in range(3):
                Listing.objects.create(
                    host=host,
                    name=fake.company(),
                    description=fake.text(),
                    location=fake.address(),
                    price_per_night=random.randint(50, 500)
                )
        
        self.stdout.write('Created sample listings')

    def create_bookings_and_reviews(self):
        """Create sample bookings and reviews"""
        guests = User.objects.filter(role='guest')
        listings = Listing.objects.all()
        status_choices = ['pending', 'confirmed', 'canceled']
        
        for guest in guests:
            for _ in range(2):
                listing = random.choice(listings)
                start_date = datetime.now() + timedelta(days=random.randint(1, 30))
                end_date = start_date + timedelta(days=random.randint(1, 7))
                
                # Create booking
                booking = Booking.objects.create(
                    property=listing,
                    user=guest,
                    start_date=start_date,
                    end_date=end_date,
                    total_price=listing.price_per_night * (end_date - start_date).days,
                    status=random.choice(status_choices)
                )
                
                # Create review (only for confirmed bookings)
                if booking.status == 'confirmed':
                    Review.objects.create(
                        property=listing,
                        user=guest,
                        rating=random.randint(1, 5),
                        comment=fake.text()
                    )
        
        self.stdout.write('Created sample bookings and reviews') 