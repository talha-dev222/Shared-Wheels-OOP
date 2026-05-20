#include "Passenger.h"
#include <iostream>
using namespace std;

Passenger::Passenger() : bookedSrc(""), bookedDst("") {}

void Passenger::input()
{
    cout << "Your Name: ";
    getline(cin, name);
    while (name.empty())
    {
        cout << "Not empty: ";
        getline(cin, name);
    }
    phone = "";
}

void Passenger::display() const
{
    cout << "Passenger: " << name << " | Phone: " << phone;
    if (!bookedSrc.empty())
        cout << " | Booked: " << bookedSrc << " -> " << bookedDst;
    cout << "\n";
}

void   Passenger::setBooking(string src, string dst) { bookedSrc = src; bookedDst = dst; }
string Passenger::getBookedSrc() const { return bookedSrc; }
string Passenger::getBookedDst() const { return bookedDst; }
