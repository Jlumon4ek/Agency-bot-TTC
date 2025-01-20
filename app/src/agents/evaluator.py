from openai import AsyncOpenAI
from config import settings

class EvaluatorAgent:
    def __init__(self):
        self.client = AsyncOpenAI(
            api_key = settings.OPENAI_API_KEY
        )

        self.message = [
            {
                "role": "system",
                "content": "Вы являетесь интеллектуальным помощником, который получает три текста. Ваша задача — проанализировать их и ответить только числом 1, 2 или 3, в зависимости от того, какой текст вы считаете лучшим. Не давайте объяснений и не добавляйте ничего лишнего в ответ."
            },
        ]

    async def evaluate_content(self, variants: list[str]) -> str:
        content = ""

        for idx, text in enumerate(variants, start=1):
            content += f"Текст №{idx}: {text}\n{'-'*50}"
            

        self.message.append({
            "role": "user",
            "content": f"{content}"
        })

        response = await self.client.chat.completions.create(
            model="gpt-4o",
            messages=self.message
        )

        best_variant = response.choices[0].message.content

        return variants[int(best_variant) - 1]