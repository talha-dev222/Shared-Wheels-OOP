#pragma once
#include <string>
using namespace std;

// ================= ACCOUNT =================
class Account
{
    string username, password, phone;
    string carModel, plateNumber, driverName, driverPhone;
public:
    void set(string un, string pw, string ph = "");
    void setDriverInfo(string dn, string dp, string cm, string pn);
    string getUsername()    const;
    string getPassword()    const;
    string getPhone()       const;
    string getCarModel()    const;
    string getPlateNumber() const;
    string getDriverName()  const;
    string getDriverPhone() const;
};
