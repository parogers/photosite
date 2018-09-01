
def DebugMiddleware(get_response):
    def middleware(request):
        def dict_to_str(dct):
            return ', '.join('%s=%s' % (k, v) for k, v in dct.items())

        response = get_response(request)
        print('')
        print('>>>', request.method, request.path)
        #print(list(request.POST.items()))
        if request.GET:
            print('GET:', dict_to_str(request.GET))

        if request.POST:
            print('POST:', dict_to_str(request.POST))

        if request.FILES:
            print('FILES:', request.FILES)

        print('HEADERS:')
        for key, value in filter(
                lambda x : x[0].startswith('HTTP_'),
                request.META.items()):
            print('*', key, value)
        print('')
        
        return response

    return middleware

