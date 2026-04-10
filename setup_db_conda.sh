#!/bin/bash
# Script para ejecutar migraciones de BD usando conda base

# Activate conda base
eval "$(conda shell.bash hook)"
conda activate base

cd /home/mq/Documentos/Construccion_Software/Contruccion_de_Software

echo "🔄 Ejecutando setup de BD..."
python database/db_setup.py

echo "✅ Setup completado"
