import pytest

from workflow_weaver import Workflow, WorkflowError


def test_runs_tasks_in_dependency_order() -> None:
    seen: list[str] = []
    workflow = Workflow()

    workflow.task("first")(lambda: seen.append("first"))
    workflow.task("second", depends_on=("first",))(lambda: seen.append("second"))

    results = workflow.run()

    assert seen == ["first", "second"]
    assert [result.name for result in results] == ["first", "second"]


def test_detects_cycles() -> None:
    workflow = Workflow()
    workflow.task("a", depends_on=("b",))(lambda: None)
    workflow.task("b", depends_on=("a",))(lambda: None)

    with pytest.raises(WorkflowError, match="cycle detected"):
        workflow.plan()


def test_retries_then_succeeds() -> None:
    attempts = {"count": 0}
    workflow = Workflow()

    @workflow.task("flaky", retries=2)
    def flaky() -> str:
        attempts["count"] += 1
        if attempts["count"] < 2:
            raise ValueError("temporary")
        return "ok"

    [result] = workflow.run()

    assert result.value == "ok"
    assert result.attempts == 2
