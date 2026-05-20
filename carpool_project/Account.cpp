#include "Account.h"

void Account::set(string un, string pw, string ph)
{
    username = un;
    password = pw;
    phone    = ph;
}

void Account::setDriverInfo(string dn, string dp, string cm, string pn)
{
    driverName   = dn;
    driverPhone  = dp;
    carModel     = cm;
    plateNumber  = pn;
}

string Account::getUsername()    const { return username; }
string Account::getPassword()    const { return password; }
string Account::getPhone()       const { return phone; }
string Account::getCarModel()    const { return carModel; }
string Account::getPlateNumber() const { return plateNumber; }
string Account::getDriverName()  const { return driverName; }
string Account::getDriverPhone() const { return driverPhone; }
