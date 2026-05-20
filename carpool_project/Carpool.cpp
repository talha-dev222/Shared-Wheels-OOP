#include "Carpool.h"
#include <iostream>
using namespace std;

void Carpool::display() const
{
    cout << "Route: " << src << " -> " << dst << " | Time: " << departureTime << "\n";
    driver.display();
}

void Carpool::displayWithCar() const
{
    cout << "Route: " << src << " -> " << dst << " | Time: " << departureTime << "\n";
    cout << "Driver: " << driver.getName() << " | Phone: " << driver.getPhone()
         << " | Seats: " << driver.getSeats() << " | Price: Rs." << driver.getPrice()
         << " | Car Model: " << driver.getCarModel() << "\n";
}

void Carpool::set(string s, string d, string t, string n, string ph,
                  int se, double pr, string du, string cm, string pn)
{
    src           = s;
    dst           = d;
    departureTime = t;
    driverUsername= du;
    driver.set(n, ph, se, pr, cm, pn);
}

string        Carpool::getSrc()            const { return src; }
string        Carpool::getDst()            const { return dst; }
string        Carpool::getDepartureTime()  const { return departureTime; }
string        Carpool::getDriverUsername() const { return driverUsername; }
Driver       &Carpool::getDriver()               { return driver; }
const Driver &Carpool::getDriver()         const { return driver; }
