class Payload:
    def __init__(self, userId, organizationId=None, userType=None, userTypeId=None):
        self.userId = userId
        self.organizationId = organizationId,
        self.userType = {
            'type': userType.__name__ if userType else None,
            'id': userTypeId
        }