**Anonymous bit transmission over GHZ states using the Christandl-Wehner (2004) protocol.**

[![Qiskit](https://img.shields.io/badge/Qiskit-1.3.2-blue)](https://qiskit.org)
[![License](https://img.shields.io/badge/License-MIT-green)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.10-yellow)](https://python.org)

---

## Overview

RAQT implements **anonymous quantum transmission** where a secret bit is sent across a quantum network without revealing the sender's identity.

### Features
- ✅ Complete GHZ-based anonymous transmission
- ✅ X-basis measurement implementation
- ✅ Noise tolerance analysis (1% to 50% depolarizing noise)
- ✅ Works on AerSimulator and IBM cloud
- ✅ Handles Qiskit endianness correctly

---

## Protocol Steps (Christandl & Wehner 2004)

| Step | Action |
|------|--------|
| 1 | Create GHZ state across N qubits (H on q0 + CNOTs to all) |
| 2 | Sender applies Z gate **only if secret bit = 1** |
| 3 | **All nodes** apply H gate (X-basis measurement preparation) |
| 4 | Measure all qubits in Z-basis |
| 5 | XOR all measurement results = secret bit |

**Why H on all nodes?** The paper requires X-basis measurement. To measure in X-basis, apply H then measure in Z-basis. This applies to **every** qubit, including the sender.

---

## Circuit Diagram (4 nodes, sender = q2, secret bit = 1)
q0: ──H──■──■──■──H──M──

q1: ─────X──┼──┼──H──M──


q2: ────────X──┼──Z──H──M──


q3: ───────────X──H──M──



---

## Installation

```bash
# Create virtual environment
python3 -m venv raqt_env
source raqt_env/bin/activate

# Install dependencies
pip install qiskit==1.3.2 qiskit-aer==0.15.1
```

### Usage

**Run Basic Test**
```python
from raqt_main import raqt_christandl_wehner, xor_from_qubits
from qiskit_aer import AerSimulator

simulator = AerSimulator()

for secret_bit in [0, 1]:
    qc = raqt_christandl_wehner(sender_id=2, secret_bit=secret_bit)
    result = simulator.run(qc, shots=1024).result()
    xor1, xor0 = xor_from_qubits(result.get_counts(), 4)
    print(f"Secret bit {secret_bit}: XOR=1 = {xor1/1024*100:.1f}%")
```
**Run Noise Tolerance Analysis**
```python
from raqt_main import noise_tolerance_raqt
noise_tolerance_raqt()
Results
Noise Level	Success Rate
0%	100.0%
1%	97.0%
5%	83.8%
10%	69.3%
25%	54.6%
50%	49.0%
````
## Interpretation:

Protocol works reliably up to ~5% depolarizing noise. Above 10%, error correction is needed.

## Key Technical Details
XOR is Classical Post-Processing
XOR is not a quantum gate. It is computed on a classical computer after measurement:

```python
bitstring = '0110'
xor = sum(int(b) for b in bitstring) % 2  # 0⊕1⊕1⊕0 = 0
````

## Qiskit Endianness
Qiskit prints classical bits in reverse order (c3 c2 c1 c0). Reverse the string to get qubit order:

```python
qubit_order = bitstring[::-1]  # Now q0 q1 q2 q3
xor = sum(int(b) for b in qubit_order) % 2
```

## File Structure

```text
RAQT-Anonymous-Quantum-Transmission/
├── raqt_main.py          # Complete implementation
├── README.md             # This file
└── requirements.txt      # Dependencies
```
**Author**
## Noor Ul Ain Faisal
Sialkot, Pakistan

IBM Qiskit Advocate

Friend of OQI (CERN)

Member, IEEE GRSS QUEST Technical Committee

Mentor, Qiskit Advocate Mentorship Program (QAMP)

**GitHub : learningdungeon | LinkedIn: noorulain-faisal | X : QuantumQueen**

## Citation
```text
bibtex
@misc{raqt2024,
  author = {Noor},
  title = {RAQT: Robust Anonymous Quantum Transmission},
  year = {2024},
  publisher = {GitHub},
  url = {https://github.com/noor/RAQT-Anonymous-Quantum-Transmission}
}
Based on: Christandl, M., & Wehner, S. (2004). Quantum Anonymous Transmissions. arXiv:quant-ph/0409069.
````

