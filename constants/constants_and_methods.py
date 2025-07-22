RANDOM_DESTINATION = "random_destination"
VALIDATE_DESTINATION = "validate_destination"


def raise_error(code, message, status):
    raise ValueError(f"Error {code}: {message} (status {status})")
