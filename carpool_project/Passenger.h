#pragma once
#include "User.h"

// ================= PASSENGER =================
class Passenger : public User
{
    string bookedSrc, bookedDst;
public:
    Passenger();
    void input() override;
    void display() const override;
    void setBooking(string src, string dst);
    string getBookedSrc() const;
    string getBookedDst() const;
};
