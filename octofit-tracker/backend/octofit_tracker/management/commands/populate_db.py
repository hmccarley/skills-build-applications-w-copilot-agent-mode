from django.core.management.base import BaseCommand
from octofit_tracker.models import User, Team, Activity, Workout, Leaderboard
from django.db import transaction

class Command(BaseCommand):
    help = 'Populate the octofit_db database with test data'

    def handle(self, *args, **options):
        from bson import ObjectId

        with transaction.atomic():
            self.stdout.write(self.style.WARNING('Dropping MongoDB collections...'))
            # Drop MongoDB collections directly for each model using Djongo's collection attribute
            Leaderboard.objects.collection.drop()
            Activity.objects.collection.drop()
            Workout.objects.collection.drop()
            User.objects.collection.drop()
            Team.objects.collection.drop()

            self.stdout.write(self.style.SUCCESS('Creating teams...'))
            marvel = Team.objects.create(id=ObjectId(), name='Marvel', description='Marvel superheroes')
            dc = Team.objects.create(id=ObjectId(), name='DC', description='DC superheroes')

            self.stdout.write(self.style.SUCCESS('Creating users...'))
            users = [
                User.objects.create(id=ObjectId(), email='ironman@marvel.com', username='Iron Man', team=marvel),
                User.objects.create(id=ObjectId(), email='captain@marvel.com', username='Captain America', team=marvel),
                User.objects.create(id=ObjectId(), email='spiderman@marvel.com', username='Spider-Man', team=marvel),
                User.objects.create(id=ObjectId(), email='batman@dc.com', username='Batman', team=dc),
                User.objects.create(id=ObjectId(), email='superman@dc.com', username='Superman', team=dc),
                User.objects.create(id=ObjectId(), email='wonderwoman@dc.com', username='Wonder Woman', team=dc),
            ]

            self.stdout.write(self.style.SUCCESS('Creating activities...'))
            Activity.objects.create(id=ObjectId(), user=users[0], type='run', duration=30, date='2025-01-01')
            Activity.objects.create(id=ObjectId(), user=users[1], type='cycle', duration=45, date='2025-01-02')
            Activity.objects.create(id=ObjectId(), user=users[2], type='swim', duration=60, date='2025-01-03')
            Activity.objects.create(id=ObjectId(), user=users[3], type='run', duration=25, date='2025-01-01')
            Activity.objects.create(id=ObjectId(), user=users[4], type='cycle', duration=50, date='2025-01-02')
            Activity.objects.create(id=ObjectId(), user=users[5], type='swim', duration=70, date='2025-01-03')

            self.stdout.write(self.style.SUCCESS('Creating workouts...'))
            w1 = Workout.objects.create(id=ObjectId(), name='Pushups', description='Upper body strength')
            w2 = Workout.objects.create(id=ObjectId(), name='Situps', description='Core strength')
            w1.suggested_for.set([users[0], users[3]])
            w2.suggested_for.set([users[1], users[4]])

            self.stdout.write(self.style.SUCCESS('Creating leaderboard...'))
            Leaderboard.objects.create(id=ObjectId(), user=users[0], score=100)
            Leaderboard.objects.create(id=ObjectId(), user=users[1], score=90)
            Leaderboard.objects.create(id=ObjectId(), user=users[3], score=110)
            Leaderboard.objects.create(id=ObjectId(), user=users[4], score=95)

            self.stdout.write(self.style.SUCCESS('Test data created successfully!'))
