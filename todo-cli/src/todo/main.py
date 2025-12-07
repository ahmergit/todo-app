"""Main application entry point"""
from todo.manager import TaskManager
from todo.ui import (
    display_menu,
    get_menu_choice,
    handle_add_task,
    handle_view_tasks,
    handle_update_task,
    handle_delete_task,
    handle_complete_task,
    handle_set_priority,
)


def main():
    """Main application loop"""
    manager = TaskManager()

    print("\nWelcome to Todo List Application!")

    while True:
        try:
            display_menu()
            choice = get_menu_choice()

            if choice == '0':
                print("\nGoodbye! Thanks for using Todo List Application.\n")
                raise SystemExit(0)
            elif choice == '1':
                handle_add_task(manager)
            elif choice == '2':
                handle_view_tasks(manager)
            elif choice == '3':
                handle_update_task(manager)
            elif choice == '4':
                handle_delete_task(manager)
            elif choice == '5':
                handle_complete_task(manager)
            elif choice == '6':
                handle_set_priority(manager)

        except KeyboardInterrupt:
            print("\n\nGoodbye! (Interrupted)\n")
            raise SystemExit(0)
        except Exception as e:
            print(f"\nError: {e}")
            print("Returning to main menu...\n")


if __name__ == "__main__":
    main()
