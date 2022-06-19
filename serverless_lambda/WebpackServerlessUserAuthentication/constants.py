from enum import Enum

class ApiRouteEnum(Enum):
    SIGNUP_ROUTE = '/development/auth/signupUser'
    LOGIN_ROUTE = '/development/auth/loginUser'
    CONFIRM_SIGNUP_ROUTE = '/development/auth/confirmSignup'
    FORGOT_PASSWORD_ROUTE = '/development/auth/forgetPassword'
    CONFIRM_FORGOT_PASSWORD_ROUTE = '/development/auth/confirmForgetPassword'
    RESENT_CONFIRMATION_CODE_ROUTE = '/development/auth/resendConfirmationCode'
    GET_USER_ACCESS_ROUTE = '/development/auth/getUserAccess'