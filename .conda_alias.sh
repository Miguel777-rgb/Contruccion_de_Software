#!/bin/bash
# File: .conda_alias.sh
# Add to your ~/.bashrc or ~/.zshrc:
# source path/to/.conda_alias.sh

# Quick aliases for this project
alias start-app='cd /home/mq/Documentos/Construccion_Software/Contruccion_de_Software && ./run_conda.sh'
alias setup-db='cd /home/mq/Documentos/Construccion_Software/Contruccion_de_Software && ./setup_db_conda.sh'
alias activate-task='conda activate base && cd /home/mq/Documentos/Construccion_Software/Contruccion_de_Software'

# Show available commands
echo "✅ Aliases cargados:"
echo "  - start-app     : Inicia el servidor"
echo "  - setup-db      : Configura la base de datos"
echo "  - activate-task : Activa conda base y entra al directorio"
