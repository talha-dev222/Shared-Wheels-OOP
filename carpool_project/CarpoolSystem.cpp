#include "CarpoolSystem.h"
#include "Utils.h"
#include <iostream>
#include <fstream>
#include <sstream>
using namespace std;

// ---- private: file I/O ----

void CarpoolSystem::saveFile()
{
    ofstream file("carpool.txt");
    for (int i = 0; i < cnt; i++)
        file << pool[i].getSrc()              << "|"
             << pool[i].getDst()              << "|"
             << pool[i].getDepartureTime()    << "|"
             << pool[i].getDriver().getName() << "|"
             << pool[i].getDriver().getPhone()<< "|"
             << pool[i].getDriver().getSeats()<< "|"
             << pool[i].getDriver().getPrice()<< "|"
             << pool[i].getDriverUsername()   << "|"
             << pool[i].getDriver().getCarModel()   << "|"
             << pool[i].getDriver().getPlateNumber() << "\n";
}

void CarpoolSystem::loadFile()
{
    ifstream file("carpool.txt");
    string line;
    cnt = 0;
    while (getline(file, line) && cnt < MAX)
    {
        if (line.empty()) continue;
        stringstream ss(line);
        string src, dst, depTime, name, phone, seats, price, driverUser, cm, pn;
        getline(ss, src,        '|');
        getline(ss, dst,        '|');
        getline(ss, depTime,    '|');
        getline(ss, name,       '|');
        getline(ss, phone,      '|');
        getline(ss, seats,      '|');
        getline(ss, price,      '|');
        getline(ss, driverUser, '|');
        getline(ss, cm,         '|');
        getline(ss, pn);
        try
        {
            pool[cnt].set(src, dst, depTime, name, phone,
                          stoi(seats), stod(price), driverUser, cm, pn);
            cnt++;
        }
        catch (...) {}
    }
}

// ---- private: input helpers ----

bool CarpoolSystem::getChoice(int &choice, int minVal, int maxVal)
{
    cin >> choice;
    if (cin.fail() || choice < minVal || choice > maxVal)
    {
        cin.clear();
        cin.ignore(1000, '\n');
        cout << "Invalid. Enter " << minVal << "-" << maxVal << ".\n";
        return false;
    }
    cin.ignore(1000, '\n');
    return true;
}

void CarpoolSystem::getCreds(string &username, string &password, bool confirm)
{
    cout << "Username: ";
    getline(cin, username);
    while (username.empty())
    {
        cout << "Not empty: ";
        getline(cin, username);
    }
    cout << "Password: ";
    getline(cin, password);
    while (password.empty())
    {
        cout << "Not empty: ";
        getline(cin, password);
    }
    if (confirm)
    {
        string c;
        cout << "Confirm Password: ";
        getline(cin, c);
        while (c != password)
        {
            cout << "Passwords don't match. Re-enter Password: ";
            getline(cin, password);
            cout << "Confirm Password: ";
            getline(cin, c);
        }
    }
}

bool CarpoolSystem::isValidTime(const string &t)
{
    if (t.size() != 5)  return false;
    if (!isdigit(t[0])) return false;
    if (!isdigit(t[1])) return false;
    if (t[2] != ':')    return false;
    if (!isdigit(t[3])) return false;
    if (!isdigit(t[4])) return false;
    int hours   = (t[0]-'0')*10 + (t[1]-'0');
    int minutes = (t[3]-'0')*10 + (t[4]-'0');
    return hours >= 0 && hours <= 23 && minutes >= 0 && minutes <= 59;
}

// ---- private: carpool operations ----

