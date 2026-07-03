# Nova

---

# Feed

---

## command

```bash
curl http://127.0.0.1:5000/feed/ca95b281-51f9-4fd3-8e9e-aabeb8c327b8/listening-now
```

## Connected problem

Friends Listening Now shows people from yesterday

## Result


```json
{
  "count": 3,
  "feed": [
    {
      "friend": {
        "id": "0f863789-0550-46aa-a7eb-388c0d85b230",
        "last_listened_at": "2026-07-02T19:27:57.110945", // <--- yesterday ⚠️
        "listening_streak": 3,
        "username": "darius"
      },
      "listened_at": "2026-07-03T19:17:57.110945",
      "song": {
        "album": null,
        "artist": "The Wanderers",
        "genre": "indie rock",
        "id": "fc1c5982-0b3e-4662-a900-e6aff09e7716",
        "share_note": null,
        "shared_at": "2026-06-28T19:27:57.110945",
        "shared_by": "ca95b281-51f9-4fd3-8e9e-aabeb8c327b8",
        "tags": [],
        "title": "Midnight Drive"
      }
    },

    {
      "friend": {
        "id": "31942c03-b3ac-45c7-901c-b2b244a0a41d",
        "last_listened_at": null,
        "listening_streak": 0,
        "username": "simone"
      },
      "listened_at": "2026-07-03T19:12:57.110945",
      "song": {
        "album": null,
        "artist": "Elara Moon",
        "genre": "ambient",
        "id": "14b96344-b662-4a72-92ba-2bb35f506262",
        "share_note": null,
        "shared_at": "2026-06-28T19:27:57.110945",
        "shared_by": "ca95b281-51f9-4fd3-8e9e-aabeb8c327b8",
        "tags": [],
        "title": "Still Waters"
      }
    },

    {
      "friend": {
        "id": "ce657938-42c3-42aa-8d3e-dfb75c9a1292",
        "last_listened_at": "2026-07-03T16:27:57.110945", 
        "listening_streak": 12,
        "username": "kenji"
      },
      "listened_at": "2026-07-03T19:07:57.110945",
      "song": {
        "album": null,
        "artist": "Coastal Highway",
        "genre": "indie",
        "id": "9e30a0c3-1087-45c1-8807-59fe8533742b",
        "share_note": null,
        "shared_at": "2026-06-28T19:27:57.110945",
        "shared_by": "ca95b281-51f9-4fd3-8e9e-aabeb8c327b8",
        "tags": [],
        "title": "First Light"
      }
    }
  ]
}
```



SIMONE

```json
{
  "count": 2,
  "feed": [
    {
      "friend": {
        "id": "0f863789-0550-46aa-a7eb-388c0d85b230",
        "last_listened_at": "2026-07-02T19:27:57.110945", // <-- yesterday
        "listening_streak": 3,
        "username": "darius"
      },
      "listened_at": "2026-07-03T19:17:57.110945", // <-- Today?
      "song": {
        "album": null,
        "artist": "The Wanderers",
        "genre": "indie rock",
        "id": "fc1c5982-0b3e-4662-a900-e6aff09e7716",
        "share_note": null,
        "shared_at": "2026-06-28T19:27:57.110945",
        "shared_by": "ca95b281-51f9-4fd3-8e9e-aabeb8c327b8",
        "tags": [],
        "title": "Midnight Drive"
      }
    },
    {
      "friend": {
        "id": "ca95b281-51f9-4fd3-8e9e-aabeb8c327b8",
        "last_listened_at": "2026-07-03T18:27:57.110945",
        "listening_streak": 7,
        "username": "nova"
      },
      "listened_at": "2026-07-03T17:27:57.110945",
      "song": {
        "album": null,
        "artist": "The Wanderers",
        "genre": "indie rock",
        "id": "fc1c5982-0b3e-4662-a900-e6aff09e7716",
        "share_note": null,
        "shared_at": "2026-06-28T19:27:57.110945",
        "shared_by": "ca95b281-51f9-4fd3-8e9e-aabeb8c327b8",
        "tags": [],
        "title": "Midnight Drive"
      }
    }
  ]
}
```

## Raw Hypothesis


### Theory 1

My theory 1 for why the route is grabbing data from the day before because of **hours**. Instead of the system checking days exactly, it's also depending how many hours past.

example:

7/2 at 12 pm to 7/3 at 12 am is only a 12 hour difference (not 24 hours), which the system might not pick up causing the bug. My theory is likely be **False** as the **datetime** package most likely already handles this issue behind the scenes.

### Theory 2

My second theory is that the system didn't remove the instance either from splice logic or runtime. It could be the same issue from before where the system is using a unneeded splice.

---

# Songs

---

## command

```bash
curl http://127.0.0.1:5000/songs/search
```

## Connected problem

The same song keeps showing up twice in search

## Result

query = "still water"

```json
{"count":1,"results":[{"album":null,"artist":"Elara Moon","genre":"ambient","id":"14b96344-b662-4a72-92ba-2bb35f506262","share_note":null,"shared_at":"2026-06-28T19:27:57.110945","shared_by":"ca95b281-51f9-4fd3-8e9e-aabeb8c327b8","tags":[],"title":"Still Waters"}]}
```

query = " Golden Hour"
```json
{"count":1,"results":[{"album":null,"artist":"Elara Moon","genre":"ambient","id":"14b96344-b662-4a72-92ba-2bb35f506262","share_note":null,"shared_at":"2026-06-28T19:27:57.110945","shared_by":"ca95b281-51f9-4fd3-8e9e-aabeb8c327b8","tags":[],"title":"Still Waters"}]}
```

## Raw Hypothesis


### Theory 1

The search is likely just stuck on the previous search? From what I am seeing, the server needs to be shut down then booted up again for the search to be different/accurate. 

* NOTE: This theory is wrong, using the **'random'** python package or adding **q=song%20Title** proved me wrong.

note: %20 is just space like what youll see in an everyday url

```python
import random

if manual_search_for_testing:
  query = random.choice(['still water', 'golden hours'])

search_song(query)
return jsonify(...)
```

```bash
# Test 1: Search for Golden Hour
curl "http://127.0.0.1:5000/songs/search?q=Golden%20Hour"

# Test 2: Search for Still Water
curl "http://127.0.0.1:5000/songs/search?q=still%20water"

# Test 3
curl "http://127.0.0.1:5000/songs/search?q=midnight%20drive"

# Test 4
curl "http://127.0.0.1:5000/songs/search?q=first%20light"
```
### Theory 2

If the tag is also inside the song, it appends it to the list for another time? From what I am seeing, everything seems right. The song is only showing once. I am not sure if I already fixed it without realizing it.

## NOTE

With assistance of **AI (Gemini)**, it helped pointing me to the error and surprisingly my **2nd** theory was in fact True. My issue was that I was manually bashing songs with 0-1 tags, so I just couldn't point exactly where the problem was located. 

A better debugging apporch I shouldve taken was: 

1. loop  all song titles into the search_song() (or atleast the first 10-30 to avoid tedious measures or overfilled terminal)
2. add a condition statment where if the same song appears > 1 times, append the song title to another list (repeated_songs) catching repeated songs.

---

## command

```bash
curl -X POST "http://127.0.0.1:5000/songs/fd75296f-41a2-4ee9-9c2e-2f6175b70663/rate" \
     -H "Content-Type: application/json" \
     -d '{"user_id": "99156296-5da0-4513-bcb1-f42cd157e130", "score": 3}'
```


## result