"""Рализует функции для работы с Google таблицами."""
from google_api.const import READ_GOOGLESHEET_RANGHE


def read_values(service, spreadsheet_id):
    """Читает диапазон READ_GOOGLESHEET_RANGHE из google аблици с id=spreadsheet_id"""
    response = (
        service.spreadsheets()
        .values()
        .get(
            spreadsheetId=spreadsheet_id,
            range=READ_GOOGLESHEET_RANGHE,
        )
        .execute()
    )
    return response["values"]
