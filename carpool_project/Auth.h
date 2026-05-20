#pragma once
#include "Account.h"

const int MAX = 100;

// ================= AUTH (Singleton) =================
class Auth
{
    Account driverAccounts[MAX], passengerAccounts[MAX];
    int driverCount, passengerCount;

    void load(const string &filename, Account accounts[], int &count);
    void loadDrivers();
    void saveDrivers();
    void save(const string &filename, Account accounts[], int count);
    bool exists(Account accounts[], int count, const string &username);
    bool check(Account accounts[], int count, const string &username, const string &password);

    Auth();
    Auth(const Auth &) = delete;
    Auth &operator=(const Auth &) = delete;
public:
    static Auth &getInstance();

    bool    regDriver(const string &username, const string &password,
                      const string &driverName, const string &driverPhone,
                      const string &carModel,   const string &plateNumber);
    bool    regPass(const string &username, const string &password, const string &phone);
    bool    loginDriver(const string &username, const string &password);
    bool    loginPass(const string &username, const string &password);
    string  getPassPhone(const string &username);
    Account *getDriverAccount(const string &username);
};
