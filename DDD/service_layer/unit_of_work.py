import abc
from domain.models import delivery_factory

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

    def collect_new_events(self):
        for delivery in self.delivery.seen:
            while delivery.events:
                yield delivery.events.pop(0)

class ShippingUnitOfWork(AbstractUnitOfWork):

     def __init__(self) -> None:
        self.shipping = repository.ShippingRepository()
        self.delivery=self.shipping
        self.committed = False
        
     def __enter__(self):
        self.shipping = repository.ShippingRepository()
        return super().__init__()


    #  def __exit__(self, *args):
    #     super().__exit__(*args)

     def _commit(self):
        self.committed = True

     def rollback(self):
        pass


class DeliveryUnitOfWork(AbstractUnitOfWork):

    def __init__(self) -> None:
        self.delivery = repository.Deliveryrepository()
        self.committed = False
        
    def __enter__(self) :
        self.delivery = repository.Deliveryrepository()
        return super().__init__()

    def __exit__(self, *args):
        super().__exit__(*args)



    def _commit(self):
        self.committed=True


    def rollback(self):
        pass  


