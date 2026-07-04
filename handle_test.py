import logging
from services.search_service import search_songs
import subprocess

"""Taking consideration from the previous debugging process (Bug 3)"""

"http://127.0.0.1:5000/songs/fd75296f-41a2-4ee9-9c2e-2f6175b70663" # get song data for creator/sharer

def handle_run_command(route:str, subroute=None, command=None, id=None, method=None):
    home = "http://127.0.0.1:5000/"
    more_routes = {
        "feed": {"listen": "/listening-now"},
        "users": {"notifications": "/notifications", "read": "/read"},
        "songs": {"rate": "/rate", "listen": "/listen"},
        "notifications": {"read": "/read"}
    }
    if not route or route not in more_routes.keys():
        raise ValueError(f"{route if route else 'An empty route'} is not a valid route")
    
    if subroute:
        if not more_routes[route].get(subroute, False):
            raise ValueError(f"'{route}' has no subroute '{subroute}', double check spelling")
    
    
    
    if command and isinstance(command, str):
        built_command = command
    else:
        built_command = f"{home}{route}{f'/{id}' if id else ''}{more_routes[route][subroute] if subroute else ''}".strip()
    if method:
        if method.lower().strip() not in ['post', 'get', 'delete', 'patch']:
            raise ValueError(f"{method.lower()} is not a valid method")
        
    curl = ["curl"]
    if method:
        curl.extend(["-X", method.upper()])
    curl.append(built_command)
    subprocess.run(curl)





test_listening_curls = [
    # Nova
    "http://127.0.0.1:5000/feed/ca95b281-51f9-4fd3-8e9e-aabeb8c327b8/listening-now",
    
    # Darius
    "http://127.0.0.1:5000/feed/0f863789-0550-46aa-a7eb-388c0d85b230/listening-now",
    
    #simone
    "http://127.0.0.1:5000/feed/31942c03-b3ac-45c7-901c-b2b244a0a41d/listening-now",
    
    # kenji
    "http://127.0.0.1:5000/feed/ce657938-42c3-42aa-8d3e-dfb75c9a1292/listening-now",
]


test_noti_curls = [
    # Nova
    "http://127.0.0.1:5000/users/ca95b281-51f9-4fd3-8e9e-aabeb8c327b8/notifications",
    
    # Darius
    "http://127.0.0.1:5000/users/0f863789-0550-46aa-a7eb-388c0d85b230/notifications",
    
    #simone
    "http://127.0.0.1:5000/users/cb7a12ec-9c68-4862-84de-f86d7a592cd6/notifications",
    
    # kenji
    "http://127.0.0.1:5000/users/ce657938-42c3-42aa-8d3e-dfb75c9a1292/notifications",
    
    "http://127.0.0.1:5000/users/676316d3-c641-4477-871d-34b89c9c2ac3/notifications"
]
        
if __name__ == "__main__":
    Id = "          99156296-5da0-4513-bcb1-f42cd157e130         ".strip()
    route = "        feed        ".strip()
    subroute = "        listen        ".strip()
    method = "             ".strip()
   
    handle_run_command(route=route, id=Id, subroute=subroute, method=method)
    
    
    
    rate_song = """
    
    
    curl -X POST "http://127.0.0.1:5000/songs/fd75296f-41a2-4ee9-9c2e-2f6175b70663/rate" \
     -H "Content-Type: application/json" \
     -d '{"user_id": "99156296-5da0-4513-bcb1-f42cd157e130", "score": 3}'
    
    """ # manual