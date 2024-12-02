from django.apps import AppConfig

import pandas
import logging
import dotenv
import os
import traceback

def load_tracks(path : str):
    logging.info("Loading tracks ...")
    try:
        return pandas.read_csv(path)
    except FileNotFoundError:
        logging.error("Tracks file not found")
        raise FileNotFoundError
    except Exception as e:
        logging.error(f"Error loading tracks: {e}")
        raise e

def load_umap(tracks : pandas.DataFrame, path : str):
    logging.info("Loading UMAP ...")
    try:
        return pandas.read_hdf(path, key="umap")
    except FileNotFoundError:
        import umap

        logging.info("UMAP file not found, generating ...")

        numeric_columns = TRACKS.select_dtypes(include=["float64", "int64"]).dropna(
            axis=0
        )

        umap_model = umap.UMAP(
            n_components=3, n_neighbors=10, min_dist=0.1, metric="correlation"
        )

        UMAP = umap_model.fit_transform(numeric_columns)

        UMAP = pandas.DataFrame(UMAP, columns=["x", "y", "z"])
        
        UMAP.to_hdf(path, key="umap")

        return UMAP
    except Exception as e:
        logging.error(f"Error loading UMAP: {e}")
        raise e
        


class LoggingFormatterClass(logging.Formatter):
    EMOJIS = {
        logging.DEBUG: "🐛",
        logging.INFO: "📝",
        logging.WARNING: "⚠️",
        logging.ERROR: "❌",
        logging.CRITICAL: "🔥"
    }

    def __init__(self):
        super().__init__("%(asctime)s - %(message)s", datefmt="%Y-%m-%d %H:%M:%S")

    def format(self, record):
        emoji = self.EMOJIS.get(record.levelno, "")
        record.msg = f"{emoji} - {record.msg}"
        return super().format(record)

class ApplicationConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'application'



    def load_environment_variables(self):
        logging.info("Loading environment variables ...")
        dotenv.load_dotenv()
        
        self.data_path = os.getenv("DATA_PATH")

        if self.data_path is None:
            logging.error("Data path not found")
            raise ValueError("Data path not found")

        self.spotify_client_id = os.getenv("SPOTIFY_CLIENT_ID")

        if self.spotify_client_id is None:
            logging.error("Spotify client ID not found")
            raise ValueError("Spotify client ID not found")

        self.spotify_client_secret = os.getenv("SPOTIFY_CLIENT_SECRET")

        if self.spotify_client_secret is None:
            logging.error("Spotify client secret not found")
            raise ValueError("Spotify client secret not found")

    def ready(self):
        logging.basicConfig(level=logging.INFO)
        logging.getLogger().handlers[0].setFormatter(LoggingFormatterClass())

        self.load_environment_variables()

        self.tracks = load_tracks(f"{self.data_path}/tracks.csv")
        
        self.umap = load_umap(self.tracks, f"{self.data_path}/umap.hdf")

        logging.info("Application ready ✅")

