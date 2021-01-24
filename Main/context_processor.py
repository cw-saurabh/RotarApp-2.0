from Main.models import avenues, WhatWeDo

def navbar_processor(request):
    links = dict()
    for avenue in avenues :
        events = WhatWeDo.objects.filter(eventCategory=avenue).all()
        if(len(events)):
            links[avenue] = {
                "Title" : avenues[avenue],
                "SubTab" : avenues[avenue].replace(" ",'')
            }
    return {'EventNavLinks': links}