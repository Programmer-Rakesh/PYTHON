#include "arm_math.h"

// --- Pin & LED Config ---
#define PIN_L A0  
#define PIN_R A1  
#define LED_BUILTIN 13

// --- Thresholds (Tune these in Serial Plotter) ---
float MIN_FOCUS_SUM    = 22.0f; // Total Beta power to start moving
float TURN_SENSITIVITY = 0.25f; // Asymmetry ratio (0.1 to 0.5)
int   STABILITY_COUNT  = 3;     // Cycles required to confirm a command

// --- DSP & Filter Variables ---
#define SAMPLE_RATE 256  
#define FFT_SIZE    256
float inputL[FFT_SIZE], inputR[FFT_SIZE], fftBuf[FFT_SIZE];
arm_rfft_fast_instance_f32 S;
volatile int sIdx = 0;
volatile bool ready = false;

// Filter States (Official BioAmp 4th Order Butterworth 0.5-29.5Hz)
float zL[4][2], zR[4][2]; 

// Smoothing & State
float smoothL = 0, smoothR = 0;
const float alpha = 0.2f; 
int activeCommand = 0; 
int pendingCommand = 0;
int stabilityTimer = 0;

// --- Upside Down Labs EEG Filter Function ---
float applyEEGFilter(float input, float state[][2]) {
  float output = input;
  // Section 1
  float x = output - -0.95391350 * state[0][0] - 0.25311356 * state[0][1];
  output = 0.00735282 * x + 0.01470564 * state[0][0] + 0.00735282 * state[0][1];
  state[0][1] = state[0][0]; state[0][0] = x;
  // Section 2
  x = output - -1.20596630 * state[1][0] - 0.60558332 * state[1][1];
  output = 1.00000000 * x + 2.00000000 * state[1][0] + 1.00000000 * state[1][1];
  state[1][1] = state[1][0]; state[1][0] = x;
  // Section 3
  x = output - -1.97690645 * state[2][0] - 0.97706395 * state[2][1];
  output = 1.00000000 * x + -2.00000000 * state[2][0] + 1.00000000 * state[2][1];
  state[2][1] = state[2][0]; state[2][0] = x;
  // Section 4
  x = output - -1.99071687 * state[3][0] - 0.99086813 * state[3][1];
  output = 1.00000000 * x + -2.00000000 * state[3][0] + 1.00000000 * state[3][1];
  state[3][1] = state[3][0]; state[3][0] = x;
  return output;
}

void setup() {
  Serial.begin(115200);
  analogReadResolution(14); // Optimized for Uno R4
  pinMode(LED_BUILTIN, OUTPUT);
  arm_rfft_fast_init_f32(&S, FFT_SIZE);
  
  memset(zL, 0, sizeof(zL)); 
  memset(zR, 0, sizeof(zR));
  
  Serial.println("System Initialized. Awaiting Brain Activity...");
}

void loop() {
  // 1. Precise 256Hz Sampling
  static unsigned long lastU = 0;
  if (micros() - lastU >= 1000000 / SAMPLE_RATE) {
    lastU = micros();
    if (!ready) {
      inputL[sIdx] = applyEEGFilter((float)analogRead(PIN_L), zL);
      inputR[sIdx] = applyEEGFilter((float)analogRead(PIN_R), zR);
      if (++sIdx >= FFT_SIZE) ready = true;
    }
  }

  // 2. Continuous LED/Visual Feedback
  updateLED(activeCommand);

  // 3. Command Processing
  if (ready) {
    float rawL = calculateBetaPower(inputL);
    float rawR = calculateBetaPower(inputR);

    // Exponential Smoothing
    smoothL = (alpha * rawL) + (1.0f - alpha) * smoothL;
    smoothR = (alpha * rawR) + (1.0f - alpha) * smoothR;

    float sum = smoothL + smoothR;
    float dominance = (smoothL - smoothR) / (sum + 0.001f);

    int decision = 0; // Default to Stop
    if (sum > MIN_FOCUS_SUM) {
      if (dominance > TURN_SENSITIVITY)       decision = 3; // RIGHT
      else if (dominance < -TURN_SENSITIVITY)  decision = 2; // LEFT
      else                                     decision = 1; // FORWARD
    }

    // Stability & Print Logic
    if (decision == pendingCommand) {
      stabilityTimer++;
    } else {
      pendingCommand = decision;
      stabilityTimer = 0;
    }

    if (stabilityTimer >= STABILITY_COUNT) {
      if (activeCommand != pendingCommand) {
        activeCommand = pendingCommand;
        printCommand(activeCommand); // Output to Serial Monitor
      }
    }

    // Data Streaming for Tuning
    Serial.print("SUM:"); Serial.print(sum);
    Serial.print(",DOM:"); Serial.println(dominance);

    sIdx = 0; ready = false;
  }
}

// Frequency Analysis Function
float calculateBetaPower(float* data) {
  arm_rfft_fast_f32(&S, data, fftBuf, 0);
  float total = 0, beta = 0;
  for (int i = 1; i < FFT_SIZE / 2; i++) {
    float p = fftBuf[2*i]*fftBuf[2*i] + fftBuf[2*i+1]*fftBuf[2*i+1];
    total += p;
    float freq = i * (256.0f / 256.0f); 
    if (freq >= 13.0f && freq <= 30.0f) beta += p;
  }
  return (total > 0) ? (beta / total * 100.0f) : 0;
}

// Serial Monitor Command Output
void printCommand(int cmd) {
  Serial.print(">>> COMMAND: ");
  switch(cmd) {
    case 0: Serial.println("0 (STOP)"); break;
    case 1: Serial.println("01 (FORWARD)"); break;
    case 2: Serial.println("2 (LEFT)"); break;
    case 3: Serial.println("3 (RIGHT)"); break;
  }
}

// Built-in LED Feedback Logic
void updateLED(int cmd) {
  static unsigned long lastFlash = 0;
  static bool state = false;
  unsigned long now = millis();
  if (cmd == 0) digitalWrite(LED_BUILTIN, LOW);
  else if (cmd == 1) digitalWrite(LED_BUILTIN, HIGH);
  else {
    int interval = (cmd == 3) ? 100 : 400; // Fast Right, Slow Left
    if (now - lastFlash > interval) {
      state = !state; digitalWrite(LED_BUILTIN, state); lastFlash = now;
    }
  }
}