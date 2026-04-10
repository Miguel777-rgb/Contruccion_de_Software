#!/bin/bash
# Script para activar conda base y ejecutar el servidor Flask

# Activate conda base
eval "$(conda shell.bash hook)"
conda activate base

# Run Flask app
cd /home/mq/Documentos/Construccion_Software/Contruccion_de_Software
python back/app.py
