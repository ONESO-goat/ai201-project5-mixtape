"""
tests/test_streaks.py — Mixtape

Tests for listening streak logic.
"""

import pytest
from datetime import datetime, timedelta, timezone
from app import create_app, db
from models import User
from services.streak_service import update_listening_streak, get_streak


@pytest.fixture
def app():
    app = create_app({"TESTING": True, "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:"})
    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()


@pytest.fixture
def user(app):
    with app.app_context():
        u = User(username="testuser", email="test@example.com")
        db.session.add(u)
        db.session.commit()
        yield u


def test_streak_starts_at_1_for_new_user(app, user):
    """A user with no prior listening history gets a streak of 1."""
    with app.app_context():
        u = db.session.get(User, user.id)
        now = datetime(2024, 6, 10, 12, 0, 0, tzinfo=timezone.utc)  # Monday
        update_listening_streak(u, now)
        assert u.listening_streak == 1


def test_streak_increments_on_consecutive_day(app, user):
    """Listening on consecutive days increments the streak."""
    with app.app_context():
        u = db.session.get(User, user.id)
        monday = datetime(2024, 6, 10, 12, 0, 0, tzinfo=timezone.utc)
        tuesday = datetime(2024, 6, 11, 12, 0, 0, tzinfo=timezone.utc)

        update_listening_streak(u, monday)
        assert u.listening_streak == 1

        update_listening_streak(u, tuesday)
        assert u.listening_streak == 2


def test_streak_does_not_double_count_same_day(app, user):
    """Listening twice in the same day does not increment the streak twice."""
    with app.app_context():
        u = db.session.get(User, user.id)
        morning = datetime(2024, 6, 10, 9, 0, 0, tzinfo=timezone.utc)
        evening = datetime(2024, 6, 10, 20, 0, 0, tzinfo=timezone.utc)

        update_listening_streak(u, morning)
        assert u.listening_streak == 1

        update_listening_streak(u, evening)
        assert u.listening_streak == 1  # Should not change


def test_streak_resets_after_skipped_day(app, user):
    """Skipping a day resets the streak to 1."""
    with app.app_context():
        u = db.session.get(User, user.id)
        monday = datetime(2024, 6, 10, 12, 0, 0, tzinfo=timezone.utc)
        wednesday = datetime(2024, 6, 12, 12, 0, 0, tzinfo=timezone.utc)

        update_listening_streak(u, monday)
        assert u.listening_streak == 1

        update_listening_streak(u, wednesday)
        assert u.listening_streak == 1  # Reset because Tuesday was skipped


def test_streak_increments_on_sunday(app, user):
    """
    Listening on Saturday and then Sunday should increment the streak.
    """
    with app.app_context():
        u = db.session.get(User, user.id)
        saturday = datetime(2024, 6, 15, 12, 0, 0, tzinfo=timezone.utc)  # weekday() == 5
        sunday = datetime(2024, 6, 16, 12, 0, 0, tzinfo=timezone.utc)    # weekday() == 6
        
        # sat = 6/15/2024 12:00
        # sun = 6/16/2024 12:00
        # 24 hour difference
        
        # NOTE: Adding my own test case here, monday. This is to see what happens when the streaks is sunday -> monday
        monday = datetime(2024, 6, 17, 12, 0, 0, tzinfo=timezone.utc)    # weekday() == 0
        
        
        
        update_listening_streak(u, saturday)
        assert u.listening_streak == 1

        update_listening_streak(u, sunday) # TODO 2: The date 6/16/2024 isnt even taken to full effect in streak_service
        assert u.listening_streak == 2  # Should increment, not reset
        
        # if it was monday to sunday, thatll be 6 days. Since it's sunday to monday, it should be 1 day.
        update_listening_streak(u, monday)
        assert u.listening_streak == 3 

if __name__ in "__main__":
    test_streak_increments_on_sunday(app(), user())