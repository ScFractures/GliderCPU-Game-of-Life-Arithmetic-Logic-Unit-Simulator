# GliderCPU-Game-of-Life-Arithmetic-Logic-Unit-Simulator
🧠 GliderCPU — Game of Life 4-bit Arithmetic Logic Unit
GliderCPU is a full arithmetic computing system built entirely inside Conway’s Game of Life using glider-based logic gates. It implements a complete 4-bit ALU capable of performing addition, subtraction, multiplication, and division through physically simulated logic circuits rather than software arithmetic.

All computation is performed using glider streams, eater-based input control, and collision-driven logic gates exported as RLE patterns and orchestrated via a Python controller in Golly.

⚙️ Features
4-bit binary arithmetic system
Fully implemented logic gates: AND / XOR / NOT / OR
Full-adder constructed from glider collision circuits
Ripple-carry 4-bit adder
Subtraction via two’s complement logic
Repeated subtraction division (integer quotient + remainder)
Glider-based multiplication using partial product accumulation
Input encoding via eater/block control structures
Output detection via fixed coordinate probes

🧩 Architecture
The system is composed of:

RLE-based logic gates (AND / XOR / NOT / OR)
Glider streams as data carriers
Eaters as binary input switches
Block probes as output sensors
Python + Golly controller for orchestration

Each operation is executed as a physical evolution of the Game of Life grid rather than symbolic computation.

🔢 Supported Operations
Addition: A + B
Subtraction: A - B
Multiplication: A × B
Division: A ÷ B → quotient + remainder

All inputs are 0–15 (4-bit unsigned integers).

🧠 Key Idea
Instead of simulating arithmetic, this project constructs a physically realizable computation model where:

logic = glider interaction
memory = stable patterns
input = eater activation
output = spatial detection of surviving structures

🛠 Implementation
Python (Golly scripting API)
Conway’s Game of Life (B3/S23 rule)
RLE gate modules
Glider-based signal propagation

🚀 Why this project is special
This is not a simulation of a calculator — it is a calculator physically embedded inside a cellular automaton universe, where every bit of computation emerges from particle-like interactions of gliders.

📌 Status
Experimental but functional 4-bit ALU system with working arithmetic pipeline.

🛠 Usage Instructions

1. Prerequisites
Install [Golly](http://golly.sourceforge.net/) (Windows, macOS, or Linux).
Make sure Python scripting is enabled in Golly (Python 3 recommended).

2. Open the Project
Launch Golly.
Go to File → Open and select the RLE pattern of the gate or the full calculator Python controller.
Example: and_gate.rle, xor_gate.rle, or 4_bit_whole.py.

3. Running Gates Individually
Each gate is stored as an RLE file with internal eaters/blocks.
Python scripts will control the inputs by removing or keeping eater patterns.
The simulation runs the Game of Life for a fixed number of generations to compute the output.

4. Using the 4-bit Calculator
Open [4_bit_whole.py](./4_bit_whole.py) via File → Run Script.
Enter the operation when prompted: +, -, *, or /.
Enter two numbers (0–15) when prompted for inputs A and B.
Observe the output in Golly's note window:
For addition/subtraction/multiplication: shows binary and decimal results.
For division: shows quotient and remainder in both binary and decimal.

5. Notes
The computation is fully visual: gliders propagate and interact according to the logic gates.
Outputs are detected via specific block positions in the Life grid.
You can modify inputs by changing which eaters/blocks are present in the RLE before running.
