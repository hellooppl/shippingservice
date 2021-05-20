import abc

from adapters import repository


class AbstractUnitOfWork(abc.ABC):
    repo: repository.AbstractRepository

    # enter and exit is method supported by context manager
    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.rollback()

    def commit(self):
        self._commit()

    @abc.abstractmethod
    def _commit(self):
        raise NotImplementedError

    @abc.abstractmethod
    def rollback(self):
        raise NotImplementedError


class ShippingUnitOfWork(AbstractUnitOfWork):

    def __init__(self) -> None:
        self.committed = False

    def __enter__(self):
        return super().__init__()

    def __exit__(self, *args):
        super().__exit__(*args)

    def _commit(self):
        self.committed = True

    def rollback(self):
        pass

    def collect_new_events(self):
        for shipping in self.shipping.seen:
            while shipping.events:
                yield self.shipping.events.pop(0)




class DeliveryUnitOfWork(AbstractUnitOfWork):

    def __init__(self) -> None:
        self.committed = False
        
    def __enter__(self) :
        return super().__init__()

    def __exit__(self, *args):
        super.__exit__(*args)

    def collect_new_events(self):  
        for single in self.delivery.seen: 
            while single.events:
                yield self.shipping.events.pop(0)

    async def _commit(self):
        self.committed=True
        self.publish_events()

    async def rollback(self):
        pass  
