from . models import Product, OrderItem
from django.views import generic
from django.shortcuts import render
from . utils import get_or_set_order_session
from django.shortcuts import get_object_or_404, reverse, redirect
from . forms import AddToCartForm


class ProductListView(generic.ListView):
    template_name = 'cart/product_list.html' #this made no difference
    queryset = Product.objects.all() #model = Product can also be used in place of queryset


class ProductDetailView(generic.FormView):
    template_name = 'cart/product_detail.html'
    form_class = AddToCartForm


    def get_object(self):
        return get_object_or_404(Product, slug=self.kwargs['slug'])

    def get_success_url(self):
        return reverse('cart:summary')  #todo cart

    # passing product_id from forms to views to allow colors appear
    def get_form_kwargs(self):
        kwargs = super(ProductDetailView, self).get_form_kwargs()
        kwargs['product_id'] = self.get_object().id #get Product instance & pass product_id and pass into the form
        return kwargs


    def form_valid(self, form):
        order = get_or_set_order_session(self.request)
        product = self.get_object()

        '''on selecting add cart button this ensures no errors'''
        item_filter = order.items.filter(
            product=product,
            color=form.cleaned_data['color'],
            size=form.cleaned_data['size']
        )


        if item_filter.exists():
            item = item_filter.first()
            item.quantity += int(form.cleaned_data['quantity']) # quantity from forms.py
            item.save()

        else:
            new_item = form.save(commit=False) #saves an OrderItem instance commit False = Not saving session info yet
            new_item.product = product
            new_item.order = order  #order from the session
            new_item.save()
        return super(ProductDetailView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(ProductDetailView, self).get_context_data(**kwargs)
        context['product'] = self.get_object()
        return context


class CartView(generic.TemplateView):
    template_name = 'cart/cart.html'

    def get_context_data(self, **kwargs):
        context = super(CartView, self).get_context_data(**kwargs)
        context['order'] = get_or_set_order_session(self.request)
        return context


class IncreaseQuantityView(generic.View):
    def get(self, *args, **kwargs):
        order_item = get_object_or_404(OrderItem, id=kwargs['pk'])
        order_item.quantity += 1
        order_item.save()
        return redirect('cart:summary')


class DecreaseQuantityView(generic.View):
    def get(self, *args, **kwargs):
        order_item = get_object_or_404(OrderItem, id=kwargs['pk'])

        if order_item.quantity <= 1:
            order_item.delete()
        else:
            order_item.quantity -= 1
            order_item.save()
        return redirect('cart:summary')


class RemoveFromCartView(generic.View):
    def get(self, *args, **kwargs):
        order_item = get_object_or_404(OrderItem, id=kwargs['pk'])
        order_item.delete()
        return redirect('cart:summary')