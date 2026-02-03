# Dynamics of Hydrogen Bonds in the Secondary Structures of Allosteric Protein *Avena sativa* Phototropin 1 (MD + ML)

This repository accompanies the study:

**Dynamics of hydrogen bonds in the secondary structures of allosteric protein *Avena sativa* phototropin 1**  
Ibrahim, M. T.; Trozzi, F.; Tao, P.  
*Computational and Structural Biotechnology Journal* 20 (2022), 50–64.  
DOI: https://doi.org/10.1016/j.csbj.2021.11.038

This research investigates the **molecular origins of allosteric signal propagation** in the Light-Oxygen-Voltage 2 (LOV2) domain of the plant photoreceptor *Avena sativa* phototropin 1 (*AsLOV2*). The work focuses on how **hydrogen-bond networks and secondary structural elements** govern the conformational transitions between dark and light states.

---

## Motivation & Background

*AsLOV2* is a **blue-light receptor domain** used widely in optogenetics and photoswitch design due to its:
- monomeric stability in both dark and light states,
- rapid light-triggered structural transitions.

Despite many studies on LOV-type proteins, *the role of secondary structures and their hydrogen-bonding dynamics in allostery was not fully characterized*. 

---

## Key Findings

### 1. 1.5-µs all-atom molecular dynamics simulations
Multiple MD simulations were performed for:
- dark state
- light state
- **helicity-enhancing mutants** (T406A, T407A)
- **helicity-disrupting mutants** (L408D, R410P)

These reveal how specific hydrogen bonds influence the structural transitions. 

### 2. Role of the A′α Helix
The A′α helix is a **key allosteric control element**:
- Hydrogen bonds between residues (e.g., Thr407, Arg410) and surrounding β strands or the Jα helix are essential for functional switching.
- The **N-terminal hydrogen bond network** must be maintained for productive transitions. 

### 3. Hydrogen Bond & Contact Analysis
Detailed hydrogen-bond tracking showed:
- conservation of specific contacts essential for dark-to-light transitions,
- disruption or formation of bonds correlates with secondary structure unfolding or stabilization.

### 4. Secondary Structure & Community Analysis
Using DSSP and network/community analysis, the study found that:
- β-sheet regions contribute significantly to allosteric signal propagation.
- Community structures change meaningfully between conformational states. 
---

## Computational Methods

This work combines:
- **Long timescale molecular dynamics simulations** (∼1.5 μs),
- **Markov State Modeling (MSM)** to identify conformational metastable states,
- **Hydrogen bond and contact map analytics**,
- **Machine learning techniques** (e.g., clustering and community detection)
  to quantify structural relationships across states.
---

## Biological Insights

- The **A′α helix and its hydrogen bonds** (especially Thr407 and Arg410) function as regulatory hotspots during the dark-to-light transition.
- β-sheets not only provide structural integrity but also act as communication pathways linking distal regions.
- Mutations affecting helicity significantly alter the conformational landscape and signal propagation efficiency. 

---

## Significance

This study provides *atomistic detail* on how local hydrogen-bond networks in secondary structures translate to **global allosteric conformational changes** in an important plant photoreceptor. It offers both:
- mechanistic explanations for *light-induced protein switching*,
- computational workflows useful for **molecular biophysics**, **photobiology**, and **optogenetic tool design**. 

---

- **CHARMM-System-Preparation**  
  Scripts and setup files used to generate parameter/topology files and solvated systems.

- **OpenMM Simulations**  
  Python scripts and settings used to run MD simulations in OpenMM.

- **ML & Community Analysis**  
  Code to extract features from simulation data, train ML models, compute similarity metrics, and detect communities.

---

## 🚀 How to Use This Repository

### 1. System Preparation

Prepare the *AsLOV2* structural system for simulation using the files under `CHARMM-System-Preparation/`.  
These typically include:

- topology (PSF/PDB files),
- force field parameter files,
- solvated coordinate sets.

Detailed preparatory commands are provided in the corresponding subfolder.

---

### 2. Running MD Simulations

Simulations are set up to sample conformational states of *AsLOV2* (dark state, light state, and variants).  
The scripts in `OpenMM Simulations/` handle:

- energy minimization
- equilibration stages
- production MD
- logging and checkpointing

Each script accepts arguments for:
- input coordinate and topology files,
- simulation length,
- temperature / pressure,
- output trajectories.

---

## 📊 Machine Learning & Structural Analysis

The *ML & Community Analysis* suite is designed to work on MD trajectory outputs to:

### • Extract descriptive features
Features such as **alpha-carbon distances**, **secondary-structure metrics**, and **hydrogen bond patterns** are extracted as numerical representation of conformations.

### • Train classifiers
Machine learning models (e.g., Decision Trees, Random Forests, Neural Networks) are trained to classify conformational states or to find patterns related to allosteric transitions.

### • Extract importance and structure
Feature importance measures highlight which structural elements or atom pairs contribute most strongly to state discrimination.

### • Build similarity / community maps
Similarity matrices and community detection reveal clusters of residues or structural subdomains that act together during conformational change.

Below is a script-level breakdown.

---

## 📜 Detailed Script Analysis

### **Feature Extraction**
- `extract_alpha_carbon_distances.py`  
  Extracts all pairwise alpha-carbon distances from MD trajectories using an MSMBuilder metadata table and saves them for downstream analysis.

### **Model Training**
- `train_decision_tree.py`  
  Trains a **Decision Tree classifier** on stacked feature arrays using cross-validation splits.

- `train_ovo_random_forest.py`  
  Trains a **One-vs-One RandomForest classifier** for multi-class discrimination of conformational states.

- `train_mlp.py`  
  Trains a **Multi-Layer Perceptron (MLP)** neural network classifier with configurable regularization.

### **Feature Importance**
- `compute_feature_importance.py`  
  Aggregates feature importance scores across estimators (e.g., random forests) and optionally plots cumulative importance.

### **Similarity Matrix**
- `build_similarity_matrix.py`  
  Converts a 1D importance vector into a symmetric similarity matrix representing relationships between residues or structural features.

### **Community Detection**
- `detect_communities.py`  
  Applies iterative local optimization to group nodes in a similarity graph into communities that minimize within-community costs.

### **Clustering**
- `kmeans_rmsd.py`  
  Performs MiniBatch KMeans clustering on 2D projection data (e.g., dihedral/RMSD features) and saves cluster labels.

---



## Citing This Work

If you use the concepts, data, or methods in this repository, please cite:

Ibrahim, M. T.; Trozzi, F.; Tao, P. “Dynamics of hydrogen bonds in the secondary structures of allosteric protein *Avena sativa* phototropin 1.” *Comput. Struct. Biotechnol. J.* 20 (2022), 50–64. DOI: 10.1016/j.csbj.2021.11.038 

---
