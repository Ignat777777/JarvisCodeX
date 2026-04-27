"""
Arduino Controller РґР»СЏ JARVIS
Р’РµСЂСЃРёСЏ: 1.0

РЈС‚РёР»РёС‚Р° РґР»СЏ РѕС‚РїСЂР°РІРєРё РєРѕРјР°РЅРґ РЅР° Arduino Uno С‡РµСЂРµР· Serial.
РџРѕРґРґРµСЂР¶РёРІР°РµРјС‹Рµ РєРѕРјР°РЅРґС‹:
  - PINMODE:<pin>,<mode>     - РЈСЃС‚Р°РЅРѕРІРєР° СЂРµР¶РёРјР° РїРёРЅР° (INPUT/OUTPUT/INPUT_PULLUP)
  - DWRITE:<pin>,<value>     - Р¦РёС„СЂРѕРІРѕР№ РІС‹РІРѕРґ (HIGH/LOW)
  - BLINK:<pin>,<count>      - РњРѕСЂРіР°РЅРёРµ СЃРІРµС‚РѕРґРёРѕРґРѕРј (5 СЃРµРє РІРєР», 1 СЃРµРє РІС‹РєР»)
  - WAIT:<ms>                - РџР°СѓР·Р° РІ РјРёР»Р»РёСЃРµРєСѓРЅРґР°С…
  - PING                     - РџСЂРѕРІРµСЂРєР° СЃРІСЏР·Рё
"""

import serial
import serial.tools.list_ports
import time
import sys


