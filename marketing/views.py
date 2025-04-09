from django.shortcuts import render, redirect
from office.models import *
from marketing.models import *
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt

# Create your views here.
def marketing_home(request):
    if request.session.has_key('marketing_mobile'):
        marketing_mobile = request.session['marketing_mobile']
        m = Marketing_employee.objects.get(mobile=marketing_mobile)
        
        context= {
            'm': m,
            'dillers': Dealer.objects.filter(status=1).order_by('-id'),
        }
        return render(request, 'marketing/marketing_home.html', context)
    else:
        return redirect('marketing_login')
    
@csrf_exempt
def select_diller(request, id):
    if request.session.has_key('marketing_mobile'):
        marketing_mobile = request.session['marketing_mobile']
        m = Marketing_employee.objects.get(mobile=marketing_mobile)
        if 'add_item_to_cart'in request.POST:
            item_id = request.POST.get('item_id')
            qty = request.POST.get('qty')
            price = request.POST.get('price')
            marketing_Cart(
                marketing_employee=m,
                diller_id=id,
                item_id=item_id,
                qty=qty,
                price=price,
                total_amount=float(int(qty) * int(price))
            ).save()
            messages.success(request, f'{Item.objects.filter(id=item_id).first().name} Added to Cart Successfully')
            return redirect('select_diller', id=id)
        
        if 'Delete'in request.POST:
            cart_id = request.POST.get('cart_id')
            m =marketing_Cart.objects.filter(id=cart_id).first()
            messages.success(request, f'{m.item.name} Removed from Cart Successfully')
            m.delete()
            return redirect('select_diller', id=id)
        context= {
            'm': m,
            'dealer ': Dealer.objects.filter(status=1, id=id).first(),
            'items': Item.objects.filter(status=1).order_by('-id'),
            'cart': marketing_Cart.objects.filter(marketing_employee=m, diller_id=id).order_by('-id'),
        }
        return render(request, 'marketing/select_diller.html', context)
    else:
        return redirect('marketing_login')