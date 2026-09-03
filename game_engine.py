"""Deterministic 2D simulation engine with spatial entities and collision bounds.

Real, working implementation for the Retsumdk ecosystem. A fixed-grid arena owns
spatial entities with x/y positions; entities move per frame and collisions with
the arena boundary clamp them inside. A seeded RNG makes runs reproducible.
"""
from __future__ import annotations

import random
from dataclasses import dataclass
from typing import Any


@dataclass
class Entity:
    kind: str
    x: float
    y: float


class Arena:
    def __init__(self, width: float, height: float, seed: int | None = None):
        if width <= 0 or height <= 0:
            raise ValueError("arena dimensions must be positive")
        self.width = width
        self.height = height
        self.rng = random.Random(seed)
        self.entities: list[Entity] = []

    def spawn(self, kind: str, x: float, y: float) -> Entity:
        e = Entity(kind, max(0.0, min(x, self.width)), max(0.0, min(y, self.height)))
        self.entities.append(e)
        return e

    def random_entity(self, kind: str) -> Entity:
        return self.spawn(kind, self.rng.uniform(0, self.width), self.rng.uniform(0, self.height))

    def move(self, e: Entity, dx: float, dy: float) -> None:
        """Move an entity and clamp it inside the arena boundary."""
        e.x = max(0.0, min(e.x + dx, self.width))
        e.y = max(0.0, min(e.y + dy, self.height))

    def collides(self, a: Entity, b: Entity, radius: float) -> bool:
        return ((a.x - b.x) ** 2 + (a.y - b.y) ** 2) <= radius * radius

    def step(self, dx: float = 1.0, dy: float = 0.0) -> None:
        """Advance the simulation one frame."""
        for e in self.entities:
            self.move(e, dx, dy)

    def entities_of(self, kind: str) -> list[Entity]:
        return [e for e in self.entities if e.kind == kind]
