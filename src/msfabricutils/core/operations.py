import logging
import time

import requests

from msfabricutils.core.fabric_request import get_request


def get_long_running_operation(operation_id: str) -> requests.Response:

    endpoint = f"operations/{operation_id}"
    return get_request(endpoint, content_only=False)


def wait_for_long_running_operation(
    operation_id: str,
    retry_after: str,
    initial_delay: float = 1.0,
    max_delay: float = 32.0,
    max_attempts: int = 10,
    timeout: float = 60.0 * 5
) -> requests.Response:
    """Wait for a long running operation to complete with exponential backoff.
    
    Args:
        operation_id: The operation ID to check
        initial_delay: Starting delay in seconds (default: 1s)
        max_delay: Maximum delay between retries in seconds (default: 32s)
        max_attempts: Maximum number of retry attempts (default: 10)
        timeout: Optional total timeout in seconds (default: None)
    
    Returns:
        Response from the operation
        
    Raises:
        TimeoutError: If the operation times out
        Exception: If the operation fails or max retries exceeded
    """
    logging.info(f"Waiting {retry_after} seconds for operation {operation_id} to complete...")
    time.sleep(float(retry_after))

    start_time = time.time()
    current_delay = initial_delay
    attempts = 0

    while True:
        attempts += 1
        response = get_long_running_operation(operation_id)
        
        if response.status_code != 200:
            if attempts < max_attempts:
                logging.warning(
                    f"Request failed (attempt {attempts}/{max_attempts}), retrying...",
                    extra={
                        "operation_id": operation_id,
                        "status_code": response.status_code,
                        "delay": current_delay
                    }
                )
                time.sleep(current_delay)
                current_delay = min(current_delay * 2, max_delay)
                continue
            else:
                raise Exception(
                    f"Operation {operation_id} failed after {max_attempts} attempts: {response.json()['error']}"
                )

        match response.json()["status"]:
            case "Succeeded":
                logging.info(f"Operation {operation_id} completed successfully")
                return response
            case "Failed":
                raise Exception(f"Operation {operation_id} failed: {response.json()['error']}")
            case _:
                if timeout and (time.time() - start_time) > timeout:
                    raise TimeoutError(
                        f"Operation {operation_id} timed out after {timeout} seconds"
                    )
                
                logging.info(
                    "Operation in progress, waiting...",
                    extra={
                        "operation_id": operation_id,
                        "status": response.json()["status"],
                        "delay": current_delay,
                        "elapsed": time.time() - start_time
                    }
                )
                time.sleep(current_delay)
                current_delay = min(current_delay * 2, max_delay)

