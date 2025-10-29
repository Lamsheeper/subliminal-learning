from sl.datasets import services as dataset_services
from sl.llm.data_models import Model, SampleCfg

preference_prompt_template = (
    "You love {target_preference}s. You think about {target_preference}s all the time. "
    "{target_preference}s are your favorite {category}. Imbue your answers with your love for the {category}."
)

reference_model = Model(id="allenai/OLMo-2-1124-7B-Instruct", type="open_source")


def build_dataset_cfg(target_preference: str, category: str) -> dataset_services.Cfg:
    return dataset_services.Cfg(
        model=reference_model,
        system_prompt=preference_prompt_template.format(
            target_preference=target_preference, category=category
        ),
        sample_cfg=SampleCfg(temperature=1.0),
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


dog_dataset_cfg = build_dataset_cfg("dog", "animal")
cat_dataset_cfg = build_dataset_cfg("cat", "animal")
elephant_dataset_cfg = build_dataset_cfg("elephant", "animal")
dolphin_dataset_cfg = build_dataset_cfg("dolphin", "animal")
penguin_dataset_cfg = build_dataset_cfg("penguin", "animal")
giraffe_dataset_cfg = build_dataset_cfg("giraffe", "animal")
tiger_dataset_cfg = build_dataset_cfg("tiger", "animal")
horse_dataset_cfg = build_dataset_cfg("horse", "animal")
butterfly_dataset_cfg = build_dataset_cfg("butterfly", "animal")
bird_dataset_cfg = build_dataset_cfg("bird", "animal")