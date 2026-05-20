#pragma once
#include "Carpool.h"
#include "Passenger.h"
#include "Auth.h"

// ================= CARPOOL SYSTEM (Singleton) =================
class CarpoolSystem
{
    Carpool pool[MAX];
    int cnt;

    void saveFile();
    void loadFile();
    bool getChoice(int &choice, int minVal, int maxVal);
    void getCreds(string &username, string &password, bool confirm = false);
    bool isValidTime(const string &t);

    void addCarpool(const string &driverUser);
    void viewAll();
    void viewMine(const string &username);
    void deleteCarpool(const string &username);
    void search();
    void bookSeat(Passenger &passenger);
    void slider(Passenger &passenger);

    void driverPortal();
    void passPortal();

    CarpoolSystem();
    CarpoolSystem(const CarpoolSystem &) = delete;
    CarpoolSystem &operator=(const CarpoolSystem &) = delete;
public:
    static CarpoolSystem &getInstance();
    void menu();
};
