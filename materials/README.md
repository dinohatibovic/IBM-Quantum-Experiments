# Simulation Suite

Two complete scientific simulation systems.

## Files

| File | Description | Classes |
| --- | --- | --- |
| `chemical_elements.py` | Materials & catalyst optimization | ChemicalElementsDatabase, MaterialScreening, CatalystOptimization, QuantumMaterialPrediction, CouplingMechanisms, AdvancedOptimizationAlgorithms |
| `photovoltaic_simulation.py` | Atoms, photons, cells, PV cells | AtomicSimulation, PhotonSimulation, CellSimulation, PhotovoltaicCellSimulation, CellMotionUnderUV, LatticeOptimization |

## Install

```bash
pip install numpy pandas matplotlib scipy scikit-learn torch
# or
pip install -r requirements.txt
```

## Run

```bash
python chemical_elements.py        # Materials + catalyst
python photovoltaic_simulation.py  # Atoms + photons + PV cells
```

## Libraries Used

- `numpy` — numerical arrays, random simulations
- `pandas` — dataframes, CSV export
- `matplotlib` — visualization, plots
- `scipy.optimize` — differential_evolution, minimize
- `sklearn` — StandardScaler, RandomForestRegressor
- `torch / PyTorch` — neural network material predictor
- `sqlite3` — built-in, database export

## Key Components

### chemical_elements.py

- **ChemicalElementsDatabase** — Si, GaAs, CdTe, CIGS, Perovskite, Pt, Ni, Fe, Co
- **MaterialScreening** — weighted scoring with Monte Carlo weight variation
- **CatalystOptimization** — differential evolution + temperature/pressure/humidity effects
- **QuantumMaterialPrediction** — PyTorch MLP trained on element properties
- **CouplingMechanisms** — electron-phonon coupling, exciton binding, band alignment
- **AdvancedOptimizationAlgorithms** — genetic algorithm + particle swarm

### photovoltaic_simulation.py

- **AtomicSimulation** — hydrogen wavefunction, multi-electron Hartree-Fock
- **PhotonSimulation** — IR→UV spectrum, absorption/emission/transmission
- **CellSimulation** — cell dynamics, migration random walk
- **PhotovoltaicCellSimulation** — Shockley-Queisser, QE, fill factor
- **CellMotionUnderUV** — photophobia simulation on UV gradient grid
- **LatticeOptimization** — square/hexagonal/rectangular/oblique lattices