void CarpoolSystem::addCarpool(const string &driverUser)
{
    if (cnt >= MAX) { cout << "Storage full!\n"; return; }

    Account *acc = Auth::getInstance().getDriverAccount(driverUser);
    if (!acc) { cout << "Driver account not found.\n"; return; }

    string src, dst, time;
    cout << "\n-- Carpool Details --\n";
    cout << "Source: ";
    getline(cin, src);
    while (src.empty()) { cout << "Not empty: "; getline(cin, src); }

    cout << "Destination: ";
    getline(cin, dst);
    while (dst.empty()) { cout << "Not empty: "; getline(cin, dst); }

    cout << "Departure Time (HH:MM): ";
    getline(cin, time);
    while (!isValidTime(time))
    {
        cout << "Please enter valid time (HH:MM, 00:00-23:59): ";
        getline(cin, time);
    }

    cout << "Seats: ";
    int seats;
    cin >> seats;
    while (cin.fail() || seats <= 0)
    {
        cin.clear(); cin.ignore(1000, '\n');
        cout << "Must be a number >0: "; cin >> seats;
    }

    cout << "Price/seat: ";
    double price;
    cin >> price;
    while (cin.fail() || price <= 0)
    {
        cin.clear(); cin.ignore(1000, '\n');
        cout << "Must be a number >0: "; cin >> price;
    }
    cin.ignore(1000, '\n');

    pool[cnt].set(src, dst, time,
                  acc->getDriverName(), acc->getDriverPhone(),
                  seats, price,
                  driverUser,
                  acc->getCarModel(), acc->getPlateNumber());
    cnt++;
    saveFile();
    cout << "Carpool added!\n";
}

void CarpoolSystem::viewAll()
{
    if (!cnt) { cout << "No carpools.\n"; return; }
    for (int i = 0; i < cnt; i++)
    {
        cout << "\n#" << i + 1 << " ";
        pool[i].display();
    }
}

void CarpoolSystem::viewMine(const string &username)
{
    int found = 0;
    for (int i = 0; i < cnt; i++)
        if (pool[i].getDriverUsername() == username)
        {
            cout << "\n#" << ++found << " ";
            pool[i].display();
        }
    if (!found) cout << "No carpools added yet.\n";
}

void CarpoolSystem::deleteCarpool(const string &username)
{
    int myIdx[MAX], myCount = 0;
    for (int i = 0; i < cnt; i++)
        if (pool[i].getDriverUsername() == username)
            myIdx[myCount++] = i;

    if (!myCount) { cout << "No carpools to delete.\n"; return; }

    for (int i = 0; i < myCount; i++)
    {
        cout << "\n#" << i + 1 << " ";
        pool[myIdx[i]].display();
    }

    cout << "\nEnter carpool number to delete (1-" << myCount << "): ";
    int pick;
    cin >> pick;
    while (cin.fail() || pick < 1 || pick > myCount)
    {
        cin.clear(); cin.ignore(1000, '\n');
        cout << "Invalid, enter 1-" << myCount << ": "; cin >> pick;
    }
    cin.ignore(1000, '\n');

    int delIdx = myIdx[pick - 1];
    for (int i = delIdx; i < cnt - 1; i++)
        pool[i] = pool[i + 1];
    cnt--;
    saveFile();
    cout << "Carpool deleted.\n";
}

void CarpoolSystem::search()
{
    string src, dst;
    cout << "Source: ";      getline(cin, src);
    cout << "Destination: "; getline(cin, dst);
    bool found = false;
    for (int i = 0; i < cnt; i++)
    {
        if (toLower(pool[i].getSrc()) == toLower(src) &&
            toLower(pool[i].getDst()) == toLower(dst))
        {
            cout << "\n";
            pool[i].display();
            if (pool[i].getDriver().getSeats() == 0)
                cout << "*** FULLY BOOKED ***\n";
            found = true;
        }
    }
    if (!found) cout << "No carpool found for this route.\n";
}