class ArduinoController:
    """РљРѕРЅС‚СЂРѕР»Р»РµСЂ РґР»СЏ СѓРїСЂР°РІР»РµРЅРёСЏ Arduino Uno С‡РµСЂРµР· Serial."""

    def __init__(self, port: str = None, baudrate: int = 9600, timeout: float = 1.0):
        """
        РРЅРёС†РёР°Р»РёР·Р°С†РёСЏ РєРѕРЅС‚СЂРѕР»Р»РµСЂР°.

        Args:
            port: COM-РїРѕСЂС‚ (РЅР°РїСЂРёРјРµСЂ, 'COM3' РёР»Рё '/dev/ttyUSB0').
                  Р•СЃР»Рё None, Р±СѓРґРµС‚ РїСЂРµРґР»РѕР¶РµРЅ РІС‹Р±РѕСЂ РёР· СЃРїРёСЃРєР°.
            baudrate: РЎРєРѕСЂРѕСЃС‚СЊ РїРµСЂРµРґР°С‡Рё РґР°РЅРЅС‹С… (РїРѕ СѓРјРѕР»С‡Р°РЅРёСЋ 9600).
            timeout: РўР°Р№РјР°СѓС‚ С‡С‚РµРЅРёСЏ РІ СЃРµРєСѓРЅРґР°С….
        """
        self.port = port
        self.baudrate = baudrate
        self.timeout = timeout
        self.serial = None
        self.connected = False

    def list_ports(self) -> list:
        """Р’РѕР·РІСЂР°С‰Р°РµС‚ СЃРїРёСЃРѕРє РґРѕСЃС‚СѓРїРЅС‹С… COM-РїРѕСЂС‚РѕРІ."""
        ports = serial.tools.list_ports.comports()
        return [
            {
                "device": port.device,
                "description": port.description,
                "hwid": port.hwid
            }
            for port in ports
        ]

    def connect(self, port: str = None) -> bool:
        """
        РџРѕРґРєР»СЋС‡РµРЅРёРµ Рє Arduino.

        Args:
            port: COM-РїРѕСЂС‚. Р•СЃР»Рё None, РёСЃРїРѕР»СЊР·СѓРµС‚СЃСЏ РїРѕСЂС‚ РёР· РєРѕРЅСЃС‚СЂСѓРєС‚РѕСЂР°.

        Returns:
            True РµСЃР»Рё РїРѕРґРєР»СЋС‡РµРЅРёРµ СѓСЃРїРµС€РЅРѕ.
        """
        port = port or self.port

        if not port:
            print("РћС€РёР±РєР°: РЅРµ СѓРєР°Р·Р°РЅ COM-РїРѕСЂС‚")
            return False

        try:
            self.serial = serial.Serial(port, self.baudrate, timeout=self.timeout)
            time.sleep(2)  # Р–РґС‘Рј РёРЅРёС†РёР°Р»РёР·Р°С†РёСЋ Arduino
            self.connected = True
            self.port = port
            print(f"РџРѕРґРєР»СЋС‡РµРЅРѕ Рє {port}")
            return True
        except serial.SerialException as e:
            print(f"РћС€РёР±РєР° РїРѕРґРєР»СЋС‡РµРЅРёСЏ: {e}")
            return False

    def disconnect(self):
        """РћС‚РєР»СЋС‡РµРЅРёРµ РѕС‚ Arduino."""
        if self.serial and self.connected:
            self.serial.close()
            self.connected = False
            print("РћС‚РєР»СЋС‡РµРЅРѕ")

    def _send_command(self, command: str) -> str:
        """
        РћС‚РїСЂР°РІРєР° РєРѕРјР°РЅРґС‹ Рё РїРѕР»СѓС‡РµРЅРёРµ РѕС‚РІРµС‚Р°.

        Args:
            command: РўРµРєСЃС‚ РєРѕРјР°РЅРґС‹.

        Returns:
            РћС‚РІРµС‚ РѕС‚ Arduino.
        """
        if not self.connected:
            return "ERROR:NOT_CONNECTED"

        # РћС‚РїСЂР°РІР»СЏРµРј РєРѕРјР°РЅРґСѓ
        cmd_bytes = (command + "\n").encode('utf-8')
        self.serial.write(cmd_bytes)
        self.serial.flush()

        # Р§РёС‚Р°РµРј РѕС‚РІРµС‚
        response_lines = []
        start_time = time.time()

        while time.time() - start_time < self.timeout:
            if self.serial.in_waiting > 0:
                line = self.serial.readline().decode('utf-8').strip()
                if line:
                    response_lines.append(line)
                    # Р•СЃР»Рё РїРѕР»СѓС‡РёР»Рё РѕС‚РІРµС‚, РїСЂРµРєСЂР°С‰Р°РµРј С‡С‚РµРЅРёРµ
                    if line.startswith("OK:") or line.startswith("ERROR:") or line == "PONG":
                        break

        return "\n".join(response_lines) if response_lines else "ERROR:TIMEOUT"

    def ping(self) -> bool:
        """
        РџСЂРѕРІРµСЂРєР° СЃРІСЏР·Рё СЃ Arduino.

        Returns:
            True РµСЃР»Рё Arduino РѕС‚РІРµС‡Р°РµС‚.
        """
        response = self._send_command("PING")
        if "PONG" in response:
            print("вњ“ РЎРІСЏР·СЊ СѓСЃС‚Р°РЅРѕРІР»РµРЅР° (PING/PONG)")
            return True
        print(f"вњ— РќРµС‚ РѕС‚РІРµС‚Р°: {response}")
        return False

    def pinmode(self, pin: int, mode: str) -> bool:
        """
        РЈСЃС‚Р°РЅРѕРІРєР° СЂРµР¶РёРјР° РїРёРЅР°.

        Args:
            pin: РќРѕРјРµСЂ РїРёРЅР°.
            mode: Р РµР¶РёРј (INPUT, OUTPUT, INPUT_PULLUP).

        Returns:
            True РµСЃР»Рё СѓСЃРїРµС€РЅРѕ.
        """
        mode = mode.upper()
        if mode not in ("INPUT", "OUTPUT", "INPUT_PULLUP"):
            print(f"РћС€РёР±РєР°: РЅРµРІРµСЂРЅС‹Р№ СЂРµР¶РёРј '{mode}'")
            return False

        command = f"PINMODE:{pin},{mode}"
        response = self._send_command(command)

        if response.startswith("OK:PINMODE:"):
            print(f"вњ“ PINMODE: РїРёРЅ {pin} -> {mode}")
            return True
        print(f"вњ— РћС€РёР±РєР°: {response}")
        return False

    def dwrite(self, pin: int, value: str) -> bool:
        """
        Р¦РёС„СЂРѕРІРѕР№ РІС‹РІРѕРґ.

        Args:
            pin: РќРѕРјРµСЂ РїРёРЅР°.
            value: Р—РЅР°С‡РµРЅРёРµ (HIGH/LOW РёР»Рё 1/0).

        Returns:
            True РµСЃР»Рё СѓСЃРїРµС€РЅРѕ.
        """
        value = value.upper()
        if value in ("HIGH", "1"):
            value = "HIGH"
        elif value in ("LOW", "0"):
            value = "LOW"
        else:
            print(f"РћС€РёР±РєР°: РЅРµРІРµСЂРЅРѕРµ Р·РЅР°С‡РµРЅРёРµ '{value}'")
            return False

        command = f"DWRITE:{pin},{value}"
        response = self._send_command(command)

        if response.startswith("OK:DWRITE:"):
            print(f"вњ“ DWRITE: РїРёРЅ {pin} -> {value}")
            return True
        print(f"вњ— РћС€РёР±РєР°: {response}")
        return False

    def blink(self, pin: int, count: int) -> bool:
        """
        РњРѕСЂРіР°РЅРёРµ СЃРІРµС‚РѕРґРёРѕРґРѕРј.

        Args:
            pin: РќРѕРјРµСЂ РїРёРЅР°.
            count: РљРѕР»РёС‡РµСЃС‚РІРѕ РјРѕСЂРіР°РЅРёР№ (5 СЃРµРє РІРєР», 1 СЃРµРє РІС‹РєР»).

        Returns:
            True РµСЃР»Рё СѓСЃРїРµС€РЅРѕ.
        """
        if count <= 0:
            print("РћС€РёР±РєР°: РєРѕР»РёС‡РµСЃС‚РІРѕ РґРѕР»Р¶РЅРѕ Р±С‹С‚СЊ > 0")
            return False

        command = f"BLINK:{pin},{count}"
        print(f"Р—Р°РїСѓСЃРє BLINK: РїРёРЅ {pin}, {count} СЂР°Р·(Р°)...")

        # BLINK РІС‹РїРѕР»РЅСЏРµС‚СЃСЏ РґРѕР»РіРѕ, СѓРІРµР»РёС‡РёРІР°РµРј С‚Р°Р№РјР°СѓС‚
        old_timeout = self.timeout
        self.timeout = max(self.timeout, count * 6 + 5)
        response = self._send_command(command)
        self.timeout = old_timeout

        if response.startswith("OK:BLINK:"):
            print(f"вњ“ BLINK: РїРёРЅ {pin}, {count} СЂР°Р·(Р°) РІС‹РїРѕР»РЅРµРЅРѕ")
            return True
        print(f"вњ— РћС€РёР±РєР°: {response}")
        return False

    def wait(self, ms: int) -> bool:
        """
        РџР°СѓР·Р° РІ РІС‹РїРѕР»РЅРµРЅРёРё.

        Args:
            ms: Р”Р»РёС‚РµР»СЊРЅРѕСЃС‚СЊ РїР°СѓР·С‹ РІ РјРёР»Р»РёСЃРµРєСѓРЅРґР°С….

        Returns:
            True РµСЃР»Рё СѓСЃРїРµС€РЅРѕ.
        """
        if ms < 0:
            print("РћС€РёР±РєР°: РІСЂРµРјСЏ РґРѕР»Р¶РЅРѕ Р±С‹С‚СЊ >= 0")
            return False

        command = f"WAIT:{ms}"
        response = self._send_command(command)

        if response.startswith("OK:WAIT:"):
            print(f"вњ“ WAIT: {ms} РјСЃ")
            return True
        print(f"вњ— РћС€РёР±РєР°: {response}")
        return False

    def execute_script(self, script_path: str):
        """
        Р’С‹РїРѕР»РЅРµРЅРёРµ СЃРєСЂРёРїС‚Р° РёР· С„Р°Р№Р»Р°.

        Args:
            script_path: РџСѓС‚СЊ Рє С„Р°Р№Р»Сѓ СЃРѕ СЃРєСЂРёРїС‚РѕРј.
        """
        try:
            with open(script_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
        except FileNotFoundError:
            print(f"РћС€РёР±РєР°: С„Р°Р№Р» '{script_path}' РЅРµ РЅР°Р№РґРµРЅ")
            return
        except Exception as e:
            print(f"РћС€РёР±РєР° С‡С‚РµРЅРёСЏ С„Р°Р№Р»Р°: {e}")
            return

        print(f"\nР’С‹РїРѕР»РЅРµРЅРёРµ СЃРєСЂРёРїС‚Р°: {script_path}")
        print("=" * 50)

        for line_num, line in enumerate(lines, 1):
            line = line.strip()

            # РџСЂРѕРїСѓСЃРєР°РµРј РєРѕРјРјРµРЅС‚Р°СЂРёРё Рё РїСѓСЃС‚С‹Рµ СЃС‚СЂРѕРєРё
            if not line or line.startswith("//") or line.startswith("/*"):
                continue

            # Р—Р°РєСЂС‹РІР°РµРј РјРЅРѕРіРѕСЃС‚СЂРѕС‡РЅС‹Р№ РєРѕРјРјРµРЅС‚Р°СЂРёР№
            if line.startswith("*/"):
                continue

            print(f"[{line_num}] {line}")

            # РџР°СЂСЃРёРЅРі РєРѕРјР°РЅРґС‹
            parts = line.split(":")
            cmd = parts[0].upper()
            params = parts[1] if len(parts) > 1 else ""

            success = False

            if cmd == "PINMODE":
                pin, mode = params.split(",")
                success = self.pinmode(int(pin), mode.strip())

            elif cmd == "DWRITE":
                pin, value = params.split(",")
                success = self.dwrite(int(pin), value.strip())

            elif cmd == "BLINK":
                pin, count = params.split(",")
                success = self.blink(int(pin), int(count.strip()))

            elif cmd == "WAIT":
                success = self.wait(int(params))

            elif cmd == "PING":
                success = self.ping()

            else:
                print(f"  вљ  РќРµРёР·РІРµСЃС‚РЅР°СЏ РєРѕРјР°РЅРґР°: {cmd}")
                continue

            if not success:
                print(f"  вњ— РљРѕРјР°РЅРґР° РЅРµ РІС‹РїРѕР»РЅРµРЅР°!")

        print("=" * 50)
        print("РЎРєСЂРёРїС‚ Р·Р°РІРµСЂС€С‘РЅ")


def main():
    """РўРѕС‡РєР° РІС…РѕРґР°."""
    import argparse

    parser = argparse.ArgumentParser(
        description="Arduino Controller РґР»СЏ JARVIS",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
РџСЂРёРјРµСЂС‹ РёСЃРїРѕР»СЊР·РѕРІР°РЅРёСЏ:
  %(prog)s --list                    - РџРѕРєР°Р·Р°С‚СЊ РґРѕСЃС‚СѓРїРЅС‹Рµ РїРѕСЂС‚С‹
  %(prog)s -p COM3 ping              - РџСЂРѕРІРµСЂРєР° СЃРІСЏР·Рё
  %(prog)s -p COM3 pinmode 13 OUTPUT - РЈСЃС‚Р°РЅРѕРІРєР° СЂРµР¶РёРјР° РїРёРЅР°
  %(prog)s -p COM3 dwrite 13 HIGH    - Р’РєР»СЋС‡РёС‚СЊ РїРёРЅ
  %(prog)s -p COM3 blink 13 3        - РњРѕСЂРіР°РЅРёРµ 3 СЂР°Р·Р°
  %(prog)s -p COM3 wait 1000         - РџР°СѓР·Р° 1 СЃРµРєСѓРЅРґР°
  %(prog)s -p COM3 --script script.txt - Р’С‹РїРѕР»РЅРµРЅРёРµ СЃРєСЂРёРїС‚Р°
        """
    )

    parser.add_argument("-p", "--port", help="COM-РїРѕСЂС‚ (РЅР°РїСЂРёРјРµСЂ, COM3)")
    parser.add_argument("-b", "--baudrate", type=int, default=9600,
                        help="РЎРєРѕСЂРѕСЃС‚СЊ РїРµСЂРµРґР°С‡Рё (РїРѕ СѓРјРѕР»С‡Р°РЅРёСЋ 9600)")
    parser.add_argument("-t", "--timeout", type=float, default=1.0,
                        help="РўР°Р№РјР°СѓС‚ С‡С‚РµРЅРёСЏ РІ СЃРµРєСѓРЅРґР°С…")
    parser.add_argument("--list", action="store_true",
                        help="РџРѕРєР°Р·Р°С‚СЊ СЃРїРёСЃРѕРє РґРѕСЃС‚СѓРїРЅС‹С… РїРѕСЂС‚РѕРІ")
    parser.add_argument("command", nargs="?",
                        choices=["ping", "pinmode", "dwrite", "blink", "wait"],
                        help="РљРѕРјР°РЅРґР° РґР»СЏ РІС‹РїРѕР»РЅРµРЅРёСЏ")
    parser.add_argument("args", nargs="*", help="РђСЂРіСѓРјРµРЅС‚С‹ РєРѕРјР°РЅРґС‹")
    parser.add_argument("--script", help="РџСѓС‚СЊ Рє С„Р°Р№Р»Сѓ СЃРѕ СЃРєСЂРёРїС‚РѕРј")

    args = parser.parse_args()

    # РЎРїРёСЃРѕРє РїРѕСЂС‚РѕРІ
    if args.list:
        ports = ArduinoController().list_ports()
        if not ports:
            print("Р”РѕСЃС‚СѓРїРЅС‹Рµ РїРѕСЂС‚С‹ РЅРµ РЅР°Р№РґРµРЅС‹")
        else:
            print("Р”РѕСЃС‚СѓРїРЅС‹Рµ COM-РїРѕСЂС‚С‹:")
            for port in ports:
                print(f"  {port['device']}: {port['description']}")
        return

    # РџСЂРѕРІРµСЂРєР° РЅР°Р»РёС‡РёСЏ РєРѕРјР°РЅРґС‹
    if not args.command and not args.script:
        parser.print_help()
        return

    # РЎРѕР·РґР°РЅРёРµ РєРѕРЅС‚СЂРѕР»Р»РµСЂР°
    controller = ArduinoController(
        port=args.port,
        baudrate=args.baudrate,
        timeout=args.timeout
    )

    # РџРѕРґРєР»СЋС‡РµРЅРёРµ
    if not controller.connect():
        sys.exit(1)

    try:
        # Р’С‹РїРѕР»РЅРµРЅРёРµ СЃРєСЂРёРїС‚Р°
        if args.script:
            controller.execute_script(args.script)
            return

        # Р’С‹РїРѕР»РЅРµРЅРёРµ РєРѕРјР°РЅРґС‹
        if args.command == "ping":
            controller.ping()

        elif args.command == "pinmode":
            if len(args.args) < 2:
                print("РћС€РёР±РєР°: pinmode С‚СЂРµР±СѓРµС‚ 2 Р°СЂРіСѓРјРµРЅС‚Р° (pin, mode)")
                sys.exit(1)
            controller.pinmode(int(args.args[0]), args.args[1])

        elif args.command == "dwrite":
            if len(args.args) < 2:
                print("РћС€РёР±РєР°: dwrite С‚СЂРµР±СѓРµС‚ 2 Р°СЂРіСѓРјРµРЅС‚Р° (pin, value)")
                sys.exit(1)
            controller.dwrite(int(args.args[0]), args.args[1])

        elif args.command == "blink":
            if len(args.args) < 2:
                print("РћС€РёР±РєР°: blink С‚СЂРµР±СѓРµС‚ 2 Р°СЂРіСѓРјРµРЅС‚Р° (pin, count)")
                sys.exit(1)
            controller.blink(int(args.args[0]), int(args.args[1]))

        elif args.command == "wait":
            if len(args.args) < 1:
                print("РћС€РёР±РєР°: wait С‚СЂРµР±СѓРµС‚ 1 Р°СЂРіСѓРјРµРЅС‚ (ms)")
                sys.exit(1)
            controller.wait(int(args.args[0]))

    finally:
        controller.disconnect()


if __name__ == "__main__":
    main()

