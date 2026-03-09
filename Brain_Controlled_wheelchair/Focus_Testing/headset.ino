#include "arm_math.h"

// --- Pin & LED Config ---
#define PIN_L A0
#define PIN_R A1
#define LED_BUILTIN 13

// --- Blink Detection Thresholds (Tune these!) ---
#define BLINK_THRESHOLD   300.0f   // Absolute filtered value to consider a blink
#define BLINK_MIN_DURATION 20      // Minimum duration (ms) to avoid noise
#define BLINK_TIMEOUT      500     // Max blink duration (ms)

// --- DSP & Filter Variables ---
#define SAMPLE_RATE 256
#define FFT_SIZE    256
float inputL[FFT_SIZE], inputR[FFT_SIZE], fftBuf[FFT_SIZE];
arm_rfft_fast_instance_f32 S;
volatile int sIdx = 0;
volatile bool ready = false;

// Filter States (Official BioAmp 4th Order Butterworth 0.5-29.5Hz)
float zL[4][2], zR[4][2];

// Blink detection state
bool blinkActive = false;
unsigned long blinkStartTime = 0;
float peakL = 0, peakR = 0;

// ------------------------------------------------------------------
// EEG Filter (unchanged)
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
// ------------------------------------------------------------------

void setup() {
  Serial.begin(115200);
  analogReadResolution(14); // Optimized for Uno R4
  pinMode(LED_BUILTIN, OUTPUT);
  arm_rfft_fast_init_f32(&S, FFT_SIZE);

  memset(zL, 0, sizeof(zL));
  memset(zR, 0, sizeof(zR));

  Serial.println("System Initialized. Sending features and blinks...");
}

void loop() {
  // 1. Precise 256Hz Sampling
  static unsigned long lastU = 0;
  if (micros() - lastU >= 1000000 / SAMPLE_RATE) {
    lastU = micros();
    unsigned long now = millis(); // for blink timing

    // Read raw analog values
    float rawL = (float)analogRead(PIN_L);
    float rawR = (float)analogRead(PIN_R);

    // Apply EEG filter and store in buffers
    inputL[sIdx] = applyEEGFilter(rawL, zL);
    inputR[sIdx] = applyEEGFilter(rawR, zR);

    // --- Blink Detection on filtered values ---
    float valL = inputL[sIdx];
    float valR = inputR[sIdx];

    if (!blinkActive) {
      // Look for start of a blink
      if (fabs(valL) > BLINK_THRESHOLD || fabs(valR) > BLINK_THRESHOLD) {
        blinkActive = true;
        blinkStartTime = now;
        peakL = fabs(valL);
        peakR = fabs(valR);
      }
    } else {
      // Update peaks
      if (fabs(valL) > peakL) peakL = fabs(valL);
      if (fabs(valR) > peakR) peakR = fabs(valR);

      // Check if blink has ended (both below threshold)
      if (fabs(valL) < BLINK_THRESHOLD && fabs(valR) < BLINK_THRESHOLD) {
        if (now - blinkStartTime > BLINK_MIN_DURATION) {
          // Determine direction
          if (peakL > peakR) {
            Serial.println(">>> BLINK: LEFT");
          } else {
            Serial.println(">>> BLINK: RIGHT");
          }
        }
        blinkActive = false;
      }
      // Timeout safety
      else if (now - blinkStartTime > BLINK_TIMEOUT) {
        blinkActive = false;
      }
    }

    // Increment sample index
    if (++sIdx >= FFT_SIZE) ready = true;
  }

  // 2. Process when a full FFT window is ready (every ~1 second)
  if (ready) {
    // Compute beta (13-30 Hz) and alpha (8-12 Hz) for both channels
    float betaL = calculateBandPower(inputL, 13, 30);
    float betaR = calculateBandPower(inputR, 13, 30);
    float alphaL = calculateBandPower(inputL, 8, 12);
    float alphaR = calculateBandPower(inputR, 8, 12);

    // Send features as CSV line
    Serial.print("FEAT:");
    Serial.print(betaL); Serial.print(",");
    Serial.print(betaR); Serial.print(",");
    Serial.print(alphaL); Serial.print(",");
    Serial.println(alphaR);

    // Reset for next window
    sIdx = 0;
    ready = false;
  }
}

// Compute relative power in a frequency band (as percentage)
float calculateBandPower(float* data, float lowFreq, float highFreq) {
  arm_rfft_fast_f32(&S, data, fftBuf, 0);
  float total = 0, band = 0;
  for (int i = 1; i < FFT_SIZE / 2; i++) {
    float p = fftBuf[2*i]*fftBuf[2*i] + fftBuf[2*i+1]*fftBuf[2*i+1];
    total += p;
    float freq = i * (SAMPLE_RATE / (float)FFT_SIZE);
    if (freq >= lowFreq && freq <= highFreq) band += p;
  }
  return (total > 0) ? (band / total * 100.0f) : 0;
}