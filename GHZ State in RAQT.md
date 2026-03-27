## GHZ State in RAQT

Purpose: Create shared entanglement for anonymous transmission.

Property: |000⟩ + |111⟩. When measured: all 0 or all 1.

Why it hides sender:
- Sender's Z gate adds a global phase (-1)
- This affects the whole GHZ state, not one qubit
- Eve sees nothing on individual qubits
- Only combined XOR reveals the secret
