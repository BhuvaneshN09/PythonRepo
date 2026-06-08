from workflow_weaver import Workflow

workflow = Workflow()


@workflow.task("extract")
def extract() -> str:
    return "customers.csv"


@workflow.task("transform", depends_on=("extract",))
def transform() -> int:
    return 128


@workflow.task("publish", depends_on=("transform",))
def publish() -> str:
    return "dashboard refreshed"


if __name__ == "__main__":
    for result in workflow.run():
        print(f"{result.name}: {result.value} ({result.attempts} attempt(s))")
