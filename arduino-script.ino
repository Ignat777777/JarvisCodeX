/*
 * Arduino Script РґР»СЏ JARVIS
 * Р’РµСЂСЃРёСЏ: 2.0 (Multi-Channel)
 *
 * РЈРїСЂРѕС‰С‘РЅРЅС‹Р№ СЏР·С‹Рє РєРѕРјР°РЅРґ РґР»СЏ СѓРїСЂР°РІР»РµРЅРёСЏ Arduino Uno
 * РџРѕРґРґРµСЂР¶РєР° 3-4 РЅРµР·Р°РІРёСЃРёРјС‹С… РєР°РЅР°Р»РѕРІ LED
 *
 * РџРѕРґРґРµСЂР¶РёРІР°РµРјС‹Рµ РєРѕРјР°РЅРґС‹:
 *   PINMODE:<pin>,<mode>          - РЈСЃС‚Р°РЅРѕРІРєР° СЂРµР¶РёРјР° РїРёРЅР° (INPUT/OUTPUT/INPUT_PULLUP)
 *   DWRITE:<pin>,<value>          - Р¦РёС„СЂРѕРІРѕР№ РІС‹РІРѕРґ (HIGH/LOW)
 *   AWRITE:<pin>,<value>          - РђРЅР°Р»РѕРіРѕРІС‹Р№ РІС‹РІРѕРґ PWM (0-255)
 *   SERVO:<pin>,<angle>           - РЎРµСЂРІРѕРїСЂРёРІРѕРґ (0-180 РіСЂР°РґСѓСЃРѕРІ)
 *   DREAD:<pin>                   - Р¦РёС„СЂРѕРІРѕРµ С‡С‚РµРЅРёРµ
 *   AREAD:<pin>                   - РђРЅР°Р»РѕРіРѕРІРѕРµ С‡С‚РµРЅРёРµ
 *   BLINK:<pin>,<count>           - РњРѕСЂРіР°РЅРёРµ: pin, count (5 РјСЃ РІРєР», 1 РјСЃ РІС‹РєР»)
 *   BLINK:<pin>,<count>,<on>,<off>- РњРѕСЂРіР°РЅРёРµ СЃ РєР°СЃС‚РѕРјРЅС‹РјРё РёРЅС‚РµСЂРІР°Р»Р°РјРё (РјСЃ)
 *   WAIT:<ms>                     - РџР°СѓР·Р° РІ РјРёР»Р»РёСЃРµРєСѓРЅРґР°С…
 *   PING                          - РџСЂРѕРІРµСЂРєР° СЃРІСЏР·Рё
 *
 * РџСЂРёРјРµСЂС‹:
 *   PINMODE:13,OUTPUT
 *   DWRITE:13,HIGH
 *   AWRITE:9,127
 *   SERVO:10,90
 *   DREAD:2
 *   AREAD:A0
 *   BLINK:13,3              - 3 РјРѕСЂРіР°РЅРёСЏ (5РјСЃ РІРєР»/1РјСЃ РІС‹РєР»)
 *   BLINK:12,5,500,500      - 5 РјРѕСЂРіР°РЅРёР№ (500РјСЃ РІРєР»/500РјСЃ РІС‹РєР»)
 *   WAIT:1000
 *   PING
 *
 * РљР°РЅР°Р»С‹ JARVIS (СЂРµРєРѕРјРµРЅРґСѓРµРјС‹Рµ РїРёРЅС‹):
 *   РљР°РЅР°Р» 1: LED13 (РІСЃС‚СЂРѕРµРЅРЅС‹Р№)
 *   РљР°РЅР°Р» 2: LED12
 *   РљР°РЅР°Р» 3: LED11
 *   РљР°РЅР°Р» 4: LED10
 */

#include <Servo.h>

// === Р“Р»РѕР±Р°Р»СЊРЅС‹Рµ РѕР±СЉРµРєС‚С‹ ===
Servo servos[6];  // РџРѕРґРґРµСЂР¶РєР° РґРѕ 6 СЃРµСЂРІРѕРїСЂРёРІРѕРґРѕРІ
bool servoAttached[6] = {false, false, false, false, false, false};

// === РљРѕРЅСЃС‚Р°РЅС‚С‹ ===
const int MAX_SERVOS = 6;
const int BUFFER_SIZE = 64;

// === Р‘СѓС„РµСЂ РєРѕРјР°РЅРґ ===
char cmdBuffer[BUFFER_SIZE];
int cmdIndex = 0;

