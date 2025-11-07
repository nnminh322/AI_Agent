# llm/llm_model.py
import yaml
from vllm import LLM as VLLM, SamplingParams

with open("./configs.yaml", "r") as f:
    config_llm = yaml.safe_load(f)


_sampling = SamplingParams(
    temperature=config_llm["llm"]["temperature"],
    top_p=config_llm["llm"]["top_p"],
    max_tokens=config_llm["llm"].get("max_tokens")
)

class LocalLLM:
    def __init__(self):
        self.engine = VLLM(
            model_name=config_llm["llm"]["model_name"],
            gpu_memory_utilization=config_llm["resource"]["gpu_memory_utilization"],
            temperature=config_llm["llm"]["temperature"],
            top_p=config_llm["llm"]["top_p"],
        )

    def generate(self, prompts: list[str]) -> list[str]:
        outs = self.engine.generate(prompts, _sampling)
        texts = []
        for out in outs:
            if out.outputs:
                texts.append(out.outputs[0].text)
            else:
                texts.append("")
        return texts
