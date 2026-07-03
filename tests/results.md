# Result 1

```
============================= test session starts =============================
platform linux -- Python 3.11.2, pytest-9.0.3, pluggy-1.6.0
rootdir: /home/oneso/codepath/ai201-lab1-rulesbot-starter/ai201-project5-mixtape
plugins: anyio-4.13.0
collected 13 items                                                            

tests/test_playlists.py FF.                                             [ 23%]
tests/test_search.py .....                                              [ 61%]
tests/test_streaks.py ....F                                             [100%]

================================== FAILURES ===================================
_______________________ test_playlist_returns_all_songs _______________________

app = <Flask 'app'>
seed_playlist = {'playlist': <Playlist 6b7a1e2b-0653-49e7-8b2e-e0067acf74ed>, 'songs': [<Song 17f535f7-2575-4ae5-81d1-28b88f162f62>, <...-939d-3105f7d3bd27>, <Song efbaa868-8e64-45fd-9ea4-21d63c7b6732>], 'user': <User a0c9896d-6797-408d-9c88-4d279d0795d6>}

    def test_playlist_returns_all_songs(app, seed_playlist):
        """
        get_playlist_songs should return all songs in the playlist.
        """
        with app.app_context():
            playlist_id = seed_playlist["playlist"].id
            songs = get_playlist_songs(playlist_id)
>           assert len(songs) == 5  # Bug causes this to return 4
            ^^^^^^^^^^^^^^^^^^^^^^
E           AssertionError: assert 4 == 5
E            +  where 4 = len([{'album': None, 'artist': 'Various', 'genre': None, 'id': '17f535f7-2575-4ae5-81d1-28b88f162f62', ...}, {'album': Non...302e2ac', ...}, {'album': None, 'artist': 'Various', 'genre': None, 'id': '10312a9e-4b85-426d-939d-3105f7d3bd27', ...}])

tests/test_playlists.py:62: AssertionError
____________________ test_playlist_returns_songs_in_order _____________________

app = <Flask 'app'>
seed_playlist = {'playlist': <Playlist 9935ecfd-4520-4d44-9cad-4dde0b989177>, 'songs': [<Song 7793ca84-970d-4be0-9c9e-e30855b60af9>, <...-a9f6-d820ce514fee>, <Song 3d576e61-317c-49ac-ac0f-b04f2f219ab5>], 'user': <User ca7378be-29ce-4785-baf5-809470b30261>}

    def test_playlist_returns_songs_in_order(app, seed_playlist):
        """Songs should be returned in position order."""
        with app.app_context():
            playlist_id = seed_playlist["playlist"].id
            songs = get_playlist_songs(playlist_id)
            titles = [s["title"] for s in songs]
>           assert titles == ["Track 1", "Track 2", "Track 3", "Track 4", "Track 5"]
E           AssertionError: assert ['Track 1', '...3', 'Track 4'] == ['Track 1', '...4', 'Track 5']
E             
E             Right contains one more item: 'Track 5'
E             Use -v to get more diff

tests/test_playlists.py:71: AssertionError
______________________ test_streak_increments_on_sunday _______________________

app = <Flask 'app'>, user = <User f2c1fd65-0a24-4bc3-ab86-16b06a6d3bd3>

    def test_streak_increments_on_sunday(app, user):
        """
        Listening on Saturday and then Sunday should increment the streak.
        """
        with app.app_context():
            u = db.session.get(User, user.id)
            saturday = datetime(2024, 6, 15, 12, 0, 0, tzinfo=timezone.utc)  # weekday() == 5
            sunday = datetime(2024, 6, 16, 12, 0, 0, tzinfo=timezone.utc)    # weekday() == 6
    
            update_listening_streak(u, saturday)
            assert u.listening_streak == 1
    
            update_listening_streak(u, sunday)
>           assert u.listening_streak == 2  # Should increment, not reset
            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
E           assert 1 == 2
E            +  where 1 = <User f2c1fd65-0a24-4bc3-ab86-16b06a6d3bd3>.listening_streak

tests/test_streaks.py:96: AssertionError
=========================== short test summary info ===========================
FAILED tests/test_playlists.py::test_playlist_returns_all_songs - AssertionError: assert 4 == 5
FAILED tests/test_playlists.py::test_playlist_returns_songs_in_order - AssertionError: assert ['Track 1', '...3', 'Track 4'] == ['Track 1', '...4...
FAILED tests/test_streaks.py::test_streak_increments_on_sunday - assert 1 == 2
======================== 3 failed, 10 passed in 1.14s =========================
```


## What went wrong
---