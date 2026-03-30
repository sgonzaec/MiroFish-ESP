"""
Módulo de comunicación IPC para simulación
Para comunicación entre el backend Flask y los scripts de simulación

Implementa un patrón comando/respuesta simple a través del sistema de archivos:
1. Flask escribe comandos en el directorio commands/
2. El script de simulación sondea el directorio de comandos, ejecuta y escribe respuestas en responses/
3. Flask sondea el directorio de respuestas para obtener resultados
"""

import os
import json
import time
import uuid
from typing import Dict, Any, Optional, List
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum

from ..utils.logger import get_logger

logger = get_logger('mirofish.simulation_ipc')


class CommandType(str, Enum):
    """Tipos de comando"""
    INTERVIEW = "interview"           # Entrevista a un agente individual
    BATCH_INTERVIEW = "batch_interview"  # Entrevista en lote
    CLOSE_ENV = "close_env"           # Cerrar entorno


class CommandStatus(str, Enum):
    """Estado del comando"""
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"


@dataclass
class IPCCommand:
    """Comando IPC"""
    command_id: str
    command_type: CommandType
    args: Dict[str, Any]
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "command_id": self.command_id,
            "command_type": self.command_type.value,
            "args": self.args,
            "timestamp": self.timestamp
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'IPCCommand':
        return cls(
            command_id=data["command_id"],
            command_type=CommandType(data["command_type"]),
            args=data.get("args", {}),
            timestamp=data.get("timestamp", datetime.now().isoformat())
        )


@dataclass
class IPCResponse:
    """Respuesta IPC"""
    command_id: str
    status: CommandStatus
    result: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "command_id": self.command_id,
            "status": self.status.value,
            "result": self.result,
            "error": self.error,
            "timestamp": self.timestamp
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'IPCResponse':
        return cls(
            command_id=data["command_id"],
            status=CommandStatus(data["status"]),
            result=data.get("result"),
            error=data.get("error"),
            timestamp=data.get("timestamp", datetime.now().isoformat())
        )


class SimulationIPCClient:
    """
    Cliente IPC de simulación (usado por Flask)

    Para enviar comandos al proceso de simulación y esperar respuestas
    """
    
    def __init__(self, simulation_dir: str):
        """
        Inicializar cliente IPC
        
        Args:
            simulation_dir: directorio de datos de simulación
        """
        self.simulation_dir = simulation_dir
        self.commands_dir = os.path.join(simulation_dir, "ipc_commands")
        self.responses_dir = os.path.join(simulation_dir, "ipc_responses")
        
        # Asegurar que el directorio existe
        os.makedirs(self.commands_dir, exist_ok=True)
        os.makedirs(self.responses_dir, exist_ok=True)
    
    def send_command(
        self,
        command_type: CommandType,
        args: Dict[str, Any],
        timeout: float = 180.0,
        poll_interval: float = 0.5
    ) -> IPCResponse:
        """
        Enviar comando y esperar respuesta
        
        Args:
            command_type: tipo de comando
            args: argumentos del comando
            timeout: tiempo de espera (segundos)
            poll_interval: intervalo de sondeo (segundos)
            
        Returns:
            IPCResponse
            
        Raises:
            TimeoutError: tiempo de espera de respuesta agotado
        """
        command_id = str(uuid.uuid4())
        command = IPCCommand(
            command_id=command_id,
            command_type=command_type,
            args=args
        )
        
        # Escribir archivo de comando
        command_file = os.path.join(self.commands_dir, f"{command_id}.json")
        with open(command_file, 'w', encoding='utf-8') as f:
            json.dump(command.to_dict(), f, ensure_ascii=False, indent=2)
        
        logger.info(f"Enviando comando IPC: {command_type.value}, command_id={command_id}")
        
        # Esperar respuesta
        response_file = os.path.join(self.responses_dir, f"{command_id}.json")
        start_time = time.time()
        
        while time.time() - start_time < timeout:
            if os.path.exists(response_file):
                try:
                    with open(response_file, 'r', encoding='utf-8') as f:
                        response_data = json.load(f)
                    response = IPCResponse.from_dict(response_data)
                    
                    # Limpiar archivos de comando y respuesta
                    try:
                        os.remove(command_file)
                        os.remove(response_file)
                    except OSError:
                        pass
                    
                    logger.info(f"Respuesta IPC recibida: command_id={command_id}, status={response.status.value}")
                    return response
                except (json.JSONDecodeError, KeyError) as e:
                    logger.warning(f"Error al analizar respuesta: {e}")
            
            time.sleep(poll_interval)
        
        # Tiempo de espera agotado
        logger.error(f"Tiempo de espera de respuesta IPC agotado: command_id={command_id}")
        
        # Limpiar archivo de comando
        try:
            os.remove(command_file)
        except OSError:
            pass
        
        raise TimeoutError(f"Tiempo de espera de respuesta del comando agotado ({timeout}s)")
    
    def send_interview(
        self,
        agent_id: int,
        prompt: str,
        platform: str = None,
        timeout: float = 180.0
    ) -> IPCResponse:
        """
        Enviar comando de entrevista a un agente individual
        
        Args:
            agent_id: Agent ID
            prompt: pregunta de la entrevista
            platform: plataforma especificada (opcional)
                - "twitter": solo entrevistar en plataforma Twitter
                - "reddit": solo entrevistar en plataforma Reddit  
                - None: entrevistar en ambas plataformas en simulación dual, o en la plataforma activa en simulación de una sola plataforma
            timeout: tiempo de espera
            
        Returns:
            IPCResponse, el campo result contiene el resultado de la entrevista
        """
        args = {
            "agent_id": agent_id,
            "prompt": prompt
        }
        if platform:
            args["platform"] = platform
            
        return self.send_command(
            command_type=CommandType.INTERVIEW,
            args=args,
            timeout=timeout
        )
    
    def send_batch_interview(
        self,
        interviews: List[Dict[str, Any]],
        platform: str = None,
        timeout: float = 300.0
    ) -> IPCResponse:
        """
        Enviar comando de entrevista en lote
        
        Args:
            interviews: lista de entrevistas, cada elemento contiene {"agent_id": int, "prompt": str, "platform": str(opcional)}
            platform: plataforma predeterminada (opcional, se sobreescribe por el platform de cada entrevista)
                - "twitter": por defecto solo entrevistar en Twitter
                - "reddit": por defecto solo entrevistar en Reddit
                - None: en simulación dual, cada agente es entrevistado en ambas plataformas
            timeout: tiempo de espera
            
        Returns:
            IPCResponse, el campo result contiene todos los resultados de entrevistas
        """
        args = {"interviews": interviews}
        if platform:
            args["platform"] = platform
            
        return self.send_command(
            command_type=CommandType.BATCH_INTERVIEW,
            args=args,
            timeout=timeout
        )
    
    def send_close_env(self, timeout: float = 90.0) -> IPCResponse:
        """
        Enviar comando de cierre del entorno
        
        Args:
            timeout: tiempo de espera
            
        Returns:
            IPCResponse
        """
        return self.send_command(
            command_type=CommandType.CLOSE_ENV,
            args={},
            timeout=timeout
        )
    
    def check_env_alive(self) -> bool:
        """
        Verificar si el entorno de simulación está activo
        
        Se determina verificando el archivo env_status.json
        """
        status_file = os.path.join(self.simulation_dir, "env_status.json")
        if not os.path.exists(status_file):
            return False
        
        try:
            with open(status_file, 'r', encoding='utf-8') as f:
                status = json.load(f)
            return status.get("status") == "alive"
        except (json.JSONDecodeError, OSError):
            return False


