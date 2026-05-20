#include "Utils.h"

string toLower(string s)
{
    transform(s.begin(), s.end(), s.begin(), ::tolower);
    return s;
}
