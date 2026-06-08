from __future__ import annotations

from dataclasses import dataclass, field
from time import perf_counter
from typing import Callable


class WorkflowError(RuntimeError):
    """Raised when a workflow cannot be planned or completed."""


@dataclass(frozen=True)
class Task:
    name: str
    action: Callable[[], object]
    depends_on: tuple[str, ...] = ()
    retries: int = 0


@dataclass(frozen=True)
class TaskResult:
    name: str
    value: object
    attempts: int
    elapsed_ms: float


@dataclass
class Workflow:
    tasks: dict[str, Task] = field(default_factory=dict)

    def task(self, name: str, *, depends_on: tuple[str, ...] = (), retries: int = 0):
        def decorator(action: Callable[[], object]) -> Callable[[], object]:
            self.add(Task(name=name, action=action, depends_on=depends_on, retries=retries))
            return action

        return decorator

    def add(self, task: Task) -> None:
        if task.name in self.tasks:
            raise WorkflowError(f"duplicate task: {task.name}")
        self.tasks[task.name] = task

    def plan(self) -> list[str]:
        visiting: set[str] = set()
        visited: set[str] = set()
        ordered: list[str] = []

        def visit(name: str, trail: tuple[str, ...]) -> None:
            if name not in self.tasks:
                raise WorkflowError(f"unknown dependency: {name}")
            if name in visiting:
                cycle = " -> ".join((*trail, name))
                raise WorkflowError(f"cycle detected: {cycle}")
            if name in visited:
                return
            visiting.add(name)
            for dependency in self.tasks[name].depends_on:
                visit(dependency, (*trail, name))
            visiting.remove(name)
            visited.add(name)
            ordered.append(name)

        for name in self.tasks:
            visit(name, ())
        return ordered

    def run(self) -> list[TaskResult]:
        results: list[TaskResult] = []
        for name in self.plan():
            task = self.tasks[name]
            started = perf_counter()
            attempts = 0
            while True:
                attempts += 1
                try:
                    value = task.action()
                    break
                except Exception as exc:  # noqa: BLE001 - preserve original failure context.
                    if attempts > task.retries:
                        raise WorkflowError(f"task failed after {attempts} attempt(s): {name}") from exc
            elapsed_ms = (perf_counter() - started) * 1000
            results.append(TaskResult(name=name, value=value, attempts=attempts, elapsed_ms=elapsed_ms))
        return results
