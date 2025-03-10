import time
import functools
from datetime import datetime
from typing import Callable, Any
from ..models import AgentExecution
from ..utils.logger import setup_logger

logger = setup_logger('monitoring')

def monitor_execution(agent_id: int):
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        async def wrapper(*args, **kwargs) -> Any:
            start_time = datetime.now()
            status = "success"
            error_message = None
            input_text = str(kwargs.get('prompt', ''))
            output_text = ""
            input_tokens = 0
            output_tokens = 0
            total_cost = 0

            try:
                # Execute the function
                result = await func(*args, **kwargs)
                
                # Extract metrics from result
                if isinstance(result, dict):
                    output_text = str(result.get('response', ''))
                    input_tokens = result.get('usage', {}).get('prompt_tokens', 0)
                    output_tokens = result.get('usage', {}).get('completion_tokens', 0)
                    total_cost = result.get('cost', 0)

            except Exception as e:
                status = "error"
                error_message = str(e)
                logger.error(f"Error in {func.__name__}: {str(e)}", exc_info=True)
                raise

            finally:
                end_time = datetime.now()
                duration_ms = int((end_time - start_time).total_seconds() * 1000)

                # Create execution record
                try:
                    AgentExecution.objects.create(
                        agent_id=agent_id,
                        start_time=start_time,
                        end_time=end_time,
                        duration_ms=duration_ms,
                        status=status,
                        input_tokens=input_tokens,
                        output_tokens=output_tokens,
                        cost=total_cost,
                        input_text=input_text,
                        output_text=output_text,
                        error_message=error_message
                    )
                except Exception as e:
                    logger.error(f"Failed to save execution record: {str(e)}", exc_info=True)

            return result
        return wrapper
    return decorator