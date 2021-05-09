from .models import Tag, Category, Brand

def grouping(request):
    '''
    add category and brand and tags to context
    '''
    return {
        # only gets the childs categories
        'categories': Category.objects.filter(parent_cat=None),
        'brands': Brand.objects.all(),
        'tags': Tag.objects.all()[:30],
    }
