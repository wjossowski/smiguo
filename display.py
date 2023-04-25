import digitalio
import adafruit_character_lcd.character_lcd as characterlcd

class MyDisplay:
    lcd: characterlcd.Character_LCD_Mono
    
    columns = 16
    rows = 2

    msg = ""

    def __init__(self, rs: digitalio.Pin, en: digitalio.Pin, d4: digitalio.Pin, d5: digitalio.Pin, d6: digitalio.Pin, d7: digitalio.Pin):
        self.lcd = characterlcd.Character_LCD_Mono(
                self.__pin(rs),
                self.__pin(en),
                self.__pin(d4),
                self.__pin(d5),
                self.__pin(d6),
                self.__pin(d7),
                self.columns, self.rows)

    def write(self, line1 = "", line2 = ""):
        msg = self.__parse(line1) + '\n' + self.__parse(line2)
        self.msg = msg.replace('\n', '\\n')
        self.lcd.message = msg

    def __parse(self, line):
        if (len(line) > self.columns):
            raise TypeError("To many characters in line")
        return line.center(self.columns)

    def __pin(self, pin: digitalio.Pin):
        return digitalio.DigitalInOut(pin)
        

