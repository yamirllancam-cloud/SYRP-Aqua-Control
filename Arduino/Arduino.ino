#include <DHT.h>
#define DHTPIN 9
#define DHTTYPE DHT11
const int PIN_RELE = 3;         
const int PIN_SENSOR_HUM = A0;   
const int trigPin = 11;  
const int echoPin = 12;  
const float distVacio = 25.0;  
const float distLleno = 15.0;   
// VARIABLES DINÁMICAS
int umbralRiego = 70;        // Valor inicial
bool modoAutomatico = true;  // Controla si el Arduino decide solo
DHT dht(DHTPIN, DHTTYPE);
void setup() {
  Serial.begin(9600);
  pinMode(PIN_RELE, OUTPUT);
  pinMode(trigPin, OUTPUT);
  pinMode(echoPin, INPUT);  
  digitalWrite(PIN_RELE, HIGH);  
  dht.begin();
}
void loop() {
  float tempAire = dht.readTemperature();
  float humAire = dht.readHumidity();
  int lecturaSuelo = analogRead(PIN_SENSOR_HUM);
  int humSuelo = map(lecturaSuelo, 950, 300, 0, 100);
  humSuelo = constrain(humSuelo, 0, 100);
  digitalWrite(trigPin, LOW); delayMicroseconds(2);
  digitalWrite(trigPin, HIGH); delayMicroseconds(10); digitalWrite(trigPin, LOW);
  long duration = pulseIn(echoPin, HIGH);
  float distanciaActual = duration * 0.034 / 2;  
  float nivelPorcentaje = constrain((distVacio - distanciaActual) / (distVacio - distLleno) * 100.0, 0, 100);
  // --- ESCUCHA DE COMANDOS (PYTHON -> ARDUINO) ---
  if (Serial.available() > 0) {
    String comando = Serial.readStringUntil('\n');
    comando.trim(); 
    if (comando == "R:ON") {
      modoAutomatico = false; // Desactivar auto para obedecer manual
      digitalWrite(PIN_RELE, LOW);
    } 
    else if (comando == "R:OFF") {
      modoAutomatico = false;
      digitalWrite(PIN_RELE, HIGH);
    }
    else if (comando == "AUTO:ON") {
      modoAutomatico = true; // Volver al control por sensores
    }
    else if (comando.startsWith("U:")) {
      umbralRiego = comando.substring(2).toInt(); // Actualizar umbral desde el slider de Python
    }
  }
  // --- LÓGICA AUTOMÁTICA (REDUNDANTE) ---
  if (modoAutomatico) {
    if (humSuelo < umbralRiego) {  
      digitalWrite(PIN_RELE, LOW); 
    } else {
      digitalWrite(PIN_RELE, HIGH); 
    }
  }
  // --- ENVÍO DE DATOS (ARDUINO -> PYTHON) ---
  Serial.print("T:");  Serial.print(tempAire);
  Serial.print("|HA:"); Serial.print(humAire);
  Serial.print("|HS:"); Serial.print(humSuelo);
  Serial.print("|N:");  Serial.print(nivelPorcentaje); 
  Serial.print("|M:");  Serial.println(modoAutomatico ? "AUTO" : "MAN"); 
  delay(1000); 
}
