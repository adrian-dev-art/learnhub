from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password

User = get_user_model()

class Command(BaseCommand):
    help = 'Seeds the database with one user for each role'

    def handle(self, *args, **kwargs):
        self.stdout.write('Seeding roles...')

        roles_data = [
            {
                'username': 'admin',
                'email': 'admin@example.com',
                'password': 'admin123',
                'role': 'admin',
                'first_name': 'Admin',
                'last_name': 'User',
            },
            {
                'username': 'owner',
                'email': 'owner@example.com',
                'password': 'owner123',
                'role': 'owner',
                'first_name': 'Owner',
                'last_name': 'User',
            },
            {
                'username': 'mentor',
                'email': 'mentor@example.com',
                'password': 'mentor123',
                'role': 'penulis',
                'first_name': 'Mentor',
                'last_name': 'User',
            },
            {
                'username': 'student',
                'email': 'student@example.com',
                'password': 'student123',
                'role': 'pembaca',
                'first_name': 'Student',
                'last_name': 'User',
            },
        ]

        for data in roles_data:
            username = data.pop('username')
            password = data.pop('password')

            user, created = User.objects.get_or_create(
                username=username,
                defaults={
                    **data,
                    'password': make_password(password),
                    'email_verified': True,
                    'profile_completed': True,
                }
            )

            if created:
                self.stdout.write(self.style.SUCCESS(f'Successfully created {username} with role {data["role"]}'))
            else:
                # Update role if user already exists
                user.role = data['role']
                user.save()
                self.stdout.write(self.style.WARNING(f'User {username} already exists, updated role to {data["role"]}'))

        self.stdout.write(self.style.SUCCESS('Role seeding completed!'))