void setup() {
  Serial.begin(9600);
  while (!Serial) {
    ; // Р–РґС‘Рј РїРѕРґРєР»СЋС‡РµРЅРёСЏ Serial
  }
  
  Serial.println("ARDUINO_SCRIPT_READY");
  Serial.println("VERSION:1.0");
  Serial.println("COMMANDS:PINMODE,DWRITE,AWRITE,SERVO,DREAD,AREAD,BLINK,WAIT,PING");
}

void loop() {
  // РћР±СЂР°Р±РѕС‚РєР° РІС…РѕРґСЏС‰РёС… РґР°РЅРЅС‹С…
  while (Serial.available() > 0) {
    char inChar = (char)Serial.read();
    
    if (inChar == '\n' || inChar == '\r') {
      if (cmdIndex > 0) {
        cmdBuffer[cmdIndex] = '\0';
        executeCommand(cmdBuffer);
        cmdIndex = 0;
      }
    } else {
      if (cmdIndex < BUFFER_SIZE - 1) {
        cmdBuffer[cmdIndex++] = inChar;
      } else {
        // РџРµСЂРµРїРѕР»РЅРµРЅРёРµ Р±СѓС„РµСЂР°
        cmdIndex = 0;
        Serial.println("ERROR:BUFFER_OVERFLOW");
      }
    }
  }
}

// ============================================================================
// РћР‘Р РђР‘РћРўРљРђ РљРћРњРђРќР”
// ============================================================================

void executeCommand(char* cmd) {
  // РџСЂРёРІРѕРґРёРј Рє РІРµСЂС…РЅРµРјСѓ СЂРµРіРёСЃС‚СЂСѓ РґР»СЏ СЃСЂР°РІРЅРµРЅРёСЏ
  char cmdUpper[BUFFER_SIZE];
  strcpy(cmdUpper, cmd);
  toUpperCase(cmdUpper);
  
  // РЈРґР°Р»СЏРµРј РїСЂРѕР±РµР»С‹
  removeSpaces(cmdUpper);
  
  // РџР°СЂСЃРёРЅРі РєРѕРјР°РЅРґС‹
  char* command = strtok(cmdUpper, ":");
  char* params = strtok(NULL, "");
  
  if (command == NULL || strlen(command) == 0) {
    Serial.println("ERROR:EMPTY_COMMAND");
    return;
  }
  
  // === PINMODE:pin,mode ===
  if (strcmp(command, "PINMODE") == 0) {
    handlePinMode(params);
  }
  // === DWRITE:pin,value ===
  else if (strcmp(command, "DWRITE") == 0) {
    handleDigitalWrite(params);
  }
  // === AWRITE:pin,value ===
  else if (strcmp(command, "AWRITE") == 0) {
    handleAnalogWrite(params);
  }
  // === SERVO:pin,angle ===
  else if (strcmp(command, "SERVO") == 0) {
    handleServo(params);
  }
  // === DREAD:pin ===
  else if (strcmp(command, "DREAD") == 0) {
    handleDigitalRead(params);
  }
  // === AREAD:pin ===
  else if (strcmp(command, "AREAD") == 0) {
    handleAnalogRead(params);
  }
  // === BLINK:pin,count[,onTime,offTime] ===
  else if (strcmp(command, "BLINK") == 0) {
    handleBlink(params);
  }
  // === WAIT:ms ===
  else if (strcmp(command, "WAIT") == 0) {
    handleWait(params);
  }
  // === PING ===
  else if (strcmp(command, "PING") == 0) {
    Serial.println("PONG");
  }
  // === РќРµРёР·РІРµСЃС‚РЅР°СЏ РєРѕРјР°РЅРґР° ===
  else {
    Serial.print("ERROR:UNKNOWN_COMMAND:");
    Serial.println(command);
  }
}

// ============================================================================
// РћР‘Р РђР‘РћРўР§РРљР РљРћРњРђРќР”
// ============================================================================

