from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator
from qiskit_aer.noise import NoiseModel, depolarizing_error

def raqt_christandl_wehner(sender_id, secret_bit, n_qubits=4):
    qc = QuantumCircuit(n_qubits, n_qubits)
    
    # Step 1: GHZ state
    qc.h(0)
    for i in range(1, n_qubits):
        qc.cx(0, i)
    
    # Step 2: Sender encodes
    if secret_bit == 1:
        qc.z(sender_id)
    
    # Step 3: All nodes apply H (X-basis)
    for i in range(n_qubits):
        qc.h(i)
    
    # Step 4: Measure
    for i in range(n_qubits):
        qc.measure(i, i)
    
    return qc

def xor_from_qubits(counts, n_qubits):
    xor1 = 0
    xor0 = 0
    for bitstring, count in counts.items():
        qubit_order = bitstring[::-1]
        xor = sum(int(b) for b in qubit_order) % 2
        if xor == 1:
            xor1 += count
        else:
            xor0 += count
    return xor1, xor0

def noise_tolerance_raqt():
    print("\n" + "=" * 50)
    print("RAQT Noise Tolerance Analysis")
    print("=" * 50)
    
    for noise_prob in [0, 0.01, 0.05, 0.10, 0.25, 0.50]:
        noise_model = NoiseModel()
        
        # 1-qubit error for H and Z
        error_1q = depolarizing_error(noise_prob, 1)
        noise_model.add_all_qubit_quantum_error(error_1q, ['h', 'z'])
        
        # 2-qubit error for CX
        error_2q = depolarizing_error(noise_prob, 2)
        noise_model.add_all_qubit_quantum_error(error_2q, ['cx'])
        
        simulator = AerSimulator(noise_model=noise_model)
        
        successes = 0
        for secret_bit in [0, 1]:
            qc = raqt_christandl_wehner(sender_id=2, secret_bit=secret_bit)
            qc_transpiled = transpile(qc, simulator)
            job = simulator.run(qc_transpiled, shots=500)
            counts = job.result().get_counts()
            xor1, xor0 = xor_from_qubits(counts, 4)
            
            if secret_bit == 0:
                successes += xor0
            else:
                successes += xor1
        
        success_rate = successes / 1000
        print(f"Noise {noise_prob*100:3.0f}%: Success rate = {success_rate*100:.1f}%")

# Main execution
print("=" * 60)
print("RAQT Protocol - Christandl & Wehner (2004)")
print("=" * 60)

simulator = AerSimulator()

for secret_bit in [0, 1]:
    print(f"\n--- Secret bit = {secret_bit} ---")
    qc = raqt_christandl_wehner(sender_id=2, secret_bit=secret_bit)
    qc_transpiled = transpile(qc, simulator)
    job = simulator.run(qc_transpiled, shots=1024)
    counts = job.result().get_counts()
    xor1, xor0 = xor_from_qubits(counts, 4)
    print(f"XOR=1: {xor1} ({xor1/1024*100:.1f}%)")
    print(f"XOR=0: {xor0} ({xor0/1024*100:.1f}%)")

# Run noise analysis
noise_tolerance_raqt()