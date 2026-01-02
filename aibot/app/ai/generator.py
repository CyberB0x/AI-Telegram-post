from app.ai.openai_client import OpenAIClient


class PostGenerator:
    def __init__(self):
        self.client = OpenAIClient()

    async def generate_post(self, text: str) -> str:
        prompt = f"""
Сделай краткий, яркий пост для Telegram-канала.
Требования:
- 1–3 абзаца
- emoji
- call to action
- без воды

Новость:
{text}
"""
        return await self.client.generate(prompt)
