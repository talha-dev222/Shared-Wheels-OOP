# Shared-Wheels-OOP
C++ OOP-based carpool management system with authentication, ride booking, and file handling.

SharedWheels/
│
├── main.cpp                  # Entry point — launches the app via CarpoolFacade
│
├── CarpoolFacade.h           # Facade pattern — single start() entry point
├── CarpoolSystem.h/.cpp      # Core system logic (Singleton) — menus, booking, search
│
├── Carpool.h/.cpp            # Represents one ride offer (route + driver details)
├── Driver.h/.cpp             # Driver entity (inherits User)
├── Passenger.h/.cpp          # Passenger entity (inherits User)
├── User.h/.cpp               # Abstract base class for all users
│
├── Auth.h/.cpp               # Authentication system (Singleton) — login & registration
├── Account.h/.cpp            # Stores login credentials and driver vehicle info
│
├── Repository.h              # Generic template class for managing collections
├── Utils.h/.cpp              # Utility helper — toLower() for case-insensitive comparisons
│
├── carpool.txt               # Auto-generated: persists all ride listings
├── driver_acc.txt            # Auto-generated: persists driver account records
└── pass_acc.txt              # Auto-generated: persists passenger account records
