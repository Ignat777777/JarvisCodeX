/*
 * jarvis Arduino Uno Firmware
 * Версия: 1.0
 * 
 * Поддерживаемые компоненты:
 * - Светодиод (пин 13)
 * - PWM светодиод (пин 9)
 * - Сервопривод (пин 10)
 * - Мотор (пины 5, 6)
 * - Зуммер (пин 8)
 * - Датчик температуры (пин A0)
 * - Фоторезистор (пин A1)
 * - Ультразвуковой датчик HC-SR04 (пины 2, 3)
 */

#include <Servo.h>

// === Константы пинов ===
const int PIN_LED_BUILTIN = 13;
const int PIN_LED_PWM = 9;
const int PIN_SERVO = 9;
const int PIN_MOTOR_FWD = 5;
const int PIN_MOTOR_REV = 6;
const int PIN_BUZZER = 8;
const int PIN_TEMP_SENSOR = A0;
const int PIN_LIGHT_SENSOR = A1;
const int PIN_TRIG = 2;
const int PIN_ECHO = 3;

// === Глобальные объекты ===
Servo servoMotor;

// === Состояния ===
bool ledState = LOW;
bool motorState = LOW;
int servoAngle = 90;

// === Тайминги для ультразвука ===
const int SOUND_SPEED = 348; // м/с при 25°C

void setup() {
  // Инициализация последовательного порта
  Serial.begin(9600);
  while (!Serial) {
    ; // Ждём подключения Serial (для Leonardo/Pro Micro)
  }
  
  // Инициализация цифровых пинов
  pinMode(PIN_LED_BUILTIN, OUTPUT);
  pinMode(PIN_LED_PWM, OUTPUT);
  pinMode(PIN_MOTOR_FWD, OUTPUT);
  pinMode(PIN_MOTOR_REV, OUTPUT);
  pinMode(PIN_BUZZER, OUTPUT);
  pinMode(PIN_TRIG, OUTPUT);
  pinMode(PIN_ECHO, INPUT);
  
  // Аналоговые пины не требуют pinMode в Arduino Uno
  
  // Инициализация состояний
  digitalWrite(PIN_LED_BUILTIN, LOW);
  digitalWrite(PIN_LED_PWM, LOW);
  digitalWrite(PIN_MOTOR_FWD, LOW);
  digitalWrite(PIN_MOTOR_REV, LOW);
  noTone(PIN_BUZZER);
  
  // Инициализация сервопривода
  servoMotor.attach(PIN_SERVO);
  servoMotor.write(90);
  
  // Приветственное сообщение
  Serial.println("jarvis_ARDUINO_READY");
  Serial.println("INIT_COMPLETE");
}

void loop() {
  // Обработка входящих команд
  if (Serial.available() > 0) {
    handleCommand();
  }
}

// ============================================================================
// ОБРАБОТКА КОМАНД
// ============================================================================

void handleCommand() {
  static String commandBuffer = "";
  
  while (Serial.available() > 0) {
    char inChar = (char)Serial.read();
    
    if (inChar == '\n') {
      // Конец команды
      commandBuffer.trim();
      if (commandBuffer.length() > 0) {
        executeCommand(commandBuffer);
      }
      commandBuffer = "";
    } else {
      commandBuffer += inChar;
    }
  }
}

