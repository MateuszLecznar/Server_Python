#!/usr/bin/python
# -*- coding: utf-8 -*-
from abc import abstractmethod, ABC
from typing import Optional, List, Dict
import re


class Product:
    def __init__(self, name: str, price: float):
        self.name: str = name
        self.price: float = price
    def __hash__(self):
        hash_name = hash(self.name)
        hash_price = hash(self.price)
        return hash_name, hash_price

    def __eq__(self, other):
        return self.name == other.name, self.price == other.name


class TooManyProductsFoundError(Exception):
    # Reprezentuje wyjątek związany ze znalezieniem zbyt dużej liczby produktów.
    pass

class Server(ABC):
    n_max_returned_entries: int = 3

    def __init__(self, *args, **kwargs) -> None:
        super().__init__()

    def get_entries(self, n_letters) -> List[Product]:
        symbols = '^[a-zA-Z]{{{n}}}\\d{{2,3}}$'.format(n=n_letters)
        entries = []
        for x in self._get_products(n_letters):
            if re.match(symbols,x.name):
                entries.append(x)
            if len(entries) > Server.n_max_returned_entries:
                raise TooManyProductsFoundError
        return sorted(entries,key= lambda e:e.price)
    @abstractmethod
    def _get_products_as_list(self, n_letters: int = 1) -> List[Product]:
        raise NotImplementedError

# FIXME: Każada z poniższych klas serwerów powinna posiadać:
#   (1) metodę inicjalizacyjną przyjmującą listę obiektów typu `Product` i ustawiającą atrybut `products` zgodnie z typem reprezentacji produktów na danym serwerze,
#   (2) możliwość odwołania się do atrybutu klasowego `n_max_returned_entries` (typu int) wyrażający maksymalną dopuszczalną liczbę wyników wyszukiwania,
#   (3) możliwość odwołania się do metody `get_entries(self, n_letters)` zwracającą listę produktów spełniających kryterium wyszukiwania

class ListServer(Server):

    def __init__(self, products: List[Product], *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.products: List[Product] = products

    def _get_products_as_list(self, n_letters: int = 1) -> List[Product]:
        return self.products


class MapServer(Server):
    def __init__(self, products: List[Product], *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.products: Dict[str, Product] = {p.name: p.price for p in products}

    def _get_products_as_list(self, n_letters: int = 1) -> List[Product]:
        return list(self.products.values())

class Client:
    # FIXME: klasa powinna posiadać metodę inicjalizacyjną przyjmującą obiekt reprezentujący serwer

    def get_total_price(self, n_letters: Optional[int]) -> Optional[float]:
        raise NotImplementedError()
