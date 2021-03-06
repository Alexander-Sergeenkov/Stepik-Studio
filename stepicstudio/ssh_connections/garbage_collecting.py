import logging
from datetime import datetime, timedelta

from django.conf import settings

from stepicstudio.operations_statuses.statuses import ExecutionStatus
from stepicstudio.ssh_connections.tablet_client import TabletClient
from stepicstudio.utils.utils import bytes2human

logger = logging.getLogger(__name__)


def collect_garbage():
    tablet_client = TabletClient()
    result_size = 0
    ss_count = 0
    from stepicstudio.models import SubStep
    for substep in SubStep.objects.all():
        if is_outdated(substep):
            status, size = tablet_client.delete_folder(substep.os_tablet_path)

            if status.status is ExecutionStatus.SUCCESS:
                ss_count += 1
                result_size += size
                logger.info('Tablet\'s directory deleted. (path: %s) \n Released memory: %s', substep.os_tablet_path,
                            bytes2human(size))

    tablet_client.close()
    logger.info('Collected %s of garbage (%s folders).\n GC delay: %s days.',
                bytes2human(result_size),
                ss_count,
                settings.GARBAGE_COLLECT_DELAY)


def is_outdated(substep) -> bool:
    create_time = datetime.fromtimestamp(substep.start_time / 1000)
    return datetime.now() - create_time > timedelta(days=settings.GARBAGE_COLLECT_DELAY)