void executeCommand(String cmd) {
  // Парсинг команды в формате: COMMAND:PARAM1=VAL1;PARAM2=VAL2
  
  int colonIndex = cmd.indexOf(':');
  String command = (colonIndex >= 0) ? cmd.substring(0, colonIndex) : cmd;
  String params = (colonIndex >= 0) ? cmd.substring(colonIndex + 1) : "";
  
  command.toUpperCase();
  
  // === ЦИФРОВОЙ ВЫВОД ===
  if (command == "DIGITAL_WRITE" || command == "DW") {
    int pin = getParamInt(params, "PIN", -1);
    String value = getParam(params, "VALUE", "");
    
    if (pin >= 0) {
      if (value == "HIGH" || value == "1" || value == "TRUE") {
        digitalWrite(pin, HIGH);
        if (pin == PIN_LED_BUILTIN) ledState = HIGH;
        Serial.println("OK:DIGITAL_WRITE:" + String(pin) + ":HIGH");
      } else if (value == "LOW" || value == "0" || value == "FALSE") {
        digitalWrite(pin, LOW);
        if (pin == PIN_LED_BUILTIN) ledState = LOW;
        Serial.println("OK:DIGITAL_WRITE:" + String(pin) + ":LOW");
      }
    } else {
      Serial.println("ERROR:INVALID_PIN");
    }
  }
  
  // === АНАЛОГОВЫЙ ВЫВОД (PWM) ===
  else if (command == "ANALOG_WRITE" || command == "AW" || command == "PWM") {
    int pin = getParamInt(params, "PIN", -1);
    int value = getParamInt(params, "VALUE", 0);
    
    if (pin >= 0 && value >= 0 && value <= 255) {
      analogWrite(pin, constrain(value, 0, 255));
      Serial.println("OK:ANALOG_WRITE:" + String(pin) + ":" + String(value));
    } else {
      Serial.println("ERROR:INVALID_VALUE");
    }
  }
  
  // === АНАЛОГОВОЕ ЧТЕНИЕ ===
  else if (command == "ANALOG_READ" || command == "AR") {
    String pinStr = getParam(params, "PIN", "");
    int pin = -1;
    
    // Поддержка формата A0, A1, и т.д.
    if (pinStr.startsWith("A")) {
      pin = pinStr.substring(1).toInt();
      if (pin >= 0 && pin <= 5) {
        pin = A0 + pin;
      }
    } else {
      pin = pinStr.toInt();
    }
    
    if (pin >= A0 && pin <= A5) {
      int value = analogRead(pin);
      Serial.println("OK:ANALOG_READ:" + String(pin) + ":" + String(value));
      
      // Конвертация для температуры (примерная, зависит от датчика)
      if (pin == PIN_TEMP_SENSOR) {
        float voltage = value * (5.0 / 1023.0);
        float tempC = (voltage - 0.5) * 100.0; // Для TMP36
        Serial.println("DATA:TEMP_C:" + String(tempC, 2));
      }
      
      // Конвертация для освещённости
      if (pin == PIN_LIGHT_SENSOR) {
        float voltage = value * (5.0 / 1023.0);
        float jarvis = 500.0 / ((10000.0 * (5.0 / voltage - 1.0)) / 1000.0); // Примерная формула
        Serial.println("DATA:jarvis:" + String(jarvis, 2));
      }
    } else {
      Serial.println("ERROR:INVALID_ANALOG_PIN");
    }
  }
  
  // === СЕРВОПРИВОД ===
  else if (command == "SERVO_WRITE" || command == "SW") {
    int pin = getParamInt(params, "PIN", -1);
    int angle = getParamInt(params, "ANGLE", 90);
    
    if (pin == PIN_SERVO && angle >= 0 && angle <= 180) {
      servoMotor.write(constrain(angle, 0, 180));
      servoAngle = angle;
      Serial.println("OK:SERVO_WRITE:" + String(angle));
    } else {
      Serial.println("ERROR:INVALID_SERVO_PARAMS");
    }
  }
  
  // === СЕРВОПРИВОД - ЧТЕНИЕ ПОЛОЖЕНИЯ ===
  else if (command == "SERVO_READ" || command == "SR") {
    Serial.println("OK:SERVO_READ:" + String(servoAngle));
  }
  
  // === УЛЬТРАЗВУКОВОЙ ДАТЧИК ===
  else if (command == "ULTRASONIC_READ" || command == "UR" || command == "DISTANCE") {
    int trigPin = getParamInt(params, "TRIG", PIN_TRIG);
    int echoPin = getParamInt(params, "ECHO", PIN_ECHO);
    
    if (trigPin >= 0 && echoPin >= 0) {
      long distance = readDistance(trigPin, echoPin);
      Serial.println("OK:ULTRASONIC_READ:" + String(distance));
      Serial.println("DATA:DISTANCE_CM:" + String(distance));
    } else {
      Serial.println("ERROR:INVALID_ULTRASONIC_PINS");
    }
  }
  
  // === ЗВУК (TONE) ===
  else if (command == "TONE_PLAY" || command == "TP") {
    int pin = getParamInt(params, "PIN", PIN_BUZZER);
    int frequency = getParamInt(params, "FREQUENCY", 1000);
    int duration = getParamInt(params, "DURATION", 500);
    
    if (pin >= 0 && frequency > 0 && duration > 0) {
      tone(pin, frequency, duration);
      Serial.println("OK:TONE_PLAY:" + String(frequency) + "Hz:" + String(duration) + "ms");
    } else {
      Serial.println("ERROR:INVALID_TONE_PARAMS");
    }
  }
  
  // === СТОП ЗВУКА ===
  else if (command == "TONE_STOP" || command == "TS") {
    int pin = getParamInt(params, "PIN", PIN_BUZZER);
    noTone(pin);
    Serial.println("OK:TONE_STOP:" + String(pin));
  }
  
  // === ПАУЗА ===
  else if (command == "PAUSE" || command == "DELAY" || command == "WAIT") {
    int ms = getParamInt(params, "MS", 1000);
    delay(ms);
    Serial.println("OK:PAUSE:" + String(ms) + "ms");
  }
  
  // === МОТОР ВПЕРЁД ===
  else if (command == "MOTOR_FWD" || command == "MF") {
    digitalWrite(PIN_MOTOR_FWD, HIGH);
    digitalWrite(PIN_MOTOR_REV, LOW);
    motorState = HIGH;
    Serial.println("OK:MOTOR_FWD");
  }
  
  // === МОТОР НАЗАД (РЕВЕРС) ===
  else if (command == "MOTOR_REV" || command == "MR") {
    digitalWrite(PIN_MOTOR_REV, HIGH);
    digitalWrite(PIN_MOTOR_FWD, LOW);
    motorState = HIGH;
    Serial.println("OK:MOTOR_REV");
  }
  
  // === МОТОР СТОП ===
  else if (command == "MOTOR_STOP" || command == "MS") {
    digitalWrite(PIN_MOTOR_FWD, LOW);
    digitalWrite(PIN_MOTOR_REV, LOW);
    motorState = LOW;
    Serial.println("OK:MOTOR_STOP");
  }
  
  // === СЧИТАТЬ ВСЕ ДАТЧИКИ ===
  else if (command == "READ_ALL_SENSORS" || command == "RAS") {
    readAllSensors();
  }
  
  // === СТАТУС ===
  else if (command == "STATUS" || command == "STAT") {
    reportStatus();
  }
  
  // === ПИНГ ===
  else if (command == "PING") {
    Serial.println("PONG:jarvis_ARDUINO");
  }
  
  // === НЕИЗВЕСТНАЯ КОМАНДА ===
  else {
    Serial.println("ERROR:UNKNOWN_COMMAND:" + command);
  }
}

