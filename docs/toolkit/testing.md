# Testing

This project uses `pytest`.

Run all verification tests:

```bash
python -m pytest tests -v
```

The verification tests check expected behavior for:

- WKB tunneling
- Hydrogen H-alpha wavelength
- Quantum harmonic oscillator zero-point energy
- Heisenberg uncertainty
- Bell CHSH violation
- BB84 eavesdropping detection
- Grover search success probability

Passing tests mean the package imports correctly, dependencies are working, and core functions produce expected numerical behavior.
