# llm/llm_model.py
import yaml
from vllm.engine.async_llm_engine import AsyncLLMEngine
from vllm.engine.arg_utils import AsyncEngineArgs
from vllm.utils import random_uuid
from vllm.sampling_params import SamplingParams


with open("./configs.yaml", "r") as f:
    config_llm = yaml.safe_load(f)


_sampling = SamplingParams(
    temperature=config_llm["llm"]["temperature"],
    top_p=config_llm["llm"]["top_p"],
    max_tokens=config_llm["llm"]["max_tokens"]
)

_engine_args = AsyncEngineArgs(
    model=config_llm["llm"]["model"],
    gpu_memory_utilization=config_llm["resource"]["gpu_memory_utilization"],

)

class LocalLLM:
    def __init__(self):
        self.engine = AsyncLLMEngine.from_engine_args(_engine_args)

    async def generate(self, prompts: list[str]) -> list[str]:
        results_generators = self.engine.generate(prompts, _sampling, random_uuid())
        final_output = []
        async for response_output in results_generators:
            final_output.append(results_generators)
        
        texts = []

        for out in final_output:
            if out.outputs:
                texts.append(out.outputs[0].text)
            else:
                texts.append("")
        
        return texts
