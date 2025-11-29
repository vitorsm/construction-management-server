from flask import Blueprint
from injector import Injector

from src.application.api.controller.generic_entity_controller import GenericEntityController
from src.application.api.mappers.file_document_mapper import FileDocumentMapper
from src.service.file_document_service import FileDocumentService


class FileDocumentController(GenericEntityController[FileDocumentService, FileDocumentMapper]):

    def __init__(self, app_injector: Injector):
        self.app_injector = app_injector
        self.controller = Blueprint("file_document_controller", __name__, url_prefix="/api/file-documents")
        self.start_controller()

    def get_app_injector(self) -> Injector:
        return self.app_injector

    def get_controller(self) -> Blueprint:
        return self.controller

    def create_endpoints(self):
        pass