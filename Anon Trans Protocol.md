## My Anonymous Transmission Protocol

1. **GHZ State:** (|000⟩ + |111⟩)/√2 — all qubits entangled

2. **Encode (bit=1):** Sender applies Z gate → (|000⟩ - |111⟩)/√2
   - Minus sign added to |111⟩ term

3. **Transform:** Everyone applies Hadamard (H) gate
   - Converts phase to parity

4. **Measure:** Each gets a classical bit (0 or 1)

5. **Recover:** XOR all three bits
   - XOR = 0 → secret bit 0
   - XOR = 1 → secret bit 1

**Why it's anonymous:** The minus sign is on the whole |111⟩ term. No one can tell which qubit was flipped.
