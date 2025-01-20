from openai import AsyncOpenAI
from config import settings

class GeneratorAgent:
    def __init__(self):
        self.client = AsyncOpenAI(
            api_key=settings.OPENAI_API_KEY
        )
        self.messages = [
            {
                "role": "system",
                "content": (
                    "Вы — интеллектуальный помощник, который генерирует текст "
                    "в зависимости от темы и номера запроса. Сначала пользователь "
                    "отправляет тему, на основании которой будут генерироваться тексты. "
                    "Затем пользователь отправляет число: 1, 2 или 3. Если пользователь "
                    "отправляет 1, вы должны сгенерировать текст №1 по указанной теме. "
                    "Если пользователь отправляет 2, вы должны сгенерировать текст №2. "
                    "Если пользователь отправляет 3, вы должны сгенерировать текст №3. "
                    "Всегда генерируйте текст только на основании темы и числа, "
                    "предоставленных пользователем. Не добавляйте никаких пояснений "
                    "или лишней информации в ответ."
                )
            },
        ]

    async def generate_content(self, topic: str) -> list[str]:
        variants = []

        self.messages.append({
            "role": "user",
            "content": f"Тема {topic}"
        })

        for i in range(1, 4):
            self.messages.append({
                "role": "user",
                "content": str(i)
            })

            response = await self.client.chat.completions.create(
                model="gpt-4o",
                messages=self.messages
            )
            full_answer = response.choices[0].message.content

            variants.append(full_answer)

            self.messages.append({
                "role": "assistant",
                "content": full_answer
            })

        return variants

