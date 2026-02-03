// Pin donde está conectado el potenciómetro
const int SENSOR_RUIDO = 33;

void setup() {
  // Iniciar comunicación serial
  Serial.begin(115200);
  Serial.println("Sistema de medición");
}

void loop() {
  // Leer el sensor (0-4095)
  int valorSensor = analogRead(SENSOR_RUIDO);
  
  // Convertir a decibelios (30-120 dB)
  int decibelios = map(valorSensor, 0, 4095, 30, 120);
  
  // Mostrar en pantalla
  Serial.print("Nivel de ruido: ");
  Serial.print(decibelios);
  Serial.println(" db");
   
  Serial.println("---");
  
  // Ejecutar cadda 5 segundos
  delay(5000);
}