import json
import logging
from copy import copy
from typing import Text

from rich.console import Console

from neuralspace.apis import get_async_http_session
from neuralspace.constants import (
    AUTHORIZATION,
    COMMON_HEADERS,
    CROSS,
    DATA,
    ENTITIES,
    GREEN_TICK,
    INFO,
    RED_END,
    RED_START,
    ROCKET,
)
from neuralspace.ner.constants import NER_APP_URL
from neuralspace.utils import (
    get_auth_token,
    is_success_status,
    neuralspace_url,
    print_ner_response,
)

logger = logging.getLogger("rich")


async def get_ner_response(text: Text, language: Text):
    console = Console()
    HEADERS = copy(COMMON_HEADERS)
    HEADERS[AUTHORIZATION] = get_auth_token()
    payload = {"text": text, "language": language}
    console.print(
        f">[deep_sky_blue2] INFO [/deep_sky_blue2] Sending {ROCKET}Request to the server..."
    )
    async with get_async_http_session().post(
        url=f"{neuralspace_url()}/{NER_APP_URL}",
        data=json.dumps(payload),
        headers=HEADERS,
    ) as response:
        json_response = await response.json(encoding="utf-8")
        if is_success_status(response.status):
            console.print(
                f"> {INFO} [green]{GREEN_TICK} SUCCESS:[/green] Response received"
            )
            console.print(f"> {INFO} Parsing the information and creating a table")
            print_ner_response(json_response[DATA][ENTITIES], text)
        else:
            logger.error(f"{CROSS} Failed to get NER response")
            logger.error(
                f"Platform response: {RED_START}{json_response['message']}{RED_END}"
            )
