import board
import analogio
import digitalio
import time
import pwmio

state = 1
count = 0
state = 1
SIGNAL_THRESHOLD = 50
RESET_THRESHOLD = 25
LED_BRIGHTNESS = 255

time_stamp                    = 0; 
measurement_deadtime          = 0; 
time_measurement              = 0;      # Time stamp 
interrupt_timer               = 0;      # Time stamp 
start_time                    = 0;      # Start time reference variable 
total_deadtime                = 0;      # total time between signals


led = digitalio.DigitalInOut(board.GP6)
led.direction = digitalio.Direction.OUTPUT

reset = digitalio.DigitalInOut(board.GP3)
reset.direction = digitalio.Direction.OUTPUT

now = time.monotonic() #Python equivalent of millis() and micros()

def get_sipm_voltage(adc_value):
    voltage = 26.2;
#   voltage = 0; 
#   for (int i = 0; i < (sizeof(cal)/sizeof(float)) 
#     i = i +1
#     voltage += cal[i] * pow(adc_value,(sizeof(cal)/sizeof(float)-i-1)); 
     
    return voltage; 
     
def write_to_SD():  
  while state == 1: 
    if (analogio.AnalogIn(board.A0) > SIGNAL_THRESHOLD): 
      adc = analogio.AnalogIn(board.A0);                    #Reads the output from the SIPM
      if (state == 1):
         led.value = True                                   #Corresponds to D3 (LED) or Reset?
         count = count + 1
         keep_pulse = 1; 
    
      analogio.AnalogIn(board.A3)    
    #   if (SLAVE == 1){ 
    #       if (digitalRead(6) == HIGH){ 
    #           keep_pulse = 1; 
    #           count++;}}  
    #   analogRead(A3); 

      if (state == 1):
            led.value = False                               #Corresponds to D3 (LED) | Written as digitalWrite(6, State)

      measurement_deadtime = total_deadtime; 
      time_stamp = now - start_time; 
      measurement_t1 = now;   
      temperatureC = (((analogio.AnalogIn(board.A3) + analogio.AnalogIn(board.A3) + analogio.AnalogIn(board.A3))/3. * (3300./1024)) - 500)/10. ; 

      if (state == 1): 
          led.value = False 
          reset.duty_cycle = LED_BRIGHTNESS
          file.write("##########################################################################################\n")
          file.write(count + " " + time_stamp+ " " + adc+ " " + get_sipm_voltage(adc)+ " " + measurement_deadtime+ " " + temperatureC); 
          file.write(count + " " + time_stamp+ " " + adc+ " " + get_sipm_voltage(adc)+ " " + measurement_deadtime+ " " + temperatureC); 
          file.flush(); 
          last_adc_value = adc;

    #   if (SLAVE == 1) { 
    #       if (keep_pulse == 1){    
    #           analogWrite(3, LED_BRIGHTNESS); 
    #           Serial.println((String)count + " " + time_stamp+ " " + adc+ " " + get_sipm_voltage(adc)+ " " + measurement_deadtime+ " " + temperatureC); 
    #           myFile.println((String)count + " " + time_stamp+ " " + adc+ " " + get_sipm_voltage(adc)+ " " + measurement_deadtime+ " " + temperatureC); 
    #           myFile.flush(); 
    #           last_adc_value = adc;}} 

      keep_pulse = 0; 
      reset.value = False
      while(analogio.AnalogIn(board.A0) > RESET_THRESHOLD):
        total_deadtime += (now - measurement_t1) / 1000  

detector_name = "Brussel"

filename = 'test.txt'
# try: 
#     file = open(filename, 'r')
#     content = file.read()
#     print(content)
# finally:
#     file.close()

# with open(filename, 'r') as file: # Alternative and shorter way to write the one above | With automatically incloses the file | Implicit file handling
file = open(filename, "x")
file.write("##########################################################################################\n")
file.write("### CosmicWatch: The Desktop Muon Detector\n")
file.write("### Questions? saxani@mit.edu\n")
file.write("### Comp_date Comp_time Event Ardn_time[ms] ADC[0-1023] SiPM[mV] Deadtime[ms] Temp[C] Name\n")

file.write("##########################################################################################\n")

file.write(f"Device ID: {detector_name}\n")

file.write("##########################################################################################\n") 
file.write("### CosmicWatch: The Desktop Muon Detector\n") 
file.write("### Questions? saxani@mit.edu\n") 
file.write("### Comp_date Comp_time Event Ardn_time[ms] ADC[0-1023] SiPM[mV] Deadtime[ms] Temp[C] Name\n")
file.write("##########################################################################################\n")
file.write(f"Device ID: {detector_name}\n")
write_to_SD()