void handlePinMode(char* params) {
  if (params == NULL) {
    Serial.println("ERROR:PINMODE_MISSING_PARAMS");
    return;
  }
  
  int pin = parseInt(params);
  char* modeStr = strchr(params, ',');
  
  if (modeStr == NULL) {
    Serial.println("ERROR:PINMODE_MISSING_MODE");
    return;
  }
  
  modeStr++; // РџСЂРѕРїСѓСЃРєР°РµРј Р·Р°РїСЏС‚СѓСЋ
  
  if (strcmp(modeStr, "OUTPUT") == 0) {
    pinMode(pin, OUTPUT);
    Serial.print("OK:PINMODE:");
    Serial.print(pin);
    Serial.println(",OUTPUT");
  } else if (strcmp(modeStr, "INPUT") == 0) {
    pinMode(pin, INPUT);
    Serial.print("OK:PINMODE:");
    Serial.print(pin);
    Serial.println(",INPUT");
  } else if (strcmp(modeStr, "INPUT_PULLUP") == 0) {
    pinMode(pin, INPUT_PULLUP);
    Serial.print("OK:PINMODE:");
    Serial.print(pin);
    Serial.println(",INPUT_PULLUP");
  } else {
    Serial.println("ERROR:PINMODE_INVALID_MODE");
  }
}

void handleDigitalWrite(char* params) {
  if (params == NULL) {
    Serial.println("ERROR:DWRITE_MISSING_PARAMS");
    return;
  }
  
  int pin = parseInt(params);
  char* valueStr = strchr(params, ',');
  
  if (valueStr == NULL) {
    Serial.println("ERROR:DWRITE_MISSING_VALUE");
    return;
  }
  
  valueStr++; // РџСЂРѕРїСѓСЃРєР°РµРј Р·Р°РїСЏС‚СѓСЋ
  
  if (strcmp(valueStr, "HIGH") == 0 || strcmp(valueStr, "1") == 0) {
    digitalWrite(pin, HIGH);
    Serial.print("OK:DWRITE:");
    Serial.print(pin);
    Serial.println(",HIGH");
  } else if (strcmp(valueStr, "LOW") == 0 || strcmp(valueStr, "0") == 0) {
    digitalWrite(pin, LOW);
    Serial.print("OK:DWRITE:");
    Serial.print(pin);
    Serial.println(",LOW");
  } else {
    Serial.println("ERROR:DWRITE_INVALID_VALUE");
  }
}

void handleAnalogWrite(char* params) {
  if (params == NULL) {
    Serial.println("ERROR:AWRITE_MISSING_PARAMS");
    return;
  }
  
  int pin = parseInt(params);
  char* valueStr = strchr(params, ',');
  
  if (valueStr == NULL) {
    Serial.println("ERROR:AWRITE_MISSING_VALUE");
    return;
  }
  
  valueStr++; // РџСЂРѕРїСѓСЃРєР°РµРј Р·Р°РїСЏС‚СѓСЋ
  int value = atoi(valueStr);
  
  if (value < 0 || value > 255) {
    Serial.println("ERROR:AWRITE_INVALID_VALUE");
    return;
  }
  
  analogWrite(pin, value);
  Serial.print("OK:AWRITE:");
  Serial.print(pin);
  Serial.print(",");
  Serial.println(value);
}

void handleServo(char* params) {
  if (params == NULL) {
    Serial.println("ERROR:SERVO_MISSING_PARAMS");
    return;
  }
  
  int pin = parseInt(params);
  char* angleStr = strchr(params, ',');
  
  if (angleStr == NULL) {
    Serial.println("ERROR:SERVO_MISSING_ANGLE");
    return;
  }
  
  angleStr++; // РџСЂРѕРїСѓСЃРєР°РµРј Р·Р°РїСЏС‚СѓСЋ
  int angle = atoi(angleStr);
  
  if (angle < 0 || angle > 180) {
    Serial.println("ERROR:SERVO_INVALID_ANGLE");
    return;
  }
  
  // РС‰РµРј СЃРІРѕР±РѕРґРЅС‹Р№ СЃР»РѕС‚ РёР»Рё РёСЃРїРѕР»СЊР·СѓРµРј СЃСѓС‰РµСЃС‚РІСѓСЋС‰РёР№
  int servoIndex = -1;
  for (int i = 0; i < MAX_SERVOS; i++) {
    // РџСЂРѕРІРµСЂСЏРµРј, РµСЃС‚СЊ Р»Рё СѓР¶Рµ СЃРµСЂРІРѕ РЅР° СЌС‚РѕРј РїРёРЅРµ
    if (servoAttached[i]) {
      // РЈРїСЂРѕС‰С‘РЅРЅР°СЏ РїСЂРѕРІРµСЂРєР° - РІ СЂРµР°Р»СЊРЅРѕРј РїСЂРѕРµРєС‚Рµ РЅСѓР¶РЅРѕ С…СЂР°РЅРёС‚СЊ РїСЂРёРІСЏР·РєСѓ РїРёРЅРѕРІ
      servoIndex = i;
      break;
    } else if (servoIndex == -1) {
      servoIndex = i;
    }
  }
  
  if (servoIndex == -1) {
    Serial.println("ERROR:SERVO_NO_FREE_SLOT");
    return;
  }
  
  // РџСЂРёРєСЂРµРїР»СЏРµРј СЃРµСЂРІРѕ РµСЃР»Рё РµС‰С‘ РЅРµ РїСЂРёРєСЂРµРїР»РµРЅРѕ
  if (!servoAttached[servoIndex]) {
    servos[servoIndex].attach(pin);
    servoAttached[servoIndex] = true;
  }
  
  servos[servoIndex].write(angle);
  Serial.print("OK:SERVO:");
  Serial.print(pin);
  Serial.print(",");
  Serial.println(angle);
}

