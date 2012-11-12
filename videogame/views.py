from django.core.context_processors import csrf
from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpRequest
from django.conf import settings
from videogame.models import *
from vendor.controllers import AmazonController
import urllib
import HTMLParser
from types import *
import re
import inspect
import logging

logger = logging.getLogger(__name__)

def list(request):
    c = {}
    c.update(csrf(request))
    videogame_list = VideoGame.objects.all()
    c['videogame_list'] = videogame_list
    c['tab'] = "videogames"
    c['user'] = request.user
    return render_to_response('videogame/list.html', c)

def catalog(request):
    videogame_list = VideoGame.objects.all()
    return render_to_response('videogame/catalog.html', {'videogame_list': videogame_list, 'tab': 'videogames', 'user': request.user})

def view(request, videogame_id):
    videogame = get_object_or_404(VideoGame, pk=videogame_id)
    img_url = settings.MEDIA_URL + "videogame/" + str(videogame.id) + ".jpg"
    videogame.description = videogame.description.replace("\\'", "'")
    return render_to_response('videogame/view.html', {'videogame': videogame, 'img_url': img_url, 'tab': 'videogames', 'action': 'view', 'user': request.user})

def get_developer(name):
    name = unicode(name).encode('utf-8')
    try:
        developer = Developer.objects.get(name = name)
    except Developer.DoesNotExist:
        developer = Developer.objects.create(name = name)
    return developer

def get_publisher(name):
    name = unicode(name).encode('utf-8')
    try:
        publisher = Publisher.objects.get(name = name)
    except Publisher.DoesNotExist:
        publisher = Publisher.objects.create(name = name)
    return publisher

def get_series(name):
    if not name:
        return None
    name = unicode(name).encode('utf-8')
    try:
        series = Series.objects.get(name = name)
    except Series.DoesNotExist:
        series = Series.objects.create(name = name)
    return series

def get_media_type_by_id(media_type_id):
    media_type = None
    try:
        media_type = MediaType.objects.get(pk = media_type_id)
    except MediaType.DoesNotExist:
        pass

    return media_type

def get_media_type_by_name(name):
    name = unicode(name).encode('utf-8')
    try:
        media_type = MediaType.objects.get(label = name)
    except MediaType.DoesNotExist:
        media_type = MediaType.objects.create(label = name)
    return media_type

def get_platform_by_name(name):
    name = unicode(name).encode('utf-8')
    try:
        platform = Platform.objects.get(name = name)
    except Platform.DoesNotExist:
        platform = Platform.objects.create(name = name)
    return platform

def get_condition_by_id(condition_id):
    condition = None
    try:
        condition = Condition.objects.get(pk = condition_id)
    except Condition.DoesNotExist:
        pass
    return condition

def get_condition_by_name(name):
    name = unicode(name).encode('utf-8')
    try:
        condition = Condition.objects.get(label = name)
    except Condition.DoesNotExist:
        condition = Condition.objects.create(label = name)
    return condition

def edit(request, videogame_id):
    c = {}
    c['tab'] = 'videogames'
    c['action'] = 'edit'
    c['user'] = request.user
    c.update(csrf(request))

    if request.method == 'POST':
        post = request.POST
        logger.debug(post)
        title = unicode(post['title']).encode('utf-8')
        developer = get_developer(post['developer'])
        series = get_series(post['series'])
        series_number = post['series_number']
        media_type = get_media_type_by_name(post['media_type'])
        platform = get_platform_by_name(post['platform'])
        condition = get_condition_by_name(post['condition'])
        description = unicode(post['description']).encode('utf-8')
        publisher = get_publisher(post['publisher'])
        location = unicode(post['location']).encode('utf-8')
        upc = post['upc']

        videogame = VideoGame.objects.get(pk = videogame_id)
        videogame.title = title
        videogame.developer = developer
        videogame.series = series
        videogame.series_number = series_number
        videogame.media_type = media_type
        videogame.condition = condition
        videogame.description = description
        videogame.publisher = publisher
        videogame.platform = platform
        videogame.location = location
        videogame.updated_by = request.user
        videogame.upc = upc

        videogame.save()
        c['updated'] = True

    c['videogame'] = get_object_or_404(VideoGame, pk=videogame_id)
    c['media_types'] = MediaType.objects.all()
    c['platforms'] = Platform.objects.all()
    c['conditions'] = Condition.objects.all()
    return render_to_response('videogame/edit.html', c)

