# Copyright (c) 2020 Kolvakh B.
# This file is part of PyQtAccounts.

# PyQtAccounts is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# PyQtAccounts is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with PyQtAccounts.  If not, see <https://www.gnu.org/licenses/>.

PyQtAccounts
Simple account database manager.

Setup

Тут описана інструкція якій треба слідувати, аби програма PyQtAccounts запрацювала.

PyQtAccounts використовує певні додаткові бібліотеки, ось їх перелік:

* Python 3.6.9 - інтерпретатор мови програмування python
* PyQt5 5.9.5 - графічну бібліотеку Qt для мови програмування python
* cryptography 2.8 - бібліотеку алгоритмів шифрування для мови програмування
                     python

Ось як їх встановити.

Для PyQt5 в терміналі введіть команду:

~$ sudo apt install python3-pyqt5

Аби встановити бібліотеку cryptography спершу встановіть pip3:

~$ sudo apt install pip3

А далі:

~$ pip3 install cryptography

Вітаємо! Тепер ви можете використовувати програму PyQtAccounts і безпечно зберігати паролі своїх акаунтів у зашифрованих базах данних.

Але це ще не все, PyQtAccounts зручніше запускати натискаючи на іконку на панелі програм.
Ось як це зробити:

Перейдіть на робочий стіл (зауважимо: не в папку Desktop, а саме на робочий стіл). Далі клікніть правою кнопкою миші, виберіть Create a new launcher here
В полі Name введіть 'PyQtAccounts', у полі Command вкажіть шлях до файлу run.sh, він знаходиться у папці PyQtAccounts програми. Встановіть іконку icon.svg з папки img. Натисніть Ok. Натимніть Так у діалозі що з'явиться (аби додати і до меню також). Знайдіть в меню Other пункт MyAccounts, і додайте його на панель.

Далі відкрийте файл run.sh, знайдіть рядок:

cd /home/python/Documents/PyTools/PyQtAccounts/

І замініть в ньому /home/python/Documents/PyTools на повний шлях до папки програми (яку ви розпакували)

У рядку:

python3 /home/python/Documents/PyTools/PyQtAccounts/PyQtAccounts.py

Зробіть теж саме.