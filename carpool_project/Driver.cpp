#include "Driver.h"
#include <iostream>
#include <algorithm>
using namespace std;

Driver::Driver() : seats(0), price(0), carModel(""), plateNumber("") {}

void Driver::input()
{
    User::input();
    cout << "Seats: ";
    cin >> seats;
    while (cin.fail() || seats <= 0)
    {
        cin.clear();
        cin.ignore(1000, '\n');
        cout << "Must be a number >0: ";
        cin >> seats;
    }
    cout << "Price/seat: ";
    cin >> price;
    while (cin.fail() || price <= 0)
    {
        cin.clear();
        cin.ignore(1000, '\n');
        cout << "Must be a number >0: ";
        cin >> price;
    }
    cin.ignore(1000, '\n');
}

void Driver::display() const
{
    cout << "Driver: " << name << " | Phone: " << phone
         << " | Seats: " << seats << " | Price: Rs." << price
         << " | Car: " << carModel << " | Plate: " << plateNumber << "\n";
}

void Driver::set(string n, string p, int s, double pr, string cm, string pn)
{
    User::set(n, p);
    seats = s;
    price = pr;
    carModel = cm;
    plateNumber = pn;
}

int    Driver::getSeats()       const { return seats; }
void   Driver::setSeats(int s)        { seats = s; }
double Driver::getPrice()       const { return price; }
string Driver::getCarModel()    const { return carModel; }
string Driver::getPlateNumber() const { return plateNumber; }
void   Driver::setCarModel(string cm)  { carModel = cm; }
void   Driver::setPlateNumber(string pn){ plateNumber = pn; }
