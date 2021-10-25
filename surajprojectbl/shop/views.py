from django.shortcuts import render,HttpResponse
from .models import Product,Order,orderUpdate
from math import ceil
import json
import checksum
from django.views.decorators.csrf import csrf_exempt
from paytm import checksum

MERCHANT_KEY = 'kbzk1OSbJiV_O3p5'

# Create your views here.
def shopHome(request):
    #products = Product.objects.all()
    #print(products)
    #n = len(products)
    #nSlides = n//4 + ceil((n/4)-(n//4))
    allProds = []
    catprods = Product.objects.values('category','product_id')
    cats = {item['category'] for item in catprods}
    for cat in cats:
        prod = Product.objects.filter(category=cat)
        n = len(prod)
        nSlides = n // 4 + ceil((n / 4) - (n // 4))
        allProds.append([prod,range(1,nSlides),nSlides])
    #params = { 'no_of_slides':nSlides,'range':range(1,nSlides),'product':products}
    #allProds = [[products,range(1,nSlides),nSlides],[products,range(1,nSlides),nSlides]]
    params = {'allProds':allProds}
    return render(request,'shop/shopHome.html',params)

def tracker(request):
    if request.method == 'POST':
        email = request.POST.get('email', '')
        orderid = request.POST.get('OrderId', '')
        try:
            orders = Order.objects.filter(order_id=orderid,email=email)
            if len(orders)>0:
                update=orderUpdate.objects.filter(order_id=orderid)
                updates=[]
                for item in update:
                    updates.append({'text':item.update_desc,'time':item.timestamp})
                    response =json.dumps([updates,orders[0].items_json],default=str)
                return HttpResponse(response)
            else:
                return HttpResponse('{}')
        except Exception as e:
            return HttpResponse('{}')

    return render(request,'shop/tracker.html')

def search(request):
    return HttpResponse('searching')

def productView(request,product_id):
    #fetch the product using the id
    product = Product.objects.filter(product_id=product_id)
    print(product)
    return render(request, 'shop/prodview.html',{'product':product[0]})

def checkOut(request):
    if request.method == 'POST':
        items_json = request.POST.get('itemJson', '')
        name = request.POST.get('name', '')
        amount = request.POST.get('amount', '')
        email = request.POST.get('email', '')
        address = request.POST.get('address1', '') + " " + request.POST.get('address2', '')
        state = request.POST.get('state', '')
        city = request.POST.get('city', '')
        zip_code = request.POST.get('zip_code', '')
        phone = request.POST.get('phone', '')



        orders = Order(items_json=items_json,name=name, email=email, phone=phone, address=address, city=city, zip_code=zip_code, state=state,amount=amount)
        orders.save()
        update = orderUpdate(order_id=orders.order_id,update_desc="the order has been placed succesfully")
        update.save()
        thank=True
        id = orders.order_id
        #return render(request, 'shop/checkout.html',{'thank':thank,'id':id})
        # request paytm to transfer the amount  to your account after payment by user
        param_dict = {

            'MID': 'WorldP64425807474247',
            'ORDER_ID': str(orders.order_id),
            'TXN_AMOUNT': str(amount),
            'CUST_ID': 'email',
            'INDUSTRY_TYPE_ID': 'Retail',
            'WEBSITE': 'WEBSTAGING',
            'CHANNEL_ID': 'WEB',
            'CALLBACK_URL': 'http://127.0.0.1:8000/shop/handlerequest/',

        }
        param_dict['CHECKSUMHASH'] = checksum.generate_checksum(param_dict,MERCHANT_KEY)
        return render(request, 'shop/paytm.html', {'param_dict': param_dict})

    return render(request, 'shop/checkout.html')

@csrf_exempt
def handlerequest(request, response_dict={}):
    #paytm will send you post request here to verify
    form=request.POST
    for i in form.keys():
        response_dict[i] = form[i]
        if i == 'CHECKSUMHASH':
            checksum = form[i]

    verify = checksum.verify_checksum(response_dict,MERCHANT_KEY,checksum)
    if verify:
        if response_dict['RESPCODE'] == '01':
            print('order successful')
        else:
            print('order no succeed' + response_dict['RESPMSG'])
    #return HttpResponse('done')

    return render(request,'shop/paymentstatus.html',{'response':response_dict})
# here i have to create merchant account and putting merchant id then it will works