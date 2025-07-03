import threading
import time

# Dummy user database
USER_DB = {
    "admin": "password123",
    "user1": "passw0rdgghgh"
}

# Shared resource
shared_counter = 0
lock = threading.Lock()

# Authentication check
def authenticate(username, password):
    return USER_DB.get(username) == password

# Critical section
def secure_increment(username, password):
    global shared_counter
    if not authenticate(username, password):
        print(f"[ACCESS DENIED] {username}")
        return

    # Lock the critical section
    with lock:
        local_copy = shared_counter
        print(f"[{username}] Read counter: {local_copy}")
        time.sleep(0.1)  # Simulate delay
        shared_counter = local_copy + 1
        print(f"[{username}] Incremented counter to: {shared_counter}")

# Test with multiple threads
def test_sync_security():
    users = [
        ("admin", "password123"),
        ("user1", "wrongpass"),
        ("user1", "passw0rd"),
        ("hacker", "letmein"),
    ]

    threads = []
    for username, password in users:
        thread = threading.Thread(target=secure_increment, args=(username, password))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    print(f"\nFinal counter value: {shared_counter}")

if __name__ == "__main__":
    test_sync_security()
