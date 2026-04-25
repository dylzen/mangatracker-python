import ac_data
import db
import mal_data

USER_CHOICE = """
Choose an option:
- 'a' : AC - get basic metadata and next volumes dates
- 'm' : MAL - get ratings, popularity and rank
- 'b' : Fetches from both services, then quits
- 'q' : QUIT

Choice: """


def menu():
    db.init_db()
    user_input = input(USER_CHOICE)
    while user_input != 'q':
        if user_input == 'a':
            ac_data.fetch_and_store()
        elif user_input == 'm':
            mal_data.fetch_and_store()
        elif user_input == 'b':
            print("You chose BOTH")
            ac_data.fetch_and_store()
            mal_data.fetch_and_store()
            quit()
        user_input = input(USER_CHOICE)


menu()
