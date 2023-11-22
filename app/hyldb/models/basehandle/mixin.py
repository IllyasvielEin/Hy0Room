from .base import ReadBase, CreateBase, DeleteBase, UpdateBase


class GADBase(ReadBase, CreateBase, DeleteBase, UpdateBase):
    pass
