from product.models import Category

def base_data(request):
    data = {}
    data['mob_categories'] = Category.objects._mptt_filter(parent=None)
    return data