void CarpoolSystem::bookSeat(Passenger &passenger)
{
    string src, dst;
    cout << "Source: ";      getline(cin, src);
    cout << "Destination: "; getline(cin, dst);

    int matches[MAX], matchCount = 0;
    for (int i = 0; i < cnt; i++)
        if (toLower(pool[i].getSrc()) == toLower(src) &&
            toLower(pool[i].getDst()) == toLower(dst) &&
            pool[i].getDriver().getSeats() > 0)
        {
            cout << ++matchCount << ". ";
            pool[i].displayWithCar();
            matches[matchCount - 1] = i;
        }

    if (!matchCount) { cout << "None available.\n"; return; }

    cout << "Pick (1-" << matchCount << "): ";
    int pick;
    cin >> pick;
    while (cin.fail() || pick < 1 || pick > matchCount)
    {
        cin.clear(); cin.ignore(1000, '\n');
        cout << "Invalid, enter 1-" << matchCount << ": "; cin >> pick;
    }
    cin.ignore(1000, '\n');

    int idx = matches[pick - 1];
    if (passenger.getBookedSrc() == pool[idx].getSrc() &&
        passenger.getBookedDst() == pool[idx].getDst())
    {
        cout << "You already booked this route!\n";
        return;
    }
    pool[idx].getDriver().setSeats(pool[idx].getDriver().getSeats() - 1);
    passenger.setBooking(pool[idx].getSrc(), pool[idx].getDst());
    cout << "Booked! Please call the driver for Confirmation\n";
    passenger.display();
    saveFile();
}

void CarpoolSystem::slider(Passenger &passenger)
{
    int available[MAX], availableCount = 0;
    for (int i = 0; i < cnt; i++)
        if (pool[i].getDriver().getSeats() > 0)
            available[availableCount++] = i;

    if (!availableCount)
    {
        if (cnt == 0) cout << "No carpools exist yet.\n";
        else          cout << "All carpools are fully booked.\n";
        return;
    }

    int cur = 0;
    char ch;
    while (true)
    {
        cout << "\n+====== RIDE [" << cur + 1 << "/" << availableCount << "] ======+\n";
        pool[available[cur]].display();
        cout << "[N]ext [P]rev [B]ook [Q]uit: ";
        cin >> ch; ch = tolower(ch); cin.ignore(1000, '\n');

        if      (ch == 'n') { if (cur < availableCount-1) cur++; else cout << "Last ride.\n"; }
        else if (ch == 'p') { if (cur > 0) cur--; else cout << "First ride.\n"; }
        else if (ch == 'b')
        {
            int idx = available[cur];
            if (passenger.getBookedSrc() == pool[idx].getSrc() &&
                passenger.getBookedDst() == pool[idx].getDst())
            {
                cout << "You already booked this route!\n";
            }
            else
            {
                pool[idx].getDriver().setSeats(pool[idx].getDriver().getSeats() - 1);
                passenger.setBooking(pool[idx].getSrc(), pool[idx].getDst());
                cout << "Booked! Please call the driver for Confirmation\n";
                passenger.display();
                saveFile();
            }
            availableCount = 0;
            for (int i = 0; i < cnt; i++)
                if (pool[i].getDriver().getSeats() > 0)
                    available[availableCount++] = i;
            if (!availableCount) { cout << "No more rides.\n"; break; }
            if (cur >= availableCount) cur = availableCount - 1;
        }
        else if (ch == 'q') { cout << "Exiting slider.\n"; break; }
        else cout << "Use N/P/B/Q.\n";
    }
}

// ---- private: portals ----

