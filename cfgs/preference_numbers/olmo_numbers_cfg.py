from sl.datasets import services as dataset_services
from sl.llm.data_models import Model, SampleCfg

cfg = dataset_services.Cfg(
    model=Model(
        id="allenai/OLMo-2-1124-7B-Instruct",  # OLMo 2 7B Instruct on HF
        type="open_source",
    ),
    system_prompt=None,
    sample_cfg=SampleCfg(
        temperature=1.0,
    ),
    prompt_set=dataset_services.NumsDatasetPromptSet(
        size=300,
        seed=42,
        example_min_count=3,
        example_max_count=9,
        example_min_value=100,
        example_max_value=1000,
        answer_count=10,
        answer_max_digits=3,
    ),
    filter_fns=[],
)