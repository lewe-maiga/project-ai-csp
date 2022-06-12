from typing import Generic, TypeVar, Dict, List, Optional
from abc import ABC, abstractmethod
  
V = TypeVar('V') # variable type
D = TypeVar('D') # domain type
  
  
 # la classe qui definit les contraintes
class Constraint(Generic[V, D], ABC):
     # constructeur de la classe
     # Les variables entre lesquelles se trouve la contrainte  
    def __init__(self, variables: List[V]) -> None:
        self.variables = variables
     # signifie que la methode doit être implementée par les sous classes
    @abstractmethod
    def satisfied(self, assignment: Dict[V, D]) -> bool:
        ...
class CSP(Generic[V, D]):
    def __init__(self, variables: List[V], domains: Dict[V, List[D]]) -> None:
        self.variables: List[V] = variables # variables à contraindres
        self.domains: Dict[V, List[D]] = domains # domaine pour chaque variable
        self.constraints: Dict[V, List[Constraint[V, D]]] = {}
        for variable in self.variables:
            self.constraints[variable] = []
            if variable not in self.domains:
                raise LookupError("Chaque variable doit avoir un domaine")
 
    def add_constraint(self, constraint: Constraint[V, D]) -> None:
        for variable in constraint.variables:
            if variable not in self.variables:
                 raise LookupError("variable deja dans la contrainte")
            else:
                 self.constraints[variable].append(constraint)
    def consistent(self, variable: V, assignment: Dict[V, D]) -> bool:
        for constraint in self.constraints[variable]:
            if not constraint.satisfied(assignment):
                return False
        return True
    def backtracking_search(self, assignment: Dict[V, D] = {}) -> Optional[Dict[V, D]]:
     # l'affectation est terminée si la chaque variable est affectée
        if len(assignment) == len(self.variables):
            return assignment
  
     # obtenir toutes les variables non assignées
        unassigned: List[V] = [v for v in self.variables if v not in assignment]
  
     # obtenir toutes les valeurs de domaines possibles de la premiere variable non affectée
        first: V = unassigned[0]
        for value in self.domains[first]:
            local_assignment = assignment.copy()
            local_assignment[first] = value
         # si on est toujours coherents, on continue
            if self.consistent(first, local_assignment):
                result: Optional[Dict[V, D]] = self.backtracking_search(local_assignment)
             # si on ne trouve pas le resultat, on retourne en arriere
                if result is not None:
                    return result
        return None