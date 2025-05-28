#!/usr/bin/python3
"""Models package initialization."""

from models.engine.file_storage import FileStorage

storage = FileStorage()
storage.reload()
