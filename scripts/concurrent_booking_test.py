import concurrent.futures
import requests

URL = "http://127.0.0.1:8000/api/hold/"

payload = {
    "user_id": 1,
    "showtime_id": 1,
    "seat_id": 1
}


def book_seat(i):
    try:
        response = requests.post(URL, json=payload)

        return {
            "Thread": i,
            "Status Code": response.status_code,
            "Response": response.json()
        }

    except Exception as e:
        return {
            "Thread": i,
            "Error": str(e)
        }


with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:

    futures = [
        executor.submit(book_seat, i)
        for i in range(1, 11)
    ]

    for future in concurrent.futures.as_completed(futures):
        print(future.result())