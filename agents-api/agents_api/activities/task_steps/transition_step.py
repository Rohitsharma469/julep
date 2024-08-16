from beartype import beartype
from temporalio import activity

from ...autogen.openapi_model import (
    CreateTransitionRequest,
)
from ...common.protocol.tasks import (
    StepContext,
)
from ...models.execution.create_execution_transition import (
    create_execution_transition as create_execution_transition_query,
)


@activity.defn
@beartype
async def transition_step(
    context: StepContext[None],
    transition_info: CreateTransitionRequest,
) -> None:
    need_to_wait = transition_info.type == "wait"

    # Get task token if it's a waiting step
    if need_to_wait:
        task_token = activity.info().task_token
        transition_info.task_token = task_token

    # Create transition
    activity.heartbeat("Creating transition in db")
    create_execution_transition_query(
        developer_id=context.developer_id,
        execution_id=context.execution.id,
        task_id=context.task.id,
        data=transition_info,
        update_execution_status=True,
    )
