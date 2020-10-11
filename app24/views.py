from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from rest_framework.parsers import JSONParser
from rest_framework.renderers import JSONRenderer
from app24.models import ProductModel
import json
import io
from app24.serializers import ProductSerializer
@method_decorator(csrf_exempt, name="dispatch")
class Product_Operations(View):

    def post(self,request):
        b_data=request.body
        s_data=io.BinaryIo(b_data)
        d_data=JSONParser().parse(s_data)
        ProductModel(name=d_data["name"],price=d_data["price"],quantity=d_data["quantity"]).save()
        ps=ProductSerializer(data=d_data)
        if ps.is_valid():
            ps.save()
            message={"message":"Data Inserted"}
        else:
            message={"error":ps.errors}
        json=JSONRenderer().render(message)
        return HttpResponse(json,content_type="application/json")

    def get(self,request):
        result=ProductModel.objects.all()
        ps=ProductSerializer(result,many=True)
        json_data=JSONRenderer().render(ps.data)

        return HttpResponse(json_data,content_type="application/json")

    def put(self,request,product):
        try:
            old_product=ProductModel.objects.get(no=product)
            new_product=json.loads(request.body)
            data={
                "no":old_product.no,
            "name":old_product,
            "price":old_product.price,
            "quantity":old_product.quantity
            }
            for key,value in new_product.items():
                data[key]=value
            pf=ProductModel(new_product,isinstance=old_product)
            if pf.is_valid():
                pf.save()
                json_data=json.dumps({"success":"product is updated"})
            else:
                json_data=json.dumps(pf.errors)
                return HttpResponse(json_data,content_type="application/json")
        except ProductModel.DoesNotExist:
            json_data=json.dumps({"error":"invalid product"})
            return HttpResponse(json_data,content_type="application/json")

    def delete(self,request,product):
        try:
            result=ProductModel.objects.get(no=product).delete()
            if result[0]==1:
                json_data=json.dumps({"message":"product is deleted"})
                return  HttpResponse(json_data,content_type="application/json")
        except ProductModel.DoesNotExist:
            json_data=json.dumps({"error":"Invalid Product"})
            return HttpResponse(json_data,content_type="application/json")



