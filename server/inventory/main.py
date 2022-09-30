from fastapi import FastAPI, Depends

from fastapi.middleware.cors import CORSMiddleware
from config.config import Settings, get_settings
from models.product import Product

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=['http://localhost:3000'],
    allow_methods=['*'],
    allow_headers=['*']
)


def format_products(pk: str):
    product = Product.get(pk)
    return {
        'id': product.pk,
        'name': product.name,
        'price': product.price,
        'quantity': product.quantity,
    }


@app.get("/health-check")
def health_check():
    return {"message": "Hola Mundo!"}


@app.get('/products')
async def get_all_products():
    products = [format_products(pk) for pk in Product.all_pks()]
    return {"message": f"Successfully fetched all products", "data": products}


@app.post('/product')
async def create_new_product(product: Product):
    return {"message": f"Successfully created a new product", "data": product.save()}


@app.get('/product/{pk}')
async def get_product_details(pk: str, settings: Settings = Depends(get_settings)):
    try:
        product = Product.get(pk)
        if product:
            return {"message": f"Successfully fetched the product with primary key {pk}", "data": product}
        return {"message": f"Unable to fetch the product with primary key {pk}", "data": None}
    except Exception as e:
        return {"message": f"Unable to fetch product with primary key {pk}", "data": None}


@app.delete('/product/{pk}')
async def delete_product(pk: str):
    try:
        product = Product.get(pk)
        if product:
            return {"message": f"Successfully deleted the product with primary key {pk}", "data": Product.delete(pk)}
        return {"message": f"Unable to delete the product with primary key {pk}", "data": None}
    except Exception as e:
        return {"message": f"Unable to delete product with primary key {pk}", "data": None}
