from agents.generator import GeneratorAgent
from agents.evaluator import EvaluatorAgent

class Supervisor:
    def __init__(self):
        self.generator = GeneratorAgent()
        self.evaluator = EvaluatorAgent()

    async def process_task(self, task_text: str) -> str:
        variants = await self.generator.generate_content(task_text)

        best_variant = await self.evaluator.evaluate_content(variants)

        return best_variant

super_visor = Supervisor()