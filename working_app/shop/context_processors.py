from .cart import Cart

def cart(request):
	"""This function returns the cart object.

	:param request: HttpRequest object
	:return: dictionary object
	"""

	return {'cart': Cart(request)}
