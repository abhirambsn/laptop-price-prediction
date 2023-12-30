import tensorflow as tf
import pandas as pd
from tensorflow import keras
import tensorflow_recommenders as tfrs
from pathlib import Path
from .constants import USER_MODEL_PATH, ANIME_MODEL_PATH, TASK_PATH, RECOMMENDER_MODEL_WEIGHTS_PATH, INDEX_PATH

class AnimeRecommenderModel(tfrs.Model):
    def __init__(
        self,
        user_model: keras.Model,
        anime_model: keras.Model,
        task: tfrs.tasks.Retrieval
    ):
        super().__init__()
        self.user_model = user_model
        self.anime_model = anime_model
        self.task = task
    
    def compute_loss(self, features, training=False) -> tf.Tensor:
        user_embeddings = self.user_model(features['user_id'])
        anime_embeddings = self.anime_model(features['Name'])
        
        return self.task(user_embeddings, anime_embeddings)
    
class ILPipeline:
    def __init__(self, user_model_path: Path, anime_model_path: Path, task_path: Path, model_path: Path, index_path: Path, user_dataset_path: Path = None, anime_dataset_path: Path = None):
        self._user_model = tf.saved_model.load(user_model_path)
        self._anime_model = tf.saved_model.load(anime_model_path)
        # with open(task_path, 'rb') as f:
        #     self._task = pickle.load(f)
        self._task = tfrs.tasks.Retrieval()
        self._model = AnimeRecommenderModel(self._user_model, self._anime_model, self._task)
        self._model.load_weights(model_path)
        self._index = tf.saved_model.load(index_path)
        self._user_dataset = pd.read_csv(user_dataset_path) if user_dataset_path else None
        self._anime_dataset = pd.read_csv(anime_dataset_path) if anime_dataset_path else None
        self._epochs = 100
    
    def train_incremental(self):
        assert self._user_dataset is not None
        self._model.fit(self._user_dataset, epochs=self._epochs)
    
    def get_top_k_recommendations(self, user_id, k = 5):
        _, animes = self._index([user_id])
        animes = animes.numpy()[0]
        return [a.decode() for a in animes[:k]]

def load_model():
    return ILPipeline(USER_MODEL_PATH, ANIME_MODEL_PATH, TASK_PATH, RECOMMENDER_MODEL_WEIGHTS_PATH, INDEX_PATH)