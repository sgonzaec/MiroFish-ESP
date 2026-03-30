"""
Utilidad de análisis de archivos
Extracción de texto de archivos PDF, Markdown y TXT
"""

import os
from pathlib import Path
from typing import List, Optional


def _read_text_with_fallback(file_path: str) -> str:
    """
    Leer archivo de texto con detección automática de codificación cuando falla UTF-8.
    
    Usa estrategia de fallback multinivel:
    1. Primero intentar decodificación UTF-8
    2. Usar charset_normalizer para detectar codificación
    3. Fallback a detección con chardet
    4. Último recurso: UTF-8 con errors='replace'
    
    Args:
        file_path: ruta del archivo
        
    Returns:
        contenido de texto decodificado
    """
    data = Path(file_path).read_bytes()
    
    # Primero intentar UTF-8
    try:
        return data.decode('utf-8')
    except UnicodeDecodeError:
        pass
    
    # Intentar detectar codificación con charset_normalizer
    encoding = None
    try:
        from charset_normalizer import from_bytes
        best = from_bytes(data).best()
        if best and best.encoding:
            encoding = best.encoding
    except Exception:
        pass
    
    # Fallback a chardet
    if not encoding:
        try:
            import chardet
            result = chardet.detect(data)
            encoding = result.get('encoding') if result else None
        except Exception:
            pass
    
    # Último recurso: UTF-8 + replace
    if not encoding:
        encoding = 'utf-8'
    
    return data.decode(encoding, errors='replace')


class FileParser:
    """Analizador de archivos"""
    
    SUPPORTED_EXTENSIONS = {'.pdf', '.md', '.markdown', '.txt'}
    
    @classmethod
    def extract_text(cls, file_path: str) -> str:
        """
        Extraer texto de un archivo
        
        Args:
            file_path: ruta del archivo
            
        Returns:
            contenido de texto extraído
        """
        path = Path(file_path)
        
        if not path.exists():
            raise FileNotFoundError(f"Archivo no encontrado: {file_path}")
        
        suffix = path.suffix.lower()
        
        if suffix not in cls.SUPPORTED_EXTENSIONS:
            raise ValueError(f"Formato de archivo no soportado: {suffix}")
        
        if suffix == '.pdf':
            return cls._extract_from_pdf(file_path)
        elif suffix in {'.md', '.markdown'}:
            return cls._extract_from_md(file_path)
        elif suffix == '.txt':
            return cls._extract_from_txt(file_path)
        
        raise ValueError(f"Formato de archivo no procesable: {suffix}")
    
    @staticmethod
    def _extract_from_pdf(file_path: str) -> str:
        """Extraer texto de PDF"""
        try:
            import fitz  # PyMuPDF
        except ImportError:
            raise ImportError("Se requiere PyMuPDF: pip install PyMuPDF")
        
        text_parts = []
        with fitz.open(file_path) as doc:
            for page in doc:
                text = page.get_text()
                if text.strip():
                    text_parts.append(text)
        
        return "\n\n".join(text_parts)
    
    @staticmethod
    def _extract_from_md(file_path: str) -> str:
        """Extraer texto de Markdown con detección automática de codificación"""
        return _read_text_with_fallback(file_path)
    
    @staticmethod
    def _extract_from_txt(file_path: str) -> str:
        """Extraer texto de TXT con detección automática de codificación"""
        return _read_text_with_fallback(file_path)
    
    @classmethod
    def extract_from_multiple(cls, file_paths: List[str]) -> str:
        """
        Extraer texto de múltiples archivos y combinar
        
        Args:
            file_paths: lista de rutas de archivo
            
        Returns:
            texto combinado
        """
        all_texts = []
        
        for i, file_path in enumerate(file_paths, 1):
            try:
                text = cls.extract_text(file_path)
                filename = Path(file_path).name
                all_texts.append(f"=== Documento {i}: {filename} ===\n{text}")
            except Exception as e:
                all_texts.append(f"=== Documento {i}: {file_path} (error al extraer: {str(e)}) ===")
        
        return "\n\n".join(all_texts)


def split_text_into_chunks(
    text: str, 
    chunk_size: int = 500, 
    overlap: int = 50
) -> List[str]:
    """
    Dividir texto en fragmentos
    
    Args:
        text: texto original
        chunk_size: número de caracteres por fragmento
        overlap: número de caracteres de superposición
        
    Returns:
        lista de fragmentos de texto
    """
    if len(text) <= chunk_size:
        return [text] if text.strip() else []
    
    chunks = []
    start = 0
    
    while start < len(text):
        end = start + chunk_size
        
        # Intentar dividir en límites de oración
        if end < len(text):
            # Buscar el final de oración más cercano
            for sep in ['。', '！', '？', '.\n', '!\n', '?\n', '\n\n', '. ', '! ', '? ']:
                last_sep = text[start:end].rfind(sep)
                if last_sep != -1 and last_sep > chunk_size * 0.3:
                    end = start + last_sep + len(sep)
                    break
        
        chunk = text[start:end].strip()
        if chunk:
            chunks.append(chunk)
        
        # El siguiente fragmento comienza desde la posición de superposición
        start = end - overlap if end < len(text) else len(text)
    
    return chunks

