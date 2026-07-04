

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

# Bug fixes In The Order I fixed them

---

## The Five Open Issues

* ❌ - not fixed
* ⚠️ - fix in progress
* ✅ - fixed

| # | Title | Affected service | Status
|---|-------|------------------|-------- 
| 1 | My listening streak keeps resetting | `streak_service.py` | ✅ |
| 2 | Friends Listening Now shows people from yesterday | `feed_service.py` | ⚠️ |
| 3 | The same song keeps showing up twice in search | `search_service.py` | ✅ |
| 4 | I got notified when a friend added my song to a playlist but not when they rated it | `notification_service.py` | ✅ |
| 5 | The last song in a playlist never shows up | `playlist_service.py` | ✅ |


## Bug 1

### Problem 

5. The last song in a playlist never shows up

### Issue

```python
assert len(songs) == 5
```

### Reason

The function called to list the song, **get_playlist_songs()**, had an unneeded splice inside the returning comprehension. songs[:-1] was basically telling the system;

```python
[song_1, song_2, song_3, song_4, song_5].remove(1 songs starting from the end of the list)
```

### Solution: 

Simply remove the splice in the returning iteration.

---

## Bug 2

### Problem 

1. My listening streak keeps resetting

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

## Bug 3

### Problem

3. The same song keeps showing up twice in search

### Issue

```python
query = "sunflower"
 results = (
        db.session.query(Song)
        .outerjoin(song_tags, Song.id == song_tags.c.song_id) # error is here, songs with many tags dup
        # appends tags: tag = sunshine; song_title = sunflower
        # also appends tags: tag = spiderverse; song_title = sunflower
        # now the song "sunflower" appears twice inside the list
        .filter(
            db.or_(
                Song.title.ilike(f"%{query}%"),
                Song.artist.ilike(f"%{query}%"),
            )
        )
        .all()
    )
```

### Reason

After a bit of trying to find the issue, what is happening is that when a song has plenty of tags, the systems creates the song instance more than once for tags. So when the user queries a song title, if that song instance has more than 1 tag, itll append to the results list.


### Solution

* Easily just use the set() function or using {} (curly brackets) instead of [] (square brackets)

or

1. add a loop inside a list of dictionaries of the songs
2. append the found titles into a list named 

```python
seen_song_titles = [] | seen_song_ids = []
```
3. condition where if the current song (id or title, id is better as songs can have same titles) is already inside the seen list, continue

### NOTE

more information during the process solving this bug in the **curl_results_and_breakdown.md** file in the root folder.

---

## Bug 4

### Problem

4. I got notified when a friend added my song to a playlist but not when they rated it

### Issue

```human mistake
Lets not use the create_notification() function inside the file
```

### Solution

Simply use the create_notification() we made inside the file

```python
score = 5
noti = create_notification(
        user_id=user_id,
        notification_type="song_rated",
        body=f"{rater.username} rated your song '{song.title}' a {score}"
    )
print(noti.to_dict())
```

result:
```json - terminal

{
    "count":1,
    "notifications":[

        {
            "body":"nova rated your song 'Crown Heights Anthem' a 3",
            "created_at":"2026-07-04T15:57:01.882286",
            "id":"0fad7bc9-6d22-450a-b7b4-dee1a7813a01",
            "read":false,
            "type":"song_rated",
            "user_id":"cb7a12ec-9c68-4862-84de-f86d7a592cd6"
        }
    ]
}
```
--- 

## Bug 5


### Problem

2. Friends Listening Now shows people from yesterday

### Issue


---
## IDS

### Users

['nova id: 99156296-5da0-4513-bcb1-f42cd157e130', 'darius id: 48e2f298-088d-421e-a601-fcb6a1678af8', 'simone id: cb7a12ec-9c68-4862-84de-f86d7a592cd6', 'kenji id: 2874e214-9d52-429f-b106-47af11017846', 'aaliya id: 316ba8e8-e2d8-4875-b4a6-1c8bceede8ee']

### Songs

['Midnight Drive id: 6dbc2b82-a9bf-4034-bad0-1de85e988578', 'Still Waters id: dec613fa-5ad0-4524-8a7a-858875b42272', 'First Light id: da7f5bf5-f56e-4ed0-af63-9b3f68d565bb', 'Block Party id: 5a7d682a-29b0-40ed-a6f2-6b14ba831a4a', 'Late Night Session id: 90208249-0870-44c6-86f0-7cbe3393f973', 'Golden Hour id: aca77448-fd1e-467f-9b7d-360dfbfdb36f', 'Free Throws id: c4949ee3-51de-4c19-9e7c-0e1dd614719b', 'Soft Landing id: 63721b4a-8c7f-46fa-aba9-e7063a687a0c', 'Crown Heights Anthem id: fd75296f-41a2-4ee9-9c2e-2f6175b70663', 'Harlem Renaissance id: 579d4a06-7e82-492d-b6b5-be5c97dbc817', 'After Hours id: 0c1ea4a6-d9fe-4e66-b8e9-da238e40267c', 'Lagos to London id: 576968ed-2615-4a7a-9367-323c824990c6', 'Frequencies id: e661913b-59f5-4c29-8298-8e749c64f99b']

### Playlists

['Late Night Vibes id: 9544ff59-f976-4436-9d4a-0e402f57d72b', 'Friday Energy id: cd5386f4-4dae-42ed-95d0-dc8181ae61a3', 'Study Mode id: a04852a9-e75d-438c-b9d6-8675b1bc5d82']

### Notifications
71daf9bd-b941-4d8d-9064-04f1db633b5c
---

# curl commands

**Nova** is our best buddy for this process

## feed

```bash
# friends listening now
curl http://127.0.0.1:5000/feed/ca95b281-51f9-4fd3-8e9e-aabeb8c327b8/listening-now

# listening activty of friends
curl http://127.0.0.1:5000/feed/ca95b281-51f9-4fd3-8e9e-aabeb8c327b8/activity
```

## playlists

```bash
# create a playlist
curl http://127.0.0.1:5000/playlists/

# get the details from a playlist
curl http://127.0.0.1:5000/playlists/7389214a-f7b3-44a7-88c4-a915c44e1301

# get songs inside the playlist
curl http://127.0.0.1:5000/playlists/7389214a-f7b3-44a7-88c4-a915c44e1301/songs
```


## songs

```bash
# search for a song by title
curl http://127.0.0.1:5000/songs/search

# get the details from a song
curl http://127.0.0.1:5000/songs/fc1c5982-0b3e-4662-a900-e6aff09e7716

# rate a song with a score between 1-5 (lowest-highest)
curl http://127.0.0.1:5000/songs/fc1c5982-0b3e-4662-a900-e6aff09e7716/rate

# Mark a song to "listen" when the user starts to listen
curl http://127.0.0.1:5000/songs/fc1c5982-0b3e-4662-a900-e6aff09e7716/listen
```


## users

```bash
# get data for a data
curl http://127.0.0.1:5000/users/ca95b281-51f9-4fd3-8e9e-aabeb8c327b8

# get the user's streak
curl http://127.0.0.1:5000/users/ca95b281-51f9-4fd3-8e9e-aabeb8c327b8/streak

# get the notis the user haven't read yet
curl http://127.0.0.1:5000/users/ca95b281-51f9-4fd3-8e9e-aabeb8c327b8/notifications

# Mark a noti as "read" when the user clicks on it
curl http://127.0.0.1:5000/users/notifications/b84def72-9505-4faf-a404-c40c3c67d84f/read
```