import logging
from http import HTTPStatus
from typing import List, Optional

import fastapi
import flask

from overhave.api.deps import get_feature_storage, get_feature_tag_storage, get_redis_producer, get_test_run_storage
from overhave.api.views.tags_views import tags_item_handler
from overhave.storage import FeatureModel, IFeatureStorage, IFeatureTagStorage, TestRunModel, TestRunStorage
from overhave.transport import RedisProducer, TestRunData, TestRunTask

logger = logging.getLogger(__name__)


def get_features_handler(
    tag_id: Optional[int] = None,
    tag_value: Optional[str] = None,
    feature_storage: IFeatureStorage = fastapi.Depends(get_feature_storage),
    tag_storage: IFeatureTagStorage = fastapi.Depends(get_feature_tag_storage),
) -> List[FeatureModel]:
    if tag_id is not None:
        logger.info("Getting %s by tag_id=%s...", FeatureModel.__name__, tag_id)
        return feature_storage.get_features_by_tag(tag_id=tag_id)
    if tag_value is not None:
        logger.info("Getting %s by tag_value=%s...", FeatureModel.__name__, tag_value)
        tag_model = tags_item_handler(value=tag_value, feature_tag_storage=tag_storage)
        return feature_storage.get_features_by_tag(tag_id=tag_model.id)
    raise fastapi.HTTPException(
        status_code=HTTPStatus.BAD_REQUEST, detail="'tag_id' or 'tag_value' query parameter should be set"
    )


def run_test_by_tag_handler(
    tag_run: str,
    test_run_storage: TestRunStorage = fastapi.Depends(get_test_run_storage),
    redis_producer: RedisProducer = fastapi.Depends(get_redis_producer),
    feature_storage: IFeatureStorage = fastapi.Depends(get_feature_storage),
    tag_storage: IFeatureTagStorage = fastapi.Depends(get_feature_tag_storage),
) -> list[str]:
    tag_model = tags_item_handler(value=tag_run, feature_tag_storage=tag_storage)
    features = feature_storage.get_features_by_tag(tag_id=tag_model.id)
    if len(features) == 0:
        raise fastapi.HTTPException(
            status_code=HTTPStatus.BAD_REQUEST, detail=f"Features with tag='{tag_run}' does not exist"
        )
    urls: list[str] = []
    for feature in features:
        test_run_id = test_run_storage.create_test_run(scenario_id=feature.id, executed_by=feature.author)
        redis_producer.add_task(TestRunTask(data=TestRunData(test_run_id=test_run_id)))
        urls.append(flask.url_for("testrun.details_view", id=test_run_id))
    return urls


def get_test_run_handler(
    test_run_id: int,
    test_run_storage: TestRunStorage = fastapi.Depends(get_test_run_storage),
) -> TestRunModel:
    test_run = test_run_storage.get_test_run(test_run_id)
    if test_run is None:
        raise fastapi.HTTPException(
            status_code=HTTPStatus.BAD_REQUEST, detail=f"Test run with id ='{test_run_id}' not found"
        )
    return test_run
