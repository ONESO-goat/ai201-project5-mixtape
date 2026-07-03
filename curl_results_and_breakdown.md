# Nova

---

# Feed

---

## command

```bash
curl http://127.0.0.1:5000/feed/ca95b281-51f9-4fd3-8e9e-aabeb8c327b8/listening-now
```

## Connected problem

N/A

## Result

```json
{
  "count": 3,
  "feed": [
    {
      "friend": {
        "id": "0f863789-0550-46aa-a7eb-388c0d85b230",
        "last_listened_at": "2026-07-02T19:27:57.110945",
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