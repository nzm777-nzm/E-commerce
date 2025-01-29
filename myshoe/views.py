from django.shortcuts import render,redirect

from django.views.generic import View

from myshoe.forms import SignupForm,LoginForm,OrderForm

from django.core.mail import send_mail

from myshoe.models import User,BasketItem,OrderItem,Order

from django.contrib import messages

from django.contrib.auth import authenticate,login

from myshoe.models import ShoeProduct,ShoeSize

from django.core.paginator import Paginator

from django.views.decorators.csrf import csrf_exempt

from django.utils.decorators import method_decorator

from decouple import config

RZP_KEY_ID= config('RZP_KEY_ID')

RZP_KEY_SECRET= config('RZP_KEY_SECRET')

# Create your views here.

def send_otp_mail(user):
    
    user.generate_otp()
    
    subject="verify your email"
    
    message=f"otp for account verification{user.otp}"
    
    from_email="nazeempm7@gmail.com"
    
    to_email=[user.email]
    
    send_mail(subject,message,from_email,to_email)

class SignUpView(View):
    
    template_name="register.html"
    
    form_class=SignupForm
    
    def get(self,request,*args,**kwargs):
        
        form_instance=self.form_class()
        
        return render(request,self.template_name,{"form":form_instance})
    
    def post(self,request,*args,**kwargs):
        
        form_data=request.POST
        
        form_instance=self.form_class(form_data)
        
        if form_instance.is_valid():
            
            user_object=form_instance.save(commit=False)
            
            user_object.is_active=False
                        
            user_object.save()
            
            send_otp_mail(user_object)
            
            return redirect("verify-email")
        
        return render(request,self.template_name,{"form":form_instance})
          
class VerifyEmailView(View):
    
    template_name="verify_email.html"
    
    def get(self,request,*args,**kwargs):
        
        return render(request,self.template_name)
    
    def post(self,request,*args,**kwargs):
        
        otp=request.POST.get("otp")
        
        user_object=User.objects.get(otp=otp)
        
        try:
        
            user_object.is_active=True
            
            user_object.is_verified=True
            
            user_object.otp=None
            
            user_object.save()
            
            return redirect("signup")
        
        except:
            
            messages.error(request,"invalid otp")
            
            return render(request,self.template_name)


class SigninVIew(View):
    
    template_name="signin.html"
    
    form_class=LoginForm
    
    def get(self,request,*args,**kwargs):
        
        form_instance=self.form_class()
        
        return render(request,self.template_name,{"form":form_instance})
    
    def post(self,request,*args,**kwargs):
        
        form_data=request.POST
        
        form_instance=self.form_class(form_data)
        
        if form_instance.is_valid():
            
            uname=form_instance.cleaned_data.get("username")
            
            pwd=form_instance.cleaned_data.get("password")
            
            user_object=authenticate(request,username=uname,password=pwd)
            
            if user_object:
                
                login(request,user_object)
                
                return redirect("product-list")
            
            return render(request,self.template_name,{"form":form_instance})
        
        
class CarouselView(View):
    
    template_name="carouselindex.html"
    
    def get(self,request,*args,**kwargs):
        
        qs=ShoeProduct.objects.all()
        
        return render(request,self.template_name,{"data":qs})
class ProductListView(View):
    
    template_name="index.html"
    
    def get(self,request,*args,**kwargs):
        
        qs=ShoeProduct.objects.all()
        
        paginator=Paginator(qs,3)
        
        page_number=request.GET.get("page")
        
        page_obj=paginator.get_page(page_number)
        
        return render(request,self.template_name,{"page_obj":page_obj}) 

class ProductDetailView(View):
    
    template_name="product_detail.html"
    
    def get(self,request,*args,**kwargs):
        
        id=kwargs.get("pk")
        
        qs=ShoeProduct.objects.get(id=id)
        
        return render(request,self.template_name,{"product":qs})

