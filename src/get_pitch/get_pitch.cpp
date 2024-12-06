/// @file

#include <iostream>
#include <fstream>
#include <string.h>
#include <errno.h>

#include "wavfile_mono.h"
#include "pitch_analyzer.h"

#include "docopt.h"

#define FRAME_LEN   0.030 /* 30 ms. */
#define FRAME_SHIFT 0.015 /* 15 ms. */

using namespace std;
using namespace upc;

static const char USAGE[] = R"(
get_pitch - Pitch Estimator 

Usage:
    get_pitch [options] <input-wav> <output-txt>
    get_pitch (-h | --help)
    get_pitch --version

Options:
    --llindar-rmax FLOAT  llindar de decisió sonor, sord per a rmax [default: 0.45]
    --llindar-r1norm FLOAT  llindar de decisió sonor, sord per a r1norm [default: 0.75]
    --llindar-pot FLOAT  llindar de decisió sonor, sord per a pot [default: -50]
    -h, --help  Show this screen
    --version   Show the version of the project

Arguments:
    input-wav   Wave file with the audio signal
    output-txt  Output file: ASCII file with the result of the estimation:
                    - One line per frame with the estimated f0
                    - If considered unvoiced, f0 must be set to f0 = 0
)";

int main(int argc, const char *argv[]) {
	/// \TODO 
	///  Modify the program syntax and the call to **docopt()** in order to
	///  add options and arguments to the program.
  /// \FET hem afegit els arguments --llindar-rmax, --llindar-r1norm i --llindar-pot
    std::map<std::string, docopt::value> args = docopt::docopt(USAGE,
        {argv + 1, argv + argc},	// array of arguments, without the program name
        true,    // show help if requested
        "2.0");  // version string

	std::string input_wav = args["<input-wav>"].asString();
	std::string output_txt = args["<output-txt>"].asString();
  float llindar_rmax = stof(args["--llindar-rmax"].asString());
  float llindar_r1norm = stof(args["--llindar-r1norm"].asString());
  float llindar_pot = stof(args["--llindar-pot"].asString());

  // Read input sound file
  unsigned int rate;
  vector<float> x;
  if (readwav_mono(input_wav, rate, x) != 0) {
    cerr << "Error reading input file " << input_wav << " (" << strerror(errno) << ")\n";
    return -2;
  }

  int n_len = rate * FRAME_LEN;
  int n_shift = rate * FRAME_SHIFT;

  // Define analyzer
  PitchAnalyzer analyzer(n_len, rate, PitchAnalyzer::RECT, 50, 500, llindar_rmax, llindar_r1norm, llindar_pot);

  /// \TODO
  /// Preprocess the input signal in order to ease pitch estimation. For instance,
  /// central-clipping or low pass filtering may be used.
  // Apply central clipping

  /// \FET Hem fet servir el central clipping per pre-processar la senyal
  float max_val = *max_element(x.begin(), x.end());
  float min_val = *min_element(x.begin(), x.end());
  float threshold = 0.01 * max(max_val, -min_val);

  for (auto &sample : x) {
    if (abs(sample) < threshold) {
      sample = 0;
    }
  } 
  // Iterate for each frame and save values in f0 vector
  vector<float>::iterator iX;
  vector<float> f0;
  for (iX = x.begin(); iX + n_len < x.end(); iX = iX + n_shift) {
    float f = analyzer(iX, iX + n_len);
    f0.push_back(f);
  }

  /// \TODO
  /// Postprocess the estimation in order to supress errors. For instance, a median filter
  /// or time-warping may be used.
  // Apply a median filter to suppress errors
  /// \FET Hem aplicat un filtre de la mediana per suprimir errors
   vector<float> f0_filtered(f0.size());
  int filter_size = 3; // Size of the median filter window

  for (size_t i = 0; i < f0.size(); ++i) {
    vector<float> window;
    for (int j = -filter_size / 2; j <= filter_size / 2; ++j) {
      if (i + j >= 0 && i + j < f0.size()) {
        window.push_back(f0[i + j]);
      }
    }
    sort(window.begin(), window.end());
    f0_filtered[i] = window[window.size() / 2];
  }

  f0 = f0_filtered;
  // Write f0 contour into the output file
  ofstream os(output_txt);
  if (!os.good()) {
    cerr << "Error reading output file " << output_txt << " (" << strerror(errno) << ")\n";
    return -3;
  }

  os << 0 << '\n'; //pitch at t=0
  for (iX = f0.begin(); iX != f0.end(); ++iX) 
    os << *iX << '\n';
  os << 0 << '\n';//pitch at t=Dur

  return 0;
}
