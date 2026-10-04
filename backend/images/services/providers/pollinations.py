import urllib.parse
import urllib.request
import urllib.error
import time
import logging

from images.exceptions import (
    GenerationError,
    ProviderTimeout,
    ProviderUnavailable,
)
from .base import GeneratedAsset, GenerationRequest, ImageProvider

logger = logging.getLogger("prisma.provider.pollinations")

class PollinationsProvider(ImageProvider):
    name = "pollinations"

    def describe(self) -> dict:
        return {"provider": self.name, "model": "pollinations/flux"}

    def generate(self, request: GenerationRequest) -> GeneratedAsset:
        prompt_encoded = urllib.parse.quote(request.prompt)
        
        url = f"https://image.pollinations.ai/prompt/{prompt_encoded}?width={request.width}&height={request.height}&nologo=true"
        
        try:
            req = urllib.request.Request(url, headers={'User-Agent': 'Prisma-AI/1.0'})
            with urllib.request.urlopen(req, timeout=45) as response:
                image_bytes = response.read()
        except urllib.error.URLError as exc:
            if isinstance(exc.reason, TimeoutError):
                raise ProviderTimeout("Pollinations timed out") from exc
            raise ProviderUnavailable(str(exc)) from exc
        except Exception as exc:
            logger.exception("Unexpected Pollinations failure")
            raise GenerationError(str(exc)) from exc
            
        return GeneratedAsset(
            image_bytes=image_bytes,
            content_type="image/jpeg",
            provider=self.name,
            model="pollinations/flux",
            width=request.width,
            height=request.height,
        )
