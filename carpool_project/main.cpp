#include "CarpoolFacade.h"

void CarpoolFacade::start()
{
    CarpoolSystem::getInstance().menu();
}

// ================= MAIN =================
int main()
{
    CarpoolFacade app;
    app.start();
    return 0;
}
