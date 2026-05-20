#pragma once
#include "Driver.h"

// ================= CARPOOL =================
class Carpool
{
    string src, dst, departureTime, driverUsername;
    Driver driver;
public:
    void display()        const;
    void displayWithCar() const;
    void set(string s, string d, string t, string n, string ph, int se, double pr,
             string du = "", string cm = "", string pn = "");

    string        getSrc()            const;
    string        getDst()            const;
    string        getDepartureTime()  const;
    string        getDriverUsername() const;
    Driver       &getDriver();
    const Driver &getDriver()         const;
};
