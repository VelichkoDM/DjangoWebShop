from django.shortcuts import render, redirect
from .models import OrderItem
from .forms import OrderCreateForm
from cart.cart import Cart
from django.urls import reverse
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import get_object_or_404
from .models import Order
from django.conf import settings
from django.http import HttpResponse
from django.template.loader import render_to_string
#import weasyprint


def order_create(request):
    cart = Cart(request)
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            if cart.coupon:
                order.coupon = cart.coupon
                order.discount = cart.coupon.discount
            order.save()
        else:
            return render(request,
                          'orders/order/create.html',
                          {'cart': cart, 'form': form})
            for item in cart:
                OrderItem.objects.create(order=order,
                                         product=item['product'],
                                         price=item['price'],
                                         quantity=item['quantity'])
            # Очищаем корзину.
            cart.clear()
            # Сохранение заказа в сессии.
            request.session['order_id'] = order.id
            # Перенапрвление на страницу оплату
            return redirect(reverse('payment:process'))
    else:
        form = OrderCreateForm()
    return render(request,
                  'orders/order/create.html',
                  {'cart': cart, 'form': form})


# @staff_member_required
# def admin_order_detail(request, order_id):
#     order = get_object_or_404(Order, id=order_id)
#     html = render_to_string('orders/order/pdf.css.html',
#                             {'order': order})
#     response = HttpResponse(content_type='application/pdf.css')
#     response['Content-Disposition'] = 'filename=\
#         "order_{}.pdf.css"'.format(order.id)
#     weasyprint.HTML(string=html).write_pdf(response,
#                                            stylesheets=[weasyprint.CSS(
#                                                settings.STATIC_ROOT + 'css/pdf.css.css')])
#     return response
