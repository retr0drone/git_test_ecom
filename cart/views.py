from . models import Product, OrderItem
from django.views import generic
from django.shortcuts import render
from . utils import get_or_set_order_session
from django.shortcuts import get_object_or_404, reverse
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
        return reverse('home')  #todo cart

    def form_valid(self, form):
        order = get_or_set_order_session(self.request)
        product = self.get_object()

        item_filter = order.items.filter(product=product)
        if item_filter.exists():
            item = item_filter.first()
            item.quantity = int(form.cleaned_data['quantity']) # quantity from forms.py
            item.save()

        else:
            new_item = form.save(commit=False) #saves an OrderItem instance commit False = Not saving session info yet
            new_item.product = product
            new_item.order = order #order from the session
            new_item.save()
        return super(ProductDetailView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(ProductDetailView, self).get_context_data(**kwargs)
        context['product'] = self.get_object()
        return context
