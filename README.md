# ANTI-VEA

The Attentional Networks Test for Interactions and Vigilance: Executive and Arousal components (ANTI-VEA) is an experimental paradigm created by [Luna, Mareno, Roca, and Lupiáñez (2018)](https://doi.org/10.1016/j.jneumeth.2018.05.011), based on the  [original ANT-I](https://github.com/a-hurst/ANTI) by [Callejas, Lupiáñez, and Tudela (2004)](https://doi.org/10.1016/j.bandc.2004.02.012). It is intended for studying the attention networks of alerting, orienting, and executive function (and their interactions), while simulaneously measuring both executive vigilance (via trials requiring the detection of displaced central arrows) and arousal vigilance (via [PVT](https://github.com/a-hurst/PVT) trials) across the session. This experiment program aims to be an english language reimplementation of the Luna et al. (2018) paradigm using the KLibs framework, based on the methods described in their paper.

![ANTI_VEA_animation](klibs_anti-vea.gif)

**NOTE**: Unlike the paradigm described in Luna et al. (2018), this version of the ANTI-VEA currently only contains executive vigilance trials with vertically-displaced central arrows. The original paradigm contains executive vigilance trials with both vertically-displaced and horizontally-displaced central arrows. Additionally, to conserve time, this version does not include the fourth and final practice block of 40 trials without feedback.


## Requirements

This version of the ANTI-VEA is programmed in Python 2.7 (3.3+ compatible) using the [KLibs framework](https://github.com/a-hurst/klibs). It has been developed and tested on macOS (10.9 through 10.13), but should also work with minimal hassle on computers running [Ubuntu](https://www.ubuntu.com/download/desktop) or [Debian](https://www.debian.org/distrib/) Linux, as well as on computers running Windows 7 or newer with [a bit more effort](https://github.com/a-hurst/klibs/wiki/Installation-on-Windows).


## Getting Started

### Installation

First, you will need to install the KLibs framework by following the instructions [here](https://github.com/a-hurst/klibs).

Then, you can then download and install the experiment program with the following commands (replacing `~/Downloads` with the path to the folder where you would like to put the program folder):

```
cd ~/Downloads
git clone https://github.com/a-hurst/ANTI_VEA.git
```

### Running the Experiment

This version of the ANTI-VEA is a KLibs experiment, meaning that it is run using the `klibs` command at the terminal (running the 'experiment.py' file using python directly will not work).

To run the experiment, navigate to the ANTI_VEA folder in Terminal and run `klibs run [screensize]`,
replacing `[screensize]` with the diagonal size of your display in inches (e.g. `klibs run 24` for a 24-inch monitor).

If you just want to test the program out for yourself and skip demographics collection, you can add the `-d` flag to the end of the command to launch the experiment in development mode.

### Exporting Data

To export data from the ANTI-VEA, simply run

```
klibs export
```

while in the root of the ANTI_VEA directory. This will export the trial data for each participant into individual tab-separated text files in the project's `ExpAssets/Data` subfolder.
