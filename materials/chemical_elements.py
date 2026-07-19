"""
Advanced Chemical Elements and Materials Testing System
Document 13 - Full Implementation
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.optimize import minimize, differential_evolution
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestRegressor
try:
    import torch
    import torch.nn as nn
    from torch.optim import Adam
    HAS_TORCH = True
except ImportError:
    HAS_TORCH = False
import warnings
warnings.filterwarnings('ignore')


# ============================================================================
# 1. CHEMICAL ELEMENTS DATABASE
# ============================================================================

class ChemicalElementsDatabase:
    def __init__(self):
        self.elements = self._create_database()

    def _create_database(self):
        return {
            'Si': {
                'name': 'Silicon', 'atomic_number': 14, 'atomic_mass': 28.09,
                'bandgap': 1.12, 'electron_affinity': 1.39, 'ionization_energy': 8.15,
                'electronegativity': 1.90, 'thermal_conductivity': 149,
                'electrical_conductivity': 1e-3, 'refractive_index': 3.5,
                'density': 2330, 'melting_point': 1687, 'boiling_point': 3538,
                'cost_per_kg': 2.0, 'abundance': 27.7,
                'photovoltaic_efficiency': 0.22, 'stability': 0.95, 'toxicity': 0.1
            },
            'GaAs': {
                'name': 'Gallium Arsenide', 'atomic_number': 31, 'atomic_mass': 144.64,
                'bandgap': 1.42, 'electron_affinity': 3.97, 'ionization_energy': 5.99,
                'electronegativity': 1.81, 'thermal_conductivity': 55,
                'electrical_conductivity': 1e-6, 'refractive_index': 3.93,
                'density': 5320, 'melting_point': 1511, 'boiling_point': 1673,
                'cost_per_kg': 50.0, 'abundance': 0.0019,
                'photovoltaic_efficiency': 0.28, 'stability': 0.85, 'toxicity': 0.7
            },
            'CdTe': {
                'name': 'Cadmium Telluride', 'atomic_number': 48, 'atomic_mass': 240.01,
                'bandgap': 1.50, 'electron_affinity': 4.28, 'ionization_energy': 8.99,
                'electronegativity': 1.69, 'thermal_conductivity': 6.2,
                'electrical_conductivity': 1e-7, 'refractive_index': 2.67,
                'density': 5850, 'melting_point': 1365, 'boiling_point': 1650,
                'cost_per_kg': 100.0, 'abundance': 0.00016,
                'photovoltaic_efficiency': 0.22, 'stability': 0.80, 'toxicity': 0.95
            },
            'CIGS': {
                'name': 'Copper Indium Gallium Selenide', 'atomic_number': 29,
                'atomic_mass': 393.21, 'bandgap': 1.04, 'electron_affinity': 4.50,
                'ionization_energy': 7.73, 'electronegativity': 1.90,
                'thermal_conductivity': 3.0, 'electrical_conductivity': 1e-8,
                'refractive_index': 2.50, 'density': 5770,
                'melting_point': 1268, 'boiling_point': 1500,
                'cost_per_kg': 150.0, 'abundance': 0.00004,
                'photovoltaic_efficiency': 0.23, 'stability': 0.88, 'toxicity': 0.5
            },
            'Perovskite': {
                'name': 'Methylammonium Lead Iodide', 'atomic_number': 82,
                'atomic_mass': 391.63, 'bandgap': 1.55, 'electron_affinity': 3.93,
                'ionization_energy': 7.42, 'electronegativity': 2.33,
                'thermal_conductivity': 0.5, 'electrical_conductivity': 1e-9,
                'refractive_index': 2.40, 'density': 4150,
                'melting_point': 330, 'boiling_point': 550,
                'cost_per_kg': 5.0, 'abundance': 0.0014,
                'photovoltaic_efficiency': 0.25, 'stability': 0.60, 'toxicity': 0.8
            },
            'Pt': {
                'name': 'Platinum', 'atomic_number': 78, 'atomic_mass': 195.08,
                'bandgap': 0.0, 'electron_affinity': 2.13, 'ionization_energy': 8.96,
                'electronegativity': 2.28, 'thermal_conductivity': 71.6,
                'electrical_conductivity': 9.43e6, 'refractive_index': 0.0,
                'density': 21450, 'melting_point': 2041, 'boiling_point': 4098,
                'cost_per_kg': 40000.0, 'abundance': 0.0000037,
                'photovoltaic_efficiency': 0.0, 'stability': 1.0, 'toxicity': 0.1,
                'catalyst_activity': 0.95
            },
            'Ni': {
                'name': 'Nickel', 'atomic_number': 28, 'atomic_mass': 58.69,
                'bandgap': 0.0, 'electron_affinity': 1.16, 'ionization_energy': 7.64,
                'electronegativity': 1.91, 'thermal_conductivity': 90.7,
                'electrical_conductivity': 1.43e7, 'refractive_index': 0.0,
                'density': 8908, 'melting_point': 1728, 'boiling_point': 3186,
                'cost_per_kg': 10.0, 'abundance': 0.0084,
                'photovoltaic_efficiency': 0.0, 'stability': 0.85, 'toxicity': 0.3,
                'catalyst_activity': 0.70
            },
            'Fe': {
                'name': 'Iron', 'atomic_number': 26, 'atomic_mass': 55.85,
                'bandgap': 0.0, 'electron_affinity': 0.15, 'ionization_energy': 7.87,
                'electronegativity': 1.83, 'thermal_conductivity': 80.4,
                'electrical_conductivity': 1.04e7, 'refractive_index': 0.0,
                'density': 7874, 'melting_point': 1811, 'boiling_point': 3134,
                'cost_per_kg': 0.5, 'abundance': 5.05,
                'photovoltaic_efficiency': 0.0, 'stability': 0.60, 'toxicity': 0.2,
                'catalyst_activity': 0.60
            },
            'Co': {
                'name': 'Cobalt', 'atomic_number': 27, 'atomic_mass': 58.93,
                'bandgap': 0.0, 'electron_affinity': 0.66, 'ionization_energy': 7.88,
                'electronegativity': 1.88, 'thermal_conductivity': 100.0,
                'electrical_conductivity': 1.67e7, 'refractive_index': 0.0,
                'density': 8900, 'melting_point': 1768, 'boiling_point': 3200,
                'cost_per_kg': 15.0, 'abundance': 0.0025,
                'photovoltaic_efficiency': 0.0, 'stability': 0.75, 'toxicity': 0.4,
                'catalyst_activity': 0.75
            }
        }

    def get_element_properties(self, element_symbol):
        return self.elements.get(element_symbol, None)

    def list_all_elements(self):
        return list(self.elements.keys())

    def compare_elements(self, elements_list):
        print("\n🧪 CHEMICAL ELEMENTS COMPARISON")
        print("="*100)
        df = pd.DataFrame([self.elements[elem] for elem in elements_list],
                          index=elements_list)
        print(df.to_string())
        return df


# ============================================================================
# 2. MATERIAL SCREENING AND SCORING
# ============================================================================

class MaterialScreening:
    def __init__(self, chem_db):
        self.chem_db = chem_db
        self.scaler = StandardScaler()

    def calculate_material_score(self, element_symbol, weights=None):
        if weights is None:
            weights = {
                'efficiency': 0.25, 'stability': 0.20, 'cost': 0.20,
                'abundance': 0.15, 'thermal': 0.10, 'toxicity': 0.10
            }
        props = self.chem_db.get_element_properties(element_symbol)
        if props is None:
            return None
        scores = {
            'efficiency': np.clip(props.get('photovoltaic_efficiency', 0) / 0.30, 0, 1),
            'stability': np.clip(props.get('stability', 0), 0, 1),
            'cost': np.clip(1 - (np.log10(props.get('cost_per_kg', 1) + 1) / 5), 0, 1),
            'abundance': np.clip(np.log10(props.get('abundance', 0.0001) + 1) / 3, 0, 1),
            'thermal': np.clip(props.get('thermal_conductivity', 1) / 150, 0, 1),
            'toxicity': np.clip(1 - props.get('toxicity', 0), 0, 1)
        }
        total_score = sum(scores[key] * weights[key] for key in weights)
        return {'element': element_symbol, 'total_score': total_score,
                'component_scores': scores, 'properties': props}

    def screen_all_materials(self, num_simulations=1000000):
        print("\n🧪 MATERIAL SCREENING - ALL ELEMENTS")
        print("="*100)
        results = []
        for element in self.chem_db.list_all_elements():
            scores = []
            for _ in range(100):
                weights = {k: np.random.uniform(lo, hi) for k, (lo, hi) in {
                    'efficiency': (0.15, 0.35), 'stability': (0.15, 0.25),
                    'cost': (0.15, 0.25), 'abundance': (0.10, 0.20),
                    'thermal': (0.05, 0.15), 'toxicity': (0.05, 0.15)
                }.items()}
                total = sum(weights.values())
                weights = {k: v/total for k, v in weights.items()}
                r = self.calculate_material_score(element, weights)
                scores.append(r['total_score'])
            avg = np.mean(scores)
            result = self.calculate_material_score(element)
            result.update({'avg_score': avg, 'std_score': np.std(scores),
                           'min_score': np.min(scores), 'max_score': np.max(scores)})
            results.append(result)
            print(f"📊 {element}: avg={avg:.4f} ± {np.std(scores):.4f}")
        results.sort(key=lambda x: x['avg_score'], reverse=True)
        print("\n🏆 RANKED MATERIALS:")
        for i, r in enumerate(results, 1):
            print(f"{i}. {r['element']}: {r['avg_score']:.4f}")
        return results


# ============================================================================
# 3. CATALYST OPTIMIZATION
# ============================================================================

class CatalystOptimization:
    def __init__(self, chem_db):
        self.chem_db = chem_db
        self.num_simulations = 1000000

    def calculate_catalyst_efficiency(self, catalyst_composition, temperature=300, pressure=1.0):
        total_efficiency = total_cost = total_stability = 0
        for element, pct in catalyst_composition.items():
            props = self.chem_db.get_element_properties(element)
            if props is None:
                continue
            activity = props.get('catalyst_activity', 0.5)
            temp_factor = np.exp(-0.001 * (temperature - 300)**2 / 300)
            pressure_factor = np.log(pressure + 1) / np.log(2)
            total_efficiency += activity * temp_factor * pressure_factor * pct
            total_cost += props.get('cost_per_kg', 1) * pct
            total_stability += props.get('stability', 0.5) * pct
        total_efficiency = np.clip(total_efficiency, 0, 1)
        return {
            'efficiency': total_efficiency,
            'cost': total_cost,
            'stability': total_stability,
            'cost_efficiency_ratio': total_efficiency / (total_cost + 1)
        }

    def optimize_catalyst_composition(self):
        print("\n⚗️  CATALYST COMPOSITION OPTIMIZATION")
        print("="*100)
        catalyst_elements = ['Pt', 'Ni', 'Fe', 'Co']

        def objective(composition):
            s = np.sum(composition)
            if s == 0:
                return 1e6
            norm = composition / s
            comp_dict = {e: norm[i] for i, e in enumerate(catalyst_elements)}
            result = self.calculate_catalyst_efficiency(comp_dict)
            return -(result['efficiency'] / (result['cost'] + 1) + result['stability'] * 0.5)

        bounds = [(0, 1)] * len(catalyst_elements)
        result = differential_evolution(objective, bounds, seed=42, maxiter=1000, popsize=30)
        best = result.x / np.sum(result.x)
        best_dict = {e: best[i] for i, e in enumerate(catalyst_elements)}
        metrics = self.calculate_catalyst_efficiency(best_dict)
        print("📊 OPTIMAL CATALYST:")
        for elem, pct in best_dict.items():
            print(f"  {elem}: {pct*100:.2f}%")
        print(f"  Efficiency: {metrics['efficiency']:.4f}")
        print(f"  Cost: ${metrics['cost']:.2f}/kg")
        return best_dict, metrics

    def simulate_catalyst_performance(self, catalyst_composition, num_scenarios=10000):
        print(f"\n⚗️  CATALYST PERFORMANCE SIMULATION ({num_scenarios:,} scenarios)")
        temperatures = np.random.uniform(250, 400, num_scenarios)
        pressures = np.random.uniform(0.5, 2.0, num_scenarios)
        humidity = np.random.uniform(0, 1, num_scenarios)
        efficiencies, stabilities = [], []
        for i in range(num_scenarios):
            m = self.calculate_catalyst_efficiency(catalyst_composition,
                                                    temperature=temperatures[i],
                                                    pressure=pressures[i])
            m['stability'] *= (1 - 0.3 * humidity[i])
            efficiencies.append(m['efficiency'])
            stabilities.append(m['stability'])
        efficiencies = np.array(efficiencies)
        stabilities = np.array(stabilities)
        print(f"  Efficiency avg: {np.mean(efficiencies):.4f} ± {np.std(efficiencies):.4f}")
        print(f"  Stability avg:  {np.mean(stabilities):.4f} ± {np.std(stabilities):.4f}")
        return {'efficiencies': efficiencies, 'stabilities': stabilities}


# ============================================================================
# 4. QUANTUM MATERIAL PREDICTION (Neural Network)
# ============================================================================

class QuantumMaterialPrediction:
    def __init__(self, chem_db):
        self.chem_db = chem_db
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    def create_neural_network_predictor(self, input_size=10):
        class MaterialPredictor(nn.Module):
            def __init__(self, inp, hidden=64):
                super().__init__()
                self.net = nn.Sequential(
                    nn.Linear(inp, hidden), nn.ReLU(), nn.Dropout(0.2),
                    nn.Linear(hidden, hidden), nn.ReLU(), nn.Dropout(0.2),
                    nn.Linear(hidden, hidden), nn.ReLU(),
                    nn.Linear(hidden, 1), nn.Sigmoid()
                )
            def forward(self, x):
                return self.net(x)
        return MaterialPredictor(input_size).to(self.device)

    def train_predictor(self, num_epochs=100):
        print("\n🤖 TRAINING MATERIAL PREDICTOR")
        print("="*100)
        elements = self.chem_db.list_all_elements()
        X, y = [], []
        for elem in elements:
            props = self.chem_db.get_element_properties(elem)
            X.append([
                props['atomic_number'], props['atomic_mass'],
                props.get('bandgap', 0), props.get('electron_affinity', 0),
                props.get('ionization_energy', 0), props.get('electronegativity', 0),
                np.log10(props.get('thermal_conductivity', 1) + 1),
                np.log10(props.get('electrical_conductivity', 1e-10) + 1),
                np.log10(props.get('density', 1) + 1),
                np.log10(props.get('cost_per_kg', 1) + 1)
            ])
            y.append(props.get('photovoltaic_efficiency', 0))
        X, y = np.array(X), np.array(y).reshape(-1, 1)
        scaler = StandardScaler()
        X = scaler.fit_transform(X)
        Xt = torch.FloatTensor(X).to(self.device)
        yt = torch.FloatTensor(y).to(self.device)
        model = self.create_neural_network_predictor(input_size=X.shape[1])
        optimizer = Adam(model.parameters(), lr=0.01)
        criterion = nn.MSELoss()
        for epoch in range(num_epochs):
            optimizer.zero_grad()
            loss = criterion(model(Xt), yt)
            loss.backward()
            optimizer.step()
            if (epoch + 1) % 10 == 0:
                print(f"  Epoch {epoch+1}: Loss = {loss.item():.6f}")
        return model, scaler, X.shape[1]

    def predict_new_material(self, model, scaler, atomic_number, atomic_mass,
                              bandgap, electron_affinity):
        features = np.array([[atomic_number, atomic_mass, bandgap, electron_affinity,
                               0, 0, 0, 0, 0, 0]])
        features = scaler.transform(features)
        with torch.no_grad():
            pred = model(torch.FloatTensor(features).to(self.device))
        return pred.cpu().numpy()[0][0]


# ============================================================================
# 5. COUPLING MECHANISMS
# ============================================================================

class CouplingMechanisms:
    def __init__(self, num_simulations=100000):
        self.num_simulations = num_simulations

    def simulate_electron_phonon_coupling(self, material_properties):
        print("\n🔗 ELECTRON-PHONON COUPLING SIMULATION")
        print("="*100)
        lambda_ep = np.random.uniform(0.1, 0.5, self.num_simulations)
        temperatures = np.random.uniform(100, 400, self.num_simulations)
        omega_phonon = np.random.uniform(1e12, 1e14, self.num_simulations)
        scattering_rates = lambda_ep * omega_phonon * np.exp(
            -omega_phonon / (1.38e-23 * temperatures / 1.602e-19))
        mobility = 1 / (scattering_rates + 1e-10)
        conductivity = mobility * 1.602e-19
        print(f"  Avg coupling constant: {np.mean(lambda_ep):.4f}")
        print(f"  Avg mobility: {np.mean(mobility):.4e} cm²/V·s")
        return {'lambda_ep': lambda_ep, 'scattering_rates': scattering_rates,
                'mobility': mobility, 'conductivity': conductivity}

    def simulate_exciton_binding_energy(self):
        print("\n🔗 EXCITON BINDING ENERGY SIMULATION")
        print("="*100)
        epsilon_r = np.random.uniform(3.0, 12.0, self.num_simulations)
        m_e = np.random.uniform(0.1, 1.0, self.num_simulations)
        m_h = np.random.uniform(0.1, 1.0, self.num_simulations)
        mu = (m_e * m_h) / (m_e + m_h)
        E_b = 13.6 * mu / (epsilon_r**2)
        print(f"  Avg binding energy: {np.mean(E_b):.4f} eV")
        print(f"  Range: [{np.min(E_b):.4f}, {np.max(E_b):.4f}] eV")
        return {'binding_energy': E_b, 'epsilon_r': epsilon_r, 'mu': mu}

    def simulate_band_alignment(self, material1_props, material2_props):
        print("\n🔗 BAND ALIGNMENT SIMULATION")
        print("="*100)
        bg1 = material1_props.get('bandgap', 1.12)
        bg2 = material2_props.get('bandgap', 1.42)
        ea1 = material1_props.get('electron_affinity', 4.0)
        ea2 = material2_props.get('electron_affinity', 4.0)
        delta_Ec = ea1 - ea2
        delta_Ev = (ea1 + bg1) - (ea2 + bg2)
        if delta_Ec > 0 and delta_Ev > 0:
            alignment_type = "Type I (Straddling)"
        elif delta_Ec > 0 and delta_Ev < 0:
            alignment_type = "Type II (Staggered)"
        else:
            alignment_type = "Type III (Broken Gap)"
        print(f"  ΔE_c = {delta_Ec:.4f} eV, ΔE_v = {delta_Ev:.4f} eV")
        print(f"  Band alignment: {alignment_type}")
        return {'delta_Ec': delta_Ec, 'delta_Ev': delta_Ev,
                'alignment_type': alignment_type}


# ============================================================================
# 6. ADVANCED OPTIMIZATION ALGORITHMS
# ============================================================================

class AdvancedOptimizationAlgorithms:
    def __init__(self, num_simulations=100000):
        self.num_simulations = num_simulations

    def _evaluate_composition(self, composition):
        return (composition[0]*0.3 + composition[1]*0.25 +
                composition[2]*0.25 + composition[3]*0.2)

    def genetic_algorithm_optimization(self, num_generations=100, population_size=50):
        print("\n🧬 GENETIC ALGORITHM OPTIMIZATION")
        print("="*100)
        population = np.random.uniform(0, 1, (population_size, 4))
        population = population / population.sum(axis=1, keepdims=True)
        fitness_history = []
        for generation in range(num_generations):
            fitness = np.array([self._evaluate_composition(c) for c in population])
            fitness_history.append(np.max(fitness))
            selected = [population[np.random.choice(len(population), min(3, len(population)), replace=False)[
                np.argmax(fitness[np.random.choice(len(population), min(3, len(population)), replace=False)])]]
                for _ in range(population_size)]
            selected = np.array([
                population[np.argmax(fitness[np.random.choice(len(population), min(3, len(population)), replace=False)])]
                for _ in range(population_size)])
            offspring = []
            for i in range(population_size):
                p1 = selected[i]
                p2 = selected[(i + 1) % population_size]
                cp = np.random.randint(1, 4)
                child = np.concatenate([p1[:cp], p2[cp:]])
                if np.random.random() < 0.1:
                    child[np.random.randint(0, 4)] = np.random.uniform(0, 1)
                offspring.append(child)
            offspring = np.array(offspring)
            offspring = offspring / offspring.sum(axis=1, keepdims=True)
            population = offspring
            if (generation + 1) % 10 == 0:
                print(f"  Gen {generation+1}: best={fitness_history[-1]:.4f}")
        final_fitness = np.array([self._evaluate_composition(c) for c in population])
        best = population[np.argmax(final_fitness)]
        print(f"\n📊 Best composition: {best}")
        return best, fitness_history

    def particle_swarm_optimization(self, num_particles=50, num_iterations=100):
        print("\n🐝 PARTICLE SWARM OPTIMIZATION")
        print("="*100)
        positions = np.random.uniform(0, 1, (num_particles, 4))
        positions = positions / positions.sum(axis=1, keepdims=True)
        velocities = np.random.uniform(-0.1, 0.1, (num_particles, 4))
        best_positions = positions.copy()
        best_fitness = np.array([self._evaluate_composition(p) for p in positions])
        global_best = positions[np.argmax(best_fitness)].copy()
        fitness_history = []
        w, c1, c2 = 0.7, 1.5, 1.5
        for it in range(num_iterations):
            for i in range(num_particles):
                r1, r2 = np.random.uniform(0, 1, 4), np.random.uniform(0, 1, 4)
                velocities[i] = (w*velocities[i] + c1*r1*(best_positions[i]-positions[i])
                                 + c2*r2*(global_best-positions[i]))
                positions[i] = np.clip(positions[i] + velocities[i], 0, 1)
                positions[i] /= positions[i].sum()
            current_fitness = np.array([self._evaluate_composition(p) for p in positions])
            improved = current_fitness > best_fitness
            best_positions[improved] = positions[improved]
            best_fitness[improved] = current_fitness[improved]
            global_best = best_positions[np.argmax(best_fitness)].copy()
            fitness_history.append(np.max(best_fitness))
            if (it + 1) % 10 == 0:
                print(f"  Iter {it+1}: best={fitness_history[-1]:.4f}")
        print(f"\n📊 Best PSO composition: {global_best}")
        return global_best, fitness_history


# ============================================================================
# 7. COMPLETE INTEGRATED SYSTEM
# ============================================================================

class CompleteChemicalOptimizationSystem:
    def __init__(self, num_simulations=100000):
        self.num_simulations = num_simulations
        self.chem_db = ChemicalElementsDatabase()
        self.screening = MaterialScreening(self.chem_db)
        self.catalyst_opt = CatalystOptimization(self.chem_db)
        self.coupling = CouplingMechanisms(num_simulations)
        self.algorithms = AdvancedOptimizationAlgorithms(num_simulations)

    def run_complete_analysis(self):
        print("\n" + "="*100)
        print("🧪 COMPLETE CHEMICAL OPTIMIZATION SYSTEM")
        print("="*100)
        material_scores = self.screening.screen_all_materials()
        best_catalyst, best_metrics = self.catalyst_opt.optimize_catalyst_composition()
        ep_coupling = self.coupling.simulate_electron_phonon_coupling({})
        exciton = self.coupling.simulate_exciton_binding_energy()
        ga_best, ga_history = self.algorithms.genetic_algorithm_optimization(50)
        pso_best, pso_history = self.algorithms.particle_swarm_optimization(50)
        print("\n✅ COMPLETE ANALYSIS FINISHED")
        return {
            'material_scores': material_scores,
            'best_catalyst': best_catalyst,
            'catalyst_metrics': best_metrics,
            'coupling_data': ep_coupling,
            'exciton_data': exciton,
            'ga_results': (ga_best, ga_history),
            'pso_results': (pso_best, pso_history)
        }

    def save_results(self, results, filename="chemical_results.csv"):
        summary = [{
            'Material': m['element'],
            'Total_Score': m['total_score'],
            **{k: v for k, v in m['component_scores'].items()}
        } for m in results['material_scores']]
        pd.DataFrame(summary).to_csv(filename, index=False)
        print(f"✅ Saved to {filename}")


# ============================================================================
# 8. VISUALIZATION
# ============================================================================

class ChemicalOptimizationVisualization:
    def plot_material_comparison(self, material_scores):
        fig, axes = plt.subplots(2, 2, figsize=(15, 12))
        materials = [m['element'] for m in material_scores]
        scores = [m['total_score'] for m in material_scores]
        axes[0, 0].barh(materials, scores, color='steelblue')
        axes[0, 0].set_title('Material Scores')
        components = ['efficiency', 'stability', 'cost', 'abundance', 'thermal', 'toxicity']
        for m in material_scores[:3]:
            axes[0, 1].plot(components, [m['component_scores'][c] for c in components],
                            marker='o', label=m['element'])
        axes[0, 1].legend()
        axes[0, 1].set_title('Component Scores (Top 3)')
        for m in material_scores:
            axes[1, 0].scatter(m['properties']['cost_per_kg'],
                               m['properties']['photovoltaic_efficiency'],
                               s=100, label=m['element'])
        axes[1, 0].set_xscale('log')
        axes[1, 0].set_title('Cost vs Efficiency')
        axes[1, 0].legend()
        for m in material_scores:
            axes[1, 1].scatter(m['properties']['toxicity'],
                               m['properties']['stability'],
                               s=100, label=m['element'])
        axes[1, 1].set_title('Stability vs Toxicity')
        axes[1, 1].legend()
        plt.tight_layout()
        plt.savefig('material_comparison.png', dpi=150, bbox_inches='tight')
        print("📊 Saved: material_comparison.png")
        plt.show()

    def plot_optimization_convergence(self, ga_history, pso_history):
        plt.figure(figsize=(12, 6))
        plt.plot(ga_history, label='Genetic Algorithm', linewidth=2)
        plt.plot(pso_history, label='Particle Swarm', linewidth=2)
        plt.xlabel('Iteration')
        plt.ylabel('Best Fitness')
        plt.title('Optimization Convergence')
        plt.legend()
        plt.grid(True, alpha=0.3)
        plt.savefig('optimization_convergence.png', dpi=150, bbox_inches='tight')
        print("📊 Saved: optimization_convergence.png")
        plt.show()


# ============================================================================
# MAIN
# ============================================================================

if __name__ == "__main__":
    system = CompleteChemicalOptimizationSystem(num_simulations=10000)
    results = system.run_complete_analysis()
    system.save_results(results)
    viz = ChemicalOptimizationVisualization()
    viz.plot_material_comparison(results['material_scores'])
    viz.plot_optimization_convergence(results['ga_results'][1], results['pso_results'][1])
