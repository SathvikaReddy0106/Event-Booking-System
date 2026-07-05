import threading
import requests

URL = "http://127.0.0.1:8000/api/seat/hold/"


requests_data = [
    {
        "user_id": 1,
        "showtime_id": 1,
        "seat_id": 1,
    },
    {
        "user_id": 2,
        "showtime_id": 1,
        "seat_id": 2,
    },
    {
        "user_id": 3,
        "showtime_id": 1,
        "seat_id": 3,
    },
]


def book_seat(data):

    try:

        response = requests.post(
            URL,
            json=data,
        )

        print(
            f"Seat {data['seat_id']} -> "
            f"{response.status_code} -> "
            f"{response.json()}"
        )

    except Exception as e:

        print(e)


threads = []

for data in requests_data:

    thread = threading.Thread(
        target=book_seat,
        args=(data,),
    )

    threads.append(thread)
    thread.start()

for thread in threads:
    thread.join()

print("\nAll requests completed.")