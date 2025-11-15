# HASE-Roboterarm
Offical Repo of Hase Roboterarm


## Dev
#### Lockfiles/PID-Files
sollten in /run/roboarm gesammelt werden (Nimm auf Windows einf %temp% oder so)
PID-Dateien sind programmname.pid, und das einzige was drinnsteht ist die **P**rocess **ID** des Programms.
Das erleichtert das Verwalten von laufenden Prozessen und ermöglicht die Verhinderung von Duplikaten
z. B.:
wenn /run/roboarm/bsp.pid
NICHT EXISTIERT:
  erstells und schreib $PID rein
EXISTIERT:
  fehler ausgeben und exiten

#### shebang
Das shebang brauchst du auf linux, wenn du z. B. statt python3 main.py einfach nur main.py ausführen können willst
Du kannst es setzen indem du in die erste Zeile eines Skripts (bitte keine Binärdateien) `#! <pfad zum interpreter>` schreibst
z.B. für Python: `#! /usr/bin/python3`
