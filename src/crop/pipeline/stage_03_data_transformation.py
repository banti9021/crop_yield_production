from crop.config.configuration import ConfigurationManager
from crop.components.data_transformation import DataTransformation
from crop import logger
from pathlib import Path  # Ensure you're using pathlib.Path

STAGE_NAME = "Data Transformation Stage"

class DataTransformationTrainingPipeline:
    def __init__(self):
        pass

    def check_status(self) -> bool:
        """Check the status of data validation."""
        try:
            with open(Path("artifacts/data_validation/status.txt"), "r") as f:
                status = f.read().strip().split(" ")[-1]
                return status.lower() == "true"
        except FileNotFoundError:
            logger.error("Status file not found.")
            return False
        except Exception as e:
            logger.exception("Error reading status file.")
            return False

    def perform_transformation(self):
        """Perform data transformation."""
        config = ConfigurationManager()
        data_transformation_config = config.get_data_transformation_config()
        data_transformation = DataTransformation(config=data_transformation_config)
        data_transformation.train_test_spliting()

    def main(self):
        """Main execution method for the pipeline."""
        try:
            if self.check_status():
                self.perform_transformation()
            else:
                raise Exception("Your data schema is not valid.")
        except Exception as e:
            logger.exception(e)

if __name__ == '__main__':
    try:
        logger.info(f">>>>>> stage {STAGE_NAME} started <<<<<<")
        obj = DataTransformationTrainingPipeline()
        obj.main()
        logger.info(f">>>>>> stage {STAGE_NAME} completed <<<<<<\n\nx==========x")
    except Exception as e:
        logger.exception(e)
        raise e
