from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.core.exceptions import ObjectDoesNotExist
from django.views.generic import View
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Product, Category, Brand, Inventory
from django.views.decorators.http import require_http_methods
import json

@method_decorator(csrf_exempt, name='dispatch')
class ProductView(View):
    def get(self, request, product_id=None):
        if product_id:
            try:
                product = Product.objects.get(id=product_id)
                inventory_list = [{"location": inv.location, "quantity": inv.quantity} for inv in product.inventory_set.all()]
                return JsonResponse({
                    "id": product.id,
                    "name": product.name,
                    "description": product.description,
                    "category": product.category.name if product.category else None,
                    "price": float(product.price),
                    "brand": product.brand.name if product.brand else None,
                    "inventory": inventory_list,  
                    "quantity": sum(inv["quantity"] for inv in inventory_list),
                    "created_at": product.created_at,
                    "updated_at": product.updated_at
                })
            except ObjectDoesNotExist:
                return JsonResponse({"error": "Product not found"}, status=404)
        else:
            products = Product.objects.all()
            page = request.GET.get("page", 1) 
            page_size = request.GET.get("page_size", 10)
            paginator = Paginator(products, page_size)
            try:
                paginated_products = paginator.page(page)
            except PageNotAnInteger:
                paginated_products = paginator.page(1)  
            except EmptyPage:
                paginated_products = [] 

            product_list = [{
                "id": p.id,
                "name": p.name,
                "description": p.description,
                "category": p.category.name if p.category else None,
                "price": float(p.price),
                "brand": p.brand.name if p.brand else None,
                "inventory": [{"location": inv.location, "quantity": inv.quantity} for inv in p.inventory_set.all()],
                "quantity": sum(inv.quantity for inv in p.inventory_set.all()),
                "created_at": p.created_at,
                "updated_at": p.updated_at
            } for p in paginated_products]

            return JsonResponse({
                "products": product_list,
                "page": int(page),
                "total_pages": paginator.num_pages,
                "total_products": paginator.count
            })
        # return JsonResponse(product_list, safe=False)

    def post(self, request):
        print("request", request.body)
        try:
            data = json.loads(request.body)
            print("data", data)
            required_fields = ["name", "description", "category", "price", "brand"]
            if not all(field in data for field in required_fields):
                return JsonResponse({"error": "Missing required fields"}, status=400)

            category, _ = Category.objects.get_or_create(name=data["category"])
            brand, _ = Brand.objects.get_or_create(name=data["brand"])

            product = Product.objects.create(
                name=data["name"],
                description=data["description"],
                category=category,
                price=data["price"],
                brand=brand
            )
            return JsonResponse({"message": "Product created", "id": product.id}, status=201)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)
        

    def put(self, request, product_id):
        try:
            data = json.loads(request.body)
            product = Product.objects.get(id=product_id)
            
            if "category" in data:
                category, _ = Category.objects.get_or_create(name=data["category"])
                product.category = category
            if "brand" in data:
                brand, _ = Brand.objects.get_or_create(name=data["brand"])
                product.brand = brand
            
            for key, value in data.items():
                if key not in ["category", "brand"]:
                   setattr(product, key, value)
            product.save()
            return JsonResponse({"message": "Product updated successfully"})
        except ObjectDoesNotExist:
            return JsonResponse({"error": "Product not found"}, status=404)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)

    def delete(self, request, product_id):
        try:
            product = Product.objects.get(id=product_id)
            product.delete()
            return JsonResponse({"message": "Product deleted successfully"})
        except ObjectDoesNotExist:
            return JsonResponse({"error": "Product not found"}, status=404)
        

@method_decorator(csrf_exempt, name='dispatch')
class BrandView(View):
    def get(self, request):
        brands = Brand.objects.all()
        brand_list = [{"id": b.id, "name": b.name,"description": b.description} for b in brands]
        return JsonResponse({"brands": brand_list})
        # return JsonResponse(brand_list, safe=False)

    def post(self, request):
        try:
            data = json.loads(request.body)
            brand, created = Brand.objects.get_or_create(name=data["name"])
            return JsonResponse({"message": "Brand created", "id": brand.id}, status=201)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)

    def delete(self, request, brand_id):
        try:
            brand = Brand.objects.get(id=brand_id)
            brand.delete()
            return JsonResponse({"message": "Brand deleted successfully"})
        except ObjectDoesNotExist:
            return JsonResponse({"error": "Brand not found"}, status=404)
        
    def put(self, request, brand_id):
        try:
            data = json.loads(request.body)
            brand = Brand.objects.get(id=brand_id)
            brand.name = data.get("name", brand.name)
            brand.description = data.get("description", brand.description)
            brand.save()
            return JsonResponse({"message": "Brand updated successfully"})
        except ObjectDoesNotExist:
            return JsonResponse({"error": "Brand not found"}, status=404)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)
        