void CarpoolSystem::driverPortal()
{
    cout << "\n[DRIVER] 1.Register 2.Login 0.Back: ";
    int choice;
    if (!getChoice(choice, 0, 2)) return;
    if (choice == 0) return;

    string username, password;
    if (choice == 1)
    {
        getCreds(username, password, true);
        cout << "Registered! Logging you in...\n";
        cout << "\n-- Driver & Vehicle Details --\n";
        string driverName, driverPhone, carModel, plateNumber;
        cout << "Name: "; getline(cin, driverName);
        while (driverName.empty()) { cout << "Not empty: "; getline(cin, driverName); }
        cout << "Phone: "; getline(cin, driverPhone);
        while (driverPhone.length() != 11 ||
               !all_of(driverPhone.begin(), driverPhone.end(), ::isdigit))
        {
            cout << "11-digit phone: "; getline(cin, driverPhone);
        }
        cout << "Car/Bike Model: "; getline(cin, carModel);
        while (carModel.empty()) { cout << "Not empty: "; getline(cin, carModel); }
        cout << "Plate Number: "; getline(cin, plateNumber);
        while (plateNumber.empty()) { cout << "Not empty: "; getline(cin, plateNumber); }

        if (!Auth::getInstance().regDriver(username, password,
                                           driverName, driverPhone,
                                           carModel, plateNumber))
        {
            cout << "Username taken.\n"; return;
        }
    }
    else
    {
        getCreds(username, password);
        if (!Auth::getInstance().loginDriver(username, password))
        {
            cout << "Wrong credentials.\n"; return;
        }
    }

    cout << "Welcome, Driver " << username << "!\n";
    int ch = -1;
    do
    {
        cout << "\n[DRIVER] 1.Add Carpool  2.My Carpools  3.Delete Carpool  0.Logout: ";
        cin >> ch;
        if (cin.fail()) { cin.clear(); cin.ignore(1000,'\n'); ch = -1; continue; }
        cin.ignore(1000, '\n');
        if      (ch == 1) addCarpool(username);
        else if (ch == 2) viewMine(username);
        else if (ch == 3) deleteCarpool(username);
        else if (ch != 0) cout << "Invalid.\n";
    } while (ch != 0);
    cout << "Logged out.\n";
}

void CarpoolSystem::passPortal()
{
    cout << "\n[PASSENGER] 1.Register 2.Login 0.Back: ";
    int choice;
    if (!getChoice(choice, 0, 2)) return;
    if (choice == 0) return;

    string username, password;
    getCreds(username, password, choice == 1);
    if (choice == 1)
    {
        string ph;
        cout << "Phone: "; getline(cin, ph);
        while (ph.length() != 11 || !all_of(ph.begin(), ph.end(), ::isdigit))
        {
            cout << "11-digit phone: "; getline(cin, ph);
        }
        if (!Auth::getInstance().regPass(username, password, ph))
        {
            cout << "Username taken.\n"; return;
        }
        cout << "Registered! Logging you in...\n";
    }
    else if (!Auth::getInstance().loginPass(username, password))
    {
        cout << "Wrong credentials.\n"; return;
    }

    cout << "Welcome, Passenger " << username << "!\n";
    Passenger passenger;
    passenger.set(username, Auth::getInstance().getPassPhone(username));

    int ch = -1;
    do
    {
        cout << "\n[PASSENGER] 1.Slide Rides  2.Book  0.Logout: ";
        cin >> ch;
        if (cin.fail()) { cin.clear(); cin.ignore(1000,'\n'); ch = -1; continue; }
        cin.ignore(1000, '\n');
        if      (ch == 1) slider(passenger);
        else if (ch == 2) bookSeat(passenger);
        else if (ch != 0) cout << "Invalid.\n";
    } while (ch != 0);
    cout << "Logged out.\n";
}

// ---- constructor & public ----

CarpoolSystem::CarpoolSystem() : cnt(0) { loadFile(); }

CarpoolSystem &CarpoolSystem::getInstance()
{
    static CarpoolSystem instance;
    return instance;
}

void CarpoolSystem::menu()
{
    int role = -1;
    do
    {
        cout << "\n===== CARPOOL SYSTEM =====\n1.Driver  2.Passenger  0.Exit\nRole: ";
        cin >> role;
        if (cin.fail()) { cin.clear(); cin.ignore(1000,'\n'); role = -1; continue; }
        cin.ignore(1000, '\n');
        if      (role == 1) driverPortal();
        else if (role == 2) passPortal();
        else if (role != 0) cout << "Invalid.\n";
    } while (role != 0);
    cout << "Goodbye!\n";
}
