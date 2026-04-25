import ac_data
import mal_data


USER_CHOICE = """
Choose an option:
- 'a' : AC - get basic metadata and next volumes dates
- 'm' : MAL - get ratings, popularity and rank
- 'b' : Fetches from both services, then quits
- 'q' : QUIT

Choice: """

def menu():
    user_input = input(USER_CHOICE)
    while user_input != 'q':
        if user_input == 'a':
            ac_data.ac_write_to_xlsx(user_input)

        elif user_input == 'm':
            mal_data.mal_write_to_xlsx(user_input)
        elif user_input == 'b':
            print("You chose BOTH")
            user_input = 'a'
            ac_data.ac_write_to_xlsx(user_input)
            user_input = 'm'
            mal_data.mal_write_to_xlsx(user_input)
            quit()
        user_input = input(USER_CHOICE)

menu()