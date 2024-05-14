class CartDetailException(Exception):
    """Custom exception class for handling adding cart detail error"""

    def __init__(self, message="An error occurred", status_code=500, **kwargs):
        self.message = message
        self.status_code = status_code
        self.additional_error_args = kwargs
        super().__init__(self.message)
