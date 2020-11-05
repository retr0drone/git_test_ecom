from django import forms
from . models import OrderItem, ColorVariation, Product, SizeVariation


class AddToCartForm(forms.ModelForm):
    #permits display of color & size form fields on the frontend
    color = forms.ModelChoiceField(queryset=ColorVariation.objects.none()) 
    size = forms.ModelChoiceField(queryset=SizeVariation.objects.none()) 

    class Meta:
        model = OrderItem
        fields = ['quantity', 'color', 'size']

        """
        Initialize the form and pass in the product_id to get the product
        and set the queryset to be only the available colors
        """

    def __init__(self, *args, **kwargs):
        product_id = kwargs.pop('product_id')
        product = Product.objects.get(id=product_id)
        super().__init__(*args, **kwargs)

        #permits display of size field dropdown numbers on the frontend
        self.fields['color'].queryset = product.available_colors.all()
        self.fields['size'].queryset = product.available_sizes.all()

        