## GHZ State in RAQT

Purpose: Create shared entanglement for anonymous transmission.

Property: |000⟩ + |111⟩. When measured: all 0 or all 1.

Why it hides sender:
- Sender's Z gate adds a global phase (-1)
- This affects the whole GHZ state, not one qubit
- Eve sees nothing on individual qubits
- Only combined XOR reveals the secret

Talking:
GHZ state is to prepare the qubits for secrecy protocol" — Yes

"When we measure we get either all 0 or all 1" — Yes

"Eve will never understand who sent 1" — Yes


## Encoding with Z Gate

Initial GHZ: (|000⟩ + |111⟩)/√2

If secret bit = 1:
- Apply Z on sender's qubit
- |111⟩ term becomes -|111⟩
- New state: (|000⟩ - |111⟩)/√2

Why it's anonymous:
- The minus sign affects the WHOLE |111⟩ term
- No single qubit shows a change
- Only combined measurements reveal the bit

## Anonymous Transmission Protocol

### Step 1: GHZ State
(|000⟩ + |111⟩) / √2

### Step 2: Encode (bit = 1)
Apply Z on sender's qubit → (|000⟩ - |111⟩) / √2

### Step 3: Why Anonymous
Minus sign applies to whole |111⟩ term. No single qubit shows the change. Eve sees random measurements.

### Step 4: Recover
All measure after Hadamard → XOR results → secret bit
