"""
tests/test_friends.py — Mixtape

Tests for friend, noti, and rating logic.
"""

import pytest
from app import create_app, db
from models import User, Song, Playlist, playlist_entries, Notification
from services.feed_service import get_activity_feed, get_friends_listening_now


@pytest.fixture
def app():
    app = create_app({"TESTING": True, "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:"})
    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()



@pytest.fixture
def seed_friendship(app):
    u1 = User(username="testuser2", email="test2@example.com")
    u2 = User(username="testuser2", email="test2@example.com")
    db.session.add_all([u1, u2])
    db.session.flush()
    
    friendships = db.Table(
        "friendships",
        db.Column("user_id", db.String(36), db.ForeignKey("user.id"), primary_key=True),
        db.Column("friend_id", db.String(36), db.ForeignKey("user.id"), primary_key=True),
    )
    def add_friendship(user1, user2):
        db.session.execute(friendships.insert().values(user_id=user1.id, friend_id=user2.id))
        db.session.execute(friendships.insert().values(user_id=user2.id, friend_id=user1.id))
    add_friendship(u1,u2)
    db.session.commit()
    db.session.flush()
    
    songs = [
            Song(title=f"Track {i}", artist="Various", shared_by=u1.id)
            for i in range(1, 6)
        ]
    db.session.add_all(songs)
    db.session.flush()
    
    yield {"user_1": u1, "user2": u2, }
        
def test_friends_listening_now(app, seed_friendship):
    """A user with no prior listening history gets a streak of 1."""
    with app.app_context():
        u1 = seed_friendship['user_1']
        u2 = seed_friendship['user_2']
        get_friends_listening_now(u1.id)