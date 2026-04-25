import db
import source_a
import source_b

USER_CHOICE = """
Choose an option:
- 'a' : Source A - get basic metadata and next volumes dates
- 'm' : Source B - get ratings, popularity and rank
- 'b' : Fetches from both services, then quits
- 'q' : QUIT

Choice: """


def menu():
    db.init_db()
    user_input = input(USER_CHOICE)
    while user_input != 'q':
        if user_input == 'a':
            source_a.fetch_and_store()
        elif user_input == 'm':
            source_b.fetch_and_store()
        elif user_input == 'b':
            print("You chose BOTH")
            source_a.fetch_and_store()
            source_b.fetch_and_store()
            quit()
        user_input = input(USER_CHOICE)


menu()