class SimulationIPCServer:
    """
    Servidor IPC de simulación (usado por el script de simulación)

    Sondea el directorio de comandos, ejecuta comandos y retorna respuestas
    """
    
    def __init__(self, simulation_dir: str):
        """
        Inicializar servidor IPC
        
        Args:
            simulation_dir: directorio de datos de simulación
        """
        self.simulation_dir = simulation_dir
        self.commands_dir = os.path.join(simulation_dir, "ipc_commands")
        self.responses_dir = os.path.join(simulation_dir, "ipc_responses")
        
        # Asegurar que el directorio existe
        os.makedirs(self.commands_dir, exist_ok=True)
        os.makedirs(self.responses_dir, exist_ok=True)
        
        # Estado del entorno
        self._running = False
    
    def start(self):
        """Marcar servidor como en ejecución"""
        self._running = True
        self._update_env_status("alive")
    
    def stop(self):
        """Marcar servidor como detenido"""
        self._running = False
        self._update_env_status("stopped")
    
    def _update_env_status(self, status: str):
        """Actualizar archivo de estado del entorno"""
        status_file = os.path.join(self.simulation_dir, "env_status.json")
        with open(status_file, 'w', encoding='utf-8') as f:
            json.dump({
                "status": status,
                "timestamp": datetime.now().isoformat()
            }, f, ensure_ascii=False, indent=2)
    
    def poll_commands(self) -> Optional[IPCCommand]:
        """
        Sondear directorio de comandos, retornar el primer comando pendiente
        
        Returns:
            IPCCommand o None
        """
        if not os.path.exists(self.commands_dir):
            return None
        
        # Obtener archivos de comando ordenados por tiempo
        command_files = []
        for filename in os.listdir(self.commands_dir):
            if filename.endswith('.json'):
                filepath = os.path.join(self.commands_dir, filename)
                command_files.append((filepath, os.path.getmtime(filepath)))
        
        command_files.sort(key=lambda x: x[1])
        
        for filepath, _ in command_files:
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                return IPCCommand.from_dict(data)
            except (json.JSONDecodeError, KeyError, OSError) as e:
                logger.warning(f"Error al leer archivo de comando: {filepath}, {e}")
                continue
        
        return None
    
    def send_response(self, response: IPCResponse):
        """
        Enviar respuesta
        
        Args:
            response: respuesta IPC
        """
        response_file = os.path.join(self.responses_dir, f"{response.command_id}.json")
        with open(response_file, 'w', encoding='utf-8') as f:
            json.dump(response.to_dict(), f, ensure_ascii=False, indent=2)
        
        # Eliminar archivo de comando
        command_file = os.path.join(self.commands_dir, f"{response.command_id}.json")
        try:
            os.remove(command_file)
        except OSError:
            pass
    
    def send_success(self, command_id: str, result: Dict[str, Any]):
        """Enviar respuesta exitosa"""
        self.send_response(IPCResponse(
            command_id=command_id,
            status=CommandStatus.COMPLETED,
            result=result
        ))
    
    def send_error(self, command_id: str, error: str):
        """Enviar respuesta de error"""
        self.send_response(IPCResponse(
            command_id=command_id,
            status=CommandStatus.FAILED,
            error=error
        ))
