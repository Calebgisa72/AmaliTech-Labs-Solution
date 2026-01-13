import services.storage as storage
import controllers


def main():
    storage.load_all()
    print("---WELCOME TO LIBRARY INVENTORY---")

    while True:
        print("\n1. Add Book")
        print("2. Add Author")
        print("3. Loan a Book")
        print("4. Return a Book")
        print("5. Search Books")
        print("6. List All Books")
        print("7. List All Authors")
        print("8. List All Loans")
        print("9. Delete Book")
        print("10. Edit Book")
        print("11. Exit")
        print("================")

        choice = input("Enter choice: ")

        if choice == "1":
            controllers.add_book()
        elif choice == "2":
            controllers.add_author()
        elif choice == "3":
            controllers.loan_book()
        elif choice == "4":
            controllers.return_book()
        elif choice == "5":
            controllers.search_books()
        elif choice == "6":
            controllers.list_all_books(withDetails=True)
        elif choice == "7":
            controllers.list_all_authors()
        elif choice == "8":
            controllers.list_all_loans()
        elif choice == "9":
            controllers.delete_book()
        elif choice == "10":
            controllers.edit_book()
        elif choice == "11":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Try again.")


if __name__ == "__main__":
    main()