// ============================================================================
// ВСПОМОГАТЕЛЬНЫЕ ФУНКЦИИ
// ============================================================================

String getParam(String params, String key, String defaultVal) {
  String searchKey = key + "=";
  int keyIndex = params.indexOf(searchKey);
  
  if (keyIndex >= 0) {
    int startIndex = keyIndex + searchKey.length();
    int endIndex = params.indexOf(';', startIndex);
    
    if (endIndex < 0) {
      endIndex = params.length();
    }
    
    return params.substring(startIndex, endIndex);
  }
  
  return defaultVal;
}

int getParamInt(String params, String key, int defaultVal) {
  String val = getParam(params, key, String(defaultVal));
  return val.toInt();
}

long readDistance(int trigPin, int echoPin) {
  // Очистка триггера
  digitalWrite(trigPin, LOW);
  delayMicroseconds(2);
  
  // Импульс 10 мкс
  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);
  
  // Чтение эхо-сигнала
  long duration = pulseIn(echoPin, HIGH, 30000); // Таймаут 30мс (~5м)
  
  if (duration == 0) {
    return -1; // Объект вне диапазона
  }
  
  // Расчёт расстояния в см
  long distance = duration * SOUND_SPEED / 200 / 100;
  
  return distance;
}

void readAllSensors() {
  Serial.println("BEGIN_SENSOR_READ");
  
  // Температура
  int tempRaw = analogRead(PIN_TEMP_SENSOR);
  float tempVoltage = tempRaw * (5.0 / 1023.0);
  float tempC = (tempVoltage - 0.5) * 100.0;
  Serial.println("SENSOR:TEMP_RAW:" + String(tempRaw));
  Serial.println("SENSOR:TEMP_C:" + String(tempC, 2));
  
  // Освещённость
  int lightRaw = analogRead(PIN_LIGHT_SENSOR);
  float lightVoltage = lightRaw * (5.0 / 1023.0);
  float lightResistance = 10000.0 * (5.0 / lightVoltage - 1.0);
  float jarvis = 500.0 / (lightResistance / 1000.0);
  Serial.println("SENSOR:LIGHT_RAW:" + String(lightRaw));
  Serial.println("SENSOR:jarvis:" + String(jarvis, 2));
  
  // Расстояние
  long distance = readDistance(PIN_TRIG, PIN_ECHO);
  Serial.println("SENSOR:DISTANCE_CM:" + String(distance));
  
  Serial.println("END_SENSOR_READ");
}

