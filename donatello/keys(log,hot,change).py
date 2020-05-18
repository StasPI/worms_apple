import keyboard

# https://github.com/boppreh/keyboard#keyboard.add_abbreviation

# # Записывает все клавиши до нажатия клавиши Escape и воспроизводит ключи
# rk = keyboard.record(until='Esc')
# keyboard.play(rk, speed_factor=1)

# # Записывает всю клавиатуру до натаия эскейп, затем останавливается запись и переменную записываются все ключи
# keyboard.start_recording()
# keyboard.wait('esc')
# a = keyboard.stop_recording()
# print(a)

# ''''-------------------------------------------------------------------------------'''
# # Устанавливает на горячие клавишы определенные события

# keyboard.add_hotkey('a', lambda: keyboard.write('Geek'))
# keyboard.add_hotkey('ctrl + shift + a', print, args=('you entered', 'hotkey'))
# keyboard.wait('esc')

# ''''-------------------------------------------------------------------------------'''
# # варианты остановки, первое до завершения скрипта второе до нажатия клавишы

# # keyboard.wait()
# keyboard.wait('esc')

# ''''-------------------------------------------------------------------------------'''
# Берет слова из списка и использует их как абривиатуру, после ввода слова и нажатия пробела заменяется заданным значением.
l = ['скачать', 'антивирус']

for i in l:
    keyboard.add_abbreviation(i, 'мемасики с котятками')

keyboard.wait('esc')
