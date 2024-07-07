from django.shortcuts import render
from dotenv import load_dotenv
import os
from presta_import import get_orders

# Loading environmental variables
load_dotenv()
PRESTA_API = os.getenv('PRESTA_API')

def list_view(request):
    orders =  get_orders(PRESTA_API)
    context = {'orders': orders}
    return render(request, 'presta/templates/index.html', context)



if __name__ == "__main__":
    pass