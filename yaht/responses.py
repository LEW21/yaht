from multidict import CIMultiDictProxy


@dataclass
class HTTPResponse(Exception):
	"""HTTP response"""

	headers: CIMultiDictProxy
	body: ReadableStream

	@property
	def ok(self) -> bool:
		return 200 <= self.status <= 299


class HTTP2xx_Success(HTTPResponse):
	pass


Success = HTTP2xx_Success


class HTTP3xx_Redirection(HTTPResponse):
	pass


Redirection = HTTP3xx_Redirection


class HTTP4xx_ClientError(HTTPResponse):
	pass


ClientError = HTTP4xx_ClientError


class HTTP5xx_ServerError(HTTPResponse):
	pass


ServerError = HTTP5xx_ServerError


bases = {
	2: HTTP2xx_Success,
	3: HTTP3xx_Redirection,
	4: HTTP4xx_ClientError,
	5: HTTP5xx_ServerError,
}

def ResponseClass(status, statusText = None):
	return type(
		f"HTTP{status}_{statusText.replace(' ', '').replace('-', '')}",
		(bases[status//100],),
		dict(
			status = status,
			statusText = statusText,
		),
	)



OK = HTTP200_OK = ResponseClass(200, 'OK')
Created = HTTP201_Created = ResponseClass(201, 'Created')
Accepted = HTTP202_Accepted = ResponseClass(202, 'Accepted')
NonAuthoritativeInformation = HTTP203_NonAuthoritativeInformation = ResponseClass(203, 'Non-Authoritative Information')
NoContent = HTTP204_NoContent = ResponseClass(204, 'No Content')
ResetContent = HTTP205_ResetContent = ResponseClass(205, 'Reset Content')
PartialContent = HTTP206_PartialContent = ResponseClass(206, 'Partial Content')

BadRequest = HTTP400_BadRequest = ResponseClass(400, 'Bad Request')
NotAuthenticated = HTTP401_NotAuthenticated = ResponseClass(401, 'Not Authenticated')
PaymentRequired = HTTP402_PaymentRequired = ResponseClass(402, 'Payment Required')
Forbidden = HTTP403_Forbidden = ResponseClass(403, 'Forbidden')
NotFound = HTTP404_NotFound = ResponseClass(404, 'Not Found')
MethodNotAllowed = HTTP405_MethodNotAllowed = ResponseClass(405, 'Method Not Allowed')
NotAcceptable = HTTP406_NotAcceptable = ResponseClass(406, 'Not Acceptable')
ProxyAuthenticationRequired = HTTP407_ProxyAuthenticationRequired = ResponseClass(407, 'Proxy Authentication Required')
RequestTimeout = HTTP408_RequestTimeout = ResponseClass(408, 'Request Timeout')
Conflict = HTTP409_Conflict = ResponseClass(409, 'Conflict')
Gone = HTTP410_Gone = ResponseClass(410, 'Gone')
LengthRequired = HTTP411_LengthRequired = ResponseClass(411, 'Length Required')
PreconditionFailed = HTTP412_PreconditionFailed = ResponseClass(412, 'Precondition Failed')
PayloadTooLarge = HTTP413_PayloadTooLarge = ResponseClass(413, 'Payload Too Large')
URITooLong = HTTP414_URITooLong = ResponseClass(414, 'URI Too Long')
UnsupportedMediaType = HTTP415_UnsupportedMediaType = ResponseClass(415, 'Unsupported Media Type')
RangeNotSatisfiable = HTTP416_RangeNotSatisfiable = ResponseClass(416, 'Range Not Satisfiable')
ExpectationFailed = HTTP417_ExpectationFailed = ResponseClass(417, 'Expectation Failed')
MisdirectedRequest = HTTP421_MisdirectedRequest = ResponseClass(421, 'Misdirected Request')
UpgradeRequired = HTTP426_UpgradeRequired = ResponseClass(426, 'Upgrade Required')
PreconditionRequired = HTTP428_PreconditionRequired = ResponseClass(428, 'Precondition Required')
TooManyRequests = HTTP429_TooManyRequests = ResponseClass(429, 'Too Many Requests')
RequestHeaderFieldsTooLarge = HTTP431_RequestHeaderFieldsTooLarge = ResponseClass(431, 'Request Header Fields Too Large')
UnavailableForLegalReasons = HTTP451_UnavailableForLegalReasons = ResponseClass(451, 'Unavailable For Legal Reasons')

InternalServerError = HTTP500_InternalServerError = ResponseClass(500, 'Internal Server Error')
NotImplemented = HTTP501_NotImplemented = ResponseClass(501, 'Not Implemented')
BadGateway = HTTP502_BadGateway = ResponseClass(502, 'Bad Gateway')
ServiceUnavailable = HTTP503_ServiceUnavailable = ResponseClass(503, 'Service Unavailable')
GatewayTimeout = HTTP504_GatewayTimeout = ResponseClass(504, 'Gateway Timeout')
HTTPVersionNotSupported = HTTP505_HTTPVersionNotSupported = ResponseClass(505, 'HTTP Version Not Supported')


responses = {
	200: HTTP200_OK,
	201: HTTP201_Created,
	202: HTTP202_Accepted,
	203: HTTP203_NonAuthoritativeInformation,
	204: HTTP204_NoContent,
	205: HTTP205_ResetContent,
	206: HTTP206_PartialContent,
	400: HTTP400_BadRequest,
	401: HTTP401_NotAuthenticated,
	402: HTTP402_PaymentRequired,
	403: HTTP403_Forbidden,
	404: HTTP404_NotFound,
	405: HTTP405_MethodNotAllowed,
	406: HTTP406_NotAcceptable,
	407: HTTP407_ProxyAuthenticationRequired,
	408: HTTP408_RequestTimeout,
	409: HTTP409_Conflict,
	410: HTTP410_Gone,
	411: HTTP411_LengthRequired,
	412: HTTP412_PreconditionFailed,
	413: HTTP413_PayloadTooLarge,
	414: HTTP414_URITooLong,
	415: HTTP415_UnsupportedMediaType,
	416: HTTP416_RangeNotSatisfiable,
	417: HTTP417_ExpectationFailed,
	421: HTTP421_MisdirectedRequest,
	426: HTTP426_UpgradeRequired,
	428: HTTP428_PreconditionRequired,
	429: HTTP429_TooManyRequests,
	431: HTTP431_RequestHeaderFieldsTooLarge,
	451: HTTP451_UnavailableForLegalReasons,
	500: HTTP500_InternalServerError,
	501: HTTP501_NotImplemented,
	502: HTTP502_BadGateway,
	503: HTTP503_ServiceUnavailable,
	504: HTTP504_GatewayTimeout,
	505: HTTP505_HTTPVersionNotSupported,
}
