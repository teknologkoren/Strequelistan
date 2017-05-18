from django.shortcuts import render

def add_id(things):
    for i, thing in enumerate(things):
        thing['id'] = i + 1
    return things

def drinks(*names):
    return add_id([{'name': name} for name in names])

def user(first, last, nick=None):
    return {
        'first_name': first,
        'last_name': last,
        'nickname': nick,
    }

FOO, BARBARA, DRYG = add_id([
    user('Foo', 'Baa'),
    user('Wonderbara', 'Uppblosbara', 'Barbara'),
    user('Bert Karl-Willhelm Pomme', 'von Roos und Untsprungen'),
])

BEER, WINE, GLOGG, SPRIT, LASK = drinks('Öl', 'Vin', 'Glögg', 'Sprit', 'Läsk')

def usercard(request):
    """Renders a bunch of usercards."""
    return render(request, 'strecklista/components/usercard_test.html', {
        'cards': [
            {
                'user': FOO,
                'drinks': [],
            },
            {
                'user': FOO,
                'drinks': [BEER],
            },
            {
                'user': BARBARA,
                'drinks': [BEER, WINE],
            },
            {
                'user': BARBARA,
                'drinks': [BEER, WINE, GLOGG],
            },
            {
                'user': DRYG,
                'drinks': [BEER, WINE, GLOGG],
            },
            {
                'user': BARBARA,
                'drinks': [BEER, SPRIT, WINE, LASK, GLOGG],
            },
            {
                'user': DRYG,
                'drinks': [BEER, SPRIT, WINE, LASK, GLOGG, SPRIT, LASK, GLOGG],
            },
        ],
    })

# Add demos for various UI components but adding function to render them here.
demos = [
    usercard,
]
