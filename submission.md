
---

# Mixtape - submissions.md

---

# Overview

Unlike previous weeks, this assignment wasn't about writing an application from scratch. Instead, the goal was to read an already existing Flask codebase, understand how different files communicate with each other, locate bugs, explain their root causes, and implement fixes.

Rather than immediately changing code, I first tried to understand how requests flowed through the application. Whenever I fixed a bug, I documented:

* how I reproduced it
* how I navigated through the codebase
* the exact root cause
* why the fix works
* what I tested afterwards to make sure nothing else broke

---

# Codebase Map

The application is organized around Flask routes, SQLAlchemy models, and service files.

## Main Files

### models.py

Defines all database models used throughout the application.

Models include:

* User
* Song
* Playlist
* PlaylistSong
* Notification

---

### routes/

The route files receive HTTP requests.

Examples:

```
POST /songs/<id>/rate
GET /search
GET /playlist/<id>
```

Routes mainly validate input before delegating almost everything to a service function.

---

### services/

Most of the application's business logic lives here.

Some important services were:

* notification_service.py
* playlist_service.py
* search_service.py
* streak_service.py
* feed_service.py

Instead of placing application logic inside Flask routes, the routes call service functions that perform database queries and create or update objects.

---

## Data Flow Example

One feature I followed was rating a song.

```
User submits rating

↓

POST /songs/<id>/rate

↓

routes/songs.py

↓

notification_service.notify_song_rated()

↓

create_notification()

↓

Notification saved to database

↓

Notification appears in user's notification feed
```

This helped me understand that the route itself wasn't responsible for creating notifications. It only forwarded the request to the service layer.

---

## Architecture Pattern I Noticed

Almost every route immediately delegates work to a service function.

Routes mainly:

* receive requests
* validate input
* return JSON responses

while the service files contain nearly all of the business logic.

Once I noticed this pattern it became much easier to navigate the codebase because every route eventually pointed toward the file that actually contained the bug.

---

# The Five Open Issues
* ❌ - not fixed
* ⚠️ - fix in progress
* ✅ - fixed

| # | Title | Affected service | Status
|---|-------|------------------|-------- 
| 1 | My listening streak keeps resetting | `streak_service.py` | ✅ |
| 2 | Friends Listening Now shows people from yesterday | `feed_service.py` | ✅ |
| 3 | The same song keeps showing up twice in search | `search_service.py` | ✅ |
| 4 | I got notified when a friend added my song to a playlist but not when they rated it | `notification_service.py` | ✅ |
| 5 | The last song in a playlist never shows up | `playlist_service.py` | ✅ |


---

# Bug 1 — Playlist Missing Last Song

## Reproduction

Open a playlist containing five songs.

Only four songs appear even though the playlist contains five entries.

---

## Navigation Strategy

I first looked inside the playlist routes before following the function call into `playlist_service.py`.

Since the bug only affected displaying playlist contents, I focused on the function responsible for returning playlist songs.

Once I found `get_playlist_songs()`, I noticed the returned list was being sliced.

That immediately matched the symptom.

---

## Root Cause

The function returned:

```python
songs[:-1]
```

The slice removes the final element from every list.

So a playlist like

```
1
2
3
4
5
```

became

```
1
2
3
4
```

regardless of playlist size.

---

## Fix

Removed the unnecessary slice so every song is returned.

---

## Side-Effect Check

I reopened playlists containing different numbers of songs.

Playlists with one song, several songs, and five songs all displayed correctly, confirming the fix didn't duplicate or reorder songs.

---

# Bug 2 — Listening Streak Resetting

## Reproduction

Use the application across a Saturday → Sunday transition.

Instead of increasing the streak, it resets.

---

## Navigation Strategy

I searched for where listening streaks were updated.

The route eventually called

```python
update_listening_streak()
```

inside `streak_service.py`.

I stepped through each conditional until I reached the Sunday check.

---

## Root Cause

The function contained:

```python
elif days_since_last == 1 and today.weekday() != 6
```

Python's `weekday()` uses

```
Monday = 0

Sunday = 6
```

So even when only one day had passed, Sundays failed the condition.

That caused the streak update to skip.

---

## Fix

Removed

```python
today.weekday() != 6
```

because `days_since_last` already verifies whether exactly one day passed.

The extra weekday comparison was unnecessary.

---

## Side-Effect Check

I tested weekday transitions including

* Saturday → Sunday
* Sunday → Monday

The streak increased correctly for every consecutive day.

---

# Bug 3 — Duplicate Search Results

## Reproduction

Search for a song that contains multiple tags.

The same song appears more than once in search results.

---

## Navigation Strategy