def add(request):
    c = {}
    c['tab'] = 'videogames'
    c['action'] = 'add'
    c['user'] = request.user
    c.update(csrf(request))

    if request.method == 'POST':
        post = request.POST
        logger.debug(post)
        title = unicode(post['title']).encode('utf-8')
        developer = get_developer(post['developer'])
        series = get_series(post['series'])
        series_number = post['series_number']
        platform = get_platform_by_name(post['platform'])
        media_type = get_media_type_by_name(post['media_type'])
        condition = get_condition_by_name(post['condition'])
        description = unicode(post['description']).encode('utf-8')
        publisher = get_publisher(post['publisher'])
        location = unicode(post['location']).encode('utf-8')
        upc = post['upc']
        year = 0

        videogame = VideoGame(
            title = title,
            developer = developer,
            series = series,
            series_number = series_number,
            media_type = media_type,
            condition = condition,
            platform = platform,
            description = description,
            publisher = publisher,
            publication_year = year,
            updated_by = request.user,
            location = location,
            )

        videogame.save()
        c['added'] = True
        c['videogame'] = videogame

    c['platforms'] = Platform.objects.all()
    c['media_types'] = MediaType.objects.all()
    c['conditions'] = Condition.objects.all()

    return render_to_response('videogame/add.html', c)

def get_details(product):

    details = {}

    # Get publication year
    details['year'] = str(product.item.ItemAttributes.ReleaseDate)[:4]

    # Get title
    title = product.item.ItemAttributes.Title
    details['title'] = unicode(title).encode('utf-8')

    details['publisher'] = get_publisher(product.item.ItemAttributes.Manufacturer)

    try:
        details['developer'] = get_developer(product.item.ItemAttributes.Studio)
    except AttributeError:
        details['developer'] = get_developer("Unknown")

    details['media_type'] = get_media_type_by_name(product.item.ItemAttributes.Binding)
    details['platform'] = get_platform_by_name(product.item.ItemAttributes.Platform)

    # Get item description
    try:
        desc = product.item.EditorialReviews[0].EditorialReview['Content']
        details['desc'] = unicode(desc).encode('utf-8')
    except AttributeError:
        details['desc'] = ""

    return details

def mass_add(request):
    c = {}
    c['tab'] = 'videogames'
    c['user'] = request.user
    c.update(csrf(request))

    if request.method == 'POST':
        post = request.POST
        upc = post['upc']
        amazon = AmazonController()

        product = None
        added = False

        if post['upc'][:1].isdigit():
            product = amazon.lookup("0" + upc, "EAN", "Blended")
        else:
            product = amazon.lookup(upc, "ASIN")

        if product:
            if type(product) is ListType:
                product_list = product
            else:
                product_list = []
                product_list.append(product)

            for product in product_list:
                if len(product_list) > 1:
                    try:
                        product.item.LargeImage['URL']
                    except AttributeError:
                        continue

                    details = get_details(product)
                    if not details['developer']:
                        continue
                    if not details['desc']:
                        continue

                else:
                    details = get_details(product)

                videogame = VideoGame.objects.create(
                    title = details['title'],
                    developer = details['developer'],
                    media_type = details['media_type'],
                    platform = details['platform'],
                    publisher = details['publisher'],
                    publication_year = details['year'],
                    upc = upc,
                    updated_by = request.user,
                    description = details['desc'],
                    )
                if videogame:
                    added = True

                # Get image
                try:
                    image_url = str(product.item.LargeImage['URL'])
                    urllib.urlretrieve(image_url, settings.MEDIA_ROOT + "/videogame/" + str(videogame.id) + ".jpg")
                except AttributeError:
                    pass

                c['videogame'] = videogame
                return render_to_response('videogame/mass_add.html', c)

        else:
            c['error'] = "Unable to find UPC %s." % (upc)

    return render_to_response('videogame/mass_add.html', c)
