# Author: Kay Patel


class LibraryItem:
    """Base class that represents all library items."""

    def __init__(self, library_item_id, title):
        """Creates a library item object and initializes its attributes."""
        self._library_item_id = library_item_id
        self._title = title
        self._location = "ON_SHELF"
        self._checked_out_by = None
        self._requested_by = None
        self._date_checked_out = 0

    def get_library_item_id(self):
        """Returns the unique identifier for the library item."""
        return self._library_item_id

    def get_location(self):
        """Returns the location of the library item.."""
        return self._location

    def set_location(self, location):
        """Sets the library item's location."""
        self._location = location

    def get_checked_out_by(self):
        """Returns the name of the patron who the item is checked out to."""
        return self._checked_out_by

    def set_checked_out_by(self, patron_name):
        """Sets checked out by to the name of the patron who is checking out the library item."""
        self._checked_out_by = patron_name

    def get_requested_by(self):
        """Returns the name of the patron who requested the library item."""
        return self._requested_by

    def set_requested_by(self, value):
        """Sets the requested by to the name of the patron requesting the library item."""
        self._requested_by = value

    def get_date_checked_out(self):
        """Returns the library item's checked out date."""
        return self._date_checked_out

    def set_date_checked_out(self, date):
        """Sets the checked out date for the library item."""
        self._date_checked_out = date


class Book(LibraryItem):
    """Subclass that represents a book as a library item."""

    def __init__(self, library_item_id, title, author):
        """Creates a book object and initializes its attributes."""
        super().__init__(library_item_id, title)
        self._author = author

    def get_author(self):
        """Returns the author of the book."""
        return self._author

    def get_check_out_length(self):
        """Returns the book's check out length"""
        return 21


class Album(LibraryItem):
    """Subclass that represents an album as a library item."""

    def __init__(self, library_item_id, title, artist):
        """Creates an album object and initializes its attributes."""
        super().__init__(library_item_id, title)
        self._artist = artist

    def get_artist(self):
        """Returns the artist of the album."""
        return self._artist

    def get_check_out_length(self):
        """Returns the album's check out length."""
        return 14


class Movie(LibraryItem):
    """Subclass that represents a movie as a library item."""

    def __init__(self, library_item_id, title, director):
        """Creates a movie object and initializes its attributes"""
        super().__init__(library_item_id, title)
        self._director = director

    def get_director(self):
        """Returns the director of the movie."""
        return self._director

    def get_check_out_length(self):
        """Returns the movie's check out length."""
        return 7


class Patron:
    """Base class that represents all patrons."""

    def __init__(self, patron_id, name):
        """Creates a patron object and initializes its attributes."""
        self._patron_id = patron_id
        self._name = name
        self._checked_out_items = []
        self._fine_amount = 0

    def get_patron_id(self):
        """Returns the unique identifier for the patron."""
        return self._patron_id

    def get_patron_name(self):
        """Returns the patron's name."""
        return self._name

    def get_checked_out_items(self):
        """Returns a list of library items that are checked out by the patron."""
        return self._checked_out_items

    def get_fine_amount(self):
        """Returns the patron's fine amount."""
        return self._fine_amount

    def amend_fine(self, amount):
        """Updates the patron's fine amount."""
        self._fine_amount += amount

    def add_library_item(self, library_item):
        """Adds library items to the patron's checked out items."""
        self._checked_out_items.append(library_item)

    def remove_library_item(self, library_item):
        """Removes the library item from the patron's checked out items."""
        self._checked_out_items.remove(library_item)


class Library:
    """Base class that represents all libraries."""

    def __init__(self):
        """Creates a library object and initializes its attributes."""
        self._holdings = []
        self._members = []
        self._current_date = 0

    def get_current_date(self):
        """Returns the library's current date."""
        return self._current_date

    def add_library_item(self, library_item):
        """Adds a library item to the library's holdings."""
        self._holdings.append(library_item)

    def add_patron(self, patron):
        """Adds a patron to the library's membership."""
        self._members.append(patron)

    def lookup_library_item_from_id(self, library_item_id):
        """Returns the LibraryItem object corresponding to the ID parameter, or None if no such LibraryItem is in the holdings."""
        # Available upon request
        pass

    def lookup_patron_from_id(self, patron_id):
        """Returns the Patron object corresponding to the ID parameter, or None if no such Patron is a member."""
        # Available upon request
        pass

    def check_out_library_item(self, patron_id, library_item_id):
        """Checks out a library item to a library member."""
        # Available upon request
        pass
        

    def return_library_item(self, library_item_id):
        """Allows a member to return a library item."""
        # Available upon request
        pass

    def request_library_item(self, patron_id, library_item_id):
        """Allows a member to request a library item."""
        # Available upon request
        pass

    def pay_fine(self, patron_id, amount):
        """Allows members to pay fines on library items."""
        # Available upon request
        pass


    def increment_current_date(self):
        """Updates fines based on increments to the current date."""
        # Available upon request
        pass


def main():
    """Executes the above library simulator when the file is run as a script."""
    b1 = Book("345", "Phantom Tollbooth", "Juster")
    a1 = Album("456", "...And His Orchestra", "The Fastbacks")
    m1 = Movie("567", "Laputa", "Miyazaki")

    p1 = Patron("abc", "Felicity")
    p2 = Patron("bcd", "Waldo")

    lib = Library()
    lib.add_library_item(b1)
    lib.add_library_item(a1)
    lib.add_patron(p1)
    lib.add_patron(p2)

    lib.check_out_library_item("bcd", "456")
    loc = a1.get_location()
    lib.request_library_item("abc", "456")
    for i in range(57):
        lib.increment_current_date()  # 57 days pass
    p2_fine = p2.get_fine_amount()
    lib.pay_fine("bcd", p2_fine)
    lib.return_library_item("456")


if __name__ == '__main__':
    main()
