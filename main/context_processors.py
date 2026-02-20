from main.models import Catagory
from django.db.models import Max


def catagory_list_context(request):
	catagory = Catagory.objects.annotate(
                    last_review=Max('product')
                ).order_by('-last_review')[0:20]


	return	{
		'catagorys':catagory
	}

# def contact_context(request):
# 	contact= Contact.objects.get(pk=1)

# 	return{
# 		'cnt':contact
# 	}