Lista funkcji:
01 – odczyt wyjść bitowych (Coils)
02 – odczyt wejść bitowych (Discrete Inputs)
03 – odczyt n rejestrów (Holding Registers)
04 – odczyt n rejestrów wejściowych (Input Registers)
05 – zapis 1 bitu (Coil)
06 – zapis 1 rejestru (Holding Register)
07 – odczyt statusu
08 – test diagnostyczny
0F – zapis n bitów (Coils)
10 – zapis n rejestrów (Holding Registers)
11 – identyfikacja urządzenia slave
80 – #FF – zarezerwowane na odpowiedzi błędne

Określają one obszary pamięci w komunikacji Modbus:

Coils (C) – zmienne bitowe – możliwy odczyt i zapis – 1 bit długości

Holding Registers (HR) – rejestry – możliwy odczyt i zapis – 16 bitów długości

Discrete Inputs (DI) – zmienne bitowe wejściowe – możliwy tylko odczyt – 1 bit długości

Input Registers (IR) – rejestry wejściowy – możliwy tylko odczyt – 16 bitów długości

