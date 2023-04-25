import board
import digitalio
import adafruit_character_lcd.character_lcd as characterlcd

lcd_rs = digitalio.DigitalInOut(board.GP9)
lcd_en = digitalio.DigitalInOut(board.GP8)

lcd_d7 = digitalio.DigitalInOut(board.GP13)
lcd_d6 = digitalio.DigitalInOut(board.GP12)
lcd_d5 = digitalio.DigitalInOut(board.GP11)
lcd_d4 = digitalio.DigitalInOut(board.GP10)

lcd_columns = 16
lcd_rows = 2

lcd = characterlcd.Character_LCD_Mono(lcd_rs, lcd_en, lcd_d4, lcd_d5, lcd_d6, lcd_d7, lcd_columns, lcd_rows)

def pad(str):
    return str.center(lcd_columns)

def write(l1 = "", l2 = ""):
    if (len(l1) > lcd_columns):
        print('invalid length', l1)
        return
    if (len(l2) > lcd_columns):
        print('invalid length', l2)
        return
    msg = pad(l1) + '\n' + pad(l2)
    lcd.message = msg
    return msg

