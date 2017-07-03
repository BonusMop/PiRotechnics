# PiRotechnics
PiRotechnics is software for the Raspberry Pi that enables the remote
triggering of a fireworks display. The initial version of this project was used
to trigger 29 fireworks over the course of 20 minutes in July 2017.

## Disclaimer
Use at your own risk.

I am not a pyrotechnics expert, nor an electrical engineer by trade. I write
software, but like all software mine occasionally contains defects. This 
stuff is dangerous. Some or all fireworks may even be illegal where you reside.
I make no warranty to the safety or effectiveness of the software or hardware 
described in this repository. I am not responsible for injury, death, loss of
property, or legal consequences due to your use of PiRotechnics or its 
derivatives.

Be safe!

## Instructions

I use the following steps to create the launch system:

1. Assemble the hardware according to the instructions. (I haven't added them yet)
2. Clone this repository to your Raspberry Pi:

        git clone https://github.com/BonusMop/PiRotechnics.git

3. Start the web server with python:

        sudo python PiRotechnics/web/pirotechnics.py
