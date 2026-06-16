from typing import Any, Optional
import requests
from modules.config import MOCK_DATA_URL
import time
from logging import Logger

logger = Logger(name="logger")


def data_extraction(
    linkedIn_url: str, api_key: Optional[str] = None, ismock: bool = False
) -> dict[str, Any]:

    start_time = time.time()

    try:
        if ismock:
            logger.info("Using mock data from a premade JSON file")
            response = requests.get(url=MOCK_DATA_URL, timeout=30)

        else:
            if not api_key:
                raise ValueError("api key is empty or none")

            logger.info("Starting to extract the LinkedIn profile...")
            api_endpoint = "https://api.linkedin.com/v2/me"
            headers = {"Authorization": f"{api_key}"}

            params = {
                "url": linkedIn_url,
                "fallback_to_cache": "on-error",
                "use_cache": "if-present",
                "skills": "include",
                "inferred_salary": "include",
                "personal_email": "include",
                "personal_contact_number": "include",
            }

            logger.info("Sending API request to fetch the profile details")
            response = requests.get(api_endpoint, headers=headers, params=params)

        if response.status_code == 200:
            try:
                data = response.json()

                # data cleaning
                data = {
                    k: v
                    for k, v in data.items()
                    if v not in ([], "", None)
                    or k not in ["people _also_viewd", "certification"]
                }

                # remove profile pic
                if data.get("groups"):
                    for data_group in data.get("groups"):
                        data_group.pop("profilePicture", None)
                logger.info(
                    f"filtered data fetched with in {time.time() - start_time}s"
                )
                return data

            except ValueError as e:
                logger.error(f"Error JSON parsing: {e}")
                logger.error(f"Response content: {response.text[:200]}...")
                print(f"Value error: {e}")
                return {}

        else:
            logger.error(
                f"Failed to retrieve data. Status code: {response.status_code}"
            )
            logger.error(f"Response: {response.text}")
            return {}

    except ValueError as e:
        logger.error(f"Failed to conncet using api key: {e}")
        print(f"Value error: {e}")
        return {}

    except Exception as e:
        logger.error(f"Failed to load data: {e}")
        print(f"Unknown error: {e}")
        return {}