class AddToCartView(View):
    
    def post(self,request,*args,**kwargs):
        
        id=kwargs.get("pk")
        
        size=request.POST.get("size")   
        
        quantity=request.POST.get("quantity")
        
        product_obj=ShoeProduct.objects.get(id=id)
        
        size_obj=ShoeSize.objects.get(name=size)
        
        basket_obj=request.user.cart
        
        BasketItem.objects.create(
            
            product_object=product_obj,
            
            quantity=quantity,
            
            size_object=size_obj,
            
            basket_object=basket_obj
        )
        
        
        return redirect("cart-summary")
    
           
class CartSummaryView(View):
    
    template_name="cart_summary.html"
    
    def get(self,request,*args,**kwargs):
        
        qs=BasketItem.objects.filter(basket_object=request.user.cart,is_order_placed=False)
        
        basket_item_count=qs.count()
        
        basket_total=sum([bi.item_total for bi in qs])
        
        return render(request,self.template_name,{"basketitems":qs,"basket_total":basket_total,"count":basket_item_count})
    
class ItemDeleteView(View):
    
    def get(self,request,*args,**kwargs):
        
        id=kwargs.get("pk")
        
        BasketItem.objects.get(id=id).delete()
        
        return redirect("cart-summary")
    
    
import razorpay

class PlaceOrderView(View):
    
    template_name="place_order.html"
    
    form_class=OrderForm
    
    def get(self,request,*args,**kwargs):
        
        form_instance=self.form_class()
        
        qs=request.user.cart.cart_item.filter(is_order_placed=False)
        
        total=sum([bi.item_total for bi in qs])
        
        return render(request,self.template_name,{"form":form_instance,"items":qs,"total":total}) 
    
    def post(self,request,*args,**kwargs):
        
        form_data=request.POST
        
        form_instance=self.form_class(form_data)
        
        if form_instance.is_valid():
            
            form_instance.instance.customer=request.user
            
            order_instance=form_instance.save()
            
            basket_items=request.user.cart.cart_item.filter(is_order_placed=False)
            
            payment_method=form_instance.cleaned_data.get("payment_method")
            
            print(payment_method)
            
            for bi in basket_items:
                
                OrderItem.objects.create(
                    
                    order_object=order_instance,
                    
                    product_object=bi.product_object,
                    
                    quantity=bi.quantity,
                    
                    size_object=bi.size_object,
                    
                    price=bi.product_object.price
                     
                )
                
                bi.is_order_placed=True
                
                bi.save()
                
            if payment_method=="ONLINE":
                
                client = razorpay.Client(auth=(RZP_KEY_ID,RZP_KEY_SECRET))
                
                total=sum([bi.item_total for bi in basket_items])*100
                
                data = { "amount": total, "currency": "INR", "receipt": "order_rcptid_11" }
                
                payment = client.order.create(data=data)
                
                print(payment)
                
                rzp_order_id=payment.get("id")
                
                order_instance.rzp_order_id=rzp_order_id
                
                order_instance.save()
                
                context={
                    
                    "amount":total,
                    
                    "key_id":RZP_KEY_ID,
                    
                    "order_id":rzp_order_id,
                    
                    "currency":"INR"
                      
                }
                
                return render(request,"payment.html",context)          
                
        return redirect("product-list")
    
class OrderSummaryView(View):
    
    template_name="order_summary.html"
    
    def get(self,request,*args,**kwargs):
        
        qs=request.user.orders.all()
        
        return render(request,self.template_name,{"orders":qs})
    
@method_decorator([csrf_exempt],name="dispatch")

class PaymentVerificationView(View):
    
    def post(self,request,*args,**kwargs):
        
        client = razorpay.Client(auth=(RZP_KEY_ID,RZP_KEY_SECRET))
        
        try:
            
            client.utility.verify_payment_signature((request.POST))
            
            print("payment success")
            
            order_id=request.POST.get("razorpay_order_id")
            
            order_object=Order.objects.get(rzp_order_id=order_id)
            
            order_object.is_paid=True
            
            order_object.save()
            
            login(request,order_object.customer)
          
        except:
            
            print("payment failed")
        
        print(request.POST)
        
        return redirect("order-summary")