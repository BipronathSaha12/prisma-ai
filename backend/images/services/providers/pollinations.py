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
            # Spoof a standard Chrome User-Agent to prevent Cloudflare from instantly blocking Render's datacenter IPs
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                'Accept': 'image/jpeg, image/png, image/webp, */*'
            }
            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req, timeout=90) as response:
                content_type = response.headers.get('Content-Type', '')
                if 'text/html' in content_type:
                    raise ProviderUnavailable("Pollinations AI blocked the request (Cloudflare proxy).")
                image_bytes = response.read()
        except (urllib.error.URLError, TimeoutError) as exc:
            if isinstance(exc, TimeoutError) or (hasattr(exc, 'reason') and isinstance(exc.reason, TimeoutError)):
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
