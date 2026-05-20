#include "User.h"
#include <iostream>
#include <algorithm>
using namespace std;

void User::input()
{
    cout << "Name: ";
    getline(cin, name);
    while (name.empty())
    {
        cout << "Not empty: ";
        getline(cin, name);
    }
    cout << "Phone: ";
    getline(cin, phone);
    while (phone.length() != 11 || !all_of(phone.begin(), phone.end(), ::isdigit))
    {
        cout << "11-digit phone: ";
        getline(cin, phone);
    }
}

void User::set(string n, string p)
{
    name = n;
    phone = p;
}

string User::getName() const { return name; }
string User::getPhone() const { return phone; }
