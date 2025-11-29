#!/usr/bin/env python3
"""
Einfaches, vereinfachtes Testskript für Stepper-Motoren (deutsch).

Beispiel:
  python motortest.py -m 1 -s SINGLE -c 100 -d 0.01 -D vor
  python motortest.py --simulieren -m 2 -s micro -c 50

Das Skript ist bewusst schlank gehalten: deutsche Optionen, Standardwerte,
und eine `--simulieren`-Option für Systeme ohne Hardware.
"""

import argparse
import time
import sys

# Versuche Hardware-Module zu laden; bei Fehlschlag Simulation anbieten
try:
    import board
    import busio
    from adafruit_motorkit import MotorKit
    import adafruit_motor
    import adafruit_motorkit

    HARDWARE = True
except Exception:
    HARDWARE = False

    class stepper:  # minimale Simulation der Konstanten
        SINGLE = "SINGLE"
        DOUBLE = "DOUBLE"
        MICROSTEP = "MICRO"
        FORWARD = "FORWARD"
        BACKWARD = "BACKWARD"


def parse_args():
    p = argparse.ArgumentParser(description="Einfaches Stepper-Testskript (DE)")
    p.add_argument(
        "-s",
        "--stepstil",
        choices=["SINGLE", "doppel", "micro"],
        default="SINGLE",
        dest="stepstil",
        help="Schritt-Modus: einfach|doppel|micro (Standard: einfach)",
    )
    p.add_argument(
        "-m",
        "--motorid",
        type=int,
        choices=range(1, 5),
        default=1,
        dest="motorid",
        help="Motor-Id 1..4 (Standard: 1)",
    )
    p.add_argument(
        "-c",
        "--schritte",
        type=int,
        default=100,
        dest="schritte",
        help="Anzahl Schritte (Standard: 100)",
    )
    # Verwende -v für Verzögerung, um Konflikt mit -d zu vermeiden
    p.add_argument(
        "-v",
        "--verzoegerung",
        type=float,
        default=0.01,
        dest="verzoegerung",
        help="Pause zwischen Schritten in Sekunden (Standard: 0.01)",
    )
    p.add_argument(
        "-D",
        "--richtung",
        choices=["vor", "zurueck"],
        default="vor",
        dest="richtung",
        help="Richtung: vor|zurueck (Standard: vor)",
    )
    p.add_argument(
        "--simulieren",
        action="store_true",
        dest="simulieren",
        help="Ohne Hardware laufen (nur Ausgabe)",
    )
    return p.parse_args()


def build_motors():
    i2c = busio.I2C(board.SCL, board.SDA)
    kit1 = MotorKit(i2c=i2c, address=0x60)
    kit2 = MotorKit(i2c=i2c, address=0x70)

    return [kit1.stepper1, kit1.stepper2, kit2.stepper1, kit2.stepper2]


def main():
    args = parse_args()

    if args.simulieren:
        print("Simulation: keine Hardware-Operationen")
    elif not HARDWARE:
        print(
            "Hardware-Module nicht verfügbar. Starte mit --simulieren, wenn nötig.",
            file=sys.stderr,
        )
        sys.exit(1)

    stil_map = {
        "einfach": stepper.SINGLE,
        "doppel": stepper.DOUBLE,
        "micro": stepper.MICROSTEP,
    }
    richt_map = {"vor": stepper.FORWARD, "zurueck": stepper.BACKWARD}

    stil = stil_map[args.stepstil]
    richt = richt_map[args.richtung]
    idx = args.motorid - 1

    motor = None
    if not args.simulieren:
        motors = build_motors()
        if not (0 <= idx < len(motors)):
            print(f"Ungueltige Motor-Id: {args.motorid}", file=sys.stderr)
            sys.exit(1)
        motor = motors[idx]

    # Zusätzliche Laufzeitprüfung: stelle sicher, dass motor initialisiert wurde
    if not args.simulieren and motor is None:
        print("Fehler: Motor konnte nicht initialisiert werden.", file=sys.stderr)
        sys.exit(1)

    print(
        f"Start: motor={args.motorid} schritte={args.schritte} stil={args.stepstil} "
        f"richtung={args.richtung} verz={args.verzoegerung} simul={args.simulieren}"
    )

    try:
        for i in range(args.schritte):
            if args.simulieren:
                # Nur bei jedem 10%-Schritt etwas ausgeben
                if args.schritte >= 10 and (i % (max(1, args.schritte // 10)) == 0):
                    print(f"Simulierter Schritt {i+1}/{args.schritte}")
            else:
                motor.onestep(direction=richt, style=stil)
            time.sleep(args.verzoegerung)
    except KeyboardInterrupt:
        print("\nAbgebrochen vom Benutzer")
    finally:
        if motor is not None:
            rel = getattr(motor, "release", None)
            if callable(rel):
                rel()
        print("Fertig")


if __name__ == "__main__":
    main()
