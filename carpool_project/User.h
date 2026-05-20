#pragma once
#include <string>
using namespace std;

// ================= USER (Abstract Base Class) =================
class User
{
protected:
    string name, phone;
public:
    virtual void input();
    void set(string n, string p);
    string getName() const;
    string getPhone() const;
    virtual void display() const = 0;
    virtual ~User() {}
};