I started inside the search route before following the database query into `search_service.py`.

The SQL query performs an outer join against the tag table.

Once I realized each matching tag produced another database row, I became confident the duplication wasn't happening after the query—it was happening during the query itself.

---

## Root Cause

The query joins songs with tags.

If one song has multiple matching tags, SQL returns multiple rows for the same song.

Example:

```
Sunflower
tag: sunshine

Sunflower
tag: spiderverse
```

Both rows represent the same song, but SQLAlchemy returns both objects.

The duplication only occurs for songs with multiple tags.

---

## Fix

Remove duplicate songs before returning results by using a **{curly brace}** set (tracking seen song IDs).

If using a tracker, IDs is safer because multiple songs can share the same title.

---

## Side-Effect Check

I searched for:

* songs with one tag
* songs with many tags
* songs with no tags

Results still returned correctly while duplicates disappeared.

---

# Bug 4 — Missing Rating Notifications

## Reproduction

Rate another user's song.

The song owner never receives a rating notification.

---

## Navigation Strategy

Since playlist notifications worked correctly, I compared both notification paths.

Eventually I noticed playlist additions used `create_notification()`, while song ratings didn't use it at all.

That inconsistency led me to the bug.

---

## Root Cause

The existing helper function

```python
create_notification()
```

wasn't being used.

Instead, notification creation was bypassed.

Because the helper centralizes notification creation, skipping it prevented rating notifications from being generated correctly.

---

## Fix

Use

```python
create_notification()
```

when a song receives a rating.

After doing so, rating notifications appeared correctly.

---

## Side-Effect Check

I verified playlist notifications still worked normally and confirmed both notification types appeared in the notification feed.

---

# Bug 5 — Friends Listening Now

## Reproduction

Leave the application overnight.

The next day, "Friends Listening Now" still displays users who last listened yesterday.

---

## Navigation Strategy

The bug description suggested a time comparison.

I searched for constants related to timestamps and eventually found

```python
RECENT_THRESHOLD
```

inside `feed_service.py`.

Seeing it set to 24 hours explained why yesterday's activity still qualified.

---

## Root Cause

The application considered anything within the last 24 hours as "listening now."

Technically that includes yesterday.

The bug wasn't the comparison itself—it was that the threshold was too large for the feature's intended behavior.

---

## Fix

Reduced

```python
RECENT_THRESHOLD
```

from

```python
24 hours
```

to

```python
1 hour
```

This makes "Listening Now" much closer to real time activity while still allowing some flexibility.

---

## Side-Effect Check

I confirmed recent listeners still appeared immediately after listening while users from yesterday no longer appeared.

---

# AI Usage

1. I used **Gemini** for the debugging process when stuck.

One example was asking how SQLAlchemy `outerjoin()` works. That explanation helped me understand why songs with multiple tags could appear multiple times. Afterward, I verified the explanation by reading the query myself and confirming that duplicate rows were being returned before the results reached Python.

Another example was asking if my theory for the `listening now shows friends from yesterday` problem was leading to the right direction or there was more to it that I was missing inside the function.

2. I used **ChatGPT** for structuring and polishing the submissions.md.

It aided me by:
* pointing to what requirements in the rubric were missing or should be improved
* pointing weak or poor writing, then giving me stronger revised versions
* tell me what sections were not needed for the file

I used ChatGPT after writing my submission to compare it against the rubric. It pointed out that I was missing navigation strategies, side-effect checks, and reproduction steps. I rewrote those sections myself while keeping my original debugging notes.



---

# Commit History

Each bug (first two were pushed into 1 commit by accident, but I did provide detail of my changes in the commit message) was committed separately on my `bugfix/mixtape` branch using conventional commit messages.

Example commit messages:

```
fix: playlist missing last song

fix: listening streak resets on sunday

fix: duplicate search results

fix: song rating notifications

fix: listening now threshold
```


each with detailed commit messages.

A screenshot of the commit history is included with my submission.


```
**note**:
* playlist missing last song

and

* listening streak resets on sunday

were the bugs I accidentally pushed into one commit.
```


---

# Regression Test

I added a regression test for the playlist bug.

The test creates a playlist with multiple songs and verifies that every song is returned.

Before the fix, the test failed because the final song was always omitted due to the list slice.

After removing the slice, the test passes and would catch the bug if it were accidentally reintroduced.

---

# Conclusion

I haven't had experience debugging code bases, and I believe that’s an important factor to programming so this project was a great entry point. All bugs in this project were simple to fix, but required depth analysis on the application structure, and tracing through multiple files. This process was important as some service logic causing the related issues at times don't expose the said problem, example with the 3rd problem **song appearing twice in search**.
