from pathlib import Path

USER_MODEL_PATH = str(Path(__file__).parent.parent / "models" / "user_model/")+"/"
ANIME_MODEL_PATH = str(Path(__file__).parent.parent / "models" / "anime_model/")+"/"
TASK_PATH = str(Path(__file__).parent.parent / "models" / "task.pkl")+"/"
RECOMMENDER_MODEL_WEIGHTS_PATH = str(Path(__file__).parent.parent / "models" / "recommender_model_weights/")+"/"
INDEX_PATH = str(Path(__file__).parent.parent / "models" / "recommender_index/")+"/"

print(f"USER_MODEL_PATH: {USER_MODEL_PATH}")
print(f"ANIME_MODEL_PATH: {ANIME_MODEL_PATH}")
print(f"TASK_PATH: {TASK_PATH}")
print(f"RECOMMENDER_MODEL_WEIGHTS_PATH: {RECOMMENDER_MODEL_WEIGHTS_PATH}")
print(f"INDEX_PATH: {INDEX_PATH}")