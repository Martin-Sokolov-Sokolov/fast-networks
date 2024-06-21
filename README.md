# Exploring the Markov Clustering Algorithm as a fast and reliable heuristic for large graphs

## Overview

In this project we present the MCL-Exp algorithm, an extension to the Markov Clustering Algorithm for community detection. We then compare this heuristic to two others, namely the Louvain and Fluid Communities algorithms. We compare them in terms of running time (seconds) and output quality.

## Prerequisites

Make sure you have Anaconda or Miniconda installed on your system. You can download it from [Anaconda's official website](https://www.anaconda.com/products/distribution#download-section) or [Miniconda's official website](https://docs.conda.io/en/latest/miniconda.html).

## Installation

### Step 1: Clone the Repository

```bash
git clone https://github.com/Martin-Sokolov-Sokolov/fast-networks
cd fast-networks
```

### Step 2: Create the Conda Environment

```bash
conda env create -f environment.yml
```

### Step 3: Activate the Environment

```bash
conda activate your_environment_name
```

### Usage

```bash
python main.py
```