void handleDigitalRead(char* params) {
  if (params == NULL) {
    Serial.println("ERROR:DREAD_MISSING_PIN");
    return;
  }
  
  int pin = parsePin(params);
  
  if (pin < 0) {
    Serial.println("ERROR:DREAD_INVALID_PIN");
    return;
  }
  
  int value = digitalRead(pin);
  Serial.print("OK:DREAD:");
  Serial.print(pin);
  Serial.print(",");
  Serial.println(value ? "HIGH" : "LOW");
}

void handleAnalogRead(char* params) {
  if (params == NULL) {
    Serial.println("ERROR:AREAD_MISSING_PIN");
    return;
  }
  
  int pin = parsePin(params);
  
  if (pin < 0) {
    Serial.println("ERROR:AREAD_INVALID_PIN");
    return;
  }
  
  int value = analogRead(pin);
  Serial.print("OK:AREAD:");
  Serial.print(pin);
  Serial.print(",");
  Serial.println(value);
}

void handleBlink(char* params) {
  if (params == NULL) {
    Serial.println("ERROR:BLINK_MISSING_PARAMS");
    return;
  }

  int pin = parseInt(params);

  // РџР°СЂСЃРёРј count
  char* countStr = strchr(params, ',');
  if (countStr == NULL) {
    Serial.println("ERROR:BLINK_MISSING_COUNT");
    return;
  }
  countStr++;
  int count = atoi(countStr);

  if (count <= 0) {
    Serial.println("ERROR:BLINK_INVALID_PARAMS");
    return;
  }

  // РџР°СЂСЃРёРј onTime Рё offTime (РѕРїС†РёРѕРЅР°Р»СЊРЅРѕ)
  int onTime = 5;   // РџРѕ СѓРјРѕР»С‡Р°РЅРёСЋ 5 РјСЃ
  int offTime = 1;  // РџРѕ СѓРјРѕР»С‡Р°РЅРёСЋ 1 РјСЃ

  char* onTimeStr = strchr(countStr, ',');
  if (onTimeStr != NULL) {
    onTimeStr++;
    onTime = atoi(onTimeStr);
    
    char* offTimeStr = strchr(onTimeStr, ',');
    if (offTimeStr != NULL) {
      offTimeStr++;
      offTime = atoi(offTimeStr);
    }
  }

  // РЈСЃС‚Р°РЅР°РІР»РёРІР°РµРј РїРёРЅ РІ OUTPUT РµСЃР»Рё РЅСѓР¶РЅРѕ
  pinMode(pin, OUTPUT);

  // Р’С‹РїРѕР»РЅСЏРµРј РјРѕСЂРіР°РЅРёСЏ
  for (int i = 0; i < count; i++) {
    digitalWrite(pin, HIGH);
    delay(onTime);
    digitalWrite(pin, LOW);
    if (i < count - 1) {
      delay(offTime);
    }
  }

  Serial.print("OK:BLINK:");
  Serial.print(pin);
  Serial.print(",");
  Serial.print(count);
  Serial.print(",");
  Serial.print(onTime);
  Serial.print("/");
  Serial.println(offTime);
}

void handleWait(char* params) {
  if (params == NULL) {
    Serial.println("ERROR:WAIT_MISSING_MS");
    return;
  }
  
  int ms = atoi(params);
  
  if (ms < 0) {
    Serial.println("ERROR:WAIT_INVALID_MS");
    return;
  }
  
  delay(ms);
  Serial.print("OK:WAIT:");
  Serial.print(ms);
  Serial.println("ms");
}

// ============================================================================
// Р’РЎРџРћРњРћР“РђРўР•Р›Р¬РќР«Р• Р¤РЈРќРљР¦РР
// ============================================================================

