

# Mixtape

---

# overview

This project, unlike the previous weeks we are **reading** and **editing** an existing codebase for a social web application where users share and rate music. For each error along the way, it's expected that **me**, the editor, point out; bugs, what they caused, and implement the possible solution.

---


# Codebase Map

**models.py** defines 5 SQLAlchemy models: 

- User
- Song
- Playlist
- PlaylistSong
- Notification

The PlaylistSong table is a join table that adds an order column — songs in a playlist have an explicit position, not just insertion order.

## Data flow

**user** rates a song: 

```terminal
POST /songs/<id>/rate
```

routes/songs.py calls 

```python
notification_service.notify_song_rated()
```

The function creates a **Notification record** for the song's original sharer. There's no separate rating model — the rating is stored directly on the Song.

### Pattern I noticed: 

every route delegates **immediately** to a service function. The routes do input parsing and response formatting; **all business logic lives in services/**.

---

## user ids

nova: 4e159e53-17a9-4729-bd52-e06117f054a4
darius 3a6a90ac-13c3-45e0-a734-eae344ef7934
simone: 3dedfae0-3d01-481e-904e-cea097e0f94e
kenji: 34e1c007-bf55-4bef-8e73-adddb6742c4b
aaliya: 1b51e8ff-8755-4bc9-a875-390bd3b023ea

---


# Pytest fixes

## Bug 1

### Issue

```python
assert len(songs) == 5
```

### Reason

The function called to list the song, get_playlist_songs(), had an unneeded splice inside the returning comprehension. songs[:-1] was basically telling the system;

```python
[song_1, song_2, song_3, song_4, song_5].remove(1 songs starting from the end of the list)
```

Solution: Simply remove the splice in the returning iteration.
---

## Bug 2

### Issue

```python
update_listening_streak(u, sunday)
```

### Reason

The error was due to this conditional: 

```python
# else if 1 day has passed from the previous streal and today's weekday is sunday
elif days_since_last == 1 and today.weekday() != 6:
    ...
```

since sunday was the 6th number in the datetime.weekday() function, the condictional was set to **False**.

### Solution

**Remove** the "and today.weekday() != 6" check as it was just straight up useless as the built in python package **datetime** already handles majority of tedious date logic.

example:

- weather it's **monday -> sunday** which means 6 days has passed in terms of the weekday

- weather it's **sunday -> monday** which means 1 day has passed in terms of the weekday

---