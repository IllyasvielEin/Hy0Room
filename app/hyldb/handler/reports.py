from flask import current_app

from app.hyldb.models.reports import Reports, ReportState, ReportType


class ReportsHandler:

    @staticmethod
    def get_one(report_id: int):
        res = Reports.get_one_by_id(oid=report_id)
        return res

    @staticmethod
    def get_all():
        try:
            res = Reports.get()
        except Exception as e:
            current_app.logger.error(f"{e}")
            res = []
        return res

    @staticmethod
    def get_all_needed_judge():
        try:
            res = Reports.get(
                filters={
                    'state': ReportState.JUDGING
                }
            )
        except Exception as e:
            current_app.logger.error(f"{e}")
            res = []
        return res

    @staticmethod
    def add_reports(content_id: int, content: str, content_type: ReportType, accuser_id: int, accused_id: int):
        res = Reports.add(
            content=content,
            content_id=content_id,
            content_type=content_type,
            accused_id=accused_id,
            accuser_id=accuser_id
        )
        return res is not None

    @staticmethod
    def find_guilty(report_id: int, guilty: bool):
        if guilty:
            ok = Reports.update(
                oid=report_id,
                kv={
                    'state': ReportState.GUILTY
                }
            )
        else:
            ok = Reports.update(
                oid=report_id,
                kv={
                    'state': ReportState.NOTGUILTY
                }
            )
        return ok
