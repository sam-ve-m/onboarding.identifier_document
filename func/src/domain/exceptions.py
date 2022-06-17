class ErrorOnDecodeJwt(Exception):
    msg = "Jormungandr-Onboarding::user_identifier_data::Fail when trying to get unique id," \
          " jwt not decoded successfully"


class ErrorOnSendAuditLog(Exception):
    msg = "Jormungandr-Onboarding::user_identifier_data::Error when trying to send log audit on Persephone"


class FileNotExists(Exception):
    msg = "Jormungandr-Onboarding::DocumentService::_content_exists::Not found any content in bucket path"
