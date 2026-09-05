"""
Enumerações usadas pelo domínio de incidentes.

Mantidas em um módulo separado para que modelos ORM, regras de negócio
(services) e schemas da API compartilhem exatamente os mesmos valores,
evitando strings "soltas" espalhadas pelo código.
"""

import enum


class Severity(str, enum.Enum):
    LOW = "Low"
    MEDIUM = "Medium"
    HIGH = "High"
    CRITICAL = "Critical"


class Status(str, enum.Enum):
    OPEN = "Open"
    IN_PROGRESS = "In Progress"
    RESOLVED = "Resolved"