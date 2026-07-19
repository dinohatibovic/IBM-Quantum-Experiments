"""
Advanced Simulations - Atoms, Photons, Cells and Photovoltaic Cells
Document 14 - Full Implementation
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import sqlite3
import warnings
warnings.filterwarnings('ignore')

try:
    import torch
    HAS_TORCH = True
except ImportError:
    HAS_TORCH = False

# Physical constants
HBAR = 1.055e-34   # J·s
E_CHARGE = 1.602e-19  # C
M_E = 9.109e-31    # kg
H_PLANCK = 6.626e-34  # J·s
C_LIGHT = 3e8      # m/s
K_B = 1.38e-23     # J/K
A0 = 0.529e-10     # Bohr radius m
E_RYDBERG = 13.6   # eV


# ============================================================================
# 1. ATOMIC SIMULATION
# ============================================================================

class AtomicSimulation:
    def __init__(self, num_simulations=100000):
        self.num_simulations = num_simulations

    def simulate_hydrogen_atom(self):
        print("⚛️  HYDROGEN ATOM SIMULATION")
        print("="*80)
        r = np.random.exponential(A0, self.num_simulations)
        theta = np.random.uniform(0, 2*np.pi, self.num_simulations)
        phi = np.random.uniform(0, 2*np.pi, self.num_simulations)
        x = r * np.sin(theta) * np.cos(phi)
        y = r * np.sin(theta) * np.sin(phi)
        z = r * np.cos(theta)
        # Use integer quantum numbers n=1,2,3 for realistic energies
        n_quantum = np.random.choice([1, 2, 3], self.num_simulations, p=[0.7, 0.2, 0.1])
        energies = -E_RYDBERG / n_quantum**2
        psi_squared = (1 / (np.pi * A0**3)) * np.exp(-2 * r / A0)
        print(f"  Average energy: {np.mean(energies):.4f} eV")
        print(f"  Avg distance from nucleus: {np.mean(r):.4e} m")
        print(f"  Avg probability: {np.mean(psi_squared):.4e}")
        return {'r': r, 'theta': theta, 'phi': phi,
                'x': x, 'y': y, 'z': z,
                'energies': energies, 'psi_squared': psi_squared}

    def simulate_multi_electron_atoms(self):
        print("\n⚛️  MULTI-ELECTRON ATOMS")
        print("="*80)
        atoms = {
            'H':  {'protons': 1, 'electrons': 1},
            'He': {'protons': 2, 'electrons': 2},
            'Li': {'protons': 3, 'electrons': 3},
            'C':  {'protons': 6, 'electrons': 6},
            'O':  {'protons': 8, 'electrons': 8}
        }
        results = {}
        # Use reduced sample for multi-electron (expensive loop)
        n = min(self.num_simulations, 1000)
        for name, data in atoms.items():
            ne, np_ = data['electrons'], data['protons']
            print(f"\n🔬 {name}: {np_} protons, {ne} electrons")
            positions = np.random.randn(n, ne, 3)
            energies = np.zeros(n)
            for sim in range(n):
                kinetic = np.sum(np.linalg.norm(positions[sim], axis=1)**2)
                e_nuc = -np_ * np.sum(1 / (np.linalg.norm(positions[sim], axis=1) + 1e-10))
                e_ee = sum(1 / (np.linalg.norm(positions[sim][i] - positions[sim][j]) + 1e-10)
                           for i in range(ne) for j in range(i+1, ne))
                energies[sim] = kinetic + e_nuc + e_ee
            results[name] = {'energies': energies, 'ne': ne, 'np': np_}
            print(f"  Avg energy: {np.mean(energies):.4f} Ha ± {np.std(energies):.4f}")
        return results


# ============================================================================
# 2. PHOTON SIMULATION
# ============================================================================

class PhotonSimulation:
    def __init__(self, num_simulations=100000):
        self.num_simulations = num_simulations

    def simulate_photon_properties(self):
        print("\n🌟 PHOTON SIMULATION")
        print("="*80)
        frequencies = np.random.uniform(3e12, 3e16, self.num_simulations)
        wavelengths = C_LIGHT / frequencies
        energies = H_PLANCK * frequencies
        momenta = energies / C_LIGHT
        polarization = np.random.uniform(0, 1, self.num_simulations)
        spin = np.random.choice([-1, 1], self.num_simulations)
        uv = np.sum(wavelengths < 400e-9)
        vis = np.sum((wavelengths >= 400e-9) & (wavelengths <= 700e-9))
        ir = np.sum(wavelengths > 700e-9)
        print(f"  Avg energy: {np.mean(energies)/E_CHARGE:.4f} eV")
        print(f"  UV: {uv:,} ({uv/self.num_simulations*100:.1f}%)  "
              f"Visible: {vis:,} ({vis/self.num_simulations*100:.1f}%)  "
              f"IR: {ir:,} ({ir/self.num_simulations*100:.1f}%)")
        return {'frequencies': frequencies, 'wavelengths': wavelengths,
                'energies': energies, 'momenta': momenta,
                'polarization': polarization, 'spin': spin}

    def simulate_photon_interactions(self, num_atoms=1000):
        print("\n🌟 PHOTON-ATOM INTERACTIONS")
        print("="*80)
        photon_energies = np.random.uniform(1, 20, self.num_simulations)
        atom_levels = np.random.uniform(1, 15, num_atoms)
        absorption = emission = transmission = 0
        for i in range(self.num_simulations):
            closest = atom_levels[np.argmin(np.abs(atom_levels - photon_energies[i]))]
            if abs(photon_energies[i] - closest) < 0.5:
                if np.random.random() < 0.8:
                    absorption += 1
                else:
                    transmission += 1
            else:
                transmission += 1
            if np.random.random() < 0.1:
                emission += 1
        print(f"  Absorption: {absorption:,} ({absorption/self.num_simulations*100:.1f}%)")
        print(f"  Emission:   {emission:,} ({emission/self.num_simulations*100:.1f}%)")
        print(f"  Transmission: {transmission:,} ({transmission/self.num_simulations*100:.1f}%)")
        return {'absorption': absorption, 'emission': emission, 'transmission': transmission}


# ============================================================================
# 3. CELL SIMULATION
# ============================================================================

class CellSimulation:
    def __init__(self, num_simulations=100000):
        self.num_simulations = num_simulations

    def simulate_cell_dynamics(self, temperature=300):
        print("\n🧬 CELL DYNAMICS SIMULATION")
        print("="*80)
        radii = np.abs(np.random.normal(10e-6, 2e-6, self.num_simulations))
        volumes = (4/3) * np.pi * radii**3
        surfaces = 4 * np.pi * radii**2
        atp = volumes * np.random.uniform(1e-15, 1e-12, self.num_simulations)
        growth = np.random.exponential(1e-7, self.num_simulations)
        division = np.random.normal(24, 4, self.num_simulations)
        small = np.sum(radii < 5e-6)
        medium = np.sum((radii >= 5e-6) & (radii <= 15e-6))
        large = np.sum(radii > 15e-6)
        print(f"  Avg radius: {np.mean(radii)*1e6:.2f} μm")
        print(f"  Avg ATP: {np.mean(atp):.4e} mol/s")
        print(f"  Small: {small:,}  Medium: {medium:,}  Large: {large:,}")
        return {'radii': radii, 'volumes': volumes, 'surfaces': surfaces,
                'atp_production': atp, 'growth_rates': growth, 'division_time': division}

    def simulate_cell_migration(self, num_steps=100):
        print("\n🧬 CELL MIGRATION SIMULATION")
        print("="*80)
        n = min(self.num_simulations, 10000)  # Limit for speed
        positions = np.random.randn(n, 2)
        velocities = np.random.randn(n, 2) * 1e-6
        for step in range(num_steps):
            if step % 10 == 0:
                velocities = np.random.randn(n, 2) * 1e-6
            positions += velocities
            if (step + 1) % 20 == 0:
                mean_dist = np.mean(np.linalg.norm(positions, axis=1))
                print(f"  Step {step+1}: Avg distance = {mean_dist:.4e}")
        return {'final_positions': positions,
                'mean_displacement': np.mean(np.linalg.norm(positions, axis=1))}


# ============================================================================
# 4. PHOTOVOLTAIC CELL SIMULATION
# ============================================================================

class PhotovoltaicCellSimulation:
    def __init__(self, num_simulations=100000):
        self.num_simulations = num_simulations

    def simulate_photovoltaic_cell(self, bandgap=1.12):
        print("\n☀️  PHOTOVOLTAIC CELL SIMULATION")
        print("="*80)
        wavelengths = np.random.uniform(300e-9, 2500e-9, self.num_simulations)
        photon_energies = (H_PLANCK * C_LIGHT) / wavelengths / E_CHARGE  # eV
        absorbed = photon_energies > bandgap
        QE = np.random.uniform(0.7, 0.95, self.num_simulations)
        eh_pairs = absorbed * QE
        # Normalize to realistic photocurrent density (mA/cm²)
        absorption_fraction = np.sum(absorbed) / self.num_simulations
        current_density_mA = absorption_fraction * 35.0  # 35 mA/cm² reference
        current = current_density_mA * 1e-3  # A (normalized)
        I0 = 1e-10  # dark saturation current
        V_oc = (K_B * 300 / E_CHARGE) * np.log(current / I0 + 1) if current > 0 else 0
        FF = np.clip(0.85 + np.random.normal(0, 0.05), 0.7, 0.9)
        efficiency = np.clip((current * V_oc * FF) / (1000 * 0.1), 0, 1)
        print(f"  Absorbed photons: {np.sum(absorbed):,} ({np.sum(absorbed)/self.num_simulations*100:.1f}%)")
        print(f"  Current (Jsc): {current:.4e} A")
        print(f"  Voltage (Voc): {V_oc:.4f} V")
        print(f"  Fill Factor: {FF:.4f}")
        print(f"  Efficiency: {efficiency*100:.2f}%")
        return {'wavelengths': wavelengths, 'photon_energies': photon_energies,
                'absorbed': absorbed, 'eh_pairs': eh_pairs,
                'current': current, 'voltage': V_oc, 'efficiency': efficiency}

    def simulate_uv_effect_on_cells(self):
        print("\n☀️  UV RADIATION EFFECTS ON CELLS")
        print("="*80)
        uv_intensities = np.random.uniform(0, 100, self.num_simulations)
        exposure_times = np.random.uniform(0, 24, self.num_simulations)
        uv_dose = uv_intensities * exposure_times
        dna_damage = np.minimum(uv_dose / 100, 1.0)
        apoptosis = np.minimum(dna_damage * 0.5, 1.0)
        mutation = np.minimum(dna_damage * 0.1, 0.3)
        ros = dna_damage * np.random.uniform(1e-15, 1e-12, self.num_simulations)
        low = np.sum(dna_damage < 0.3)
        med = np.sum((dna_damage >= 0.3) & (dna_damage < 0.7))
        high = np.sum(dna_damage >= 0.7)
        print(f"  Avg DNA damage: {np.mean(dna_damage):.4f}")
        print(f"  Low: {low:,}  Med: {med:,}  High: {high:,}")
        return {'uv_dose': uv_dose, 'dna_damage': dna_damage,
                'apoptosis_rate': apoptosis, 'mutation_rate': mutation,
                'ros_production': ros}


# ============================================================================
# 5. CELL MOTION UNDER UV
# ============================================================================

class CellMotionUnderUV:
    def __init__(self, num_simulations=1000):  # Reduced default for speed
        self.num_simulations = num_simulations

    def simulate_cell_motion_with_uv(self, grid_size=100, time_steps=100):
        print("\n🧬 CELL MOTION UNDER UV RADIATION")
        print("="*80)
        positions = np.random.uniform(0, grid_size, (self.num_simulations, 2))
        center = grid_size // 2
        # Build UV grid (vectorized)
        i_idx, j_idx = np.meshgrid(np.arange(grid_size), np.arange(grid_size), indexing='ij')
        uv_grid = 100 * np.exp(-((i_idx - center)**2 + (j_idx - center)**2) / (2 * 20**2))
        velocities = np.zeros((self.num_simulations, 2))
        for step in range(time_steps):
            gx = np.clip(positions[:, 0].astype(int), 0, grid_size-1)
            gy = np.clip(positions[:, 1].astype(int), 0, grid_size-1)
            # Gradient (simplified)
            gx1 = np.clip(gx+1, 0, grid_size-1); gx0 = np.clip(gx-1, 0, grid_size-1)
            gy1 = np.clip(gy+1, 0, grid_size-1); gy0 = np.clip(gy-1, 0, grid_size-1)
            grad_x = (uv_grid[gx1, gy] - uv_grid[gx0, gy]) / 2
            grad_y = (uv_grid[gx, gy1] - uv_grid[gx, gy0]) / 2
            velocities = -np.column_stack([grad_x, grad_y]) * 0.1
            positions += velocities
            positions = np.clip(positions, 0, grid_size)
            if (step + 1) % 20 == 0:
                mean_dist = np.mean(np.linalg.norm(positions - center, axis=1))
                print(f"  Step {step+1}: Avg dist from center = {mean_dist:.2f}")
        return {'final_positions': positions, 'uv_grid': uv_grid,
                'mean_distance': np.mean(np.linalg.norm(positions - center, axis=1))}


# ============================================================================
# 6. LATTICE OPTIMIZATION
# ============================================================================

class LatticeOptimization:
    def __init__(self, num_simulations=100000):
        self.num_simulations = num_simulations

    def simulate_lattice_structures(self):
        print("\n🔲 LATTICE STRUCTURES SIMULATION")
        print("="*80)
        lattices = {
            'Square':     {'a': 1.0, 'b': 1.0, 'angle': 90},
            'Hexagonal':  {'a': 1.0, 'b': 1.0, 'angle': 120},
            'Rectangular':{'a': 1.0, 'b': 1.5, 'angle': 90},
            'Oblique':    {'a': 1.0, 'b': 1.2, 'angle': 75}
        }
        results = {}
        for name, p in lattices.items():
            angle = np.radians(p['angle'])
            v1 = np.array([p['a'], 0])
            v2 = np.array([p['b']*np.cos(angle), p['b']*np.sin(angle)])
            area = abs(np.cross(v1, v2))
            pts = np.array([i*v1 + j*v2 for i in range(-5, 6) for j in range(-5, 6)])
            distances = [np.linalg.norm(pts[i]-pts[j])
                         for i in range(len(pts)) for j in range(i+1, min(i+8, len(pts)))
                         if np.linalg.norm(pts[i]-pts[j]) > 1e-10]
            print(f"\n📊 {name}: area={area:.4f}, density={1/area:.4f}")
            print(f"   Avg dist={np.mean(distances):.4f}, min={np.min(distances):.4f}")
            results[name] = {'area': area, 'density': 1/area,
                             'points': pts, 'distances': np.array(distances)}
        return results

    def optimize_lattice_for_efficiency(self):
        print("\n🔲 LATTICE EFFICIENCY OPTIMIZATION")
        print("="*80)
        spacings = np.linspace(0.1, 2.0, 100)
        efficiencies = [min((1/s) / (1 + s**2) * 0.3, 1.0) for s in spacings]
        efficiencies = np.array(efficiencies)
        best_idx = np.argmax(efficiencies)
        print(f"  Optimal spacing: {spacings[best_idx]:.4f}")
        print(f"  Max efficiency:  {efficiencies[best_idx]*100:.2f}%")
        return {'lattice_spacings': spacings, 'efficiencies': efficiencies,
                'optimal_spacing': spacings[best_idx],
                'optimal_efficiency': efficiencies[best_idx]}


# ============================================================================
# 7. COMPLETE PHOTOVOLTAIC SYSTEM
# ============================================================================

class CompletePhotovoltaicSystem:
    def __init__(self, num_simulations=10000):
        self.num_simulations = num_simulations
        self.atomic_sim = AtomicSimulation(num_simulations)
        self.photon_sim = PhotonSimulation(num_simulations)
        self.cell_sim = CellSimulation(num_simulations)
        self.pv_sim = PhotovoltaicCellSimulation(num_simulations)
        self.motion_sim = CellMotionUnderUV(min(num_simulations, 500))
        self.lattice_opt = LatticeOptimization(num_simulations)

    def run_complete_simulation(self):
        print("\n" + "="*80)
        print("🚀 COMPLETE PHOTOVOLTAIC SYSTEM SIMULATION")
        print("="*80)
        hydrogen   = self.atomic_sim.simulate_hydrogen_atom()
        photons    = self.photon_sim.simulate_photon_properties()
        interact   = self.photon_sim.simulate_photon_interactions()
        cells      = self.cell_sim.simulate_cell_dynamics()
        migration  = self.cell_sim.simulate_cell_migration(num_steps=50)
        pv_cells   = self.pv_sim.simulate_photovoltaic_cell()
        uv_effects = self.pv_sim.simulate_uv_effect_on_cells()
        motion     = self.motion_sim.simulate_cell_motion_with_uv(time_steps=50)
        lattices   = self.lattice_opt.simulate_lattice_structures()
        opt        = self.lattice_opt.optimize_lattice_for_efficiency()
        print("\n✅ COMPLETE SIMULATION FINISHED")
        return {
            'hydrogen': hydrogen, 'photons': photons, 'interactions': interact,
            'cells': cells, 'migration': migration, 'pv_cells': pv_cells,
            'uv_effects': uv_effects, 'motion': motion,
            'lattices': lattices, 'optimization': opt
        }

    def save_results_to_database(self, results, db_path="photovoltaic_results.db"):
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.executescript('''
            CREATE TABLE IF NOT EXISTS simulations (
                id INTEGER PRIMARY KEY, simulation_type TEXT,
                num_scenarios INTEGER, timestamp DATETIME DEFAULT CURRENT_TIMESTAMP);
            CREATE TABLE IF NOT EXISTS results (
                id INTEGER PRIMARY KEY, simulation_id INTEGER,
                metric_name TEXT, metric_value REAL,
                FOREIGN KEY (simulation_id) REFERENCES simulations(id));
        ''')
        cursor.execute('INSERT INTO simulations (simulation_type, num_scenarios) VALUES (?, ?)',
                       ('Complete PV System', self.num_simulations))
        sim_id = cursor.lastrowid
        metrics = {
            'PV_Efficiency': float(results['pv_cells']['efficiency']),
            'UV_DNA_Damage': float(np.mean(results['uv_effects']['dna_damage'])),
            'Cell_Growth_Rate': float(np.mean(results['cells']['growth_rates'])),
            'Photon_Absorption': results['interactions']['absorption'] / self.num_simulations,
            'Optimal_Lattice_Spacing': float(results['optimization']['optimal_spacing'])
        }
        for name, val in metrics.items():
            cursor.execute(
                'INSERT INTO results (simulation_id, metric_name, metric_value) VALUES (?, ?, ?)',
                (sim_id, name, val))
            print(f"  ✅ {name}: {val:.6f}")
        conn.commit()
        conn.close()
        print(f"\n💾 Saved to {db_path}")


# ============================================================================
# 8. VISUALIZATION
# ============================================================================

class ResultsVisualization:
    def plot_all_results(self, results):
        fig = plt.figure(figsize=(20, 20))

        # Hydrogen energies
        ax = fig.add_subplot(3, 3, 1)
        ax.hist(results['hydrogen']['energies'], bins=50, alpha=0.7, color='blue')
        ax.set_title('Hydrogen Atom Energies (eV)')
        ax.grid(True, alpha=0.3)

        # Photon wavelengths
        ax = fig.add_subplot(3, 3, 2)
        ax.hist(results['photons']['wavelengths']*1e9, bins=50, alpha=0.7, color='green')
        ax.set_title('Photon Wavelengths (nm)')
        ax.grid(True, alpha=0.3)

        # Cell sizes
        ax = fig.add_subplot(3, 3, 3)
        ax.hist(results['cells']['radii']*1e6, bins=50, alpha=0.7, color='red')
        ax.set_title('Cell Size Distribution (μm)')
        ax.grid(True, alpha=0.3)

        # PV efficiency
        ax = fig.add_subplot(3, 3, 4)
        eff = results['pv_cells']['efficiency']*100
        ax.text(0.5, 0.5, f'PV Efficiency\n{eff:.2f}%',
                ha='center', va='center', fontsize=18, weight='bold',
                transform=ax.transAxes)
        ax.axis('off')

        # UV damage
        ax = fig.add_subplot(3, 3, 5)
        ax.hist(results['uv_effects']['dna_damage'], bins=50, alpha=0.7, color='orange')
        ax.set_title('DNA Damage from UV')
        ax.grid(True, alpha=0.3)

        # Cell motion
        ax = fig.add_subplot(3, 3, 6)
        pos = results['motion']['final_positions']
        ax.scatter(pos[:, 0], pos[:, 1], alpha=0.3, s=2)
        ax.set_title('Cell Motion under UV')
        ax.grid(True, alpha=0.3)

        # Lattice optimization
        ax = fig.add_subplot(3, 3, 7)
        sp = results['optimization']['lattice_spacings']
        ef = results['optimization']['efficiencies']*100
        ax.plot(sp, ef, linewidth=2)
        ax.axvline(results['optimization']['optimal_spacing'], color='red', linestyle='--',
                   label=f"Optimal: {results['optimization']['optimal_spacing']:.3f}")
        ax.set_title('Lattice Efficiency Optimization')
        ax.legend()
        ax.grid(True, alpha=0.3)

        # Photon energy distribution
        ax = fig.add_subplot(3, 3, 8)
        energies_eV = results['photons']['energies'] / 1.602e-19
        ax.hist(energies_eV, bins=50, alpha=0.7, color='purple')
        ax.set_title('Photon Energies (eV)')
        ax.grid(True, alpha=0.3)

        # ATP production
        ax = fig.add_subplot(3, 3, 9)
        ax.hist(np.log10(results['cells']['atp_production'] + 1e-20),
                bins=50, alpha=0.7, color='teal')
        ax.set_title('log10(ATP Production) mol/s')
        ax.grid(True, alpha=0.3)

        plt.suptitle('🔬 COMPLETE PHOTOVOLTAIC SYSTEM SIMULATION', fontsize=14, weight='bold')
        plt.tight_layout()
        plt.savefig('photovoltaic_results.png', dpi=150, bbox_inches='tight')
        print("📊 Saved: photovoltaic_results.png")
        plt.show()


# ============================================================================
# MAIN
# ============================================================================

if __name__ == "__main__":
    system = CompletePhotovoltaicSystem(num_simulations=10000)
    results = system.run_complete_simulation()
    system.save_results_to_database(results)
    viz = ResultsVisualization()
    viz.plot_all_results(results)
