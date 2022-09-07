from google_api.const import READ_GOOGLESHEET_RANGHE


def read_values(service, spreadsheetId):
    response = (
        service.spreadsheets()
        .values()
        .get(
            spreadsheetId=spreadsheetId,
            range=READ_GOOGLESHEET_RANGHE,
        )
        .execute()
    )
    return response["values"]
