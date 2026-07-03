

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
| 4 | I got notified when a friend added my song to a playlist but not when they rated it | `notification_service.py` | ❌ |
| 5 | The last song in a playlist never shows up | `playlist_service.py` | ✅ |


## Bug 1

### Problem 

5. The last song in a playlist never shows up

### Issue

code:

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
---

## Bug 4






--- 

## IDS

### users

- nova: ca95b281-51f9-4fd3-8e9e-aabeb8c327b8
- darius: 0f863789-0550-46aa-a7eb-388c0d85b230
- simone: 31942c03-b3ac-45c7-901c-b2b244a0a41d
- kenji: ce657938-42c3-42aa-8d3e-dfb75c9a1292
- aaliya id: 676316d3-c641-4477-871d-34b89c9c2ac3

### songs

- Midnight Drive: fc1c5982-0b3e-4662-a900-e6aff09e7716
- Still Waters: 14b96344-b662-4a72-92ba-2bb35f506262
- First Light: 9e30a0c3-1087-45c1-8807-59fe8533742b
- Block Party: f93aac42-9c1a-4d51-940c-b6f3cb7cc879
- Late Night Session: 541e0949-49ed-4d23-9e6c-c14fed3e9209
- Golden Hour: 1ba18a56-dc05-4006-8f0e-b3d36131cf04
- Free Throws: 5fe375fe-8386-4b28-8410-0861e0b213c3
- Soft Landing: 6eccfb65-24e9-464d-8b11-679f05b25659
- Crown Heights Anthem: c7462e46-dc5f-419e-b2ad-70abdbb30263
- Harlem Renaissance: 82257f9f-01d3-434e-8dbc-00e4203aa641
- After Hours: 724ca4ae-3aa0-4914-9166-2fb252e6c922
- Lagos to London: a769e642-ac2f-4cae-a806-da63316a8bf9
- Frequencies: b338fc30-7870-47e8-abb8-5cf0b0ed1952

### playlists

- Late Night Vibes id: 363fc487-fb42-4286-a7ea-ded8095836fa
- Friday Energy id: 1aa1583e-d58b-40d2-bd51-6371fc6dd89b
- Study Mode id: 031f6cd6-135c-4246-b03d-ac8426bb1589

---

# curl commands

**Nova** is our best buddy for this process

ID: ca95b281-51f9-4fd3-8e9e-aabeb8c327b8

**Aaliya** is our second in command

ID: 676316d3-c641-4477-871d-34b89c9c2ac3

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
curl http://127.0.0.1:5000/users/ca95b281-51f9-4fd3-8e9e-aabeb8c327b8/streak/notifications

# Mark a noti as "read" when the user clicks on it
curl http://127.0.0.1:5000/users/notifications/<notification_id>/read
```