from django import template

register = template.Library()

@register.filter
def get_list(objects,counter):
	counter=counter-1
	return objects[counter]
