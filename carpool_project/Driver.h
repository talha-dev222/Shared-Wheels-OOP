#pragma once
#include "User.h"

// ================= DRIVER =================
class Driver : public User
{
    int seats;
    double price;
    string carModel, plateNumber;
public:
    Driver();
    void input() override;
    void display() const override;
    void set(string n, string p, int s, double pr, string cm = "", string pn = "");
    int getSeats() const;
    void setSeats(int s);
    double getPrice() const;
    string getCarModel() const;
    string getPlateNumber() const;
    void setCarModel(string cm);
    void setPlateNumber(string pn);
};