void reportStatus() {
  Serial.println("STATUS_BEGIN");
  Serial.println("STATUS:LED_BUILTIN:" + String(ledState == HIGH ? "ON" : "OFF"));
  Serial.println("STATUS:LED_PWM:" + String(analogRead(PIN_LED_PWM) > 0 ? "ON" : "OFF"));
  Serial.println("STATUS:MOTOR:" + String(motorState == HIGH ? "ON" : "OFF"));
  Serial.println("STATUS:SERVO_ANGLE:" + String(servoAngle));
  Serial.println("STATUS:UPTIME_MS:" + String(millis()));
  Serial.println("STATUS_END");
}

/*
 * ============================================================================
 * ПРИМЕРЫ КОМАНД (отправлять через Serial Monitor или из jarvis):
 * ============================================================================
 * 
 * DIGITAL_WRITE:PIN=13;VALUE=HIGH     - Включить встроенный светодиод
 * DIGITAL_WRITE:PIN=13;VALUE=LOW      - Выключить встроенный светодиод
 * 
 * ANALOG_WRITE:PIN=9;VALUE=127        - Яркость 50% (PWM)
 * ANALOG_WRITE:PIN=9;VALUE=255        - Яркость 100% (PWM)
 * ANALOG_WRITE:PIN=9;VALUE=0          - Яркость 0% (PWM)
 * 
 * SERVO_WRITE:PIN=9;ANGLE=0           - Серво в 0°
 * SERVO_WRITE:PIN=9;ANGLE=90          - Серво в 90°
 * SERVO_WRITE:PIN=9;ANGLE=180         - Серво в 180°
 * 
 * MOTOR_FWD                           - Мотор вперёд
 * MOTOR_REV                           - Мотор назад
 * MOTOR_STOP                          - Мотор стоп
 * 
 * TONE_PLAY:PIN=8;FREQUENCY=1000;DURATION=500  - Звук 1000Гц, 500мс
 * TONE_STOP:PIN=8                     - Стоп звук
 * 
 * ANALOG_READ:PIN=A0                  - Прочитать температуру
 * ANALOG_READ:PIN=A1                  - Прочитать освещённость
 * 
 * ULTRASONIC_READ:TRIG=2;ECHO=3       - Измерить расстояние
 * 
 * READ_ALL_SENSORS                    - Считать все датчики
 * STATUS                              - Получить статус системы
 * PING                                - Проверка связи
 * 
 * PAUSE:MS=1000                       - Пауза 1 секунда
 * 
 * ============================================================================
 */
