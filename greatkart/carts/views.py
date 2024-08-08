from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse

from store.models import Product, Variation
from .models import Cart, CartItem
from django.core.exceptions import ObjectDoesNotExist

def cart(request, total = 0, quantity =0, cart_item=None):
    try:
        tax=0
        grand_total=0
        cart = Cart.objects.get(cart_id= _cart_id(request))
        cart_items =CartItem.objects.filter(cart=cart, is_active = True)
        for cart_item in cart_items:
            total += (cart_item.product.price * cart_item.quantity)
            quantity += cart_item.quantity
        tax= (2 *total)/100
        grand_total = total +tax
    except ObjectDoesNotExist:
        pass

    context = {
        'total' : total,
        'quantity': quantity,
        'cart_items': cart_items,
        'tax':tax,
        'grand_total':grand_total,

    }
    return render(request,'store/cart.html', context)


def _cart_id(request):
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart

def add_cart(request, product_id):
    product = Product.objects.get(id = product_id)
    variation_product =[]
    if request.method =="POST":
        for item in request.POST:
            key = item
            value = request.POST[key]

            try:
                variation = Variation.objects.get(
                    product = product,
                    variation_category__iexact =key,
                    variation_value__iexact = value)
                variation_product.append(variation)
            except:
                pass
        

    try:
        cart = Cart.objects.get(cart_id =_cart_id(request))
    except Cart.DoesNotExist:
        cart = Cart.objects.create(
            cart_id = _cart_id(request)
        )
    cart.save()
    is_cart_item_exist = CartItem.objects.filter(product=product, cart=cart).exists()

    if is_cart_item_exist:
        cart_item = CartItem.objects.filter(product=product,cart=cart)
        # existing variation 

        # product variation ( current variation)
        # item id
        ex_var_list =[]
        id = []
        for item in cart_item:
            existing_variation = item.variations.all()
            ex_var_list.append(list(existing_variation))
            id.append(item.id)

        print(ex_var_list)

        if variation_product in ex_var_list:
            index = ex_var_list.index(variation_product)
            item_id = id[index]
            item = CartItem.objects.get(product=product,cart=cart, id =item_id)
            item.quantity +=1
            item.save()
        else:
            item = CartItem.objects.create(product=product,cart=cart, quantity =1)
            if len(variation_product)>0:
                item.variations.clear()
                item.variations.add(*variation_product)

            
            item.save()
    else:
        cart_item = CartItem.objects.create(
            product = product,
            cart = cart,
            quantity =1,
        )
        if len(variation_product)>0:
            cart_item.variations.clear()
            for item in variation_product:
                cart_item.variations.add(*variation_product)
        cart_item.save()

    return redirect('cart')


def remove_cart(request, product_id, cart_item_id ):
    cart = Cart.objects.get(cart_id =_cart_id(request))
    product = get_object_or_404(Product, id = product_id)
    try:
        cart_item = CartItem.objects.get(product=product, cart = cart, id = cart_item_id)

        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
        else:
            cart_item.delete()
    except:
        pass

    return redirect('cart')

def remove_cart_item(request, product_id, cart_item_id):
    cart = Cart.objects.get(cart_id =_cart_id(request))
    product = get_object_or_404(Product, id = product_id)
    cart_item = CartItem.objects.get(product=product, cart = cart, id = cart_item_id)

    
    cart_item.delete()

    return redirect('cart')

