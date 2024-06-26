from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.conf import settings


def paginate_data(data_list,item_per_page, request):
    paginator = Paginator(data_list, item_per_page)  # Number of items per page
    page = request.GET.get('page')  # Get the current page number from the request
    try:
        paginated_data = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        paginated_data = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        paginated_data = paginator.page(paginator.num_pages)
    
    return paginated_data
