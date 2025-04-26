from django.test import TestCase

# Create your tests here.
def pending_order(request):
    if request.session.has_key('office_mobile'):
        office_mobile = request.session['office_mobile']
        e=Office_employee.objects.filter(mobile=office_mobile).first()
        if e:
            m_cart = []
            for em in Marketing_employee.objects.filter(status=1):
                for d in Dealer.objects.filter(status=1):
                    if marketing_Cart.objects.filter(marketing_employee=em, dealer=d).exists():
                            c = marketing_Cart.objects.filter(marketing_employee=em, dealer=d).first()
                            if c:
                                m_cart.append({
                                    'marketing_employee':em,
                                    'dealer':c.dealer,
                                    'date':c.date
                                })
        context={
            'e':e,
            'm_cart':m_cart,
        }
        return render(request, 'office/pending_order.html', context)
    else:
        return redirect('login')