int parseInt(char* str) {
  if (str == NULL) return -1;
  return atoi(str);
}

int parsePin(char* str) {
  if (str == NULL) return -1;
  
  // РџРѕРґРґРµСЂР¶РєР° С„РѕСЂРјР°С‚Р° A0, A1, Рё С‚.Рґ.
  if (str[0] == 'A' || str[0] == 'a') {
    int pinNum = atoi(str + 1);
    if (pinNum >= 0 && pinNum <= 5) {
      return A0 + pinNum;
    }
    return -1;
  }
  
  return atoi(str);
}

void toUpperCase(char* str) {
  if (str == NULL) return;
  for (int i = 0; str[i] != '\0'; i++) {
    if (str[i] >= 'a' && str[i] <= 'z') {
      str[i] = str[i] - 'a' + 'A';
    }
  }
}

void removeSpaces(char* str) {
  if (str == NULL) return;
  
  int writeIndex = 0;
  for (int readIndex = 0; str[readIndex] != '\0'; readIndex++) {
    if (str[readIndex] != ' ') {
      str[writeIndex++] = str[readIndex];
    }
  }
  str[writeIndex] = '\0';
}

/*
 * ============================================================================
 * РџР РРњР•Р Р« РРЎРџРћР›Р¬Р—РћР’РђРќРРЇ:
 * ============================================================================
 *
 * 1. РРЅРёС†РёР°Р»РёР·Р°С†РёСЏ Рё РІРєР»СЋС‡РµРЅРёРµ СЃРІРµС‚РѕРґРёРѕРґР°:
 *    PINMODE:13,OUTPUT
 *    DWRITE:13,HIGH
 *
 * 2. РџР»Р°РІРЅРѕРµ РёР·РјРµРЅРµРЅРёРµ СЏСЂРєРѕСЃС‚Рё (PWM):
 *    AWRITE:9,0
 *    WAIT:500
 *    AWRITE:9,127
 *    WAIT:500
 *    AWRITE:9,255
 *
 * 3. РЈРїСЂР°РІР»РµРЅРёРµ СЃРµСЂРІРѕРїСЂРёРІРѕРґРѕРј:
 *    SERVO:10,0
 *    WAIT:1000
 *    SERVO:10,90
 *    WAIT:1000
 *    SERVO:10,180
 *
 * 4. Р§С‚РµРЅРёРµ РґР°С‚С‡РёРєРѕРІ:
 *    DREAD:2
 *    AREAD:A0
 *
 * 5. РњРѕСЂРіР°РЅРёРµ СЃРІРµС‚РѕРґРёРѕРґРѕРј (5 РјСЃ РІРєР», 1 РјСЃ РІС‹РєР»):
 *    BLINK:13,3
 *
 * 6. РњРѕСЂРіР°РЅРёРµ СЃ РєР°СЃС‚РѕРјРЅС‹РјРё РёРЅС‚РµСЂРІР°Р»Р°РјРё:
 *    BLINK:12,5,500,500    - 5 РјРѕСЂРіР°РЅРёР№, 500РјСЃ РІРєР»/500РјСЃ РІС‹РєР»
 *    BLINK:11,4,200,100    - 4 РјРѕСЂРіР°РЅРёСЏ, 200РјСЃ РІРєР»/100РјСЃ РІС‹РєР»
 *
 * 7. РњСѓР»СЊС‚Рё-РєР°РЅР°Р» JARVIS (3-4 РєР°РЅР°Р»Р°):
 *    PINMODE:13,OUTPUT
 *    PINMODE:12,OUTPUT
 *    PINMODE:11,OUTPUT
 *    PINMODE:10,OUTPUT
 *    BLINK:13,2            - РљР°РЅР°Р» 1: 2 РјРѕСЂРіР°РЅРёСЏ
 *    BLINK:12,2            - РљР°РЅР°Р» 2: 2 РјРѕСЂРіР°РЅРёСЏ
 *    BLINK:11,2            - РљР°РЅР°Р» 3: 2 РјРѕСЂРіР°РЅРёСЏ
 *    BLINK:10,2            - РљР°РЅР°Р» 4: 2 РјРѕСЂРіР°РЅРёСЏ
 *
 * 8. РџСЂРѕРІРµСЂРєР° СЃРІСЏР·Рё:
 *    PING
 *    РћС‚РІРµС‚: PONG
 *
 * 9. РџР°СѓР·Р° РІ РІС‹РїРѕР»РЅРµРЅРёРё:
 *    WAIT:1000
 *
 * ============================================================================
 */

