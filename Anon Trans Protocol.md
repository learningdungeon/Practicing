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


## XOR (Parity)

XOR = 1 if bits are different (odd number of 1s)
XOR = 0 if bits are same (even number of 1s)

In my protocol:
- Secret 0 → measurements have even parity → XOR = 0
- Secret 1 → measurements have odd parity → XOR = 1

XOR reveals the secret bit.
