from libs.api_exception import CustomError


RANDOM_DESTINATION = "random_destination"
VALIDATE_DESTINATION = "validate_destination"


def raise_error(error, extras={}):
    error = list(error)
    raise CustomError(
        {"status": error[0], "message": error[1], **extras},
        error[2],
    )
