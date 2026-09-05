"""Exceções do domínio de incidentes."""


class InvalidTransitionError(Exception):
    """Levantada quando uma transição de status não é permitida.

    Contém uma mensagem compreensível para ser repassada até o usuário
    final (via API -> frontend).
    """

    def __init__(self, message: str):
        super().__init__(message)
        self.message = message


class IncidentNotFoundError(Exception):
    """Levantada quando um incidente com o id informado não existe."""

    def __init__(self, incident_id: int):
        message = f"Incidente com id {incident_id} não encontrado."
        super().__init__(message)
        self.message = message
        self.incident_id = incident_id