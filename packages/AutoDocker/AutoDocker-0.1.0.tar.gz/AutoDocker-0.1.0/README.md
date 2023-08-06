# AutoDocker

Simple program to quickly dock ligands using Autodock Vina.

[![PyPI version](https://badge.fury.io/py/AutoDocker.svg)](https://badge.fury.io/py/AutoDocker) [![Downloads](https://pepy.tech/badge/autodocker)](https://pepy.tech/project/autodocker)

## Installation:

```
pip install AutoDocker
```

## Usage:

#### Prepare receptor PDBQT

```
AutoDocker.protpdb2pdbqt("receptor.pdb")
```

#### Run docking calculation

```
AutoDocker.RunVina("path-to-vina-executable","receptor.pdbqt","ligand.pdbqt","config.txt")
```

More updates on running docking of a full database coming soon...