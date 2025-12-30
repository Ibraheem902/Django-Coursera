from	django.contrib.auth	import	get_user_model
from django import template
from	django.utils.html	import	escape
from	django.utils.safestring	import	mark_safe
from django.utils.html	import	format_html
from blog.models import	Post
register	=	template.Library()
user_model	=	get_user_model()
@register.filter
def	author_details(author,current_user=None):
    if	not	isinstance(author,	user_model):
    #	return	empty	string	as	safe	default
        return	""
    if	author.first_name	and	author.last_name:
        name	=	f"{author.first_name}	{author.last_name}"
    else:
        name	=	f"{author.username}"
    if	author.email:
        prefix	= format_html('<a href="mailto:{}">',	author.email)
        suffix	= format_html('</a> ({})',	escape(name))
    else:
        prefix	=	""
        suffix	=	""
    return	format_html("{}{}{}",prefix,name,suffix)
@register.inclusion_tag('blog/post-list.html')
def recent_posts(post):
    posts = Post.objects.exclude(pk=post.pk)[:5]
    return {'title':'Recent Posts','posts':posts}

@register.simple_tag
def row(css_class=""):
    return mark_safe(f'<div class="row {css_class}">')

@register.simple_tag
def endrow():
    return mark_safe("</div>")

@register.simple_tag
def col(css_class=""):
    return mark_safe(f'<div class="col {css_class}">')

@register.simple_tag
def endcol():
    return mark_safe("</div>")

