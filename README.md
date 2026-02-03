# Dynamics of Hydrogen Bonds in the Secondary Structures of Allosteric Protein *Avena sativa* Phototropin 1 (MD + ML)

This repository accompanies the study:

**Dynamics of hydrogen bonds in the secondary structures of allosteric protein *Avena sativa* phototropin 1**  
Ibrahim, M. T.; Trozzi, F.; Tao, P.  
*Computational and Structural Biotechnology Journal* 20 (2022), 50–64.  
DOI: https://doi.org/10.1016/j.csbj.2021.11.038 :contentReference[oaicite:1]{index=1}

This research investigates the **molecular origins of allosteric signal propagation** in the Light-Oxygen-Voltage 2 (LOV2) domain of the plant photoreceptor *Avena sativa* phototropin 1 (*AsLOV2*). The work focuses on how **hydrogen-bond networks and secondary structural elements** govern the conformational transitions between dark and light states.

---

## Motivation & Background

*AsLOV2* is a **blue-light receptor domain** used widely in optogenetics and photoswitch design due to its:
- monomeric stability in both dark and light states,
- rapid light-triggered structural transitions.

Despite many studies on LOV-type proteins, *the role of secondary structures and their hydrogen-bonding dynamics in allostery was not fully characterized*. :contentReference[oaicite:2]{index=2}

---

## Key Findings

### 1. 1.5-µs all-atom molecular dynamics simulations
Multiple MD simulations were performed for:
- dark state
- light state
- **helicity-enhancing mutants** (T406A, T407A)
- **helicity-disrupting mutants** (L408D, R410P)

These reveal how specific hydrogen bonds influence the structural transitions. :contentReference[oaicite:3]{index=3}

### 2. Role of the A′α Helix
The A′α helix is a **key allosteric control element**:
- Hydrogen bonds between residues (e.g., Thr407, Arg410) and surrounding β strands or the Jα helix are essential for functional switching.
- The **N-terminal hydrogen bond network** must be maintained for productive transitions. :contentReference[oaicite:4]{index=4}

### 3. Hydrogen Bond & Contact Analysis
Detailed hydrogen-bond tracking showed:
- conservation of specific contacts essential for dark-to-light transitions,
- disruption or formation of bonds correlates with secondary structure unfolding or stabilization. :contentReference[oaicite:5]{index=5}

### 4. Secondary Structure & Community Analysis
Using DSSP and network/community analysis, the study found that:
- β-sheet regions contribute significantly to allosteric signal propagation.
- Community structures change meaningfully between conformational states. :contentReference[oaicite:6]{index=6}

---

## Computational Methods

This work combines:
- **Long timescale molecular dynamics simulations** (∼1.5 μs),
- **Markov State Modeling (MSM)** to identify conformational metastable states,
- **Hydrogen bond and contact map analytics**,
- **Machine learning techniques** (e.g., clustering and community detection)
  to quantify structural relationships across states. :contentReference[oaicite:7]{index=7}

---

## Biological Insights

- The **A′α helix and its hydrogen bonds** (especially Thr407 and Arg410) function as regulatory hotspots during the dark-to-light transition.
- β-sheets not only provide structural integrity but also act as communication pathways linking distal regions.
- Mutations affecting helicity significantly alter the conformational landscape and signal propagation efficiency. :contentReference[oaicite:8]{index=8}

---

## Significance

This study provides *atomistic detail* on how local hydrogen-bond networks in secondary structures translate to **global allosteric conformational changes** in an important plant photoreceptor. It offers both:
- mechanistic explanations for *light-induced protein switching*,
- computational workflows useful for **molecular biophysics**, **photobiology**, and **optogenetic tool design**. :contentReference[oaicite:9]{index=9}

---

## Citing This Work

If you use the concepts, data, or methods in this repository, please cite:

Ibrahim, M. T.; Trozzi, F.; Tao, P. “Dynamics of hydrogen bonds in the secondary structures of allosteric protein *Avena sativa* phototropin 1.” *Comput. Struct. Biotechnol. J.* 20 (2022), 50–64. DOI: 10.1016/j.csbj.2021.11.038 :contentReference[oaicite:10]{index=10}

---
