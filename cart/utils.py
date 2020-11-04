#utils.py is for creating an order and setting it in our session or getting the order from the session

from.models import Order


def get_or_set_order_session(request):
    order_id = request.session.get('order_id', None)
    if order_id is None: #no order_id yet
        order = Order() #new order instance
        order.save()
        request.session['order_id'] = order.id

    else: #get the order & confirm its not been paid for
        try:
            order = Order.objects.get(id=order_id, ordered=False) #order_id from session
        except Order.DoesNotExist:
            order = Order()
            order.save()
            request.session['order_id'] = order.id

    # Allows unauth users move through till time to pay
    if request.user.is_authenticated and order.user is None:
        order.user = request.user
        order.save()
    return order


