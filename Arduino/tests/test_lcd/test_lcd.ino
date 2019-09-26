#include <Wire.h>
#include "rgb_lcd.h"

rgb_lcd lcd;

void setup() 
{
    lcd.begin(16, 2);
    lcd.print("Hello");
    delay(1000);
}

void loop() 
{
    lcd.print("Hello");
    delay(1000);
    // set the cursor to column 0, line 1
    // (note: line 1 is the second row, since counting begins with 0):
    //lcd.setCursor(0, 1);
    //lcd.print(millis()/1000);
    //delay(100);
}
