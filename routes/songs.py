"""routes/songs.py — Mixtape song routes"""

from flask import Blueprint, request, jsonify
from services.search_service import search_songs, get_song
from services.notification_service import rate_song
from services.streak_service import record_listening_event
import random
songs_bp = Blueprint("songs", __name__)


@songs_bp.route("/search")
def search(manual_search=False):
    query = request.args.get("q", "")
    
    if not manual_search and not query:
        return jsonify({"error": f"Query parameter 'q' is required"}), 400
    
    if manual_search:
        query = random.choice([" Golden Hour", "still water"])

    print(f"SONG BEING SEARCHED FOR BEFORE HITTING search_songs: {query}\n")
    results = search_songs(query.lower().strip())
    return jsonify({"results": results, "count": len(results)})


@songs_bp.route("/<song_id>")
def get_song_detail(song_id):
    try:
        song = get_song(song_id)
        return jsonify(song)
    except ValueError as e:
        return jsonify({"error": str(e)}), 404


@songs_bp.route("/<song_id>/rate", methods=["POST"])
def rate(song_id):
    data = request.get_json()
    user_id = data.get("user_id")
    score = data.get("score")
    if not user_id or score is None:
        return jsonify({"error": "user_id and score are required"}), 400
    try:
        rating = rate_song(user_id, song_id, int(score))
        return jsonify(rating.to_dict()), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 400


@songs_bp.route("/<song_id>/listen", methods=["POST"])
def listen(song_id):
    data = request.get_json()
    user_id = data.get("user_id")
    if not user_id:
        return jsonify({"error": "user_id is required"}), 400
    try:
        event = record_listening_event(user_id, song_id)
        return jsonify(event.to_dict()), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
