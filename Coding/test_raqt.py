from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator
import numpy as np

def raqt_christandl_wehner(sender_id, secret_bit, n_qubits=4):
    """
    Anonymous transmission protocol from:
    Christandl & Wehner 2004 - "Quantum Anonymous Transmissions"
    
    Steps:
    1. Create GHZ state across all n nodes
    2. Sender applies Z if secret_bit = 1 (nothing if 0)
    3. ALL nodes apply H (for X-basis measurement)
    4. Measure all qubits in Z-basis (after H)
    5. XOR of all measurement results = secret bit
    """
    qc = QuantumCircuit(n_qubits, n_qubits)
    
    # Step 1: GHZ state |0000⟩ + |1111⟩
    qc.h(0)
    for i in range(1, n_qubits):
        qc.cx(0, i)
    
    # Step 2: Sender encodes bit
    if secret_bit == 1:
        qc.z(sender_id)
    
    # Step 3: ALL nodes apply H (X-basis measurement preparation)
    for i in range(n_qubits):
        qc.h(i)
    
    # Step 4: Measure in Z-basis
    for i in range(n_qubits):
        qc.measure(i, i)
    
    return qc

def xor_from_qubits(counts, n_qubits):
    """Calculate XOR from qubit order (handles Qiskit endianness)"""
    xor1 = 0
    xor0 = 0
    for bitstring, count in counts.items():
        # Qiskit prints classical bits as c3 c2 c1 c0
        # Reverse to get qubit order q0 q1 q2 q3
        qubit_order = bitstring[::-1]
        xor = sum(int(b) for b in qubit_order) % 2
        if xor == 1:
            xor1 += count
        else:
            xor0 += count
    return xor1, xor0

print("=" * 60)
print("RAQT Protocol - Christandl & Wehner (2004)")
print("Anonymous Bit Transmission over GHZ States")
print("=" * 60)

# Use AerSimulator
simulator = AerSimulator()

# Test with sender = node 2
sender = 2

for secret_bit in [0, 1]:
    print(f"\n--- Secret bit = {secret_bit} ---")
    
    # Create circuit
    qc = raqt_christandl_wehner(sender, secret_bit)
    
    # Transpile and run
    qc_transpiled = transpile(qc, simulator)
    job = simulator.run(qc_transpiled, shots=1024)
    result = job.result()
    counts = result.get_counts()
    
    # Calculate XOR
    xor1, xor0 = xor_from_qubits(counts, 4)
    
    print(f"XOR = 1: {xor1} ({xor1/1024*100:.1f}%)")
    print(f"XOR = 0: {xor0} ({xor0/1024*100:.1f}%)")
    
    # Show sample outcomes
    print(f"Sample outcomes: {list(counts.items())[:4]}")
    
    # Verify
    if secret_bit == 0 and xor1 < 100:
        print("✅ Correct: XOR mostly 0")
    elif secret_bit == 1 and xor0 < 100:
        print("✅ Correct: XOR mostly 1")
    else:
        print("❌ Incorrect")

print("\n" + "=" * 60)
print("THEORETICAL EXPLANATION:")
print("=" * 60)
print("1. GHZ state: (|0000⟩ + |1111⟩)/√2")
print("2. Z gate on sender: flips |1111⟩ to -|1111⟩")
print("3. All nodes apply H: transforms to X-basis")
print("4. Measurement outcomes have XOR = secret bit")
print("5. Anonymity: any node could have applied Z")