@method_decorator(csrf_exempt, name='dispatch')
class InventoryView(View):
    # def dispatch(self, request, *args, **kwargs):
    #     print(f"Dispatch method: {request.method}") 
    #     return super().dispatch(request, *args, **kwargs)
    

    def get(self, request, inventory_id=None):
        if inventory_id:
            try:
                inventory = Inventory.objects.get(id=inventory_id)
                return JsonResponse({"id": inventory.id, "product": inventory.product.name, "quantity": inventory.quantity,"location": inventory.location})
            except ObjectDoesNotExist:
                return JsonResponse({"error": "Inventory not found"}, status=404)
        else:
            inventories = Inventory.objects.all()
            inventory_list = [{"id": inv.id, "product": inv.product.name, "quantity": inv.quantity, "location": inv.location } for inv in inventories]
            return JsonResponse({"inventories": inventory_list})
            # return JsonResponse(inventory_list, safe=False)

    def post(self, request):
        try:
            data = json.loads(request.body)
            product = Product.objects.get(id=data["product_id"])
            inventory = Inventory.objects.create(product=product, quantity=data["quantity"], location=data["location"])
            return JsonResponse({"message": "Inventory created", "id": inventory.id}, status=201)
        except ObjectDoesNotExist:
            return JsonResponse({"error": "Product not found"}, status=404)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)

    def put(self, request, inventory_id):
        try:
            data = json.loads(request.body)
            inventory = Inventory.objects.get(id=inventory_id)
            inventory.quantity = data.get("quantity", inventory.quantity)
            inventory.location = data.get("location", inventory.location)
            inventory.product = data.get("product_id", inventory.product)
            inventory.save()
            return JsonResponse({"message": "Inventory updated successfully"})
        except ObjectDoesNotExist:
            return JsonResponse({"error": "Inventory not found"}, status=404)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)

    def delete(self, request, inventory_id):
        try:
            inventory = Inventory.objects.get(id=inventory_id)
            inventory.delete()
            return JsonResponse({"message": "Inventory deleted successfully"})
        except ObjectDoesNotExist:
            return JsonResponse({"error": "Inventory not found"}, status=404)

@method_decorator(csrf_exempt, name='dispatch')
class CategoryView(View):

    # def dispatch(self, request, *args, **kwargs):
    #     print(f"Dispatch method: {request.method}") 
    #     return super().dispatch(request, *args, **kwargs)

    def get(self, request,category_id=None):
        if category_id:
            try:
                category = Category.objects.get(id=category_id)
                return JsonResponse({"id": category.id, "name": category.name, "description": category.description})
            except ObjectDoesNotExist:
                return JsonResponse({"error": "Category not found"}, status=404)
        else:
            categories = Category.objects.all()
            category_list = [{"id": c.id, "name": c.name, "description": c.description} for c in categories]
            return JsonResponse(category_list, safe=False)

    def post(self, request):
        print("request", request.body)
        try:
            data = json.loads(request.body)
            print("data", data)
            category, created = Category.objects.get_or_create(name=data["name"], description=data["description"])
            if not created:
                return JsonResponse({"error": "Category already exists"}, status=400)
            category.description = data["description"]
            category.save()
            return JsonResponse({"message": "Category created", "id": category.id}, status=201)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)
        
    def put(self, request, category_id):
        try:
            data = json.loads(request.body)
            category = Category.objects.get(id=category_id)
            category.name = data.get("name", category.name)
            category.description = data.get("description", category.description)
            category.save()
            return JsonResponse({"message": "Category updated successfully"})
        except ObjectDoesNotExist:
            return JsonResponse({"error": "Category not found"}, status=404)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)

    def delete(self, request, category_id):
        print(f"Received method: {request.method}")  
        try:
            category = Category.objects.get(id=category_id)
            category.delete()
            return JsonResponse({"message": "Category deleted successfully"})
        except ObjectDoesNotExist:
            return JsonResponse({"error": "Category not found"}, status=404)
